"""Calendar router — recurring aquarium care tasks with per-day completion tracking."""
import calendar as cal_lib
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import CalendarTask, CalendarCompletion

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


# ── helpers ───────────────────────────────────────────────────────────────────

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
    if task.recurrence_type == "every_n_days":
        delta = (d - start).days
        return (delta % (task.interval_days or 1)) == 0
    if task.recurrence_type == "weekdays":
        return d.weekday() in task.recurrence_days
    return False


# ── endpoints ─────────────────────────────────────────────────────────────────

@router.get("/tasks")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    """List all active calendar tasks."""
    result = await db.execute(select(CalendarTask).where(CalendarTask.active == True))
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
        }
        for t in tasks
    ]


@router.get("/month/{year}/{month}")
async def get_month(year: int, month: int, db: AsyncSession = Depends(get_db)):
    """Return all days in the given month with scheduled tasks and completion status."""
    if not (1 <= month <= 12):
        raise HTTPException(400, "Invalid month")

    result = await db.execute(select(CalendarTask).where(CalendarTask.active == True))
    tasks = result.scalars().all()

    # Fetch all completions for this month in one query
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
                    "completed": comp_key in comp_set,
                    "completed_at": comp_at.isoformat() if comp_at else None,
                })
        days.append({"date": date_str, "day": day_num, "tasks": day_tasks})

    return {"year": year, "month": month, "days": days}


class CompleteRequest(BaseModel):
    task_id: int
    date: str   # YYYY-MM-DD


@router.post("/complete")
async def toggle_complete(req: CompleteRequest, db: AsyncSession = Depends(get_db)):
    """Toggle completion of a task on a given date. Returns new completed state."""
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
        return {"completed": False}
    else:
        db.add(CalendarCompletion(task_id=req.task_id, date=req.date))
        await db.commit()
        return {"completed": True}
