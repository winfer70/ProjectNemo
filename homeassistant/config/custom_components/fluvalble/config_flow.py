"""Config flow for Fluval Shaker BLE."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak, async_discovered_service_info
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN

FLUVAL_SERVICE_UUID = "0000180a-0000-1000-8000-00805f9b34fb"


class FluvalBLEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            await self.async_set_unique_id(user_input["mac"].upper())
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"Fluval Shaker {user_input['mac']}", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("mac"): str,
            }),
            description_placeholders={
                "instructions": "Find the MAC address in the Fluval app or by scanning BLE devices"
            },
        )

    async def async_step_bluetooth(self, discovery_info: BluetoothServiceInfoBleak) -> FlowResult:
        """Handle Bluetooth discovery — auto-populate MAC."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        return await self.async_step_user({"mac": discovery_info.address})
