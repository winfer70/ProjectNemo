"""ntfy push notification client."""
import logging

import httpx

from config import settings

logger = logging.getLogger("nemo.ntfy")


class NtfyClient:
    async def send(
        self,
        title: str,
        message: str,
        priority: int = 3,
        tags: list[str] | None = None,
    ) -> None:
        if not settings.ntfy_url:
            return
        headers: dict[str, str] = {
            "Title": title,
            "Priority": str(priority),
        }
        if tags:
            headers["Tags"] = ",".join(tags)
        if settings.ntfy_token:
            headers["Authorization"] = f"Bearer {settings.ntfy_token}"
        url = f"{settings.ntfy_url.rstrip('/')}/{settings.ntfy_topic}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(url, content=message.encode(), headers=headers)
        except Exception as exc:
            logger.warning("ntfy send failed: %s", exc)


ntfy_client = NtfyClient()
