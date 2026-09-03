"""Website -> Kamilo/Heimdall voice assistant bridge.

Lets the web app send typed or (browser-transcribed) spoken text straight to
Home Assistant's conversation API - the same pipeline a smart speaker uses -
so "just tell the AI what to update" works from the site itself, no separate
device needed.
"""
from fastapi import APIRouter, HTTPException

from models.schemas import AssistantAsk, AssistantReply
from services.ha_client import ha_client

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/ask", response_model=AssistantReply)
async def ask(body: AssistantAsk):
    text = body.text.strip()
    if not text:
        raise HTTPException(422, "text is required")

    try:
        data = await ha_client.converse(text, body.language, body.conversation_id)
    except Exception as e:
        raise HTTPException(502, f"Assistant unavailable: {type(e).__name__}: {e}")

    response = data.get("response", {})
    speech = response.get("speech", {}).get("plain", {}).get("speech")
    reply = speech or "…"
    return AssistantReply(
        reply=reply,
        response_type=response.get("response_type"),
        conversation_id=data.get("conversation_id"),
    )
