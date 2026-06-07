# ProjectNemo — Design Brief

> For UI/UX design reference. Features marked ✅ are live; features marked 🔜 are planned and should be designed as if complete.

---

## What It Is

**ProjectNemo** is a mobile-first PWA for managing a home aquarium. Runs on a Raspberry Pi (REDACTED-HOST) at home, accessed from phone/tablet. Dark theme, Polish/English bilingual, real-time data from sensors and smart plugs via Home Assistant.

Primary user: one person, daily use, mostly on mobile while standing at the tank.

---

## Tech Stack (for context, not design)

- Vue 3 + Pinia, no router (tab-based)
- FastAPI + SQLite backend on REDACTED-HOST
- Home Assistant REST API → Tapo P110 smart plugs (filter, heater, air pump, light)
- WebSocket push every 30s (temp, pH, plug states + watts)
- n8n → Telegram for notifications
- BLE for light control (not always connected)

---

## Design System (current)

### Colors
```
--bg:           #0e1117   (main background)
--surface:      #161b22   (cards, tiles)
--surface-alt:  #1c2333   (elevated cards, modals)
--border:       #30363d   (dividers, borders)
--accent:       #58a6ff   (primary CTA, active states)
--accent-warm:  #f0883e   (warnings, feeding mode)
--success:      #3fb950   (healthy, done, on)
--danger:       #f85149   (alerts, off/error)
--warning:      #d29922   (caution, low supply)
--text:         #e6edf3   (primary text)
--text-muted:   #8b949e   (secondary text, labels)
```

### Typography
- Font: system-ui / -apple-system (native)
- Base size: 14px
- Title "PROJECT NEMO": 15px bold
- Clock: **same size as title (15px), bold** 🔜 centered in header
- Card titles: 13px, color `--text-muted`, uppercase tracking
- Values/numbers: 20-24px bold

### Spacing
- Card padding: 16px
- Gap between tiles: 12px
- Border-radius: 12px (cards), 8px (buttons), 20px (pills)

### Layout
- Mobile-first, max ~430px
- Header: 48px fixed top
- Bottom tab bar: 60px fixed bottom (🔜 auto-hides on scroll down, reappears on scroll up)
- Content area: scrollable between header and nav bar

---

## Navigation (5 tabs, bottom bar)

| Tab | Icon | Label EN | Label PL |
|-----|------|----------|----------|
| schedule | calendar-check | Schedule | Harmonogram |
| live | activity/pulse | Live | Na Żywo |
| tests | droplet | Tests | Testy |
| calendar | calendar | Calendar | Kalendarz |
| livestock | fish | Livestock | Obsada |

Active tab: `--accent` color. Inactive: `--text-muted`.

---

## Screen 1 — Harmonogram (Schedule) ← HOME SCREEN

The main daily-use screen. All tiles stack vertically, single column.

### Header (global, all screens)
```
┌─────────────────────────────────────┐
│  🐟 PROJECT NEMO    [clock]  EN|PL  │  ← clock centered, bold 15px 🔜
└─────────────────────────────────────┘
```
🔜 Clock moves to center, bold. Locale toggle right-aligned.

---

### Tile 1 — Dzisiaj (Today's Tasks) 🔜 replaces Karmienie tile

Shows calendar tasks due today + overdue. Feed Now action embedded.

```
┌─────────────────────────────────────┐
│ DZISIAJ / TODAY           [date]    │
│─────────────────────────────────────│
│ ✅ Zmiana wody 20%         done     │  ← green checkmark, strikethrough
│ 🔴 Wymień wkład filtra     2 dni po │  ← overdue = red badge
│ ⏳ Dozowanie nawozów       dziś     │  ← pending = accent color
│ ⏳ Test wody               dziś     │
│─────────────────────────────────────│
│  [✓ Zrobione]  [⏰ Jutro]  [+ Dodaj]│  ← action row per selected task
│─────────────────────────────────────│
│        [🐟 Karm Teraz]              │  ← Feed Now CTA button, warm accent
│   Filter + pompa stop 3 min        │  ← shown only when feeding active
│   [████████░░] 1:42 pozostało      │  ← countdown progress bar
│                    [✗ Anuluj]      │  ← Cancel feeding button
└─────────────────────────────────────┘
```

