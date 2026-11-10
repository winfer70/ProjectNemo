"""Kamilo conversation platform."""
from __future__ import annotations

import asyncio
import logging

import aiohttp
from homeassistant.components.conversation import (
    ConversationEntity,
    ConversationEntityFeature,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.intent import IntentResponse

from . import CONF_TOKEN, CONF_URL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([KamiloConversationEntity(entry)])


class KamiloConversationEntity(ConversationEntity):
    """Proxies conversation turns to kamilo-core /ha/chat."""

    _attr_name = "Kamilo"
    _attr_unique_id = "kamilo_agent_conversation"
    _attr_supported_features = ConversationEntityFeature.CONTROL
    _attr_has_entity_name = False

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._url = entry.data[CONF_URL].rstrip("/")
        self._token = entry.data[CONF_TOKEN]

    @property
    def supported_languages(self) -> str:
        return "*"

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        lang = user_input.language or "en"
        intent_response = IntentResponse(language=lang)

        try:
            # Tool-calling queries (device control, portfolio lookups) can take
            # well over 30s on a 14B model — 30s was tight enough that even a
            # single-tool query sometimes hit it, surfacing as a generic
            # "Kamilo error" with no indication it was actually a timeout.
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=90)) as session:
                async with session.post(
                    f"{self._url}/ha/chat",
                    json={"text": user_input.text, "language": lang},
                    headers={
                        "X-Kamilo-Token": self._token,
                        "Content-Type": "application/json",
                    },
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        reply = data.get("response", "")
                    elif resp.status == 401:
                        reply = "Kamilo: invalid token. Check KAMILO_HA_TOKENS."
                    else:
                        reply = f"Kamilo: HTTP {resp.status}"
        except aiohttp.ClientConnectorError:
            _LOGGER.error("Cannot reach Kamilo at %s", self._url)
            reply = "Kamilo is unreachable." if lang == "en" else "Nie mogę połączyć się z Kamilo."
        except (asyncio.TimeoutError, aiohttp.ServerTimeoutError):
            _LOGGER.error("Kamilo request timed out after 90s")
            reply = "Kamilo took too long to answer." if lang == "en" else "Kamilo zbyt długo odpowiadał."
        except Exception as exc:
            _LOGGER.error("Kamilo request error: %s", exc)
            reply = "Kamilo error." if lang == "en" else "Błąd Kamilo."

        intent_response.async_set_speech(reply)
        return ConversationResult(
            response=intent_response,
            conversation_id=user_input.conversation_id,
        )
