"""Water test sessions + readings + trends."""
import base64
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import settings
from database import get_db
from models.orm import WaterTestParameter, WaterTestParameterNorm, WaterTestReading, WaterTestSession, WaterTestSnooze
from models.schemas import (
    WaterTestParameterOut,
    WaterTestParameterNormIn,
    WaterTestReminderOut,
    WaterTestSnoozeIn,
    WaterTestSessionCreate,
    WaterTestSessionOut,
    WaterTestReadingOut,
    WaterTestCurrentOut,
    SensorHistoryPoint,
)
from services.n8n_client import n8n_client
from services.ntfy_client import ntfy_client
from services.websocket_manager import broadcast_change
from services import ollama_vision, scan_cache, strip_cv

import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/water-tests", tags=["water-tests"])





def _reading_out(r: WaterTestReading, session_tested_at: datetime | None = None) -> WaterTestReadingOut:
    p = r.parameter
    updated = getattr(r, "updated_at", None) or session_tested_at
    if updated is None and getattr(r, "session", None) is not None:
        updated = r.session.tested_at
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
        updated_at=updated,
    )


async def _effective_norms_map(db: AsyncSession, tank_id: int) -> dict[int, tuple[float | None, float | None, int | None]]:
    """parameter_id -> (min_safe, max_safe, test_frequency_days), using this
    tank's override row when one exists, else the parameter's global default."""
    params_result = await db.execute(select(WaterTestParameter))
    norms = {p.id: (p.min_safe, p.max_safe, p.test_frequency_days) for p in params_result.scalars().all()}

    norms_result = await db.execute(
        select(WaterTestParameterNorm).where(WaterTestParameterNorm.tank_id == tank_id)
    )
    for n in norms_result.scalars().all():
        base = norms.get(n.parameter_id, (None, None, None))
        norms[n.parameter_id] = (n.min_safe, n.max_safe, n.test_frequency_days if n.test_frequency_days is not None else base[2])
    return norms


def _build_scan_response(
    results: dict,
    params_by_key: dict,
    cache_id: int,
    cache_hit: bool,
    cv_results: dict | None = None,
) -> dict:
    """Build the analyze_strip JSON response including out_of_range flags."""
    prefill: dict[int, float] = {}
    out_of_range: dict[int, bool] = {}
    for key, value in results.items():
        if value is None:
            continue
        param = params_by_key.get(key)
        if not param:
            continue
        prefill[param.id] = value
        if cv_results and key in cv_results:
            oor = cv_results[key]["out_of_range"]
        else:
            oor = False
            if param.min_safe is not None and value < param.min_safe:
                oor = True
            if param.max_safe is not None and value > param.max_safe:
                oor = True
        out_of_range[param.id] = oor
    return {
        "raw": results,
        "prefill": prefill,
        "out_of_range": out_of_range,
        "cache_id": cache_id,
        "cache_hit": cache_hit,
    }


