"""WebSocket live push + scheduled jobs (daily summary, overdue checks)."""
import asyncio
import json
import logging
from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect

from config import settings
from services.ha_client import ha_client
from services.influx_client import influx_client
from services.n8n_client import n8n_client

logger = logging.getLogger("nemo.ws")

_connections: set[WebSocket] = set()


async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    _connections.add(websocket)
    logger.info("WS client connected — total %d", len(_connections))
    try:
        while True:
            # Keep connection alive; client can send pings
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


async def live_push_loop():
    """Push sensor + device data to all connected clients every 30 s."""
    while True:
        try:
            temp = await ha_client.get_state_float(settings.esphome_temp_entity)
            ph = await ha_client.get_state_float(settings.esphome_ph_entity)

            devices = []
            for entity_id in [
                settings.tapo_filter_entity,
                settings.tapo_heater_entity,
                settings.tapo_light_entity,
                settings.tapo_air_entity,
            ]:
                state = await ha_client.get_entity_state(entity_id)
                devices.append({
                    "entity_id": entity_id,
                    "state": state.get("state"),
                    "watts": state.get("attributes", {}).get("current_power_w"),
                    "kwh_today": state.get("attributes", {}).get("today_energy_kwh"),
                })

            await _broadcast({
                "type": "live",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "sensors": {"temperature": temp, "ph": ph, "tds": None, "orp": None},
                "devices": devices,
            })
        except Exception as exc:
            logger.warning("live_push_loop error: %s", exc)

        await asyncio.sleep(30)
