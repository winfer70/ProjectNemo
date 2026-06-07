"""Obsada (livestock) CRUD + species image search."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Fish, Plant
from models.schemas import (
    FishCreate, FishOut, FishUpdate,
    PlantCreate, PlantOut, PlantUpdate,
    ImageSearchResult,
)
from services.image_search import search_species

router = APIRouter(prefix="/api/obsada", tags=["obsada"])


# ── Fish ──────────────────────────────────────────────────────────────────────

@router.get("/fish", response_model=list[FishOut])
async def list_fish(db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Fish).order_by(Fish.added_at))
    return rows.all()


@router.post("/fish", response_model=FishOut, status_code=201)
async def create_fish(body: FishCreate, db: AsyncSession = Depends(get_db)):
    fish = Fish(**body.model_dump())
    db.add(fish)
    await db.commit()
    await db.refresh(fish)
    return fish


@router.put("/fish/{fish_id}", response_model=FishOut)
async def update_fish(fish_id: int, body: FishUpdate, db: AsyncSession = Depends(get_db)):
    fish = await db.get(Fish, fish_id)
    if not fish:
        raise HTTPException(404, "Fish not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(fish, k, v)
    await db.commit()
    await db.refresh(fish)
    return fish


@router.delete("/fish/{fish_id}", status_code=204)
async def delete_fish(fish_id: int, db: AsyncSession = Depends(get_db)):
    fish = await db.get(Fish, fish_id)
    if not fish:
        raise HTTPException(404, "Fish not found")
    await db.delete(fish)
    await db.commit()


# ── Plants ────────────────────────────────────────────────────────────────────

@router.get("/plants", response_model=list[PlantOut])
async def list_plants(db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Plant).order_by(Plant.added_at))
    return rows.all()


@router.post("/plants", response_model=PlantOut, status_code=201)
async def create_plant(body: PlantCreate, db: AsyncSession = Depends(get_db)):
    plant = Plant(**body.model_dump())
    db.add(plant)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.put("/plants/{plant_id}", response_model=PlantOut)
async def update_plant(plant_id: int, body: PlantUpdate, db: AsyncSession = Depends(get_db)):
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(404, "Plant not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(plant, k, v)
    await db.commit()
    await db.refresh(plant)
    return plant


@router.delete("/plants/{plant_id}", status_code=204)
async def delete_plant(plant_id: int, db: AsyncSession = Depends(get_db)):
    plant = await db.get(Plant, plant_id)
    if not plant:
        raise HTTPException(404, "Plant not found")
    await db.delete(plant)
    await db.commit()


# ── Image search ──────────────────────────────────────────────────────────────

@router.get("/search", response_model=ImageSearchResult)
async def species_search(q: str, type: str = "fish"):
    return await search_species(q, type)
