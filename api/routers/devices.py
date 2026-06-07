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


@router.get("", response_model=list[DeviceOut])
async def list_devices():
    devices = []
    for d in DEVICE_MAP:
        state_data = await ha_client.get_entity_state(d["entity_id"])
        devices.append(DeviceOut(
            entity_id=d["entity_id"],
            name=d["name"],
            name_pl=d["name_pl"],
            state=state_data.get("state", "unavailable"),
            watts=state_data.get("attributes", {}).get("current_power_w"),
            kwh_today=state_data.get("attributes", {}).get("today_energy_kwh"),
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
