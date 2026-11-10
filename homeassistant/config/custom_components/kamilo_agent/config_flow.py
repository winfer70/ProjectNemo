"""Config flow for Kamilo conversation agent."""
from __future__ import annotations

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN, CONF_URL, CONF_TOKEN

DEFAULT_URL = "http://192.168.0.125:8100"


class KamiloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kamilo."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input[CONF_URL].rstrip("/")
            token = user_input[CONF_TOKEN]

            # Validate: ping /health
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{url}/health",
                        timeout=aiohttp.ClientTimeout(total=5),
                    ) as resp:
                        if resp.status != 200:
                            errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Kamilo",
                    data={CONF_URL: url, CONF_TOKEN: token},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=DEFAULT_URL): str,
                    vol.Required(CONF_TOKEN): str,
                }
            ),
            errors=errors,
        )
