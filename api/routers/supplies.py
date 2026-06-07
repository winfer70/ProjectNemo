"""Supplies / inventory CRUD + restock."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Supply
from models.schemas import SupplyCreate, SupplyOut, SupplyUpdate, RestockRequest
from services.websocket_manager import broadcast_change

router = APIRouter(prefix="/api/supplies", tags=["supplies"])


def _to_out(s: Supply) -> SupplyOut:
    out = SupplyOut.model_validate(s)
    out.low = s.current_amount <= s.min_threshold
    return out


@router.get("", response_model=list[SupplyOut])
async def list_supplies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Supply).order_by(Supply.name))
    return [_to_out(s) for s in result.scalars().all()]


@router.post("", response_model=SupplyOut)
async def create_supply(data: SupplyCreate, db: AsyncSession = Depends(get_db)):
    supply = Supply(**data.model_dump())
    db.add(supply)
    await db.commit()
    await broadcast_change("supplies")
    await db.refresh(supply)
    return _to_out(supply)


@router.put("/{supply_id}", response_model=SupplyOut)
async def update_supply(
    supply_id: int, data: SupplyUpdate, db: AsyncSession = Depends(get_db)
):
    supply = await db.get(Supply, supply_id)
    if not supply:
        raise HTTPException(404, "Supply not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(supply, field, value)
    await db.commit()
    await broadcast_change("supplies")
    await db.refresh(supply)
    return _to_out(supply)


@router.post("/{supply_id}/restock", response_model=SupplyOut)
async def restock_supply(
    supply_id: int, body: RestockRequest, db: AsyncSession = Depends(get_db)
):
    supply = await db.get(Supply, supply_id)
    if not supply:
        raise HTTPException(404, "Supply not found")
    supply.current_amount = body.new_amount
    await db.commit()
    await broadcast_change("supplies")
    await db.refresh(supply)
    return _to_out(supply)
