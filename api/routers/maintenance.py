"""Maintenance tasks — list, steps, complete with checkboxes."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm import MaintenanceLog, MaintenanceTask, Supply
from models.schemas import MaintenanceCompleteRequest, MaintenanceTaskOut
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
        name=task.name,
        name_pl=task.name_pl,
        interval_days=task.interval_days,
        last_completed=task.last_completed,
        next_due=task.next_due,
        days_until=_days_until(task.next_due),
        steps=task.steps,
        required_parts=task.required_parts,
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

    # Decrement supply stock for replaced parts
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
