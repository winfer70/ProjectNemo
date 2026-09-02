"""APScheduler jobs — daily summary, overdue checks, feeding pause auto-resume."""
import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, and_, desc, func
from sqlalchemy.orm import selectinload

from config import settings
from database import AsyncSessionLocal
from models.orm import (
    DosingTask, FeedingPause, FeedingSchedule, MaintenanceTask, Supply,
    WaterTestReading, WaterTestSession, WaterTestSnooze,
)
from services.ha_client import ha_client
from services.n8n_client import n8n_client
from services.ntfy_client import ntfy_client
from services.influx_client import influx_client

logger = logging.getLogger("nemo.scheduler")

scheduler = AsyncIOScheduler(timezone="Europe/Dublin")
DUBLIN_TZ = ZoneInfo("Europe/Dublin")


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

        supply_result = await db.execute(select(Supply))
        for supply in supply_result.scalars().all():
            if supply.current_amount <= supply.min_threshold:
                await n8n_client.supply_low(supply)


TANK_NAMES = {1: settings.tank_1_name, 2: settings.tank_2_name}


@scheduler.scheduled_job("cron", hour="*/6")
async def water_test_snooze_escalation():
    """A due water-test reminder gets snoozed in the UI first (no Telegram
    yet); only once it's been snoozed for 2+ days without a new reading do
    we escalate to Telegram - once per snooze, with last-tested date and
    what a high reading of that parameter can do to the tank."""
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(WaterTestSnooze).options(selectinload(WaterTestSnooze.parameter))
        )
        for snooze in result.scalars().all():
            if snooze.notified_at is not None:
                continue
            snoozed_at = snooze.snoozed_at.replace(tzinfo=timezone.utc) if snooze.snoozed_at.tzinfo is None else snooze.snoozed_at
            if (now - snoozed_at) < timedelta(days=2):
                continue

            param = snooze.parameter
            tank_name = TANK_NAMES.get(snooze.tank_id, f"Tank {snooze.tank_id}")

            last_result = await db.execute(
                select(WaterTestReading, WaterTestSession.tested_at)
                .join(WaterTestSession, WaterTestReading.session_id == WaterTestSession.id)
                .where(WaterTestSession.tank_id == snooze.tank_id, WaterTestReading.parameter_id == param.id)
                .order_by(desc(func.coalesce(WaterTestReading.updated_at, WaterTestSession.tested_at)))
                .limit(1)
            )
            row = last_result.first()
            if row:
                reading, session_tested_at = row
                last_at = reading.updated_at or session_tested_at
                last_str_en = last_at.strftime("%d %b %Y")
                last_str_pl = last_at.strftime("%d.%m.%Y")
            else:
                last_str_en = "never"
                last_str_pl = "nigdy"

            effect_en = f" {param.high_effect_en}" if param.high_effect_en else ""
            effect_pl = f" {param.high_effect_pl}" if param.high_effect_pl else ""
            await n8n_client.reminder(
                f"🧪 {tank_name}: {param.name_en} test still overdue (last tested: {last_str_en}).{effect_en}",
                f"🧪 {tank_name}: test {param.name_pl} wciąż zaległy (ostatni test: {last_str_pl}).{effect_pl}",
            )
            snooze.notified_at = now
        await db.commit()


@scheduler.scheduled_job("cron", minute="*")
async def feeding_reminder():
    """Fire a 5-min-early Telegram warning for any tank whose FeedingSchedule
    entry is coming up - press Feed Now for that tank when it fires."""
    target_hm = (datetime.now(DUBLIN_TZ) + timedelta(minutes=5)).strftime("%H:%M")
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(FeedingSchedule).where(
                FeedingSchedule.active == True, FeedingSchedule.time_of_day == target_hm  # noqa: E712
            )
        )
        for feeding in result.scalars().all():
            tank_name = TANK_NAMES.get(feeding.tank_id, f"Tank {feeding.tank_id}")
            await n8n_client.reminder(
                f"Feeding in 5 min ({tank_name}) — press Feed Now at {feeding.time_of_day}",
                f"Karmienie za 5 min ({tank_name}) — wciśnij Karm Teraz o {feeding.time_of_day}",
            )
            await ntfy_client.send(
                "Feeding time",
                f"{tank_name}: press Feed Now. See today's rotation.",
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


@scheduler.scheduled_job("cron", minute="*")
async def dosing_reminder():
    """Fire a Telegram reminder for any active dosing task scheduled for this exact minute."""
    now_hm = datetime.now(DUBLIN_TZ).strftime("%H:%M")
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(DosingTask)
            .options(selectinload(DosingTask.supply))
            .where(DosingTask.active == True, DosingTask.time_of_day == now_hm)  # noqa: E712
        )
        for task in result.scalars().all():
            supply = task.supply
            note = f" ({task.notes})" if task.notes else ""
            note_pl = f" ({task.notes_pl})" if task.notes_pl else ""
            await n8n_client.reminder(
                f"💧 Dose {task.dose_amount}{task.dose_unit} {supply.name}{note}",
                f"💧 Dawka {task.dose_amount}{task.dose_unit} {supply.name_pl or supply.name}{note_pl}",
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
