"""Device control — Tapo P110 toggle + Fluval RGBW sliders."""
import asyncio

from fastapi import APIRouter, Depends, HTTPException

from config import settings
from models.schemas import DeviceOut, FluvalChannels
from services.ha_client import ha_client

router = APIRouter(prefix="/api/devices", tags=["devices"])

DEVICE_MAP = [
    {"entity_id": settings.tapo_filter_entity, "name": "Filter", "name_pl": "Filtr", "role": "filter", "tank_id": 1},
    {"entity_id": settings.tapo_heater_entity, "name": "Heater", "name_pl": "Grzałka", "role": "heater", "tank_id": 1},
    {"entity_id": settings.tapo_light_entity, "name": "Light", "name_pl": "Światło", "role": "light", "tank_id": 1},
    {"entity_id": settings.tapo_air_entity, "name": "Air Pump", "name_pl": "Pompa Powietrza", "role": "air", "tank_id": 1},
    # Tank 2 (Akwarium Salon) - single Meross power strip, no power monitoring
    # available on this integration (watts/kwh will read as None).
    {"entity_id": settings.tapo_heater_entity_2, "name": "Heater", "name_pl": "Grzałka", "role": "heater", "tank_id": 2},
    {"entity_id": settings.tapo_filter_entity_2, "name": "Filter+Pump", "name_pl": "Filtr+Pompka", "role": "filter", "tank_id": 2},
    {"entity_id": settings.tapo_light_entity_2, "name": "Light", "name_pl": "Światło", "role": "light", "tank_id": 2},
]


def _power_entities(switch_id: str) -> tuple[str, str]:
    """Derive Tapo power/energy sensor entity IDs from a switch entity ID."""
    base = switch_id.removeprefix("switch.")
    return f"sensor.{base}_current_consumption", f"sensor.{base}_today_s_consumption"


@router.get("", response_model=list[DeviceOut])
async def list_devices(tank_id: int | None = None):
    wanted = [d for d in DEVICE_MAP if tank_id is None or d["tank_id"] == tank_id]

    async def _fetch(d: dict) -> DeviceOut:
        watts_entity, kwh_entity = _power_entities(d["entity_id"])
        state_data, kwh_today = await asyncio.gather(
            ha_client.get_entity_state(d["entity_id"]),
            ha_client.get_state_float(kwh_entity),
        )
        state_str = state_data.get("state", "unavailable")
        watts = await ha_client.get_state_float(watts_entity) if state_str == "on" else None
        return DeviceOut(
            entity_id=d["entity_id"],
            name=d["name"],
            name_pl=d["name_pl"],
            state=state_str,
            watts=watts,
            kwh_today=kwh_today,
            role=d["role"],
            tank_id=d["tank_id"],
        )

    # All devices fetched concurrently instead of one-by-one - this was the
    # main reason the tank view was slow to load (up to ~20 sequential HA
    # round-trips for 7 devices).
    return list(await asyncio.gather(*(_fetch(d) for d in wanted)))


@router.post("/{entity_id}/toggle")
async def toggle_device(entity_id: str):
    allowed = {d["entity_id"] for d in DEVICE_MAP}
    if entity_id not in allowed:
        raise HTTPException(403, "Entity not in allowed device list")
    await ha_client.toggle_entity(entity_id)
    return {"ok": True}


@router.put("/fluval/channels")
async def set_fluval_channels(channels: FluvalChannels):
    for val in (channels.r, channels.g, channels.b, channels.w, channels.ch5):
        if not 0 <= val <= 100:
            raise HTTPException(422, "Channel values must be 0–100")
    await ha_client.set_fluval_channels(channels.r, channels.g, channels.b, channels.w, channels.ch5)
    return {"ok": True, **channels.model_dump()}
