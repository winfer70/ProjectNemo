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
    # Tank 1 ("Akwarium Kuchnia") has no Tapo-plug light entry - the tank
    # light is BLE-controlled (Fluval, with its own on-board schedule, see
    # the Oswietlenie/Lighting tile) and the Tapo plug once considered for
    # this role stayed an office light instead. Confirmed with the user
    # 2026-09-21 - do not re-add without a real physical light plug.
    {"entity_id": settings.tapo_air_entity, "name": "Air Pump", "name_pl": "Pompa Powietrza", "role": "air", "tank_id": 1},
    # Tank 2 (Akwarium Salon) runs on a Meross power strip, addressed via
    # switch.smart_switch_... entity IDs (not Tapo). Confirmed: this Meross
    # strip has no power-monitoring hardware at all, so there is no sensor
    # entity to look up here, ever - `power_monitored: False` below skips
    # the HA lookup entirely instead of guessing at nonexistent sensor IDs.
    # watts/kwh_today will permanently read as None for these three devices.
    {"entity_id": settings.tapo_heater_entity_2, "name": "Heater", "name_pl": "Grzałka", "role": "heater", "tank_id": 2, "power_monitored": False},
    {"entity_id": settings.tapo_filter_entity_2, "name": "Filter+Pump", "name_pl": "Filtr+Pompka", "role": "filter", "tank_id": 2, "power_monitored": False},
    {"entity_id": settings.tapo_light_entity_2, "name": "Light", "name_pl": "Światło", "role": "light", "tank_id": 2, "power_monitored": False},
]


def _power_entities(switch_id: str) -> tuple[str, str]:
    """Derive Tapo power/energy sensor entity IDs from a switch entity ID.

    Only called for devices with power_monitored=True (Tank 1's Tapo
    plugs) - see the power_monitored=False entries in DEVICE_MAP above for
    Tank 2's Meross strip, which has no power-monitoring hardware.
    """
    base = switch_id.removeprefix("switch.")
    return f"sensor.{base}_current_consumption", f"sensor.{base}_today_s_consumption"


async def fetch_device(d: dict) -> DeviceOut:
    """Fetch live state + power data for one DEVICE_MAP entry from HA.

    Devices with power_monitored=False (Tank 2's Meross strip - no
    power-monitoring hardware) skip the sensor lookup entirely and always
    report watts=None / kwh_today=None.
    """
    power_monitored = d.get("power_monitored", True)
    if power_monitored:
        watts_entity, kwh_entity = _power_entities(d["entity_id"])
        state_data, kwh_today = await asyncio.gather(
            ha_client.get_entity_state(d["entity_id"]),
            ha_client.get_state_float(kwh_entity),
        )
    else:
        state_data = await ha_client.get_entity_state(d["entity_id"])
        kwh_today = None
    state_str = state_data.get("state", "unavailable")
    watts = await ha_client.get_state_float(watts_entity) if power_monitored and state_str == "on" else None
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
