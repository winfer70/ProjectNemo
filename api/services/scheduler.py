"""APScheduler jobs — daily summary, overdue checks, feeding pause auto-resume."""
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, and_

from config import settings
from database import AsyncSessionLocal
from models.orm import FeedingPause, MaintenanceTask, Supply, WaterTestSession
from services.ha_client import ha_client
from services.n8n_client import n8n_client
from services.ntfy_client import ntfy_client
from services.influx_client import influx_client

logger = logging.getLogger("nemo.scheduler")

scheduler = AsyncIOScheduler(timezone="Europe/Dublin")


@scheduler.scheduled_job("cron", hour=8, minute=5)
async def daily_summary():
    temp = None
    if settings.zigbee_temp_entity:
        temp = await ha_client.get_state_float(settings.zigbee_temp_entity)
    if temp is None:
        temp = await ha_client.get_state_float(settings.esphome_temp_entity)
    ph = await ha_client.get_state_float(settings.esphome_ph_entity)

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
    temp_str = f"{temp:.1f}°C" if temp is not None else "—"
    await ntfy_client.send(
        "Daily summary",
        f"Temp: {temp_str} | pH: {ph or '—'} | Next: {soonest.name if soonest else 'none'}",
        priority=2,
        tags=["information_source"],
    )


@scheduler.scheduled_job("cron", hour=9, minute=0)
async def check_overdue():
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
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

        supply_result = await db.execute(select(Supply))
        for supply in supply_result.scalars().all():
            if supply.current_amount <= supply.min_threshold:
                await n8n_client.supply_low(supply)


@scheduler.scheduled_job("cron", hour=18, minute=55)
async def feeding_reminder():
    """5-min warning before 19:00 feeding — trigger filter pause."""
    await n8n_client.reminder(
        "Feeding in 5 min — trigger 3-min filter pause at 19:00",
        "Karmienie za 5 min — wcisnij pauze filtra o 19:00",
    )
    await ntfy_client.send(
        "Feeding time",
        "Trigger 3-min filter pause now. Feed: see today's rotation.",
        priority=4,
        tags=["fish"],
    )


@scheduler.scheduled_job("cron", day_of_week="sat", hour=9, minute=0)
async def saturday_maintenance_reminder():
    """Saturday morning: water change day reminder."""
    await n8n_client.reminder(
        "Water change day — produce 22L RO + 8L tap, blend 30L total",
        "Dzien wymiany wody — przygotuj 22L RO + 8L kranowej, razem 30L",
    )
    await ntfy_client.send(
        "Water change Saturday",
        "Produce 22L RO + blend with 8L tap = 30L. Add Prime. Change 30L. AF Life Essence 25ml + Yokuchi 5 pumps.",
        priority=4,
        tags=["droplet"],
    )


@scheduler.scheduled_job("interval", seconds=30)
async def resume_feeding_pauses():
    """Auto-resume devices whose feeding pause timer has expired."""
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(FeedingPause).where(
                and_(
                    FeedingPause.cancelled_at.is_(None),
                    FeedingPause.resumed_at.is_(None),
                    FeedingPause.resume_at <= now,
                )
            )
        )
        pauses = result.scalars().all()
        for pause in pauses:
            try:
                await ha_client.resume_devices(pause.paused_entities)
                logger.info("Auto-resumed feeding pause %d: %s", pause.id, pause.paused_entities)
            except Exception as exc:
                logger.warning("Failed to resume devices for pause %d: %s", pause.id, exc)
            pause.resumed_at = now
        if pauses:
            await db.commit()
