"""Water test sessions + readings + trends."""
import base64
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
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
from services import ollama_vision, scan_cache, strip_cv

import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/water-tests", tags=["water-tests"])





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
