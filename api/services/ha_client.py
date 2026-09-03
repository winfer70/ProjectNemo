"""Home Assistant REST API client."""
import httpx

from ble_manager import ble_manager
from config import settings


class HAClient:
    def __init__(self):
        self._base = settings.ha_url.rstrip("/")
        self._headers = {
            "Authorization": f"Bearer {settings.ha_token}",
            "Content-Type": "application/json",
        }
        # Reused across all requests - avoids a fresh TCP/TLS handshake on
        # every single HA call, which was the main cause of slow page loads
        # when a view fetches many entities (e.g. the devices list).
        self._client = httpx.AsyncClient(base_url=self._base, headers=self._headers, timeout=5)

    async def get_entity_state(self, entity_id: str) -> dict:
        try:
            r = await self._client.get(f"/api/states/{entity_id}")
            r.raise_for_status()
            return r.json()
        except Exception:
            return {"state": "unavailable", "attributes": {}}

    async def get_state_float(self, entity_id: str) -> float | None:
        data = await self.get_entity_state(entity_id)
        try:
            return float(data["state"])
        except (KeyError, ValueError, TypeError):
            return None

    async def toggle_entity(self, entity_id: str):
        domain = entity_id.split(".")[0]
        await self._client.post(
            f"/api/services/{domain}/toggle", json={"entity_id": entity_id},
        )

    async def call_service(self, domain: str, service: str, data: dict):
        r = await self._client.post(f"/api/services/{domain}/{service}", json=data, timeout=10)
        r.raise_for_status()

    async def turn_on_entity(self, entity_id: str):
        domain = entity_id.split(".")[0]
        await self.call_service(domain, "turn_on", {"entity_id": entity_id})

    async def turn_off_entity(self, entity_id: str):
        domain = entity_id.split(".")[0]
        await self.call_service(domain, "turn_off", {"entity_id": entity_id})

    async def pause_devices_for_feeding(self, entity_ids: list[str]):
        """Turn off multiple devices for feeding mode."""
        for eid in entity_ids:
            await self.turn_off_entity(eid)

    async def resume_devices(self, entity_ids: list[str]):
        """Turn on devices after feeding pause ends."""
        for eid in entity_ids:
            await self.turn_on_entity(eid)

    async def pause_filter_for_feeding(self):
        """Legacy: turn off filter only."""
        await self.turn_off_entity(settings.tapo_filter_entity)

    async def set_fluval_channels(self, r: int, g: int, b: int, w: int, ch5: int = 0):
        """Broadcast Fluval RGBW channel values to the tablet BLE gateway."""
        await ble_manager.broadcast(
            {"type": "fluval_channels", "r": r, "g": g, "b": b, "w": w, "ch5": ch5}
        )

    async def converse(self, text: str, language: str = "en", conversation_id: str | None = None) -> dict:
        """Send text to HA's conversation API (Kamilo/Heimdall or whichever
        agent is configured) - the same pipeline voice commands go through,
        just typed/spoken from the website instead of a smart speaker."""
        payload = {"text": text, "language": language}
        if settings.ha_conversation_agent_id:
            payload["agent_id"] = settings.ha_conversation_agent_id
        if conversation_id:
            payload["conversation_id"] = conversation_id
        r = await self._client.post("/api/conversation/process", json=payload, timeout=20)
        r.raise_for_status()
        return r.json()


ha_client = HAClient()
