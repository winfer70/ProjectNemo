"""Pydantic schemas for API request/response validation."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# ── Supplies ──────────────────────────────────────────────────────────────────

class SupplyBase(BaseModel):
    name: str
    name_pl: str
    type: str
    current_amount: float
    unit: str
    min_threshold: float = 0
    purchase_link: str | None = None
    notes: str | None = None


class SupplyCreate(SupplyBase):
    pass


class SupplyUpdate(BaseModel):
    current_amount: float | None = None
    min_threshold: float | None = None
    purchase_link: str | None = None
    notes: str | None = None


class SupplyOut(SupplyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    low: bool = False


# ── Dosing ────────────────────────────────────────────────────────────────────

class DosingTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    supply_id: int
    supply_name: str
    supply_name_pl: str
    dose_amount: float
    dose_unit: str
    time_of_day: str | None
    active: bool
    notes: str | None
    notes_pl: str | None
    current_supply: float
    supply_unit: str
    supply_low: bool


class DoseCompleteRequest(BaseModel):
    notes: str | None = None


class RestockRequest(BaseModel):
    new_amount: float


class DosingTaskCreate(BaseModel):
    supply_id: int
    dose_amount: float
    dose_unit: str = "ml"
    time_of_day: str | None = None
    notes: str | None = None
    notes_pl: str | None = None


class DosingTaskUpdate(BaseModel):
    dose_amount: float | None = None
    dose_unit: str | None = None
    time_of_day: str | None = None
    active: bool | None = None
    notes: str | None = None
    notes_pl: str | None = None


# ── Maintenance ───────────────────────────────────────────────────────────────

class MaintenanceTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    name_pl: str
    interval_days: int
    last_completed: datetime | None
    next_due: datetime | None
    days_until: int | None
    steps: list[dict[str, Any]]
    required_parts: list[dict[str, Any]]
    started_at: datetime | None = None
    affects_entity: str | None = None


class MaintenanceCompleteRequest(BaseModel):
    parts_replaced: list[dict[str, Any]] = []
    notes: str | None = None


class MaintenanceStartRequest(BaseModel):
    affects_entity: str | None = None


# ── Feeding ───────────────────────────────────────────────────────────────────

class FeedingScheduleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    time_of_day: str
    active: bool
    notes: str | None


class FeedingScheduleCreate(BaseModel):
    time_of_day: str
    active: bool = True
    notes: str | None = None


class FeedingLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    scheduled_id: int | None
    timestamp: datetime
    manual: bool
    notes: str | None


class FeedingStatusOut(BaseModel):
    paused: bool
    resume_in_secs: int | None = None
    paused_entities: list[str] = []


# ── Water Tests ───────────────────────────────────────────────────────────────

class WaterTestParameterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    key: str
    name_en: str
    name_pl: str
    unit: str
    min_safe: float | None
    max_safe: float | None
    category: str


class WaterTestReadingIn(BaseModel):
    parameter_id: int
    value: float
    notes: str | None = None


class WaterTestSessionCreate(BaseModel):
    tested_at: datetime | None = None
    notes: str | None = None
    readings: list[WaterTestReadingIn]
    scan_cache_id: int | None = None


class WaterTestReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    parameter_id: int
    parameter_key: str
    parameter_name_en: str
    parameter_name_pl: str
    unit: str
    value: float
    out_of_range: bool
    notes: str | None


class WaterTestSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tested_at: datetime
    notes: str | None
    readings: list[WaterTestReadingOut]


# ── Sensors ───────────────────────────────────────────────────────────────────

class SensorCurrentOut(BaseModel):
    temperature: float | None
    ph: float | None
    tds: float | None
    orp: float | None
    updated_at: datetime


class SensorHistoryPoint(BaseModel):
    time: datetime
    value: float


class DeviceOut(BaseModel):
    entity_id: str
    name: str
    name_pl: str
    state: str
    watts: float | None
    kwh_today: float | None
    role: str


class FluvalChannels(BaseModel):
    r: int
    g: int
    b: int
    w: int
    ch5: int = 0


# ── Obsada (Livestock) ────────────────────────────────────────────────────────

class FishCreate(BaseModel):
    name_en: str
    name_pl: str | None = None
    latin: str | None = None
    qty: int = 1
    zone: str | None = None
    status: str = "planned"
    temp: str | None = None
    notes_pl: str | None = None
    img: str | None = None


class FishUpdate(BaseModel):
    name_en: str | None = None
    name_pl: str | None = None
    latin: str | None = None
    qty: int | None = None
    zone: str | None = None
    status: str | None = None
    temp: str | None = None
    notes_pl: str | None = None
    img: str | None = None


class FishOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name_en: str
    name_pl: str | None
    latin: str | None
    qty: int
    zone: str | None
    status: str
    temp: str | None
    notes_pl: str | None
    img: str | None
    added_at: datetime


class PlantCreate(BaseModel):
    name_en: str
    name_pl: str | None = None
    latin: str | None = None
    location: str | None = None
    notes_pl: str | None = None
    img: str | None = None


class PlantUpdate(BaseModel):
    name_en: str | None = None
    name_pl: str | None = None
    latin: str | None = None
    location: str | None = None
    notes_pl: str | None = None
    img: str | None = None


class PlantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name_en: str
    name_pl: str | None
    latin: str | None
    location: str | None
    notes_pl: str | None
    img: str | None
    added_at: datetime


class ImageResult(BaseModel):
    url: str
    source: str
    thumb: str | None = None


class ImageSearchResult(BaseModel):
    query: str
    scientific_name: str | None = None
    common_name: str | None = None
    wiki_extract: str | None = None
    wiki_url: str | None = None
    images: list[ImageResult] = []


# ── Calendar ──────────────────────────────────────────────────────────────────

class CalendarTaskCreate(BaseModel):
    name: str
    name_pl: str
    color: str = "#00b4d8"
    recurrence_type: str = "once"
    interval_days: int | None = None
    recurrence_days: list[int] = []
    start_date: str
    end_date: str | None = None
    amount: str | None = None
    notes_pl: str | None = None


class CalendarTaskUpdate(BaseModel):
    name: str | None = None
    name_pl: str | None = None
    color: str | None = None
    recurrence_type: str | None = None
    interval_days: int | None = None
    recurrence_days: list[int] | None = None
    start_date: str | None = None
    end_date: str | None = None
    amount: str | None = None
    notes_pl: str | None = None
    active: bool | None = None
