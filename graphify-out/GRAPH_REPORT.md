# Graph Report - .  (2026-08-12)

## Corpus Check
- 46 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 355 nodes · 685 edges · 22 communities detected
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 287 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Base` - 22 edges
2. `FeedingPause` - 17 edges
3. `MaintenanceTask` - 16 edges
4. `Supply` - 14 edges
5. `analyze_strip()` - 13 edges
6. `analyze_strip()` - 13 edges
7. `WaterTestSession` - 12 edges
8. `HAClient` - 12 edges
9. `CalendarTask` - 11 edges
10. `Database seeder for ProjectNemo reference data — called once by main.py on start` - 11 edges

## Surprising Connections (you probably didn't know these)
- `A recurring aquarium care task shown in the calendar.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `Records that a CalendarTask was completed on a specific date.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `InfluxDB v2 client — write sensor data, query history.` --uses--> `SensorHistoryPoint`  [INFERRED]
  api\services\influx_client.py → api\models\schemas.py
- `FeedingLog` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `CalendarTask` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (42): Base, Base, DeclarativeBase, Maintenance tasks — list, start, complete with checkboxes., Mark task as in-progress. Suppresses device-off alerts for affects_entity., DoseLog, DosingTask, FeedingPause (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (45): BaseModel, Daily dosing tasks — complete dose, restock supplies, CRUD., Add amount to supply current_amount (resupply flow)., Obsada (livestock) CRUD + species image search., FeedingLog, Feeding schedule CRUD + Feed Now + Cancel Feed + Feed Status., Immediately cancel feeding pause and resume devices., Return current feeding pause state. (+37 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (17): BaseSettings, Settings, list_devices(), _power_entities(), Device control — Tapo P110 toggle + Fluval RGBW sliders., Derive Tapo power/energy sensor entity IDs from a switch entity ID., InfluxClient, InfluxDB v2 client — write sensor data, query history. (+9 more)

### Community 3 - "Community 3"
Cohesion: 0.1
Nodes (15): cancel_feed(), feed_now(), feed_status(), create_supply(), list_supplies(), restock_supply(), _to_out(), update_supply() (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (24): Exception, analyze_strip(), _assign_pads_by_column(), _cluster_rows(), CVDetectionError, debug_analyze_strip(), _detect_orientation(), _enforce_pad_x_consistency() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (23): analyze_strip(), _assign_pads_by_column(), _cluster_rows(), CVDetectionError, debug_analyze_strip(), _detect_orientation(), _enforce_pad_x_consistency(), _find_cells() (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (15): CompleteRequest, get_month(), get_today(), list_tasks(), Calendar router — recurring aquarium care tasks with per-day completion tracking, Return tasks due today + overdue tasks from last 7 days., Return True if this task is scheduled on the given date., List all active calendar tasks. (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (7): BLEConnectionManager, BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T, Home Assistant REST API client., on_startup(), FastAPI application orchestrator for the ProjectNemo aquarium monitoring system., Add new columns to existing tables. SQLite-safe: errors mean column exists., _run_migrations()

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (5): HAClient, Turn off multiple devices for feeding mode., Turn on devices after feeding pause ends., Legacy: turn off filter only., Broadcast Fluval RGBW channel values to the tablet BLE gateway.

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (10): async_setup_entry(), FluvalChannelNumber, Number entities for each Fluval RGBW channel., NumberEntity, build_set_channels_command(), build_single_channel_command(), Fluval Shaker BLE protocol implementation., Build the BLE write payload for setting all channels simultaneously.     r, g, (+2 more)

### Community 10 - "Community 10"
Cohesion: 0.21
Nodes (5): _cmd1(), connect(), _doSetChannels(), _enqueue(), Continuous sensor data — current state + history from InfluxDB.

### Community 11 - "Community 11"
Cohesion: 0.27
Nodes (10): find_db(), main(), migrate_calendar_tasks(), migrate_dosing_tasks(), migrate_fish(), migrate_supplies(), Insert supplies that do not already exist (checked by name).     Returns a mapp, Insert dosing tasks linked to the new supplies.     Skips silently if a dosing (+2 more)

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 0.38
Nodes (4): _days_until(), list_maintenance(), start_maintenance(), _to_out()

### Community 14 - "Community 14"
Cohesion: 0.43
Nodes (5): _build_task_out(), create_dosing_task(), list_dosing_tasks(), restock_supply(), update_dosing_task()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (3): _compute_hashes(), lookup(), SHA256 + perceptual hash cache for strip scan results.

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (3): FluvalBLEConfigFlow, Config flow for Fluval Shaker BLE., Handle Bluetooth discovery — auto-populate MAC.

### Community 17 - "Community 17"
Cohesion: 0.6
Nodes (4): fetch_wikipedia_image(), main(), _query_wiki(), Try full latin, then genus+species (skipping cf./sp./var.), then genus only.

### Community 18 - "Community 18"
Cohesion: 0.67
Nodes (3): _commons_images(), Species image and metadata search — Wikipedia summary + Wikimedia Commons fallba, search_species()

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **41 isolated node(s):** `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.`, `Pydantic schemas for API request/response validation.`, `Try full latin, then genus+species (skipping cf./sp./var.), then genus only.` (+36 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 19`** (2 nodes): `__init__.py`, `Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `waterTests.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `vite.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HAClient` connect `Community 8` to `Community 7`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Base` connect `Community 0` to `Community 1`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `Base` (e.g. with `Supply` and `DosingTask`) actually correct?**
  _`Base` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `FeedingPause` (e.g. with `Base` and `Feeding schedule CRUD + Feed Now + Cancel Feed + Feed Status.`) actually correct?**
  _`FeedingPause` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `MaintenanceTask` (e.g. with `Base` and `Maintenance tasks — list, start, complete with checkboxes.`) actually correct?**
  _`MaintenanceTask` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.` to the rest of the system?**
  _41 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._