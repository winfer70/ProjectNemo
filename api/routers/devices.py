"""Device control — Tapo P110 toggle + Fluval RGBW sliders."""
from fastapi import APIRouter, Depends, HTTPException

from config import settings
from models.schemas import DeviceOut, FluvalChannels
from services.ha_client import ha_client

router = APIRouter(prefix="/api/devices", tags=["devices"])

DEVICE_MAP = [
    {"entity_id": settings.tapo_filter_entity, "name": "Filter", "name_pl": "Filtr", "role": "filter"},
    {"entity_id": settings.tapo_heater_entity, "name": "Heater", "name_pl": "Grzałka", "role": "heater"},
    {"entity_id": settings.tapo_light_entity, "name": "Light", "name_pl": "Światło", "role": "light"},
    {"entity_id": settings.tapo_air_entity, "name": "Air Pump", "name_pl": "Pompa Powietrza", "role": "air"},
]


def _power_entities(switch_id: str) -> tuple[str, str]:
    """Derive Tapo power/energy sensor entity IDs from a switch entity ID."""
    base = switch_id.removeprefix("switch.")
    return f"sensor.{base}_current_consumption", f"sensor.{base}_today_s_consumption"


@router.get("", response_model=list[DeviceOut])
async def list_devices():
    devices = []
    for d in DEVICE_MAP:
        state_data = await ha_client.get_entity_state(d["entity_id"])
        state_str = state_data.get("state", "unavailable")
        watts_entity, kwh_entity = _power_entities(d["entity_id"])
        watts = await ha_client.get_state_float(watts_entity) if state_str == "on" else None
        kwh_today = await ha_client.get_state_float(kwh_entity)
        devices.append(DeviceOut(
            entity_id=d["entity_id"],
            name=d["name"],
            name_pl=d["name_pl"],
            state=state_str,
            watts=watts,
            kwh_today=kwh_today,
            role=d["role"],
        ))
    return devices


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
