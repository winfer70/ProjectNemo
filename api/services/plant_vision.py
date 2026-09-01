"""Plant leaf deficiency recognition via a configured Ollama vision endpoint.

Mirrors ollama_vision.py's pattern (same model, same resize/JSON-extraction
approach) - one close-up photo of a single affected leaf in, one
classification out. Deliberately NOT attempting multi-leaf/whole-plant
detection - see plant_health.py module docstring for why.
"""
import base64
import io
import json
import logging
import re

import httpx
from PIL import Image

from config import settings
from services.plant_deficiencies import DEFICIENCIES, VALID_KEYS

logger = logging.getLogger(__name__)

MAX_PX = 1024

_SYSTEM = (
    "You are a precise aquarium/aquatic plant health diagnostician. "
    "You are shown a close-up photo of ONE leaf from an aquarium plant. "
    "Classify it against a fixed list of nutrient deficiencies. "
    "If the leaf looks uniformly green with no discoloration, deformity, "
    "holes, or dead patches, classify it as 'normal'. "
    "You must respond with only a JSON object."
)


def _build_user_prompt() -> str:
    lines = ["Classify the leaf in this photo as exactly one of these keys:\n"]
    for d in DEFICIENCIES:
        lines.append(f"- {d['key']}: {d['symptom_en']}")
    lines.append(
        "\nRespond with ONLY this JSON (no explanation, no markdown):\n"
        '{"deficiency_key": "iron", "confidence": 0.8, "reasoning": "short reason"}'
    )
    return "\n".join(lines)


def _resize(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    img.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


async def analyze_plant_leaf(image_bytes: bytes) -> dict:
    """Returns {"deficiency_key": str, "confidence": float, "reasoning": str}.

    Raises ValueError if OLLAMA_URL isn't configured, the model's response
    has no parseable JSON, or the classified key isn't one of ours (a
    hallucinated key is a real failure mode worth surfacing, not silently
    coercing to 'normal').
    """
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
            {"role": "user", "content": _build_user_prompt(), "images": [b64]},
        ],
    }

    async with httpx.AsyncClient(timeout=240) as client:
        r = await client.post(f"{settings.ollama_url}/api/chat", json=payload)
        r.raise_for_status()
        raw = r.json()["message"]["content"]

    logger.info("llava-phi3 plant-leaf raw response: %s", raw[:500])

    match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in llava-phi3 response: {raw[:300]}")
    data = json.loads(match.group())

    key = data.get("deficiency_key")
    if key not in VALID_KEYS:
        raise ValueError(f"Model returned an unknown deficiency_key: {key!r}")

    return {
        "deficiency_key": key,
        "confidence": float(data["confidence"]) if data.get("confidence") is not None else None,
        "reasoning": data.get("reasoning"),
    }
