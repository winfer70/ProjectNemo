"""Test strip analysis via moondream on REDACTED-HOST Ollama."""
import base64
import io
import json
import logging
import re

import httpx
from PIL import Image

from config import settings

logger = logging.getLogger(__name__)

MAX_PX = 1024

STRIP_PROMPT = (
    "This image shows an aquarium water test strip on the left and a color reference chart on the right. "
    "Compare each strip pad color to the corresponding row in the chart and pick the closest matching number. "
    "The 9 pads from top to bottom are: copper, nitrate, nitrite, free_chlorine, gh, total_alkalinity, kh, ph, ammonia. "
    "Most pads will be white or near-zero — only pick a non-zero value if the color clearly matches. "
    "Reply with ONLY a JSON object using these exact keys. "
    "Valid values for each key: "
    "copper: 0, 0.2, 0.5, 1, 2, 5 | "
    "nitrate: 0, 10, 25, 50, 100, 250 | "
    "nitrite: 0, 1, 5, 10 | "
    "free_chlorine: 0, 0.5, 1, 3, 5, 10, 20 | "
    "gh: 0, 25, 50, 125, 250, 425 | "
    "total_alkalinity: 0, 40, 80, 120, 180, 240 | "
    "kh: 0, 40, 80, 120, 180, 300 | "
    "ph: 6.2, 6.8, 7.2, 7.6, 7.8, 8.4 | "
    "ammonia: 0, 0.5, 1, 3, 5, 10"
)


def _resize(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    img.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


async def analyze_strip(image_bytes: bytes) -> dict[str, float | None]:
    resized = _resize(image_bytes)
    b64 = base64.b64encode(resized).decode()
    payload = {
        "model": "moondream",
        "prompt": STRIP_PROMPT,
        "images": [b64],
        "stream": False,
        "options": {"temperature": 0},
    }
    async with httpx.AsyncClient(timeout=240) as client:
        r = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
        r.raise_for_status()
        raw = r.json()["response"]

    logger.info("moondream raw response: %s", raw[:500])

    match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in moondream response: {raw[:300]}")
    data = json.loads(match.group())
    return {k: (float(v) if v is not None else None) for k, v in data.items()}
