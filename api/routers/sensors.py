"""Continuous sensor data — current state + history from InfluxDB."""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query

from models.schemas import SensorCurrentOut, SensorHistoryPoint
from services.ha_client import ha_client
from services.influx_client import influx_client

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("/current", response_model=SensorCurrentOut)
async def current_sensors():
    temp = await ha_client.get_state_float("sensor.nemo_sensor_temperature")
    ph = await ha_client.get_state_float("sensor.nemo_sensor_ph")
    return SensorCurrentOut(
        temperature=temp,
        ph=ph,
        tds=None,   # Phase B — not yet wired
        orp=None,   # Phase B — not yet wired
        updated_at=datetime.now(timezone.utc),
    )


@router.get("/history")
async def sensor_history(
    measurement: str = Query(..., description="temperature | ph | tds | orp"),
    hours: int = Query(24, ge=1, le=168),
):
    points = await influx_client.query_history(measurement, hours)
    return points
