"""SHA256 + perceptual hash cache for strip scan results."""
import hashlib
import io

import imagehash
from PIL import Image
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import StripScanCache

PHASH_THRESHOLD = 10


def _compute_hashes(image_bytes: bytes) -> tuple[str, str]:
    sha256 = hashlib.sha256(image_bytes).hexdigest()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    phash = str(imagehash.phash(img))
    return sha256, phash


async def lookup(db: AsyncSession, image_bytes: bytes) -> tuple[StripScanCache | None, str, str]:
    sha256, phash = _compute_hashes(image_bytes)

    result = await db.execute(
        select(StripScanCache).where(StripScanCache.image_sha256 == sha256)
    )
    row = result.scalar_one_or_none()
    if row:
        return row, sha256, phash

    result = await db.execute(select(StripScanCache))
    rows = result.scalars().all()
    img_phash = imagehash.hex_to_hash(phash)
    for row in rows:
        if img_phash - imagehash.hex_to_hash(row.image_phash) <= PHASH_THRESHOLD:
            return row, sha256, phash

    return None, sha256, phash


async def store(db: AsyncSession, sha256: str, phash: str, ai_result: dict) -> StripScanCache:
    row = StripScanCache(image_sha256=sha256, image_phash=phash)
    row.ai_result = ai_result
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def save_correction(db: AsyncSession, cache_id: int, corrected: dict) -> None:
    result = await db.execute(
        select(StripScanCache).where(StripScanCache.id == cache_id)
    )
    row = result.scalar_one_or_none()
    if row:
        row.corrected_result = corrected
        await db.commit()
