"""Continuous sensor data — current state + history from InfluxDB."""
import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query

from config import settings
from models.schemas import SensorCurrentOut, SensorHistoryPoint, TankTemperatureOut
from services.ha_client import ha_client
from services.influx_client import influx_client

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("/current", response_model=SensorCurrentOut)
async def current_sensors():
    async def _tank1_temp():
        if settings.zigbee_temp_entity:
            v = await ha_client.get_state_float(settings.zigbee_temp_entity)
            if v is not None:
                return v
        return await ha_client.get_state_float(settings.esphome_temp_entity)

    async def _tank2_temp():
        if settings.zigbee_temp_entity_2:
            return await ha_client.get_state_float(settings.zigbee_temp_entity_2)
        return None

    # Fetched concurrently instead of one-by-one - each is an independent HA call.
    temp, temp_2, ph = await asyncio.gather(
        _tank1_temp(), _tank2_temp(), ha_client.get_state_float(settings.esphome_ph_entity),
    )
    return SensorCurrentOut(
        temperature=temp,
        ph=ph,
        tds=None,
        orp=None,
        updated_at=datetime.now(timezone.utc),
        tanks=[
            TankTemperatureOut(id="1", name=settings.tank_1_name, temperature=temp),
            TankTemperatureOut(id="2", name=settings.tank_2_name, temperature=temp_2),
        ],
    )


@router.get("/history")
async def sensor_history(
    measurement: str = Query(..., description="temperature | ph | tds | orp"),
    hours: int = Query(24, ge=1, le=168),
):
    points = await influx_client.query_history(measurement, hours)
    return points
