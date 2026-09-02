"""Feeding schedule CRUD + Feed Now + Cancel Feed + Feed Status."""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import FeedingLog, FeedingPause, FeedingSchedule
from models.schemas import FeedingLogOut, FeedingScheduleCreate, FeedingScheduleOut, FeedingStatusOut
from services.ha_client import ha_client
from services.websocket_manager import broadcast_change
from config import settings

router = APIRouter(prefix="/api", tags=["schedule"])

FEEDING_PAUSE_SECS = 180  # 3 minutes

# Tank 1 (Akwarium Kuchnia): separate filter + air pump Tapo switches.
# Tank 2 (Akwarium Salon): one Meross outlet powers filter+pump together.
FEED_ENTITIES_BY_TANK = {
    1: [settings.tapo_filter_entity, settings.tapo_air_entity],
    2: [settings.tapo_filter_entity_2],
}


@router.get("/schedule/feedings", response_model=list[FeedingScheduleOut])
async def list_feedings(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FeedingSchedule)
        .where(FeedingSchedule.tank_id == tank_id)
        .order_by(FeedingSchedule.time_of_day)
    )
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
async def feeding_history(tank_id: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FeedingLog)
        .where(FeedingLog.tank_id == tank_id)
        .order_by(desc(FeedingLog.timestamp))
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/actions/feed-status", response_model=FeedingStatusOut)
async def feed_status(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Return current feeding pause state."""
    now = datetime.utcnow()
    result = await db.execute(
        select(FeedingPause).where(
            and_(
                FeedingPause.tank_id == tank_id,
                FeedingPause.cancelled_at.is_(None),
                FeedingPause.resumed_at.is_(None),
            )
        ).order_by(desc(FeedingPause.started_at)).limit(1)
    )
    pause = result.scalar_one_or_none()
    if not pause:
        return FeedingStatusOut(paused=False)
    remaining = int((pause.resume_at - now).total_seconds())
    if remaining <= 0:
        return FeedingStatusOut(paused=False)
    return FeedingStatusOut(
        paused=True,
        resume_in_secs=remaining,
        paused_entities=pause.paused_entities,
    )


@router.post("/actions/feed-now")
async def feed_now(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Pause the tank's filter/pump devices for 3 min, log feed."""
    entities = FEED_ENTITIES_BY_TANK.get(tank_id)
    if not entities:
        raise HTTPException(422, f"Unknown tank_id {tank_id}")
    await ha_client.pause_devices_for_feeding(entities)

    now = datetime.utcnow()
    pause = FeedingPause(
        tank_id=tank_id,
        started_at=now,
        resume_at=now + timedelta(seconds=FEEDING_PAUSE_SECS),
    )
    pause.paused_entities = entities
    db.add(pause)

    log = FeedingLog(tank_id=tank_id, manual=True, timestamp=now, notes="Feed Now button")
    db.add(log)
    await db.commit()
    await broadcast_change("schedule")
    return {"ok": True, "pause_seconds": FEEDING_PAUSE_SECS}


@router.post("/actions/cancel-feed")
async def cancel_feed(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Immediately cancel feeding pause and resume devices."""
    now = datetime.utcnow()
    result = await db.execute(
        select(FeedingPause).where(
            and_(
                FeedingPause.tank_id == tank_id,
                FeedingPause.cancelled_at.is_(None),
                FeedingPause.resumed_at.is_(None),
            )
        ).order_by(desc(FeedingPause.started_at)).limit(1)
    )
    pause = result.scalar_one_or_none()
    if not pause:
        raise HTTPException(404, "No active feeding pause")

    await ha_client.resume_devices(pause.paused_entities)
    pause.cancelled_at = now
    await db.commit()
    await broadcast_change("schedule")
    return {"ok": True}