States:
- **Normal**: task list + Feed Now button
- **Feeding active**: progress bar replaces button, Cancel appears, tile background shifts to `--accent-warm` tint
- **No tasks today**: "Brak zadań na dziś 🎉" empty state, Feed Now still visible
- **Overdue tasks**: red left border on row, "X dni po" badge

Task row tap: expands inline → shows [✓ Zrobione] [⏰ Snooze 1h] [📅 Jutro] buttons.

---

### Tile 2 — Dozowanie (Dosing)

Current: shows list of scheduled doses (chemical name, amount, time). Mark as done deducts from supply.

🔜 Additions:
- Per-supply **Uzupełnij** (Restock) button: opens mini-modal with amount input → adds to `current_amount`
- Per-task **edit** button: change dose amount, time of day
- **+ Dodaj dawkę** button at bottom → add new DosingTask

```
┌─────────────────────────────────────┐
│ DOZOWANIE                    [+ Add]│
│─────────────────────────────────────│
│ 💧 Nawóz A   5ml  08:00    [✓][✏️] │  ← done / edit
│    Pozostało: 245ml  ████████░░ 82% │  ← supply bar, green→yellow→red
│    [+ Uzupełnij]                    │
│─────────────────────────────────────│
│ 💧 Nawóz B   2ml  20:00    [✓][✏️] │
│    Pozostało: 12ml   ██░░░░░░░░ 9%  │  ← red = below threshold
│    [+ Uzupełnij]                    │
└─────────────────────────────────────┘
```

Supply bar colors: >50% green, 20-50% yellow/warning, <20% red/danger.
Restock modal: number input + unit label + confirm.

---

### Tile 3 — Oświetlenie (Lighting)

Current: BLE toggle for light (on/off), shows connected/disconnected state. Keep as-is.

```
┌─────────────────────────────────────┐
│ OŚWIETLENIE                         │
│─────────────────────────────────────│
│ 💡 Światło         [●────] ON       │  ← toggle
│    BLE: Połączono  ●                │  ← status dot
└─────────────────────────────────────┘
```

If BLE disconnected: dim toggle, "Niepołączono" label, tap = attempt reconnect.

---

### Tile 4 — Konserwacja (Maintenance) + Tile 5 side by side 🔜

Two tiles in same row (50/50 split) on wide enough screens, stacked on narrow:

```
┌──────────────────┐┌──────────────────┐
│ KONSERWACJA      ││ WTYCZKI          │
│──────────────────││──────────────────│
│ ⚙️ Filtr  7 dni  ││ 🔌 Filtr  ● ON   │
│ 🔴 Wkład  2 dni+ ││    12W           │
│ ⚙️ Szybka 14 dni ││ 🔌 Grzałka ● ON  │
│                  ││    35W           │
│ [▶ Start]        ││ 🔌 Pompa  ● ON   │
│                  ││    8W            │
│                  ││ 🔌 Światło ○ OFF │
│                  ││    0W            │
└──────────────────┘└──────────────────┘
```

**Konserwacja tile:**
- Task list with next-due dates
- Overdue = red left border + bold
- **[▶ Start]** button → sets task `in_progress`, changes button to [✓ Zakończ]
- While `in_progress`: device warnings suppressed for that task's `affects_entity`
- 🔜 Water change task type: Start → turns off filter + heater, shows "Wymiana w toku" banner on schedule screen → tap [✓ Zrobiono] to resume devices

**Inteligentne Wtyczki tile (NEW):** 🔜
- Each device: icon + name + status dot (green=ON, red=OFF) + live watts
- Tap any device row → bottom sheet modal:
  ```
  ┌─────────────────────────────────────┐
  │ ⚙️ Filtr (switch.tapo_filter)       │
  │─────────────────────────────────────│
  │ Status:     ● WŁĄCZONY              │
  │ Moc:        12W                     │
  │ Zużycie dziś: 0.28 kWh             │
  │ Stan od:    14:22                   │
  │─────────────────────────────────────│
  │     [Wyłącz]      [Zamknij]        │
  └─────────────────────────────────────┘
  ```
