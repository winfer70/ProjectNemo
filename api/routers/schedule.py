"""Feeding schedule CRUD + Feed Now action."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import FeedingLog, FeedingSchedule
from models.schemas import FeedingLogOut, FeedingScheduleCreate, FeedingScheduleOut
from services.ha_client import ha_client
from services.websocket_manager import broadcast_change

router = APIRouter(prefix="/api", tags=["schedule"])


@router.get("/schedule/feedings", response_model=list[FeedingScheduleOut])
async def list_feedings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeedingSchedule).order_by(FeedingSchedule.time_of_day))
    return result.scalars().all()


@router.post("/schedule/feedings", response_model=FeedingScheduleOut)
async def create_feeding(data: FeedingScheduleCreate, db: AsyncSession = Depends(get_db)):
    feeding = FeedingSchedule(**data.model_dump())
    db.add(feeding)
    await db.commit()
    await broadcast_change("schedule")
    await db.refresh(feeding)
    return feeding


@router.delete("/schedule/feedings/{feeding_id}")
async def delete_feeding(feeding_id: int, db: AsyncSession = Depends(get_db)):
    feeding = await db.get(FeedingSchedule, feeding_id)
    if not feeding:
        raise HTTPException(404, "Feeding schedule not found")
    await db.delete(feeding)
    await db.commit()
    await broadcast_change("schedule")
    return {"ok": True}


@router.get("/schedule/feedings/history", response_model=list[FeedingLogOut])
async def feeding_history(limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FeedingLog).order_by(desc(FeedingLog.timestamp)).limit(limit)
    )
    return result.scalars().all()


@router.post("/actions/feed-now")
async def feed_now(db: AsyncSession = Depends(get_db)):
    """Pause filter for 10 min via HA, log feed timestamp."""
    await ha_client.pause_filter_for_feeding()
    log = FeedingLog(manual=True, timestamp=datetime.utcnow(), notes="Feed Now button")
    db.add(log)
    await db.commit()
    await broadcast_change("schedule")
    return {"ok": True, "filter_pause_minutes": 10}