@router.post("/analyze_strip")
async def analyze_strip(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    image_bytes = await file.read()

    params_result = await db.execute(select(WaterTestParameter))
    params_list = params_result.scalars().all()
    params_by_key = {p.key: p for p in params_list}

    cached, sha256, phash = await scan_cache.lookup(db, image_bytes)
    if cached:
        results = cached.corrected_result or cached.ai_result
        return _build_scan_response(results, params_by_key, cached.id, True)

    # Try OpenCV strip reader first
    cv_results = None
    try:
        cv_params = {k: {"min_safe": p.min_safe, "max_safe": p.max_safe} for k, p in params_by_key.items()}
        cv_raw = strip_cv.analyze_strip(image_bytes, cv_params)
        cv_results = cv_raw
        results = {k: v["value"] for k, v in cv_raw.items() if v["value"] is not None}
        logger.info("strip_cv succeeded for %d params", len(results))
    except strip_cv.CVDetectionError as e:
        logger.warning("strip_cv failed (%s), falling back to LLM", e)
        cv_results = None
        results = None
    except Exception as e:
        logger.warning("strip_cv unexpected error (%s: %s), falling back to LLM", type(e).__name__, e)
        cv_results = None
        results = None

    if results is None:
        try:
            results = await ollama_vision.analyze_strip(image_bytes)
        except Exception as e:
            logger.error("analyze_strip LLM failed: %s: %s\n%s", type(e).__name__, e, traceback.format_exc())
            raise HTTPException(502, f"Vision analysis failed: {type(e).__name__}: {e}")

    cache_row = await scan_cache.store(db, sha256, phash, results)
    return _build_scan_response(results, params_by_key, cache_row.id, False, cv_results)


@router.post("/debug_strip")
async def debug_strip(file: UploadFile = File(...)):
    """Return annotated JPEG + per-row HSV debug data.

    Response JSON:
      image_b64: base64 JPEG — green=pad, orange=ref, blue=all cells
      rows: list of {row, param, pad_bbox, pad_hsv, n_refs, white_check}
    """
    image_bytes = await file.read()
    try:
        annotated_bytes, row_debug = strip_cv.debug_analyze_strip(image_bytes)
    except Exception as e:
        raise HTTPException(500, f"debug_strip failed: {e}")
    return JSONResponse({
        "image_b64": base64.b64encode(annotated_bytes).decode(),
        "rows": row_debug,
    })


@router.get("/parameters", response_model=list[WaterTestParameterOut])
async def list_parameters(tank_id: int | None = None, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WaterTestParameter).order_by(WaterTestParameter.id))
    params = result.scalars().all()
    if tank_id is None:
        return params

    norms = await _effective_norms_map(db, tank_id)
    return [
        WaterTestParameterOut(
            id=p.id, key=p.key, name_en=p.name_en, name_pl=p.name_pl, unit=p.unit,
            category=p.category,
            min_safe=norms[p.id][0], max_safe=norms[p.id][1], test_frequency_days=norms[p.id][2],
        )
        for p in params
    ]


@router.put("/parameters/{param_id}/norms", response_model=WaterTestParameterOut)
async def set_parameter_norm(
    param_id: int,
    data: WaterTestParameterNormIn,
    db: AsyncSession = Depends(get_db),
):
    """Upsert this tank's safe-range + test-frequency override for one parameter."""
    param = await db.get(WaterTestParameter, param_id)
    if not param:
        raise HTTPException(404, "Parameter not found")

    result = await db.execute(
        select(WaterTestParameterNorm).where(
            WaterTestParameterNorm.tank_id == data.tank_id,
            WaterTestParameterNorm.parameter_id == param_id,
        )
    )
    norm = result.scalar_one_or_none()
    if norm:
        norm.min_safe = data.min_safe
        norm.max_safe = data.max_safe
        norm.test_frequency_days = data.test_frequency_days
    else:
        norm = WaterTestParameterNorm(
            tank_id=data.tank_id, parameter_id=param_id,
            min_safe=data.min_safe, max_safe=data.max_safe,
            test_frequency_days=data.test_frequency_days,
        )
        db.add(norm)

    # Existing readings for this tank+parameter were flagged out_of_range
    # using whatever norm was active when they were logged - recompute them
    # against the new range so the status shown in the table stays correct.
    readings_result = await db.execute(
        select(WaterTestReading)
        .join(WaterTestSession, WaterTestReading.session_id == WaterTestSession.id)
        .where(
            WaterTestSession.tank_id == data.tank_id,
            WaterTestReading.parameter_id == param_id,
        )
    )
    for reading in readings_result.scalars().all():
        oor = False
        if data.min_safe is not None and reading.value < data.min_safe:
            oor = True
        if data.max_safe is not None and reading.value > data.max_safe:
            oor = True
        reading.out_of_range = oor

    await db.commit()
    await broadcast_change("water_tests")

    return WaterTestParameterOut(
        id=param.id, key=param.key, name_en=param.name_en, name_pl=param.name_pl,
        unit=param.unit, category=param.category,
        min_safe=data.min_safe, max_safe=data.max_safe, test_frequency_days=data.test_frequency_days,
    )


