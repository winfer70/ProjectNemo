# Graph Report - .  (2026-09-19)

## Corpus Check
- 56 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 420 nodes · 950 edges · 30 communities detected
- Extraction: 50% EXTRACTED · 50% INFERRED · 0% AMBIGUOUS · INFERRED: 477 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Base` - 28 edges
2. `WaterTestSession` - 20 edges
3. `WaterTestReading` - 20 edges
4. `FeedingPause` - 19 edges
5. `WaterTestSnooze` - 19 edges
6. `MaintenanceTask` - 18 edges
7. `Supply` - 16 edges
8. `Water test sessions + readings + trends.` - 16 edges
9. `parameter_id -> (min_safe, max_safe, test_frequency_days), using this     tank'` - 16 edges
10. `Build the analyze_strip JSON response including out_of_range flags.` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Per-tank override of a parameter's safe range and test frequency -     two diff` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `A recurring aquarium care task shown in the calendar.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `Records that a CalendarTask was completed on a specific date.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `InfluxDB v2 client — write sensor data, query history.` --uses--> `SensorHistoryPoint`  [INFERRED]
  api\services\influx_client.py → api\models\schemas.py
- `FeedingLog` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (56): Website -> Kamilo/Heimdall voice assistant bridge.  Lets the web app send type, BaseModel, Daily dosing tasks — complete dose, restock supplies, CRUD., Add amount to supply current_amount (resupply flow)., Obsada (livestock) CRUD + species image search., Per-tank override of a parameter's safe range and test frequency -     two diff, WaterTestParameter, WaterTestParameterNorm (+48 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (42): Base, Base, DeclarativeBase, Maintenance tasks — list, start, complete with checkboxes., Mark task as in-progress. Suppresses device-off alerts for affects_entity., DoseLog, DosingTask, FeedingPause (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (19): BaseSettings, Settings, InfluxClient, InfluxDB v2 client — write sensor data, query history., NtfyClient, ntfy push notification client., analyze_strip(), Test strip analysis via a configured Ollama endpoint. (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.16
Nodes (24): Exception, analyze_strip(), _assign_pads_by_column(), _cluster_rows(), CVDetectionError, debug_analyze_strip(), _detect_orientation(), _enforce_pad_x_consistency() (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (10): BLEConnectionManager, BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T, Home Assistant REST API client., on_startup(), FastAPI application orchestrator for the ProjectNemo aquarium monitoring system., Add new columns to existing tables. SQLite-safe: errors mean column exists., _run_migrations(), mounted() (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.2
Nodes (19): correct_event(), create_event(), _find_plant_by_name(), kamilo_treat(), list_deficiencies(), Plant health tracking - static deficiency reference + logged issues.  Two ways, The ONLY way an event becomes 'treated' - explicit user action     (website tic, Self-improving-loop hook: user (via website or Kamilo) says the     diagnosis w (+11 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (15): CompleteRequest, get_month(), get_today(), list_tasks(), Calendar router — recurring aquarium care tasks with per-day completion tracking, Return tasks due today + overdue tasks from last 7 days, for a tank., Return True if this task is scheduled on the given date., List all active calendar tasks for a tank. (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (17): analyze_strip(), _build_scan_response(), create_session(), current_values(), debug_strip(), _effective_norms_map(), kamilo_log(), latest_session() (+9 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (6): HAClient, Turn off multiple devices for feeding mode., Turn on devices after feeding pause ends., Legacy: turn off filter only., Broadcast Fluval RGBW channel values to the tablet BLE gateway., Send text to HA's conversation API (Kamilo/Heimdall or whichever         agent

### Community 9 - "Community 9"
Cohesion: 0.23
Nodes (12): FeedingLog, cancel_feed(), feed_now(), feed_status(), Feeding schedule CRUD + Feed Now + Cancel Feed + Feed Status., Immediately cancel feeding pause and resume devices., Return current feeding pause state., Pause the tank's filter/pump devices for 3 min, log feed. (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (10): async_setup_entry(), FluvalChannelNumber, Number entities for each Fluval RGBW channel., NumberEntity, build_set_channels_command(), build_single_channel_command(), Fluval Shaker BLE protocol implementation., Build the BLE write payload for setting all channels simultaneously.     r, g, (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.21
Nodes (4): _cmd1(), connect(), _doSetChannels(), _enqueue()

### Community 12 - "Community 12"
Cohesion: 0.27
Nodes (10): find_db(), main(), migrate_calendar_tasks(), migrate_dosing_tasks(), migrate_fish(), migrate_supplies(), Insert supplies that do not already exist (checked by name).     Returns a mapp, Insert dosing tasks linked to the new supplies.     Skips silently if a dosing (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (2): N8NClient, n8n webhook client — fires Telegram notifications.

### Community 14 - "Community 14"
Cohesion: 0.39
Nodes (7): _broadcast(), broadcast_change(), _get_device_meta(), _get_entity_names(), _get_suppressed_entities(), live_push_loop(), _power_entities()

### Community 15 - "Community 15"
Cohesion: 0.43
Nodes (5): _build_task_out(), create_dosing_task(), list_dosing_tasks(), restock_supply(), update_dosing_task()

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (3): _power_entities(), Device control — Tapo P110 toggle + Fluval RGBW sliders., Derive Tapo power/energy sensor entity IDs from a switch entity ID.

### Community 17 - "Community 17"
Cohesion: 0.38
Nodes (4): _days_until(), list_maintenance(), start_maintenance(), _to_out()

### Community 18 - "Community 18"
Cohesion: 0.38
Nodes (6): _commons_images(), Species image and metadata search — Wikipedia summary + Wikimedia Commons fallba, Resolve free-text (common name, minor misspelling, non-canonical     capitaliza, Search Commons file titles (intitle:) for the query - restricting to     the ti, _resolve_wiki_title(), search_species()

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (3): _compute_hashes(), lookup(), SHA256 + perceptual hash cache for strip scan results.

### Community 20 - "Community 20"
Cohesion: 0.4
Nodes (3): FluvalBLEConfigFlow, Config flow for Fluval Shaker BLE., Handle Bluetooth discovery — auto-populate MAC.

### Community 21 - "Community 21"
Cohesion: 0.6
Nodes (4): fetch_wikipedia_image(), main(), _query_wiki(), Try full latin, then genus+species (skipping cf./sp./var.), then genus only.

### Community 22 - "Community 22"
Cohesion: 0.83
Nodes (3): column_exists(), find_db(), main()

### Community 23 - "Community 23"
Cohesion: 0.83
Nodes (3): column_exists(), find_db(), main()

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (2): find_db(), main()

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Static reference data for the plant-health deficiency diagram/legend.  Matches

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **40 isolated node(s):** `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.`, `Pydantic schemas for API request/response validation.`, `Manual log - user tapped a leaf on the reference diagram for a plant.` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 25`** (2 nodes): `__init__.py`, `Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (2 nodes): `plant_deficiencies.py`, `Static reference data for the plant-health deficiency diagram/legend.  Matches`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `plantHealth.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `waterTests.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `vite.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Base` connect `Community 1` to `Community 0`, `Community 9`, `Community 2`, `Community 6`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `HAClient` connect `Community 8` to `Community 4`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Base` (e.g. with `Supply` and `DosingTask`) actually correct?**
  _`Base` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `WaterTestSession` (e.g. with `Base` and `Water test sessions + readings + trends.`) actually correct?**
  _`WaterTestSession` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `WaterTestReading` (e.g. with `Base` and `Water test sessions + readings + trends.`) actually correct?**
  _`WaterTestReading` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.` to the rest of the system?**
  _40 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._