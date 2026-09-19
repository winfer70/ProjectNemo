"""Device control — Tapo P110 toggle + Fluval RGBW sliders."""
import asyncio

from fastapi import APIRouter, Depends, HTTPException

from models.schemas import DeviceOut, FluvalChannels
from services.device_status import DEVICE_MAP, fetch_device
from services.ha_client import ha_client

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("", response_model=list[DeviceOut])
async def list_devices(tank_id: int | None = None):
    wanted = [d for d in DEVICE_MAP if tank_id is None or d["tank_id"] == tank_id]

    # All devices fetched concurrently instead of one-by-one - this was the
    # main reason the tank view was slow to load (up to ~20 sequential HA
    # round-trips for 7 devices).
    return list(await asyncio.gather(*(fetch_device(d) for d in wanted)))


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
