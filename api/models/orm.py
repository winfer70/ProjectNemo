"""SQLAlchemy ORM model definitions — imported by all routers and seed_data.py."""
import json
from datetime import datetime

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    name_pl: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(20))
    current_amount: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10))
    min_threshold: Mapped[float] = mapped_column(Float, default=0)
    purchase_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    dosing_tasks: Mapped[list["DosingTask"]] = relationship(back_populates="supply")
    dose_logs: Mapped[list["DoseLog"]] = relationship(back_populates="supply")


class DosingTask(Base):
    __tablename__ = "dosing_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"))
    dose_amount: Mapped[float] = mapped_column(Float)
    dose_unit: Mapped[str] = mapped_column(String(10))
    time_of_day: Mapped[str | None] = mapped_column(String(5), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes_pl: Mapped[str | None] = mapped_column(Text, nullable=True)

    supply: Mapped["Supply"] = relationship(back_populates="dosing_tasks")


class DoseLog(Base):
    __tablename__ = "dose_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"))
    amount: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    supply: Mapped["Supply"] = relationship(back_populates="dose_logs")


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    name_pl: Mapped[str] = mapped_column(String(100))
    interval_days: Mapped[int] = mapped_column(Integer)
    last_completed: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_due: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    affects_entity: Mapped[str | None] = mapped_column(String(100), nullable=True)
    _steps: Mapped[str] = mapped_column("steps", Text, default="[]")
    _required_parts: Mapped[str] = mapped_column("required_parts", Text, default="[]")

    logs: Mapped[list["MaintenanceLog"]] = relationship(back_populates="task")

    @property
    def steps(self) -> list:
        return json.loads(self._steps)

    @steps.setter
    def steps(self, value: list):
        self._steps = json.dumps(value, ensure_ascii=False)

    @property
    def required_parts(self) -> list:
        return json.loads(self._required_parts)

    @required_parts.setter
    def required_parts(self, value: list):
        self._required_parts = json.dumps(value)


class MaintenanceLog(Base):
    __tablename__ = "maintenance_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("maintenance_tasks.id"))
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    _parts_replaced: Mapped[str] = mapped_column("parts_replaced", Text, default="[]")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    task: Mapped["MaintenanceTask"] = relationship(back_populates="logs")

    @property
    def parts_replaced(self) -> list:
        return json.loads(self._parts_replaced)

    @parts_replaced.setter
    def parts_replaced(self, value: list):
        self._parts_replaced = json.dumps(value)


class FeedingSchedule(Base):
    __tablename__ = "feeding_schedule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time_of_day: Mapped[str] = mapped_column(String(5))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    logs: Mapped[list["FeedingLog"]] = relationship(back_populates="schedule")


class FeedingLog(Base):
    __tablename__ = "feeding_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scheduled_id: Mapped[int | None] = mapped_column(ForeignKey("feeding_schedule.id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    manual: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    schedule: Mapped["FeedingSchedule | None"] = relationship(back_populates="logs")


class FeedingPause(Base):
    """Tracks active device pauses for feeding mode."""
    __tablename__ = "feeding_pauses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resume_at: Mapped[datetime] = mapped_column(DateTime)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resumed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    _paused_entities: Mapped[str] = mapped_column("paused_entities", Text, default="[]")

    @property
    def paused_entities(self) -> list:
        return json.loads(self._paused_entities)

    @paused_entities.setter
    def paused_entities(self, value: list):
        self._paused_entities = json.dumps(value)


class WaterTestParameter(Base):
    __tablename__ = "water_test_parameters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(20), unique=True)
    name_en: Mapped[str] = mapped_column(String(80))
    name_pl: Mapped[str] = mapped_column(String(80))
    unit: Mapped[str] = mapped_column(String(20))
    min_safe: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_safe: Mapped[float | None] = mapped_column(Float, nullable=True)
    category: Mapped[str] = mapped_column(String(20))

    readings: Mapped[list["WaterTestReading"]] = relationship(back_populates="parameter")


class WaterTestSession(Base):
    __tablename__ = "water_test_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tested_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    readings: Mapped[list["WaterTestReading"]] = relationship(back_populates="session")


class WaterTestReading(Base):
    __tablename__ = "water_test_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("water_test_sessions.id"))
    parameter_id: Mapped[int] = mapped_column(ForeignKey("water_test_parameters.id"))
    value: Mapped[float] = mapped_column(Float)
    out_of_range: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    session: Mapped["WaterTestSession"] = relationship(back_populates="readings")
    parameter: Mapped["WaterTestParameter"] = relationship(back_populates="readings")


class CalendarTask(Base):
    """A recurring aquarium care task shown in the calendar."""
    __tablename__ = "calendar_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    name_pl: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(20))
    recurrence_type: Mapped[str] = mapped_column(String(20))
    interval_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    _recurrence_days: Mapped[str | None] = mapped_column("recurrence_days", Text, nullable=True)
    start_date: Mapped[str] = mapped_column(String(10))
    end_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    amount: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes_pl: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    completions: Mapped[list["CalendarCompletion"]] = relationship(back_populates="task")

    @property
    def recurrence_days(self) -> list:
        return json.loads(self._recurrence_days) if self._recurrence_days else []

    @recurrence_days.setter
    def recurrence_days(self, value: list):
        self._recurrence_days = json.dumps(value) if value is not None else None


class CalendarCompletion(Base):
    """Records that a CalendarTask was completed on a specific date."""
    __tablename__ = "calendar_completions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("calendar_tasks.id"))
    date: Mapped[str] = mapped_column(String(10))
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    task: Mapped["CalendarTask"] = relationship(back_populates="completions")


class Fish(Base):
    __tablename__ = "fish"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_en: Mapped[str] = mapped_column(String(100))
    name_pl: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latin: Mapped[str | None] = mapped_column(String(150), nullable=True)
    qty: Mapped[int] = mapped_column(Integer, default=1)
    zone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="planned")
    temp: Mapped[str | None] = mapped_column(String(30), nullable=True)
    notes_pl: Mapped[str | None] = mapped_column(Text, nullable=True)
    img: Mapped[str | None] = mapped_column(Text, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_en: Mapped[str] = mapped_column(String(100))
    name_pl: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latin: Mapped[str | None] = mapped_column(String(150), nullable=True)
    location: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes_pl: Mapped[str | None] = mapped_column(Text, nullable=True)
    img: Mapped[str | None] = mapped_column(Text, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class StripScanCache(Base):
    __tablename__ = "strip_scan_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_sha256: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    image_phash: Mapped[str] = mapped_column(String(16))
    _ai_result: Mapped[str] = mapped_column("ai_result", Text)
    _corrected_result: Mapped[str | None] = mapped_column("corrected_result", Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def ai_result(self) -> dict:
        return json.loads(self._ai_result)

    @ai_result.setter
    def ai_result(self, value: dict):
        self._ai_result = json.dumps(value)

    @property
    def corrected_result(self) -> dict | None:
        return json.loads(self._corrected_result) if self._corrected_result else None

    @corrected_result.setter
    def corrected_result(self, value: dict | None):
        self._corrected_result = json.dumps(value) if value is not None else None
