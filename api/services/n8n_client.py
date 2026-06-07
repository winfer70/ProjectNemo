"""n8n webhook client — fires Telegram notifications."""
import httpx

from config import settings


class N8NClient:
    async def _post(self, webhook_id: str, payload: dict):
        if not webhook_id or not settings.n8n_base_url:
            return
        url = f"{settings.n8n_base_url}/webhook/{webhook_id}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(url, json=payload)
        except Exception:
            pass  # notifications are best-effort, never block the main flow

    async def alert(self, message_en: str, message_pl: str):
        await self._post(settings.n8n_webhook_alert, {
            "message_en": message_en,
            "message_pl": message_pl,
            "lang": settings.telegram_lang,
        })

    async def reminder(self, message_en: str, message_pl: str):
        await self._post(settings.n8n_webhook_reminder, {
            "message_en": message_en,
            "message_pl": message_pl,
            "lang": settings.telegram_lang,
        })

    async def supply_low(self, supply):
        await self._post(settings.n8n_webhook_supply, {
            "name_en": supply.name,
            "name_pl": supply.name_pl,
            "amount": supply.current_amount,
            "unit": supply.unit,
            "purchase_link": supply.purchase_link or "",
            "lang": settings.telegram_lang,
        })

    async def water_test_alert(self, param, value: float):
        await self._post(settings.n8n_webhook_alert, {
            "type": "water_test",
            "param_key": param.key,
            "param_name_en": param.name_en,
            "param_name_pl": param.name_pl,
            "value": value,
            "unit": param.unit,
            "min_safe": param.min_safe,
            "max_safe": param.max_safe,
            "lang": settings.telegram_lang,
        })

    async def maintenance_completed(self, task):
        await self.reminder(
            f"✅ {task.name} completed. Next due: {task.next_due.strftime('%d %b %Y') if task.next_due else '?'}",
            f"✅ {task.name_pl} ukończona. Następna: {task.next_due.strftime('%d %b %Y') if task.next_due else '?'}",
        )

    async def daily_summary(self, payload: dict):
        await self._post(settings.n8n_webhook_daily, {**payload, "lang": settings.telegram_lang})


n8n_client = N8NClient()
