# Graph Report - .  (2026-05-21)

## Corpus Check
- 33 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 181 nodes · 314 edges · 17 communities detected
- Extraction: 66% EXTRACTED · 34% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Base` - 17 edges
2. `CalendarTask` - 12 edges
3. `CalendarCompletion` - 10 edges
4. `Supply` - 9 edges
5. `Water test sessions + readings + trends.` - 9 edges
6. `HAClient` - 8 edges
7. `N8NClient` - 8 edges
8. `MaintenanceTask` - 7 edges
9. `FeedingSchedule` - 7 edges
10. `Daily dosing tasks — complete dose, restock supplies.` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Records that a CalendarTask was completed on a specific date.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `InfluxDB v2 client — write sensor data, query history.` --uses--> `SensorHistoryPoint`  [INFERRED]
  api\services\influx_client.py → api\models\schemas.py
- `CalendarCompletion` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `SQLAlchemy ORM models — maps to SQLite tables.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `A recurring aquarium care task shown in the calendar.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (30): BaseModel, Device control — Tapo P110 toggle + Fluval RGBW sliders., Daily dosing tasks — complete dose, restock supplies., Feeding schedule CRUD + Feed Now action., Pause filter for 10 min via HA, log feed timestamp., DeviceOut, DoseCompleteRequest, DosingTaskOut (+22 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (21): Base, Base, DeclarativeBase, Maintenance tasks — list, steps, complete with checkboxes., CalendarTask, DoseLog, DosingTask, FeedingLog (+13 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (7): BaseSettings, Settings, FastAPI application entry point., _broadcast(), live_push_loop(), WebSocket live push + scheduled jobs (daily summary, overdue checks)., Push sensor + device data to all connected clients every 30 s.

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (3): _build_task_out(), list_dosing_tasks(), feed_now()

### Community 4 - "Community 4"
Cohesion: 0.18
Nodes (10): async_setup_entry(), FluvalChannelNumber, Number entities for each Fluval RGBW channel., NumberEntity, build_set_channels_command(), build_single_channel_command(), Fluval Shaker BLE protocol implementation., Build the BLE write payload for setting all channels simultaneously.     r, g, b (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.24
Nodes (12): CompleteRequest, get_month(), list_tasks(), Calendar router — recurring aquarium care tasks with per-day completion tracking, Toggle completion of a task on a given date. Returns new completed state., Return True if this task is scheduled on the given date., List all active calendar tasks., Return all days in the given month with scheduled tasks and completion status. (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.21
Nodes (4): HAClient, Home Assistant REST API client., Turn filter off; HA automation restarts it after 10 min., Set Fluval RGBW via HA number entities (0–100 each).

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (2): N8NClient, n8n webhook client — fires Telegram notifications.

### Community 8 - "Community 8"
Cohesion: 0.43
Nodes (4): create_session(), latest_session(), list_sessions(), _reading_out()

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (2): InfluxClient, InfluxDB v2 client — write sensor data, query history.

### Community 10 - "Community 10"
Cohesion: 0.47
Nodes (3): _days_until(), list_maintenance(), _to_out()

### Community 11 - "Community 11"
Cohesion: 0.6
Nodes (5): create_supply(), list_supplies(), restock_supply(), _to_out(), update_supply()

### Community 12 - "Community 12"
Cohesion: 0.4
Nodes (3): FluvalBLEConfigFlow, Config flow for Fluval Shaker BLE., Handle Bluetooth discovery — auto-populate MAC.

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/fl

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **15 isolated node(s):** `FastAPI application entry point.`, `Pydantic schemas for API request/response validation.`, `Home Assistant REST API client.`, `Turn filter off; HA automation restarts it after 10 min.`, `Set Fluval RGBW via HA number entities (0–100 each).` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (2 nodes): `__init__.py`, `Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/fl`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `waterTests.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `vite.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Base` connect `Community 1` to `Community 3`, `Community 5`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Base` (e.g. with `Supply` and `DosingTask`) actually correct?**
  _`Base` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CalendarTask` (e.g. with `Base` and `CompleteRequest`) actually correct?**
  _`CalendarTask` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CalendarCompletion` (e.g. with `Base` and `CompleteRequest`) actually correct?**
  _`CalendarCompletion` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FastAPI application entry point.`, `Pydantic schemas for API request/response validation.`, `Home Assistant REST API client.` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._