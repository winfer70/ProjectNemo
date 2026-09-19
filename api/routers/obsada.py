"""Obsada (livestock) CRUD + species image search."""
import os
import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
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

# ── Local image hosting (upload / fetch-from-url) ───────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
OBSADA_IMAGES_DIR = os.path.join(STATIC_DIR, "obsada_images")
os.makedirs(OBSADA_IMAGES_DIR, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp",
}
MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10MB cap for fetched/uploaded images


def _ext_from_content_type(content_type: str | None) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",
    }
    return mapping.get((content_type or "").split(";")[0].strip().lower(), "")


class FetchImageBody(BaseModel):
    url: str


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


# ── Local image hosting ─────────────────────────────────────────────────────

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Save a user-uploaded image locally and return its served URL."""
    content_type = (file.content_type or "").split(";")[0].strip().lower()
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower()

    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES and ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(400, "File does not look like an image")

    if not ext:
        ext = _ext_from_content_type(content_type) or ".jpg"

    body = await file.read()
    if not body:
        raise HTTPException(400, "Empty file")
    if len(body) > MAX_IMAGE_BYTES:
        raise HTTPException(400, "Image too large (max 10MB)")

    filename = f"{uuid.uuid4()}{ext}"
    dest = os.path.join(OBSADA_IMAGES_DIR, filename)
    with open(dest, "wb") as f:
        f.write(body)

    return {"url": f"/static/obsada_images/{filename}"}


@router.post("/fetch-image")
async def fetch_image(body: FetchImageBody):
    """Download an externally-hosted image server-side and re-host it locally,
    so we end up serving our own copy instead of hot-linking a third-party
    URL (which can disappear or block hotlinking at any time)."""
    url = (body.url or "").strip()
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(400, "Invalid URL")

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "ProjectNemo/1.0"})
    except Exception:
        raise HTTPException(400, "Could not fetch image from URL")

    if resp.status_code != 200:
        raise HTTPException(400, f"Could not fetch image (status {resp.status_code})")

    content_type = (resp.headers.get("content-type") or "").split(";")[0].strip().lower()
    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise HTTPException(400, "URL does not point to a supported image type")

    content = resp.content
    if not content:
        raise HTTPException(400, "Empty image response")
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(400, "Image too large (max 10MB)")

    ext = os.path.splitext(url.split("?")[0])[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        ext = _ext_from_content_type(content_type) or ".jpg"

    filename = f"{uuid.uuid4()}{ext}"
    dest = os.path.join(OBSADA_IMAGES_DIR, filename)
    with open(dest, "wb") as f:
        f.write(content)

    return {"url": f"/static/obsada_images/{filename}"}
