"""Calendar router — recurring aquarium care tasks with per-day completion tracking."""
import calendar as cal_lib
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import CalendarTask, CalendarCompletion
from models.schemas import CalendarTaskCreate, CalendarTaskUpdate
from services.websocket_manager import broadcast_change

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


def _task_applies(task: CalendarTask, d: date) -> bool:
    """Return True if this task is scheduled on the given date."""
    start = date.fromisoformat(task.start_date)
    if d < start:
        return False
    if task.end_date:
        end = date.fromisoformat(task.end_date)
        if d > end:
            return False
    if task.recurrence_type == "daily":
        return True
    if task.recurrence_type == "once":
        return d == start
    if task.recurrence_type == "every_n_days":
        delta = (d - start).days
        return (delta % (task.interval_days or 1)) == 0
    if task.recurrence_type == "weekdays":
        return d.weekday() in task.recurrence_days
    return False


# ── Task CRUD ──────────────────────────────────────────────────────────────────

@router.get("/tasks")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """List all active calendar tasks."""
    result = await db.execute(select(CalendarTask).where(CalendarTask.active == True))  # noqa: E712
    tasks = result.scalars().all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "name_pl": t.name_pl,
            "color": t.color,
            "recurrence_type": t.recurrence_type,
            "interval_days": t.interval_days,
            "recurrence_days": t.recurrence_days,
            "start_date": t.start_date,
            "end_date": t.end_date,
            "amount": t.amount,
            "notes_pl": t.notes_pl,
        }
        for t in tasks
    ]


@router.post("/tasks", status_code=201)
async def create_task(data: CalendarTaskCreate, db: AsyncSession = Depends(get_db)):
    task = CalendarTask(
        name=data.name,
        name_pl=data.name_pl,
        color=data.color,
        recurrence_type=data.recurrence_type,
        interval_days=data.interval_days,
        start_date=data.start_date,
        end_date=data.end_date,
        amount=data.amount,
        notes_pl=data.notes_pl,
        active=True,
    )
    task.recurrence_days = data.recurrence_days
    db.add(task)
    await db.commit()
    await db.refresh(task)
    await broadcast_change("calendar")
    return {"id": task.id, "ok": True}


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    data: CalendarTaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    task = await db.get(CalendarTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "recurrence_days":
            task.recurrence_days = value
        else:
            setattr(task, field, value)
    await db.commit()
    await broadcast_change("calendar")
    return {"ok": True}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await db.get(CalendarTask, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task.active = False
    await db.commit()
    await broadcast_change("calendar")
    return {"ok": True}


# ── Today view ─────────────────────────────────────────────────────────────────

@router.get("/today")
async def get_today(db: AsyncSession = Depends(get_db)):
    """Return tasks due today + overdue tasks from last 7 days."""
    today = date.today()
    today_str = today.isoformat()

    result = await db.execute(select(CalendarTask).where(CalendarTask.active == True))  # noqa: E712
    tasks = result.scalars().all()

    comp_result = await db.execute(
        select(CalendarCompletion).where(CalendarCompletion.date == today_str)
    )
    today_completions = {c.task_id for c in comp_result.scalars().all()}

    due = []
    seen_task_ids = set()

    for t in tasks:
        if _task_applies(t, today):
            due.append({
                "id": t.id,
                "name": t.name,
                "name_pl": t.name_pl,
                "color": t.color,
                "amount": t.amount,
                "notes_pl": t.notes_pl,
                "completed": t.id in today_completions,
                "date": today_str,
                "overdue_days": 0,
            })
            seen_task_ids.add(t.id)

    for days_ago in range(1, 8):
        past_date = today - timedelta(days=days_ago)
        past_str = past_date.isoformat()
        for t in tasks:
            if t.id in seen_task_ids:
                continue
            if not _task_applies(t, past_date):
                continue
            comp_check = await db.execute(
                select(CalendarCompletion).where(
                    and_(
                        CalendarCompletion.task_id == t.id,
                        CalendarCompletion.date == past_str,
                    )
                )
            )
            if not comp_check.scalar_one_or_none():
                due.append({
                    "id": t.id,
                    "name": t.name,
                    "name_pl": t.name_pl,
                    "color": t.color,
                    "amount": t.amount,
                    "notes_pl": t.notes_pl,
                    "completed": False,
                    "date": past_str,
                    "overdue_days": days_ago,
                })
                seen_task_ids.add(t.id)

    return {"date": today_str, "tasks": due}


# ── Month view ─────────────────────────────────────────────────────────────────

@router.get("/month/{year}/{month}")
async def get_month(year: int, month: int, db: AsyncSession = Depends(get_db)):
    if not (1 <= month <= 12):
        raise HTTPException(400, "Invalid month")

    result = await db.execute(select(CalendarTask).where(CalendarTask.active == True))  # noqa: E712
    tasks = result.scalars().all()

    prefix = f"{year:04d}-{month:02d}"
    comp_result = await db.execute(
        select(CalendarCompletion).where(CalendarCompletion.date.like(f"{prefix}%"))
    )
    completions = comp_result.scalars().all()
    comp_set: dict[tuple, datetime] = {(c.task_id, c.date): c.completed_at for c in completions}

    _, days_in_month = cal_lib.monthrange(year, month)
    days = []
    for day_num in range(1, days_in_month + 1):
        d = date(year, month, day_num)
        date_str = d.isoformat()
        day_tasks = []
        for t in tasks:
            if _task_applies(t, d):
                comp_key = (t.id, date_str)
                comp_at = comp_set.get(comp_key)
                day_tasks.append({
                    "id": t.id,
                    "name": t.name,
                    "name_pl": t.name_pl,
                    "color": t.color,
                    "amount": t.amount,
                    "notes_pl": t.notes_pl,
                    "completed": comp_key in comp_set,
                    "completed_at": comp_at.isoformat() if comp_at else None,
                })
        days.append({"date": date_str, "day": day_num, "tasks": day_tasks})

    return {"year": year, "month": month, "days": days}


class CompleteRequest(BaseModel):
    task_id: int
    date: str


@router.post("/complete")
async def toggle_complete(req: CompleteRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(CalendarCompletion).where(
            and_(
                CalendarCompletion.task_id == req.task_id,
                CalendarCompletion.date == req.date,
            )
        )
    )
    comp = existing.scalar_one_or_none()
    if comp:
        await db.delete(comp)
        await db.commit()
        await broadcast_change("calendar")
        return {"completed": False}
    else:
        db.add(CalendarCompletion(task_id=req.task_id, date=req.date))
        try:
            await db.commit()
        except IntegrityError:
            # A concurrent request (double-click, retry, etc.) already inserted
            # the same (task_id, date) row — the unique index rejected ours.
            # That's fine: the task is completed either way.
            await db.rollback()
        await broadcast_change("calendar")
        return {"completed": True}