- OFF state highlighted: row background `--danger` tint, watts shows "0W"
- If device off and not in feeding/maintenance mode: orange warning icon

---

## Screen 2 — Na Żywo (Live Data)

Real-time sensor dashboard. WebSocket push every 30s.

```
┌─────────────────────────────────────┐
│ NA ŻYWO           ● Połączono       │
│─────────────────────────────────────│
│  🌡️ Temperatura        pH           │
│    26.4°C             7.2           │
│    ──────────        ──────         │
│    min 26.0  max 27.0  optimal      │
│─────────────────────────────────────│
│ URZĄDZENIA                          │
│ Filter     ● ON   [toggle]   12W   │
│ Heater     ● ON   [toggle]   35W   │
│ Air Pump   ● ON   [toggle]    8W   │
│ Light      ○ OFF  [toggle]    0W   │
└─────────────────────────────────────┘
```

Device name + status dot + toggle switch + live watts.
🔜 Names now always showing (bug fix: was missing).

---

## Screen 3 — Testy Wody (Water Tests)

Parameter history + AI test strip scanning.

```
┌─────────────────────────────────────┐
│ TESTY WODY              [📷 Skanuj] │
│─────────────────────────────────────│
│ Ostatni test: 3 dni temu            │
│─────────────────────────────────────│
│ Parametr   Wartość  Status  Trend   │
│ GH         12 °dH   ✅ OK   →      │
│ KH          6 °dH   ✅ OK   ↗      │
│ pH          7.2     ✅ OK   →      │
│ NO2         0 ppm   ✅ OK   →      │
│ NO3        25 ppm   ⚠️ High  ↗     │
│ NH3         0 ppm   ✅ OK   →      │
│─────────────────────────────────────│
│ [Historia]  [Cykl zbiornika]        │
└─────────────────────────────────────┘
```

Scan flow: camera → strip detection → CV color matching → AI fallback → confirm values → save.
Trend arrows: → stable, ↗ rising, ↘ falling (last 3 readings).

---

## Screen 4 — Kalendarz (Calendar)

Monthly calendar with recurring maintenance/care task scheduling.

```
┌─────────────────────────────────────┐
│ KALENDARZ              [+ Nowe]     │
│─────────────────────────────────────│
│   Czerwiec 2026        < >          │
│─────────────────────────────────────│
│ Pn  Wt  Śr  Cz  Pt  Sb  Nd        │
│  1   2   3   4   5●  6   7         │  ← ● = has tasks
│  8   9  10  11  12  13  14         │
│ 15  16  17  18  19  20  21         │
│ 22  23  24  25  26  27  28         │
│─────────────────────────────────────│
│ 5 Cze — Środa                       │
│ ⏳ Wymiana wody 20%    [✓][✏️][🗑]  │
│ ✅ Test wody           [✓][✏️][🗑]  │
│─────────────────────────────────────│
│ [+ Dodaj zadanie]                   │
└─────────────────────────────────────┘
```

🔜 Full CRUD:
- **+ Nowe / + Dodaj zadanie** → modal: title, date, repeat (once / daily / every N days / weekdays), notes
- Tap task → edit modal (same fields)
- Delete confirmation inline
- Calendar dots on days that have tasks

---

## Screen 5 — Obsada (Livestock)

Fish and plant inventory.

```
┌─────────────────────────────────────┐
│ OBSADA                   [+ Dodaj]  │
│─────────────────────────────────────│
│ RYBY (8)                            │
│─────────────────────────────────────│
│ [img] Neon Tetra         in_tank ▼  │  ← status badge, tappable to edit
│       Paracheirodon innesi          │
│       Dodano: 2025-03-12  x6        │
│─────────────────────────────────────│
│ [img] Corydoras          planned ▼  │
│       Corydoras paleatus            │
│       Planowane: 2026-07  x4        │
│─────────────────────────────────────│
│ ROŚLINY (4)                         │
│ [img] Vallisneria        in_tank ▼  │
│       Vallisneria spiralis          │
└─────────────────────────────────────┘
```

🔜 Status lifecycle badge (tappable):
- `planned` → gray pill
- `in_tank` → green pill  
- `sold` → blue pill
- `deceased` → red/muted pill

