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

    async def get_entity_state(self, entity_id: str) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            try:
                r = await client.get(
                    f"{self._base}/api/states/{entity_id}", headers=self._headers
                )
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
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(
                f"{self._base}/api/services/{domain}/toggle",
                headers=self._headers,
                json={"entity_id": entity_id},
            )

    async def call_service(self, domain: str, service: str, data: dict):
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{self._base}/api/services/{domain}/{service}",
                headers=self._headers,
                json=data,
            )
            r.raise_for_status()

    async def pause_filter_for_feeding(self):
        """Turn filter off; HA automation restarts it after 10 min."""
        await self.call_service(
            "switch", "turn_off",
            {"entity_id": settings.tapo_filter_entity},
        )

    async def set_fluval_channels(self, r: int, g: int, b: int, w: int, ch5: int = 0):
        """Broadcast Fluval RGBW channel values to the tablet BLE gateway."""
        await ble_manager.broadcast(
            {"type": "fluval_channels", "r": r, "g": g, "b": b, "w": w, "ch5": ch5}
        )


ha_client = HAClient()
