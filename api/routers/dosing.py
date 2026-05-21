"""Daily dosing tasks — complete dose, restock supplies."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm import DoseLog, DosingTask, Supply
from models.schemas import DoseCompleteRequest, DosingTaskOut, RestockRequest
from services.ha_client import ha_client

router = APIRouter(prefix="/api/dosing", tags=["dosing"])


async def _build_task_out(task: DosingTask) -> DosingTaskOut:
    s = task.supply
    return DosingTaskOut(
        id=task.id,
        supply_id=s.id,
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

    # fire supply warning if now below threshold
    if supply.current_amount <= supply.min_threshold:
        from services.n8n_client import n8n_client
        await n8n_client.supply_low(supply)

    return {"ok": True, "remaining": supply.current_amount}
