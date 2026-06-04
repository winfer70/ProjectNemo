"""Water test sessions + readings + trends."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm import WaterTestParameter, WaterTestReading, WaterTestSession
from models.schemas import (
    WaterTestParameterOut,
    WaterTestSessionCreate,
    WaterTestSessionOut,
    WaterTestReadingOut,
    SensorHistoryPoint,
)
from services.n8n_client import n8n_client
from services.websocket_manager import broadcast_change
from services import ollama_vision

import logging
import traceback

logger = logging.getLogger(__name__)





def _reading_out(r: WaterTestReading) -> WaterTestReadingOut:
    p = r.parameter
    return WaterTestReadingOut(
        id=r.id,
        parameter_id=r.parameter_id,
        parameter_key=p.key,
        parameter_name_en=p.name_en,
        parameter_name_pl=p.name_pl,
        unit=p.unit,
        value=r.value,
        out_of_range=r.out_of_range,
        notes=r.notes,
    )


@router.post("/analyze_strip")
async def analyze_strip(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    image_bytes = await file.read()
    try:
        results = await ollama_vision.analyze_strip(image_bytes)
    except Exception as e:
        logger.error("analyze_strip failed: %s: %s\n%s", type(e).__name__, e, traceback.format_exc())
        raise HTTPException(502, f"Vision analysis failed: {type(e).__name__}: {e}")

    params_result = await db.execute(select(WaterTestParameter))
    params_by_key = {p.key: p for p in params_result.scalars().all()}

    prefill = {
        params_by_key[key].id: value
        for key, value in results.items()
        if value is not None and key in params_by_key
    }
    return {"raw": results, "prefill": prefill}


@router.get("/parameters", response_model=list[WaterTestParameterOut])
async def list_parameters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WaterTestParameter).order_by(WaterTestParameter.id))
    return result.scalars().all()


@router.get("/sessions", response_model=list[WaterTestSessionOut])
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WaterTestSession)
        .options(selectinload(WaterTestSession.readings).selectinload(WaterTestReading.parameter))
        .order_by(desc(WaterTestSession.tested_at))
        .limit(limit)
        .offset(offset)
    )
    sessions = result.scalars().all()
    return [
        WaterTestSessionOut(
            id=s.id,
            tested_at=s.tested_at,
            notes=s.notes,
            readings=[_reading_out(r) for r in s.readings],
        )
        for s in sessions
    ]


@router.get("/sessions/latest", response_model=WaterTestSessionOut | None)
async def latest_session(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WaterTestSession)
        .options(selectinload(WaterTestSession.readings).selectinload(WaterTestReading.parameter))
        .order_by(desc(WaterTestSession.tested_at))
        .limit(1)
    )
    session = result.scalar_one_or_none()
    if not session:
        return None
    return WaterTestSessionOut(
        id=session.id,
        tested_at=session.tested_at,
        notes=session.notes,
        readings=[_reading_out(r) for r in session.readings],
    )


@router.post("/sessions", response_model=WaterTestSessionOut)
async def create_session(
    data: WaterTestSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    params_result = await db.execute(select(WaterTestParameter))
    params = {p.id: p for p in params_result.scalars().all()}

    session = WaterTestSession(
        tested_at=data.tested_at or datetime.utcnow(),
        notes=data.notes,
    )
    db.add(session)
    await db.flush()

    out_of_range_alerts = []
    for reading_in in data.readings:
        param = params.get(reading_in.parameter_id)
        if not param:
            raise HTTPException(422, f"Unknown parameter_id {reading_in.parameter_id}")

        oor = False
        if param.min_safe is not None and reading_in.value < param.min_safe:
            oor = True
        if param.max_safe is not None and reading_in.value > param.max_safe:
            oor = True

        reading = WaterTestReading(
            session_id=session.id,
            parameter_id=param.id,
            value=reading_in.value,
            out_of_range=oor,
            notes=reading_in.notes,
        )
        db.add(reading)
        if oor:
            out_of_range_alerts.append((param, reading_in.value))

    await db.commit()
    await broadcast_change("water_tests")

    # fire Telegram alerts for out-of-range readings
    for param, value in out_of_range_alerts:
        await n8n_client.water_test_alert(param, value)

    # reload with relationships
    result = await db.execute(
        select(WaterTestSession)
        .options(selectinload(WaterTestSession.readings).selectinload(WaterTestReading.parameter))
        .where(WaterTestSession.id == session.id)
    )
    session = result.scalar_one()
    return WaterTestSessionOut(
        id=session.id,
        tested_at=session.tested_at,
        notes=session.notes,
        readings=[_reading_out(r) for r in session.readings],
    )


@router.get("/trends/{param_key}", response_model=list[SensorHistoryPoint])
async def parameter_trend(
    param_key: str,
    n: int = 10,
    db: AsyncSession = Depends(get_db),
):
    param_result = await db.execute(
        select(WaterTestParameter).where(WaterTestParameter.key == param_key)
    )
    param = param_result.scalar_one_or_none()
    if not param:
        raise HTTPException(404, f"Parameter {param_key!r} not found")

    result = await db.execute(
        select(WaterTestReading, WaterTestSession.tested_at)
        .join(WaterTestSession)
        .where(WaterTestReading.parameter_id == param.id)
        .order_by(desc(WaterTestSession.tested_at))
        .limit(n)
    )
    rows = result.all()
    return [SensorHistoryPoint(time=tested_at, value=r.value) for r, tested_at in reversed(rows)]
