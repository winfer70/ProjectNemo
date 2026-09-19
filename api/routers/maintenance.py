"""Maintenance tasks — list, start, complete with checkboxes."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm import MaintenanceLog, MaintenanceSnooze, MaintenanceTask, Supply
from models.schemas import MaintenanceCompleteRequest, MaintenanceStartRequest, MaintenanceTaskOut
from services.n8n_client import n8n_client
from services.websocket_manager import broadcast_change

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


def _days_until(next_due: datetime | None) -> int | None:
    if next_due is None:
        return None
    delta = next_due.date() - datetime.utcnow().date()
    return delta.days


def _to_out(task: MaintenanceTask) -> MaintenanceTaskOut:
    return MaintenanceTaskOut(
        id=task.id,
        tank_id=task.tank_id,
        name=task.name,
        name_pl=task.name_pl,
        interval_days=task.interval_days,
        last_completed=task.last_completed,
        next_due=task.next_due,
        days_until=_days_until(task.next_due),
        steps=task.steps,
        required_parts=task.required_parts,
        started_at=task.started_at,
        affects_entity=task.affects_entity,
    )


@router.get("", response_model=list[MaintenanceTaskOut])
async def list_maintenance(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MaintenanceTask).order_by(MaintenanceTask.next_due))
    return [_to_out(t) for t in result.scalars().all()]


@router.get("/{task_id}/steps")
async def get_steps(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(MaintenanceTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return {
        "id": task.id,
        "name": task.name,
        "name_pl": task.name_pl,
        "steps": task.steps,
        "required_parts": task.required_parts,
    }


@router.post("/{task_id}/start")
async def start_maintenance(
    task_id: int,
    body: MaintenanceStartRequest,
    db: AsyncSession = Depends(get_db),
):
    """Mark task as in-progress. Suppresses device-off alerts for affects_entity."""
    task = await db.get(MaintenanceTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task.started_at = datetime.utcnow()
    if body.affects_entity:
        task.affects_entity = body.affects_entity
    await db.commit()
    await broadcast_change("maintenance")
    return {"ok": True}


@router.post("/{task_id}/snooze")
async def snooze_maintenance(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Defer an overdue maintenance task's on-screen due-reminder. Idempotent
    insert, same pattern as water_tests.py's snooze_reminder - the hourly
    maintenance_snooze_reminder job (services/scheduler.py) then keeps
    sending a repeating Telegram nudge until the task is actually completed,
    which deletes this row (see complete_maintenance below)."""
    task = await db.get(MaintenanceTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    result = await db.execute(select(MaintenanceSnooze).where(MaintenanceSnooze.task_id == task_id))
    if not result.scalar_one_or_none():
        db.add(MaintenanceSnooze(task_id=task_id))
        await db.commit()
    return {"ok": True}


@router.post("/{task_id}/complete")
async def complete_maintenance(
    task_id: int,
    body: MaintenanceCompleteRequest,
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(MaintenanceTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    now = datetime.utcnow()
    task.last_completed = now
    task.next_due = now + timedelta(days=task.interval_days)
    task.started_at = None  # clear in-progress state

    # A completed task resolves any pending "remind me later" for it - the
    # hourly Telegram nudge (services/scheduler.py's maintenance_snooze_reminder)
    # only fires while a MaintenanceSnooze row exists for this task.
    snooze_result = await db.execute(
        select(MaintenanceSnooze).where(MaintenanceSnooze.task_id == task_id)
    )
    snooze = snooze_result.scalar_one_or_none()
    if snooze:
        await db.delete(snooze)

    for part in body.parts_replaced:
        if sid := part.get("supply_id"):
            supply = await db.get(Supply, sid)
            if supply and supply.type == "part":
                supply.current_amount = max(0, supply.current_amount - part.get("quantity", 1))
                if supply.current_amount <= supply.min_threshold:
                    await n8n_client.supply_low(supply)

    log = MaintenanceLog(task_id=task_id, completed_at=now, notes=body.notes)
    log.parts_replaced = body.parts_replaced
    db.add(log)
    await db.commit()
    await broadcast_change("maintenance")

    await n8n_client.maintenance_completed(task)

    return {"ok": True, "next_due": task.next_due}
