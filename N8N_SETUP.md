# n8n Workflow Setup — Project Nemo Telegram Notifications

## Prerequisites
- n8n already running on the automation host
- Telegram bot created via @BotFather — copy the bot token
- Your personal Telegram chat ID (send any message to @userinfobot)

## Step 1: Create Telegram credentials in n8n
1. n8n → Settings → Credentials → New
2. Type: Telegram API
3. Access Token: paste bot token
4. Save as "Nemo Telegram Bot"

## Step 2: Create four webhook workflows

### Workflow 1: nemo-alert (water params, temperature, pH out of range)

Trigger: Webhook (POST)
→ IF node: check `body.type == "water_test"`
  → TRUE: Format message with param name, value, safe range
  → FALSE: Use message_en / message_pl directly
→ Switch on body.lang:
  - "en" → send English
  - "pl" → send Polish
  - "both" → send both (one message, PL/EN)
→ Telegram: Send Message to your chat_id

**Webhook URL** (copy to .env as N8N_WEBHOOK_ALERT):
```
http://localhost:5678/webhook/nemo-alert
```

Message format for water test:
```
🧪 {{ $json.param_name_en }} / {{ $json.param_name_pl }}
Value: {{ $json.value }} {{ $json.unit }}
Safe range: {{ $json.min_safe ?? "—" }} – {{ $json.max_safe ?? "—" }}
⚠️ OUT OF SAFE RANGE
```

### Workflow 2: nemo-reminder (maintenance due, water test overdue)

Trigger: Webhook (POST)
→ Telegram: Send message_en + message_pl to chat_id

**Webhook URL** → N8N_WEBHOOK_REMINDER

### Workflow 3: nemo-supply (supply low warnings)

Trigger: Webhook (POST)
→ Telegram message:
```
📦 Low supply: {{ $json.name_en }} / {{ $json.name_pl }}
Amount left: {{ $json.amount }}{{ $json.unit }}
{{ $json.purchase_link ? "Order: " + $json.purchase_link : "" }}
```

**Webhook URL** → N8N_WEBHOOK_SUPPLY

### Workflow 4: nemo-daily (08:05 daily summary)

Trigger: Webhook (POST)
→ Telegram message:
```
🐟 Nemo Daily Summary
🌡️ {{ $json.temperature ?? "—" }}°C  |  pH {{ $json.ph ?? "—" }}
💧 Last water test: {{ $json.days_since_test }} days ago
🔧 Next maintenance: {{ $json.next_maintenance }} in {{ $json.next_maintenance_days }} days
```

**Webhook URL** → N8N_WEBHOOK_DAILY

## Step 3: Update .env
Copy each webhook path (the UUID after `/webhook/`) into the corresponding
N8N_WEBHOOK_* variable in your `.env` file.

## Step 4: Test
```bash
curl -X POST http://localhost:5678/webhook/nemo-alert \
  -H "Content-Type: application/json" \
  -d '{"message_en":"Test alert","message_pl":"Test alert PL","lang":"both"}'
```
You should receive a Telegram message within seconds.

## Telegram message language
Set `TELEGRAM_LANG=both` for PL+EN (recommended while setting up).
Switch to `pl` or `en` for single-language after preferences settle.
