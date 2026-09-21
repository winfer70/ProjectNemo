"""WebSocket live push + device-off alerting."""
import asyncio
import json
import logging
from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect

from config import settings
from services.device_status import DEVICE_MAP, fetch_device
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
            settings.tapo_air_entity: ("Air Pump", "Pompa Powietrza"),
            settings.tapo_heater_entity_2: ("Heater (Salon)", "Grzałka (Salon)"),
            settings.tapo_filter_entity_2: ("Filter+Pump (Salon)", "Filtr+Pompka (Salon)"),
            settings.tapo_light_entity_2: ("Light (Salon)", "Światło (Salon)"),
        }
    return _ENTITY_NAMES


# DEVICE_MAP (imported from services.device_status) is the single shared
# source of device metadata + power_monitored flags - this module used to
# keep its own duplicate copy (_get_device_meta) that never got the Tank 2
# power_monitored=False fix, so it kept polling nonexistent Meross power
# sensors every 30s. Removed in favor of the shared list.


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


async def live_push_loop():
    """Push sensor + device data every 30s and check for device-off alerts."""
    while True:
        try:
            temp = None
            if settings.zigbee_temp_entity:
                temp = await ha_client.get_state_float(settings.zigbee_temp_entity)
            if temp is None:
                temp = await ha_client.get_state_float(settings.esphome_temp_entity)
            temp_2 = None
            if settings.zigbee_temp_entity_2:
                temp_2 = await ha_client.get_state_float(settings.zigbee_temp_entity_2)
            ph = await ha_client.get_state_float(settings.esphome_ph_entity)

            now_dt = datetime.now(timezone.utc)
            suppressed = await _get_suppressed_entities()
            names = _get_entity_names()

            devices = []
            for d in DEVICE_MAP:
                entity_id = d["entity_id"]
                dev_out = await fetch_device(d)
                state_str = dev_out.state

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

                devices.append({
                    "entity_id": entity_id,
                    "name": d["name"],
                    "name_pl": d["name_pl"],
                    "role": d["role"],
                    "tank_id": d["tank_id"],
                    "state": state_str,
                    "watts": dev_out.watts,
                    "kwh_today": dev_out.kwh_today,
                })

            await _broadcast({
                "type": "live",
                "timestamp": now_dt.isoformat(),
                "sensors": {
                    "temperature": temp, "ph": ph, "tds": None, "orp": None,
                    "tanks": [
                        {"id": "1", "name": settings.tank_1_name, "temperature": temp},
                        {"id": "2", "name": settings.tank_2_name, "temperature": temp_2},
                    ],
                },
                "devices": devices,
            })
        except Exception as exc:
            logger.warning("live_push_loop error: %s", exc)

        await asyncio.sleep(30)
