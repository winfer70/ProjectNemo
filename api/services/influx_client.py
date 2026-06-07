"""InfluxDB v2 client — write sensor data, query history."""
from datetime import datetime, timedelta, timezone

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from config import settings
from models.schemas import SensorHistoryPoint


class InfluxClient:
    def __init__(self):
        self._client = influxdb_client.InfluxDBClient(
            url=settings.influxdb_url,
            token=settings.influxdb_token,
            org=settings.influxdb_org,
        )
        self._write = self._client.write_api(write_options=SYNCHRONOUS)
        self._query = self._client.query_api()

    def write_sensor(self, measurement: str, value: float, tags: dict | None = None):
        point = (
            influxdb_client.Point(measurement)
            .field("value", value)
        )
        for k, v in (tags or {}).items():
            point = point.tag(k, v)
        self._write.write(bucket=settings.influxdb_bucket, record=point)

    def write_power(self, device: str, watts: float, kwh_today: float):
        point = (
            influxdb_client.Point("power")
            .tag("device", device)
            .field("watts", watts)
            .field("kwh_today", kwh_today)
        )
        self._write.write(bucket=settings.influxdb_bucket, record=point)

    async def query_history(
        self, measurement: str, hours: int = 24
    ) -> list[SensorHistoryPoint]:
        flux = f"""
from(bucket: "{settings.influxdb_bucket}")
  |> range(start: -{hours}h)
  |> filter(fn: (r) => r._measurement == "{measurement}")
  |> filter(fn: (r) => r._field == "value")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
  |> sort(columns: ["_time"])
"""
        try:
            tables = self._query.query(flux, org=settings.influxdb_org)
            points = []
            for table in tables:
                for record in table.records:
                    points.append(SensorHistoryPoint(time=record.get_time(), value=record.get_value()))
            return points
        except Exception:
            return []


influx_client = InfluxClient()
