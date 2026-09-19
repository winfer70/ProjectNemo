"""Shared smart-plug device status fetching.

DEVICE_MAP and fetch_device() used to live only inside routers/devices.py.
Pulled out here so both the devices router and the power-history scheduler
job (services/scheduler.py) can fetch the same live HA device state without
duplicating the fetch logic.
"""
import asyncio

from config import settings
from models.schemas import DeviceOut
from services.ha_client import ha_client

DEVICE_MAP = [
    {"entity_id": settings.tapo_filter_entity, "name": "Filter", "name_pl": "Filtr", "role": "filter", "tank_id": 1},
    {"entity_id": settings.tapo_heater_entity, "name": "Heater", "name_pl": "Grzałka", "role": "heater", "tank_id": 1},
    {"entity_id": settings.tapo_light_entity, "name": "Light", "name_pl": "Światło", "role": "light", "tank_id": 1},
    {"entity_id": settings.tapo_air_entity, "name": "Air Pump", "name_pl": "Pompa Powietrza", "role": "air", "tank_id": 1},
    # Tank 2 (Akwarium Salon) - Meross power strip, addressed via
    # switch.smart_switch_... entity IDs (not Tapo). _power_entities() below
    # derives power/energy sensor IDs using Tapo naming conventions, which do
    # NOT apply to this Meross integration.
    # TODO: confirm the real Meross power-sensor entity IDs for these three
    # outlets (if the integration exposes per-outlet power/energy sensors at
    # all) from Home Assistant -> Developer Tools -> States, then update
    # _power_entities() (or give these entries their own sensor id fields)
    # accordingly. Until that's done, watts/kwh_today for Tank 2 devices will
    # always read as None - this is a known, accepted limitation, not a bug
    # to guess around.
    {"entity_id": settings.tapo_heater_entity_2, "name": "Heater", "name_pl": "Grzałka", "role": "heater", "tank_id": 2},
    {"entity_id": settings.tapo_filter_entity_2, "name": "Filter+Pump", "name_pl": "Filtr+Pompka", "role": "filter", "tank_id": 2},
    {"entity_id": settings.tapo_light_entity_2, "name": "Light", "name_pl": "Światło", "role": "light", "tank_id": 2},
]


def _power_entities(switch_id: str) -> tuple[str, str]:
    """Derive Tapo power/energy sensor entity IDs from a switch entity ID.

    Only valid for the Tapo-style tank_id==1 devices - see the TODO on the
    tank_id==2 entries in DEVICE_MAP above for why this does not apply to
    Tank 2's Meross power strip.
    """
    base = switch_id.removeprefix("switch.")
    return f"sensor.{base}_current_consumption", f"sensor.{base}_today_s_consumption"


async def fetch_device(d: dict) -> DeviceOut:
    """Fetch live state + power data for one DEVICE_MAP entry from HA.

    Gracefully degrades to watts=None / kwh_today=None when the power
    sensors don't exist or HA can't be reached (see HAClient.get_state_float)
    - this is expected for Tank 2 devices today.
    """
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
