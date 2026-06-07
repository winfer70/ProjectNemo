"""Number entities for each Fluval RGBW channel."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .protocol import (
    CHANNEL_B,
    CHANNEL_G,
    CHANNEL_R,
    CHANNEL_W,
    GATT_CHAR_UUID,
    build_single_channel_command,
)

_LOGGER = logging.getLogger(__name__)

CHANNEL_DEFS = [
    ("r", "Red",   CHANNEL_R, "mdi:led-strip-variant"),
    ("g", "Green", CHANNEL_G, "mdi:led-strip-variant"),
    ("b", "Blue",  CHANNEL_B, "mdi:led-strip-variant"),
    ("w", "White", CHANNEL_W, "mdi:white-balance-sunny"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    mac: str = entry.data["mac"]
    entities = [
        FluvalChannelNumber(mac, key, name, channel_id, icon)
        for key, name, channel_id, icon in CHANNEL_DEFS
    ]
    async_add_entities(entities)


class FluvalChannelNumber(NumberEntity):
    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "%"

    def __init__(self, mac: str, key: str, name: str, channel_id: int, icon: str):
        self._mac = mac
        self._key = key
        self._channel_id = channel_id
        self._attr_name = f"Fluval Shaker {name}"
        self._attr_unique_id = f"fluval_{mac}_{key}"
        self._attr_icon = icon
        self._attr_native_value: float = 0

    async def async_set_native_value(self, value: float) -> None:
        from homeassistant.components.bluetooth import async_ble_device_from_address
        from bleak import BleakClient

        device = async_ble_device_from_address(self.hass, self._mac, connectable=True)
        if not device:
            _LOGGER.warning("Fluval BLE device %s not found", self._mac)
            return

        command = build_single_channel_command(self._channel_id, int(value))
        try:
            async with BleakClient(device) as client:
                await client.write_gatt_char(GATT_CHAR_UUID, command, response=False)
            self._attr_native_value = value
            self.async_write_ha_state()
        except Exception as exc:
            _LOGGER.error("Fluval BLE write failed: %s", exc)
