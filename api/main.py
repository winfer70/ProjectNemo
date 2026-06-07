"""FastAPI application orchestrator for the ProjectNemo aquarium monitoring system."""
import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from config import settings
from database import init_db, AsyncSessionLocal
from ble_manager import ble_manager
from routers import calendar, devices, dosing, maintenance, obsada, schedule, sensors, supplies, water_tests
from seed_data import seed
from services.scheduler import scheduler
from services.websocket_manager import live_push_loop, ws_endpoint

logging.basicConfig(level=settings.log_level.upper())
logging.getLogger().setLevel(settings.log_level.upper())

app = FastAPI(title="Project Nemo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schedule.router)
app.include_router(calendar.router)
app.include_router(dosing.router)
app.include_router(supplies.router)
app.include_router(maintenance.router)
app.include_router(water_tests.router)
app.include_router(sensors.router)
app.include_router(devices.router)
app.include_router(obsada.router)


@app.websocket("/ws/ble")
async def ble_ws(websocket: WebSocket):
    await ble_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ble_manager.disconnect(websocket)


@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await ws_endpoint(websocket)


async def _run_migrations():
    """Add new columns to existing tables. SQLite-safe: errors mean column exists."""
    async with AsyncSessionLocal() as db:
        migrations = [
            "ALTER TABLE maintenance_tasks ADD COLUMN started_at DATETIME",
            "ALTER TABLE maintenance_tasks ADD COLUMN affects_entity VARCHAR(100)",
        ]
        for sql in migrations:
            try:
                await db.execute(text(sql))
                await db.commit()
            except Exception:
                pass  # column already exists


@app.on_event("startup")
async def on_startup():
    await init_db()
    await _run_migrations()
    async with AsyncSessionLocal() as db:
        await seed(db)
    scheduler.start()
    asyncio.create_task(live_push_loop())


@app.on_event("shutdown")
async def on_shutdown():
    scheduler.shutdown(wait=False)


@app.get("/health")
async def health():
    return {"status": "ok"}
