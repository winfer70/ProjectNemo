"""Daily dosing tasks — complete dose, restock supplies, CRUD."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm import DoseLog, DosingTask, Supply
from models.schemas import (
    DoseCompleteRequest, DosingTaskCreate, DosingTaskOut, DosingTaskUpdate, RestockRequest
)
from services.websocket_manager import broadcast_change

router = APIRouter(prefix="/api/dosing", tags=["dosing"])


async def _build_task_out(task: DosingTask) -> DosingTaskOut:
    s = task.supply
    return DosingTaskOut(
        id=task.id,
        supply_id=s.id,
        tank_id=task.tank_id,
        supply_name=s.name,
        supply_name_pl=s.name_pl,
        dose_amount=task.dose_amount,
        dose_unit=task.dose_unit,
        time_of_day=task.time_of_day,
        active=task.active,
        notes=task.notes,
        notes_pl=task.notes_pl,
        current_supply=s.current_amount,
        supply_unit=s.unit,
        supply_low=s.current_amount <= s.min_threshold,
    )


@router.get("", response_model=list[DosingTaskOut])
async def list_dosing_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DosingTask)
        .options(selectinload(DosingTask.supply))
        .where(DosingTask.active == True)  # noqa: E712
    )
    tasks = result.scalars().all()
    return [await _build_task_out(t) for t in tasks]


@router.post("", response_model=DosingTaskOut, status_code=201)
async def create_dosing_task(data: DosingTaskCreate, db: AsyncSession = Depends(get_db)):
    supply = await db.get(Supply, data.supply_id)
    if not supply:
        raise HTTPException(404, "Supply not found")
    task = DosingTask(**data.model_dump())
    db.add(task)
    await db.commit()
    result = await db.execute(
        select(DosingTask).options(selectinload(DosingTask.supply)).where(DosingTask.id == task.id)
    )
    task = result.scalar_one()
    await broadcast_change("dosing")
    return await _build_task_out(task)


@router.put("/{task_id}", response_model=DosingTaskOut)
async def update_dosing_task(
    task_id: int,
    data: DosingTaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DosingTask)
        .options(selectinload(DosingTask.supply))
        .where(DosingTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Dosing task not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await broadcast_change("dosing")
    return await _build_task_out(task)


@router.post("/{task_id}/complete")
async def complete_dose(
    task_id: int,
    body: DoseCompleteRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(DosingTask)
        .options(selectinload(DosingTask.supply))
        .where(DosingTask.id == task_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(404, "Dosing task not found")

    supply = task.supply
    if supply.type == "liquid":
        supply.current_amount = max(0.0, supply.current_amount - task.dose_amount)

    log = DoseLog(supply_id=supply.id, amount=task.dose_amount, notes=body.notes)
    db.add(log)
    await db.commit()
    await broadcast_change("dosing")
    await broadcast_change("supplies")

    if supply.current_amount <= supply.min_threshold:
        from services.n8n_client import n8n_client
        await n8n_client.supply_low(supply)

    return {"ok": True, "remaining": supply.current_amount}


@router.post("/supplies/{supply_id}/restock")
async def restock_supply(
    supply_id: int,
    body: RestockRequest,
    db: AsyncSession = Depends(get_db),
):
    """Add amount to supply current_amount (resupply flow)."""
    supply = await db.get(Supply, supply_id)
    if not supply:
        raise HTTPException(404, "Supply not found")
    supply.current_amount += body.new_amount
    await db.commit()
    await broadcast_change("dosing")
    await broadcast_change("supplies")
    return {"ok": True, "new_amount": supply.current_amount}
