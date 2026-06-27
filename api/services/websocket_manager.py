"""WebSocket live push + device-off alerting."""
import asyncio
import json
import logging
from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect

from config import settings
from services.ha_client import ha_client
from services.n8n_client import n8n_client
from services.ntfy_client import ntfy_client

logger = logging.getLogger("nemo.ws")

_connections: set[WebSocket] = set()

_device_off_since: dict[str, datetime] = {}
_device_alert_sent: set[str] = set()

DEVICE_OFF_ALERT_MINUTES = 10

_ENTITY_NAMES: dict[str, tuple[str, str]] | None = None


def _get_entity_names() -> dict[str, tuple[str, str]]:
    global _ENTITY_NAMES
    if _ENTITY_NAMES is None:
        _ENTITY_NAMES = {
            settings.tapo_filter_entity: ("Filter", "Filtr"),
            settings.tapo_heater_entity: ("Heater", "Grzałka"),
            settings.tapo_light_entity: ("Light", "Światło"),
            settings.tapo_air_entity: ("Air Pump", "Pompa Powietrza"),
        }
    return _ENTITY_NAMES


_DEVICE_META: list[dict] | None = None


def _get_device_meta() -> list[dict]:
    global _DEVICE_META
    if _DEVICE_META is None:
        _DEVICE_META = [
            {"entity_id": settings.tapo_filter_entity, "name": "Filter", "name_pl": "Filtr", "role": "filter"},
            {"entity_id": settings.tapo_heater_entity, "name": "Heater", "name_pl": "Grzałka", "role": "heater"},
            {"entity_id": settings.tapo_light_entity, "name": "Light", "name_pl": "Światło", "role": "light"},
            {"entity_id": settings.tapo_air_entity, "name": "Air Pump", "name_pl": "Pompa Powietrza", "role": "air"},
        ]
    return _DEVICE_META


async def _get_suppressed_entities() -> set[str]:
    """Return entity IDs that should NOT trigger device-off alerts."""
    suppressed: set[str] = set()
    try:
        from database import AsyncSessionLocal
        from models.orm import FeedingPause, MaintenanceTask
        from sqlalchemy import select, and_

        async with AsyncSessionLocal() as db:
            now = datetime.now(timezone.utc)
            fp_result = await db.execute(
                select(FeedingPause).where(
                    and_(
                        FeedingPause.cancelled_at.is_(None),
                        FeedingPause.resumed_at.is_(None),
                        FeedingPause.resume_at > now,
                    )
                )
            )
            for fp in fp_result.scalars().all():
                suppressed.update(fp.paused_entities)

            mt_result = await db.execute(
                select(MaintenanceTask).where(MaintenanceTask.started_at.isnot(None))
            )
            for mt in mt_result.scalars().all():
                if mt.affects_entity:
                    suppressed.add(mt.affects_entity)
    except Exception as exc:
        logger.warning("suppressed entity check failed: %s", exc)
    return suppressed


async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    _connections.add(websocket)
    logger.info("WS client connected — total %d", len(_connections))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        _connections.discard(websocket)
        logger.info("WS client disconnected — total %d", len(_connections))


async def _broadcast(data: dict):
    dead = set()
    for ws in list(_connections):
        try:
            await ws.send_text(json.dumps(data))
        except Exception:
            dead.add(ws)
    _connections.difference_update(dead)


async def broadcast_change(domain: str):
    """Notify all WS clients that a domain's data changed so they re-fetch."""
    await _broadcast({"type": "invalidate", "domain": domain})


def _power_entities(switch_id: str) -> tuple[str, str]:
    """Derive Tapo power/energy sensor entity IDs from a switch entity ID."""
    base = switch_id.removeprefix("switch.")
    return f"sensor.{base}_current_consumption", f"sensor.{base}_today_s_consumption"


async def live_push_loop():
    """Push sensor + device data every 30s and check for device-off alerts."""
    while True:
        try:
            temp = None
            if settings.zigbee_temp_entity:
                temp = await ha_client.get_state_float(settings.zigbee_temp_entity)
            if temp is None:
                temp = await ha_client.get_state_float(settings.esphome_temp_entity)
            ph = await ha_client.get_state_float(settings.esphome_ph_entity)

            now_dt = datetime.now(timezone.utc)
            suppressed = await _get_suppressed_entities()
            names = _get_entity_names()
            meta = _get_device_meta()

            devices = []
            for d in meta:
                entity_id = d["entity_id"]
                state = await ha_client.get_entity_state(entity_id)
                state_str = state.get("state")

                if state_str == "on":
                    _device_off_since.pop(entity_id, None)
                    _device_alert_sent.discard(entity_id)
                elif state_str == "off":
                    if entity_id not in _device_off_since:
                        _device_off_since[entity_id] = now_dt
                    off_since = _device_off_since[entity_id]
                    off_minutes = (now_dt - off_since).total_seconds() / 60

                    if (
                        off_minutes >= DEVICE_OFF_ALERT_MINUTES
                        and entity_id not in suppressed
                        and entity_id not in _device_alert_sent
                    ):
                        name_en, name_pl = names.get(entity_id, (entity_id, entity_id))
                        try:
                            await n8n_client.reminder(
                                f"⚠️ {name_en} has been OFF for {int(off_minutes)} minutes",
                                f"⚠️ {name_pl} wyłączony od {int(off_minutes)} minut",
                            )
                        except Exception as exc:
                            logger.warning("device-off alert failed for %s: %s", entity_id, exc)
                        _device_alert_sent.add(entity_id)

                watts_entity, kwh_entity = _power_entities(entity_id)
                watts = await ha_client.get_state_float(watts_entity) if state_str == "on" else None
                kwh_today = await ha_client.get_state_float(kwh_entity)
                devices.append({
                    "entity_id": entity_id,
                    "name": d["name"],
                    "name_pl": d["name_pl"],
                    "role": d["role"],
                    "state": state_str,
                    "watts": watts,
                    "kwh_today": kwh_today,
                })

            await _broadcast({
                "type": "live",
                "timestamp": now_dt.isoformat(),
                "sensors": {"temperature": temp, "ph": ph, "tds": None, "orp": None},
                "devices": devices,
            })
        except Exception as exc:
            logger.warning("live_push_loop error: %s", exc)

        await asyncio.sleep(30)
