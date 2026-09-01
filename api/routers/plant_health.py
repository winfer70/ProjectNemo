"""Plant health tracking - static deficiency reference + logged issues.

Two ways an issue gets logged, both land in the same `plant_health_events`
table so the rest of the app (list view, Kamilo tools) doesn't care which:
  - manual: user taps a leaf on the reference diagram for a specific plant.
  - ai_scan: user photographs one affected leaf, POSTs it to /scan, the
    local Ollama vision model (services/plant_vision.py) classifies it.

Deliberately single-leaf-per-photo, not whole-plant multi-leaf detection -
that's a much harder CV problem (object detection, not classification) and
isn't what's built here. See services/plant_vision.py's module docstring.

An event is only ever marked "treated" by an explicit user action (website
tick or a Kamilo write-tool call reporting what was actually done) - never
auto-resolved just because a new photo looks better.
"""
import hashlib
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Plant, PlantHealthEvent
from models.schemas import (
    DeficiencyOut,
    PlantHealthEventCreate,
    PlantHealthEventOut,
    PlantHealthEventTreat,
    PlantHealthEventCorrect,
)
from services.plant_deficiencies import DEFICIENCIES, DEFICIENCIES_BY_KEY, VALID_KEYS
from services.plant_vision import analyze_plant_leaf
from services.websocket_manager import broadcast_change

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/plant-health", tags=["plant-health"])


@router.get("/deficiencies", response_model=list[DeficiencyOut])
async def list_deficiencies():
    """Static reference chart - no DB involved, always available."""
    return DEFICIENCIES