@router.get("/reminders", response_model=list[WaterTestReminderOut])
async def list_reminders(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Manual-category parameters that are due (or overdue) for this tank,
    based on the last time each was actually tested here."""
    params_result = await db.execute(
        select(WaterTestParameter).where(WaterTestParameter.category == "manual").order_by(WaterTestParameter.id)
    )
    params = params_result.scalars().all()
    norms = await _effective_norms_map(db, tank_id)

    readings_result = await db.execute(
        select(WaterTestReading, WaterTestSession.tested_at)
        .join(WaterTestSession, WaterTestReading.session_id == WaterTestSession.id)
        .where(WaterTestSession.tank_id == tank_id)
        .order_by(desc(func.coalesce(WaterTestReading.updated_at, WaterTestSession.tested_at)))
    )
    last_tested: dict[int, datetime] = {}
    for reading, session_tested_at in readings_result.all():
        if reading.parameter_id not in last_tested:
            last_tested[reading.parameter_id] = reading.updated_at or session_tested_at

    snoozes_result = await db.execute(select(WaterTestSnooze).where(WaterTestSnooze.tank_id == tank_id))
    snoozes = {s.parameter_id: s for s in snoozes_result.scalars().all()}

    now = datetime.utcnow()
    out = []
    for p in params:
        _, _, frequency_days = norms.get(p.id, (p.min_safe, p.max_safe, p.test_frequency_days))
        if frequency_days is None:
            continue
        last_at = last_tested.get(p.id)
        due = last_at is None or (now - last_at) >= timedelta(days=frequency_days)
        if not due:
            continue
        out.append(WaterTestReminderOut(
            parameter_id=p.id, key=p.key, name_en=p.name_en, name_pl=p.name_pl, unit=p.unit,
            last_tested_at=last_at, frequency_days=frequency_days, due=True,
            snoozed_at=snoozes[p.id].snoozed_at if p.id in snoozes else None,
            high_effect_en=p.high_effect_en, high_effect_pl=p.high_effect_pl,
        ))
    return out


@router.post("/reminders/{parameter_id}/snooze")
async def snooze_reminder(
    parameter_id: int,
    data: WaterTestSnoozeIn,
    db: AsyncSession = Depends(get_db),
):
    """Defer a due reminder. Keeps the original snoozed_at on repeat taps so
    the \"snoozed for more than 2 days\" escalation check stays accurate."""
    result = await db.execute(
        select(WaterTestSnooze).where(
            WaterTestSnooze.tank_id == data.tank_id,
            WaterTestSnooze.parameter_id == parameter_id,
        )
    )
    if not result.scalar_one_or_none():
        db.add(WaterTestSnooze(tank_id=data.tank_id, parameter_id=parameter_id))
        await db.commit()
    return {"ok": True}


@router.get("/sessions", response_model=list[WaterTestSessionOut])
async def list_sessions(
    tank_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(WaterTestSession)
        .options(selectinload(WaterTestSession.readings).selectinload(WaterTestReading.parameter))
        .order_by(desc(WaterTestSession.tested_at))
    )
    if tank_id is not None:
        query = query.where(WaterTestSession.tank_id == tank_id)
    result = await db.execute(query.limit(limit).offset(offset))
    sessions = result.scalars().all()
    return [
        WaterTestSessionOut(
            id=s.id,
            tank_id=s.tank_id,
            tested_at=s.tested_at,
            notes=s.notes,
            readings=[_reading_out(r, s.tested_at) for r in s.readings],
        )
        for s in sessions
    ]


@router.get("/current", response_model=WaterTestCurrentOut)
async def current_values(tank_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Latest value per parameter for this tank, each with its own updated_at."""
    result = await db.execute(
        select(WaterTestReading)
        .join(WaterTestSession, WaterTestReading.session_id == WaterTestSession.id)
        .options(
            selectinload(WaterTestReading.parameter),
            selectinload(WaterTestReading.session),
        )
        .where(WaterTestSession.tank_id == tank_id)
        .order_by(desc(func.coalesce(WaterTestReading.updated_at, WaterTestSession.tested_at)))
    )
    latest: dict[int, WaterTestReading] = {}
    for r in result.scalars().all():
        if r.parameter_id not in latest:
            latest[r.parameter_id] = r
    readings = [
        _reading_out(r, r.session.tested_at if r.session else None)
        for r in sorted(latest.values(), key=lambda x: x.parameter_id)
    ]
    return WaterTestCurrentOut(tank_id=tank_id, readings=readings)


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
        tank_id=session.tank_id,
        tested_at=session.tested_at,
        notes=session.notes,
        readings=[_reading_out(r, session.tested_at) for r in session.readings],
    )


@router.post("/sessions", response_model=WaterTestSessionOut)
async def create_session(
    data: WaterTestSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    params_result = await db.execute(select(WaterTestParameter))
    params = {p.id: p for p in params_result.scalars().all()}
    norms = await _effective_norms_map(db, data.tank_id or 1)

    stamped = data.tested_at or datetime.utcnow()
    session = WaterTestSession(
        tank_id=data.tank_id,
        tested_at=stamped,
        notes=data.notes,
    )
    db.add(session)
    await db.flush()

    out_of_range_alerts = []
    for reading_in in data.readings:
        param = params.get(reading_in.parameter_id)
        if not param:
            raise HTTPException(422, f"Unknown parameter_id {reading_in.parameter_id}")

        min_safe, max_safe, _ = norms.get(param.id, (param.min_safe, param.max_safe, param.test_frequency_days))
        oor = False
        if min_safe is not None and reading_in.value < min_safe:
            oor = True
        if max_safe is not None and reading_in.value > max_safe:
            oor = True

        reading = WaterTestReading(
            session_id=session.id,
            parameter_id=param.id,
            value=reading_in.value,
            out_of_range=oor,
            notes=reading_in.notes,
            updated_at=stamped,
        )
        db.add(reading)
        if oor:
            out_of_range_alerts.append((param, reading_in.value))

    # a fresh reading resolves any pending "remind me later" for this param
    tested_tank_id = data.tank_id or 1
    param_ids = [r.parameter_id for r in data.readings]
    if param_ids:
        snoozes_result = await db.execute(
            select(WaterTestSnooze).where(
                WaterTestSnooze.tank_id == tested_tank_id,
                WaterTestSnooze.parameter_id.in_(param_ids),
            )
        )
        for snooze in snoozes_result.scalars().all():
            await db.delete(snooze)

    await db.commit()
    await broadcast_change("water_tests")

    logger.info("create_session scan_cache_id=%s", data.scan_cache_id)
    if data.scan_cache_id:
        corrected = {
            params[r.parameter_id].key: r.value
            for r in data.readings
            if r.parameter_id in params
        }
        await scan_cache.save_correction(db, data.scan_cache_id, corrected)

    # fire Telegram alerts for out-of-range readings
    for param, value in out_of_range_alerts:
        await n8n_client.water_test_alert(param, value)
        await ntfy_client.send(
            "Water test alert",
            f"{param.name_en} out of range: {value} {param.unit or ''}".strip(),
            priority=4,
            tags=["test_tube"],
        )

    # reload with relationships
    result = await db.execute(
        select(WaterTestSession)
        .options(selectinload(WaterTestSession.readings).selectinload(WaterTestReading.parameter))
        .where(WaterTestSession.id == session.id)
    )
    session = result.scalar_one()
    return WaterTestSessionOut(
        id=session.id,
        tank_id=session.tank_id,
        tested_at=session.tested_at,
        notes=session.notes,
        readings=[_reading_out(r, session.tested_at) for r in session.readings],
    )


@router.post("/readings", response_model=WaterTestCurrentOut)
async def upsert_readings(
    data: WaterTestSessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add or change specific parameters. Does not replace the rest of the table.

    Writes a new session containing only the posted keys. GET /current then
    shows those new values plus older params that were not in this payload.
    """
    if not data.readings:
        raise HTTPException(422, "readings required")
    await create_session(data, db)
    return await current_values(data.tank_id or 1, db)


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
