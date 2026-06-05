"""BLE gateway WebSocket connection manager.

The Samsung tablet placed beside the aquarium connects here and executes
GATT writes locally, bridging the ~5 m floor gap between REDACTED-HOST and the
Fluval Aquasky 2.0 light where direct Bluetooth is not reachable.

Both main.py (endpoint registration) and services/ha_client.py (broadcast
calls) import the singleton from this module, avoiding a circular import.
"""
import logging

from fastapi import WebSocket

logger = logging.getLogger("nemo.ble")


class BLEConnectionManager:
    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)
        logger.info("BLE gateway connected — total %d", len(self.clients))

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)
        logger.info("BLE gateway disconnected — total %d", len(self.clients))

    async def broadcast(self, payload: dict):
        dead: set[WebSocket] = set()
        for ws in self.clients:
            try:
                await ws.send_json(payload)
            except Exception:
                dead.add(ws)
        self.clients -= dead


ble_manager = BLEConnectionManager()