@router.get("/events", response_model=list[PlantHealthEventOut])
async def list_events(
    plant_id: int | None = None,
    tank_id: int | None = None,
    status: str | None = Query(None, pattern="^(pending|treated)$"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(PlantHealthEvent).order_by(desc(PlantHealthEvent.detected_at))
    if plant_id is not None:
        stmt = stmt.where(PlantHealthEvent.plant_id == plant_id)
    if tank_id is not None:
        stmt = stmt.where(PlantHealthEvent.tank_id == tank_id)
    if status is not None:
        stmt = stmt.where(PlantHealthEvent.status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/events", response_model=PlantHealthEventOut, status_code=201)
async def create_event(data: PlantHealthEventCreate, db: AsyncSession = Depends(get_db)):
    """Manual log - user tapped a deficiency on the reference diagram."""
    if data.deficiency_key not in VALID_KEYS:
        raise HTTPException(422, f"Unknown deficiency_key {data.deficiency_key!r}")
    plant = await db.get(Plant, data.plant_id)
    if not plant:
        raise HTTPException(404, "Plant not found")

    event = PlantHealthEvent(
        plant_id=data.plant_id,
        tank_id=data.tank_id if data.tank_id is not None else plant.tank_id,
        deficiency_key=data.deficiency_key,
        source="manual",
        notes=data.notes,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    await broadcast_change("plant_health")
    return event


@router.post("/scan", response_model=PlantHealthEventOut, status_code=201)
async def scan_leaf(
    plant_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Camera path: one photo of one leaf -> Ollama vision classification
    -> a new pending event, same as a manual log but source='ai_scan' with
    a confidence score attached."""
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(404, "Plant not found")

    image_bytes = await file.read()
    photo_hash = hashlib.sha256(image_bytes).hexdigest()

    try:
        result = await analyze_plant_leaf(image_bytes)
    except ValueError as exc:
        raise HTTPException(422, str(exc))

    event = PlantHealthEvent(
        plant_id=plant_id,
        tank_id=plant.tank_id,
        deficiency_key=result["deficiency_key"],
        source="ai_scan",
        confidence=result["confidence"],
        photo_hash=photo_hash,
        notes=result.get("reasoning"),
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    await broadcast_change("plant_health")
    return event


@router.patch("/events/{event_id}/treat", response_model=PlantHealthEventOut)
async def treat_event(
    event_id: int,
    data: PlantHealthEventTreat,
    db: AsyncSession = Depends(get_db),
):
    """The ONLY way an event becomes 'treated' - explicit user action
    (website tick or a Kamilo write-tool reporting what was actually
    done). Never set automatically."""
    event = await db.get(PlantHealthEvent, event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    event.status = "treated"
    event.treatment_notes = data.treatment_notes
    event.treated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    await broadcast_change("plant_health")
    return event


@router.patch("/events/{event_id}/correct", response_model=PlantHealthEventOut)
async def correct_event(
    event_id: int,
    data: PlantHealthEventCorrect,
    db: AsyncSession = Depends(get_db),
):
    """Self-improving-loop hook: user (via website or Kamilo) says the
    diagnosis was wrong. Logs the correction against the event rather than
    silently overwriting deficiency_key, so the original AI/manual call is
    still visible for future reference."""
    if data.corrected_deficiency_key not in VALID_KEYS:
        raise HTTPException(422, f"Unknown deficiency_key {data.corrected_deficiency_key!r}")
    event = await db.get(PlantHealthEvent, event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    event.corrected_deficiency_key = data.corrected_deficiency_key
    event.correction_notes = data.correction_notes
    await db.commit()
    await db.refresh(event)
    await broadcast_change("plant_health")
    return event


# ── Kamilo (voice) convenience endpoints ─────────────────────────────────────
# Voice input can't supply a plant_id or event_id, only a spoken plant name -
# these do the name -> plant -> latest-pending-event resolution server-side
# so the HA script stays a thin passthrough, matching the existing
# heimdall_aquarium_temp_history pattern (see PROJECTNEMO_API.md).

async def _find_plant_by_name(db: AsyncSession, name: str) -> Plant | None:
    needle = name.strip().lower()
    result = await db.execute(select(Plant))
    for plant in result.scalars().all():
        haystack = " ".join(filter(None, [plant.name_en, plant.name_pl, plant.latin])).lower()
        if needle in haystack:
            return plant
    return None


@router.get("/kamilo/status")
async def kamilo_status(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlantHealthEvent)
        .where(PlantHealthEvent.status == "pending")
        .order_by(desc(PlantHealthEvent.detected_at))
    )
    events = result.scalars().all()
    if not events:
        return {"pending_count": 0, "issues": [], "summary": "No plant health issues are currently pending."}

    issues = []
    for e in events:
        plant = await db.get(Plant, e.plant_id)
        deficiency = DEFICIENCIES_BY_KEY.get(e.deficiency_key)
        days_ago = (datetime.now(timezone.utc) - e.detected_at.replace(tzinfo=timezone.utc)).days
        issues.append({
            "plant_name": plant.name_en if plant else "unknown plant",
            "deficiency_name": deficiency["name_en"] if deficiency else e.deficiency_key,
            "days_ago": days_ago,
        })

    lines = [f"{i['plant_name']}: {i['deficiency_name']} ({i['days_ago']} day(s) ago)" for i in issues]
    summary = f"{len(issues)} pending plant health issue(s): " + "; ".join(lines)
    return {"pending_count": len(issues), "issues": issues, "summary": summary}


@router.post("/kamilo/treat")
async def kamilo_treat(plant_name: str, treatment_notes: str | None = None, db: AsyncSession = Depends(get_db)):
    plant = await _find_plant_by_name(db, plant_name)
    if not plant:
        return {"status": "not_found", "summary": f"No plant matching '{plant_name}' was found."}

    result = await db.execute(
        select(PlantHealthEvent)
        .where(PlantHealthEvent.plant_id == plant.id, PlantHealthEvent.status == "pending")
        .order_by(desc(PlantHealthEvent.detected_at))
    )
    event = result.scalars().first()
    if not event:
        return {"status": "no_pending_issue", "summary": f"{plant.name_en} has no pending health issues."}

    event.status = "treated"
    event.treatment_notes = treatment_notes
    event.treated_at = datetime.now(timezone.utc)
    await db.commit()
    await broadcast_change("plant_health")

    deficiency = DEFICIENCIES_BY_KEY.get(event.deficiency_key)
    deficiency_name = deficiency["name_en"] if deficiency else event.deficiency_key
    return {
        "status": "treated",
        "plant_name": plant.name_en,
        "deficiency_name": deficiency_name,
        "summary": f"Marked {deficiency_name} on {plant.name_en} as treated.",
    }

