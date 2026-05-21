"""APScheduler jobs — daily summary, overdue maintenance/test checks."""
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from database import AsyncSessionLocal
from models.orm import MaintenanceTask, Supply, WaterTestSession
from services.ha_client import ha_client
from services.n8n_client import n8n_client
from services.influx_client import influx_client

logger = logging.getLogger("nemo.scheduler")

scheduler = AsyncIOScheduler(timezone="Europe/Dublin")


@scheduler.scheduled_job("cron", hour=8, minute=5)
async def daily_summary():
    temp = await ha_client.get_state_float("sensor.nemo_sensor_temperature")
    ph = await ha_client.get_state_float("sensor.nemo_sensor_ph")

    async with AsyncSessionLocal() as db:
        last_session = await db.execute(
            select(WaterTestSession).order_by(WaterTestSession.tested_at.desc()).limit(1)
        )
        last_test = last_session.scalar_one_or_none()
        days_since_test = (
            (datetime.now(timezone.utc) - last_test.tested_at.replace(tzinfo=timezone.utc)).days
            if last_test
            else "?"
        )

        maint_result = await db.execute(
            select(MaintenanceTask).order_by(MaintenanceTask.next_due)
        )
        tasks = maint_result.scalars().all()
        soonest = tasks[0] if tasks else None

    await n8n_client.daily_summary({
        "temperature": temp,
        "ph": ph,
        "days_since_test": days_since_test,
        "next_maintenance": soonest.name if soonest else "none",
        "next_maintenance_pl": soonest.name_pl if soonest else "brak",
        "next_maintenance_days": (soonest.next_due - datetime.now(timezone.utc)).days
        if soonest and soonest.next_due
        else None,
    })


@scheduler.scheduled_job("cron", hour=9, minute=0)
async def check_overdue():
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        # Maintenance due / overdue
        result = await db.execute(select(MaintenanceTask))
        for task in result.scalars().all():
            if task.next_due is None:
                continue
            due = task.next_due.replace(tzinfo=timezone.utc) if task.next_due.tzinfo is None else task.next_due
            days_until = (due - now).days
            if days_until == 0:
                await n8n_client.reminder(
                    f"🔧 {task.name} due today!",
                    f"🔧 {task.name_pl} — dziś!",
                )
            elif days_until == 7:
                parts_list = "\n".join(f"☐ {p['supply_name']}" for p in task.required_parts)
                await n8n_client.reminder(
                    f"🔧 {task.name} in 7 days. Check parts:\n{parts_list or '(none required)'}",
                    f"🔧 {task.name_pl} za 7 dni. Sprawdź części:\n{parts_list or '(brak)'}",
                )

        # Water test overdue (>7 days since last session)
        last = await db.execute(
            select(WaterTestSession).order_by(WaterTestSession.tested_at.desc()).limit(1)
        )
        last_test = last.scalar_one_or_none()
        if last_test:
            tested_at = last_test.tested_at.replace(tzinfo=timezone.utc) if last_test.tested_at.tzinfo is None else last_test.tested_at
            days_ago = (now - tested_at).days
            if days_ago >= 7:
                await n8n_client.reminder(
                    f"🧪 Water test overdue — last tested {days_ago} days ago",
                    f"🧪 Test wody zaległy — ostatni test {days_ago} dni temu",
                )

        # Supply warnings
        supply_result = await db.execute(select(Supply))
        for supply in supply_result.scalars().all():
            if supply.current_amount <= supply.min_threshold:
                await n8n_client.supply_low(supply)
