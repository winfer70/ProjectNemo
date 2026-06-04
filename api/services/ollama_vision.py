"""Test strip analysis via LLaVA on REDACTED-HOST Ollama."""
import base64
import io
import json
import re

import httpx
from PIL import Image

from config import settings

MAX_PX = 1024  # LLaVA doesn't benefit from higher res; keeps payload small

STRIP_PROMPT = """This photo shows an aquarium water test strip next to its reference color chart.

Match each pad's color to the closest value on the reference chart. Return ONLY a valid JSON object with these exact keys and numeric values (no units, no extra text, use null if a pad is unreadable):

{
  "copper": <mg/L — nearest: 0, 0.05, 0.2, 0.5, 1.0>,
  "nitrate": <mg/L — nearest: 0, 20, 40, 80, 160, 200>,
  "nitrite": <mg/L — nearest: 0, 0.5, 1, 3, 5, 10>,
  "free_chlorine": <mg/L — nearest: 0, 0.5, 1, 2, 4>,
  "gh": <ppm — nearest: 0, 25, 50, 125, 250, 500>,
  "total_alkalinity": <ppm — nearest: 0, 40, 80, 120, 180, 240>,
  "kh": <ppm — nearest: 0, 40, 80, 120, 180, 240>,
  "ph": <nearest: 6.2, 6.8, 7.2, 7.6, 8.0, 8.4>,
  "ammonia": <mg/L — nearest: 0, 0.25, 0.5, 1.0, 3.0, 6.0>
}"""


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
        "model": "llava:13b",
        "prompt": STRIP_PROMPT,
        "images": [b64],
        "stream": False,
        "options": {"temperature": 0},
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
        r.raise_for_status()
        raw = r.json()["response"]

    match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in llava response: {raw[:300]}")
    data = json.loads(match.group())
    return {k: (float(v) if v is not None else None) for k, v in data.items()}