Tap status badge → inline status picker (planned / in_tank / sold / deceased).
Tap card → full edit modal (name, species, count, date, image, notes, status).

---

## Modals & Overlays

### Feed Now — active state (overlay on Schedule tile)
- Tile 1 gets warm tint background (#f0883e at 10% opacity)
- Progress bar (accent-warm fill) with countdown "X:XX pozostało"
- [✗ Anuluj karmienie] danger-outlined button

### Smart Plug Detail (bottom sheet) 🔜
- Slides up from bottom, 60% screen height
- Drag handle at top
- Device name + entity ID (small, muted)
- Status, watts, kWh today, on-since time
- Toggle button
- Close by dragging down or tapping backdrop

### Restock Supply (mini-modal) 🔜
- Centered modal, small
- "Ile dodajesz?" label + number input + unit
- [Anuluj] [Uzupełnij]

### Calendar Task Edit/Add (modal) 🔜
- Full-height modal
- Fields: Title (PL), Title (EN), Date picker, Repeat dropdown, Notes
- [Anuluj] [Zapisz]

---

## Notification System (Telegram)

> Not visible in app UI, but context for design:

- Morning digest (8AM): today's tasks via Telegram with inline reply buttons
- **Inline buttons on task**: ✅ Zrobione / ⏰ Odłóż 1h / 📅 Jutro
- Device alert: if filter/heater/air off >10 min (not during feeding or maintenance) → Telegram warning

---

## Key Interaction Patterns

| Pattern | Implementation |
|---------|---------------|
| Pull to refresh | All views |
| Swipe task to complete | Calendar task rows |
| Long-press | Show context menu (edit/delete) |
| Bottom sheet | Smart plug details, heavy modals |
| Progress bar | Feeding countdown |
| Status badges | Obsada, device states |
| Dot indicator | Calendar days with tasks |
| Supply bar | Dozowanie supply levels |
| Scroll-hide nav | Nav bar hides on scroll down, shows on scroll up |

---

## Empty States

| Screen | Empty state text |
|--------|-----------------|
| Today's tasks | "Brak zadań na dziś 🎉" |
| Dosing | "Brak zaplanowanych dawek" + [+ Dodaj] |
| Livestock | "Dodaj pierwsze ryby 🐠" |
| Calendar day | "Wolny dzień" |
| Water tests | "Brak testów — dodaj pierwszy wynik" |

---

## Constraints

- **Mobile-first**: designed for 390px-430px width (iPhone 14 Pro range). Tablet ≥ 768px can show 2-column grid.
- **Dark only**: no light mode.
- **Polish primary**: PL labels shown when locale=pl, EN when locale=en.
- **Offline-tolerant**: show stale data with "Ostatnia synchronizacja: X min temu" if WebSocket drops.
- **No router**: single-page, tab-based component swap. No URLs change.

---

## Data Sources Summary

| Data | Source | Refresh |
|------|--------|---------|
| Temp / pH | BLE sensor → FastAPI | WebSocket 30s |
| Plug status / watts | Home Assistant → FastAPI | WebSocket 30s |
| Calendar tasks | SQLite | On load / after mutation |
| Dosing tasks + supplies | SQLite | On load |
| Livestock | SQLite | On load |
| Water test history | SQLite | On load |
| Maintenance tasks | SQLite | On load |
| Feeding pause state | SQLite (FeedingPause table) | WebSocket + poll |

---

## File Structure Reference

```
ui/src/
  App.vue                   — shell, header, tab bar
  style.css                 — full design system
  views/
    ScheduleView.vue        — HOME: today tasks + dosing + lighting + maintenance + plugs
    LiveView.vue            — real-time sensors + device toggles
    WaterTestsView.vue      — test history + strip scan
    CalendarView.vue        — monthly calendar + task CRUD
    LivestockView.vue       — fish/plant inventory
  stores/
    schedule.js             — feeding state, filter pause, dosing
    calendar.js             — task data, completions
    sensors.js              — WebSocket, plug states
    maintenance.js          — maintenance tasks
    obsada.js               — livestock data
  components/
    ObsadaAddModal.vue      — add/edit fish/plant
    MaintenanceModal.vue    — complete maintenance task
```
