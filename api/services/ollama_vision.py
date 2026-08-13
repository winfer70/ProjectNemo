"""Test strip analysis via a configured Ollama endpoint."""
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

_SYSTEM = (
    "You are a precise aquarium water test strip reader. "
    "Your job is to compare pad colors on a test strip to a reference color chart. "
    "CRITICAL: The '0' column in the reference chart is WHITE or very pale cream. "
    "If a pad is white, off-white, or the same pale color as the 0-column → value is 0. "
    "Only assign non-zero if the pad has an OBVIOUS, CLEARLY VISIBLE color that is distinctly different from white. "
    "When uncertain, choose 0. You must respond with only a JSON object."
)

_USER = (
    "Analyze this test strip image. Compare each pad to the reference chart.\n\n"
    "ORIENTATION: The test strip has a blank white plastic HANDLE at the BOTTOM. "
    "Count pads starting from the TOP of the strip (furthest from the handle).\n\n"
    "The 9 pads from TOP to BOTTOM (top = away from handle, bottom = near handle):\n"
    "1. copper  (TOP pad, furthest from handle)\n"
    "2. nitrate\n3. nitrite\n4. free_chlorine\n"
    "5. gh\n6. total_alkalinity\n7. kh\n8. ph\n"
    "9. ammonia (BOTTOM pad, closest to handle)\n\n"
    "WHITE or pale pad = 0. Only non-zero if CLEARLY colored differently from white.\n\n"
    "Valid values:\n"
    "copper: 0, 0.2, 0.5, 1, 2, 5\n"
    "nitrate: 0, 10, 25, 50, 100, 250\n"
    "nitrite: 0, 1, 5, 10\n"
    "free_chlorine: 0, 0.5, 1, 3, 5, 10, 20\n"
    "gh: 0, 25, 50, 125, 250, 425\n"
    "total_alkalinity: 0, 40, 80, 120, 180, 240\n"
    "kh: 0, 40, 80, 120, 180, 300\n"
    "ph: 6.2, 6.8, 7.2, 7.6, 7.8, 8.4\n"
    "ammonia: 0, 0.5, 1, 3, 5, 10\n\n"
    "Respond with ONLY this JSON (no explanation, no markdown):\n"
    '{"copper": 0, "nitrate": 0, "nitrite": 0, "free_chlorine": 0, "gh": 125, "total_alkalinity": 80, "kh": 40, "ph": 7.2, "ammonia": 0}'
)


def _resize(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    img.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


async def analyze_strip(image_bytes: bytes) -> dict[str, float | None]:
    if not settings.ollama_url:
        raise ValueError("OLLAMA_URL is not configured")

    resized = _resize(image_bytes)
    b64 = base64.b64encode(resized).decode()

    payload = {
        "model": "llava-phi3",
        "stream": False,
        "options": {"temperature": 0},
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": _USER, "images": [b64]},
        ],
    }

    async with httpx.AsyncClient(timeout=240) as client:
        r = await client.post(f"{settings.ollama_url}/api/chat", json=payload)
        r.raise_for_status()
        raw = r.json()["message"]["content"]

    logger.info("llava-phi3 raw response: %s", raw[:500])

    match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in llava-phi3 response: {raw[:300]}")
    data = json.loads(match.group())
    return {k: (float(v) if v is not None else None) for k, v in data.items()}
