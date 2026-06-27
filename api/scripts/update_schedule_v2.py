#!/usr/bin/env python3
"""
update_schedule_v2.py — One-time migration script for ProjectNemo.

Run via:
    docker exec nemo-api python scripts/update_schedule_v2.py

What this script does:
  1. Adds new Supplies (upsert by name: insert if name not present, skip if exists)
  2. Adds daily DosingTasks for the new supplies (skip if already linked to supply)
  3. Replaces old feeding CalendarTasks (matched by name pattern) with a new
     consolidated feeding schedule, morning dosing reminder, Friday water test,
     and Saturday maintenance
  4. Updates Fish quantities and notes to match current tank inventory (by latin name)

Safe to re-run: all operations are idempotent — duplicates are skipped, not created.
"""

import json
import os
import sqlite3
from datetime import date

# ──────────────────────────────────────────────────────────────────────────────
# DB path resolution
# ──────────────────────────────────────────────────────────────────────────────

DB_CANDIDATES = [
    "/app/data/nemo.db",
    "./data/nemo.db",
    "../data/nemo.db",
]


def find_db() -> str:
    for path in DB_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"nemo.db not found. Searched: {DB_CANDIDATES}"
    )


# ──────────────────────────────────────────────────────────────────────────────
# Data definitions
# ──────────────────────────────────────────────────────────────────────────────

NEW_SUPPLIES = [
    {
        "name": "MasterLine AllInOne Golden",
        "name_pl": "MasterLine AllInOne Golden",
        "type": "liquid",
        "current_amount": 500,
        "unit": "ml",
        "min_threshold": 50,
        "notes": "Daily 2ml column fertilizer",
    },
    {
        "name": "MasterLine Carbo",
        "name_pl": "MasterLine Carbo",
        "type": "liquid",
        "current_amount": 500,
        "unit": "ml",
        "min_threshold": 50,
        "notes": "Daily 2ml carbon + algae defense",
    },
    {
        "name": "Aquaforest AF Life Essence",
        "name_pl": "Aquaforest AF Life Essence",
        "type": "liquid",
        "current_amount": 250,
        "unit": "ml",
        "min_threshold": 25,
        "notes": "25ml weekly Saturday",
    },
    {
        "name": "Yokuchi bitaMIN",
        "name_pl": "Yokuchi bitaMIN",
        "type": "liquid",
        "current_amount": 50,
        "unit": "pumps",
        "min_threshold": 5,
        "notes": "5 pumps weekly Saturday via filter stream",
    },
    {
        "name": "Tubi-Cubi",
        "name_pl": "Tubi-Cubi (Tropical)",
        "type": "food",
        "current_amount": 6,
        "unit": "cubes",
        "min_threshold": 2,
        "notes": "Wed + Sat premium meat feeding, 1 cube pressed on glass",
    },
    {
        "name": "AF Liquid Artemia",
        "name_pl": "AF Liquid Artemia",
        "type": "food",
        "current_amount": 1,
        "unit": "bottle",
        "min_threshold": 0,
        "notes": "Friday premium meat, 1/2 tsp two-zone method",
    },
]

DOSING_TASKS = [
    {
        "supply_name": "MasterLine AllInOne Golden",
        "dose_amount": 2.0,
        "dose_unit": "ml",
        "time_of_day": "08:00",
        "notes": "After lights ON. Liquid fertilizer for water column plants.",
    },
    {
        "supply_name": "MasterLine Carbo",
        "dose_amount": 2.0,
        "dose_unit": "ml",
        "time_of_day": "08:00",
        "notes": "After lights ON. Carbon source + algae suppression.",
    },
]

TODAY = date.today().isoformat()

# New calendar tasks to insert after deleting old feeding tasks.
# recurrence_days is stored as a JSON string in the DB (matches ORM property).
NEW_CALENDAR_TASKS = [
    # Standard feeding: Mon(0), Tue(1), Thu(3), Sun(6)
    {
        "name": "Standard Feeding",
        "name_pl": "Karmienie standardowe",
        "color": "#00b4d8",
        "recurrence_type": "weekdays",
        "recurrence_days": [0, 1, 3, 6],
        "start_date": TODAY,
        "notes_pl": (
            "19:00 \u2014 Pauza filtra 3min. "
            "G\u00f3ra/\u015brodek: flaki (rozkruszone, namoczone 1min, 2-strefowo). "
            "D\u00f3\u0142: 1 tabletka Cory pod korzeniem."
        ),
    },
    # Premium meat days: Wed(2), Fri(4), Sat(5)
    {
        "name": "Premium Meat Feeding",
        "name_pl": "Karmienie premium",
        "color": "#f77f00",
        "recurrence_type": "weekdays",
        "recurrence_days": [2, 4, 5],
        "start_date": TODAY,
        "notes_pl": (
            "\u015ar+Sob: 1 kostk\u0119 Tubi-Cubi przyci\u015bnij do szyby. "
            "Pt: AF Liquid Artemia 1/2 \u0142y\u017ceczki 2-strefowo. "
            "D\u00f3\u0142: 1/2 tabletki Cory przy kokosach przed zga\u015bleniem."
        ),
    },
    # Daily dosing reminder
    {
        "name": "Morning Dosing",
        "name_pl": "Poranne dozowanie",
        "color": "#2dc653",
        "recurrence_type": "daily",
        "recurrence_days": [],
        "start_date": TODAY,
        "notes_pl": (
            "Po w\u0142\u0105czeniu \u015bwiate\u0142: "
            "2ml MasterLine Golden + 2ml MasterLine Carbo"
        ),
    },
    # Friday water test
    {
        "name": "Friday Water Test",
        "name_pl": "Pi\u0105tkowy test wody",
        "color": "#f72585",
        "recurrence_type": "weekdays",
        "recurrence_days": [4],
        "start_date": TODAY,
        "notes_pl": (
            "Test przed wymian\u0105: KH (cel 5), GH (cel 12), pH (cel 7.6), "
            "NO3 (cel <15ppm). Sprawd\u017a szyby \u2014 je\u015bli zielony film: "
            "ogranicz Golden+Carbo do 1ml."
        ),
    },
]

# Saturday maintenance — update existing "water change" / "wymiana" task notes
# if one exists, otherwise insert as a new task.
SATURDAY_MAINTENANCE = {
    "name": "Saturday Maintenance",
    "name_pl": "Konserwacja sobota",
    "color": "#9b5de5",
    "recurrence_type": "weekdays",
    "recurrence_days": [5],
    "start_date": TODAY,
    "notes_pl": (
        "1. 22L RO/DI + 8L kranowej = 30L. "
        "2. Dodaj Seachem Prime. "
        "3. Wymie\u0144 30L. "
        "4. AF Life Essence 25ml do kolumny. "
        "5. Yokuchi bitaMIN 5 pompek do filtra."
    ),
}

FISH_UPDATES = [
    {
        "latin": "Trichopodus leerii",
        "qty": 3,
        "notes_pl": "1M + 2F (harem). Labyrinthfish, wra\u017cliwy na ruch powierzchni.",
    },
    {
        "latin": "Desmopuntius pentazona",
        "qty": 9,
        "notes_pl": "Spokojne szkolne ryby, w pe\u0142ni opancerzone.",
    },
    {
        "latin": "Hyphessobrycon loretoensis",
        "qty": 3,
        "notes_pl": "Pozosta\u0142o\u015b\u0107 starego stada. Nie uzupe\u0142niamy.",
    },
    {
        "latin": "Garra flavatra",
        "qty": 5,
        "notes_pl": "Aktywni diurnalni czy\u015bczacze.",
    },
    {
        "latin": "Pangio kuhlii",
        "qty": 9,
        "notes_pl": "Nocne denniki, zamieszkuj\u0105 kokosy Niteangel.",
    },
    {
        "latin": "Corydoras trilineatus",
        "qty": 6,
        "notes_pl": "Aktywne korytki piaskowe.",
    },
    {
        "latin": "Caridina multidentata",
        "qty": 3,
        "notes_pl": "Ukryte krewetki czyszcz\u0105ce.",
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Migration steps
# ──────────────────────────────────────────────────────────────────────────────

def migrate_supplies(cur: sqlite3.Cursor) -> dict:
    """
    Insert supplies that do not already exist (checked by name).
    Returns a mapping of supply name -> supply id for all target supplies.
    """
    supply_id_map: dict = {}
    for s in NEW_SUPPLIES:
        row = cur.execute(
            "SELECT id FROM supplies WHERE name = ?", (s["name"],)
        ).fetchone()
        if row:
            supply_id_map[s["name"]] = row[0]
            print(f"  Supply already exists, skipping: {s['name']}")
        else:
            cur.execute(
                """INSERT INTO supplies
                       (name, name_pl, type, current_amount, unit, min_threshold, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    s["name"], s["name_pl"], s["type"],
                    s["current_amount"], s["unit"], s["min_threshold"], s["notes"],
                ),
            )
            supply_id_map[s["name"]] = cur.lastrowid
            print(f"  Added supply: {s['name']}")
    return supply_id_map


def migrate_dosing_tasks(cur: sqlite3.Cursor, supply_id_map: dict) -> None:
    """
    Insert dosing tasks linked to the new supplies.
    Skips silently if a dosing task already exists for that supply_id.
    """
    for dt in DOSING_TASKS:
        supply_name = dt["supply_name"]
        supply_id = supply_id_map.get(supply_name)
        if supply_id is None:
            print(f"  WARNING: supply not found for dosing task, skipping: {supply_name}")
            continue

        existing = cur.execute(
            "SELECT id FROM dosing_tasks WHERE supply_id = ?", (supply_id,)
        ).fetchone()
        if existing:
            print(f"  Dosing task already exists for supply: {supply_name}")
        else:
            cur.execute(
                """INSERT INTO dosing_tasks
                       (supply_id, dose_amount, dose_unit, time_of_day, active, notes)
                   VALUES (?, ?, ?, ?, 1, ?)""",
                (
                    supply_id, dt["dose_amount"], dt["dose_unit"],
                    dt["time_of_day"], dt["notes"],
                ),
            )
            print(
                f"  Added dosing task: {supply_name} "
                f"{dt['dose_amount']}{dt['dose_unit']} @ {dt['time_of_day']}"
            )


def migrate_calendar_tasks(cur: sqlite3.Cursor) -> None:
    """
    1. Delete all calendar tasks whose name (EN or PL) contains 'feed' or
       'karmienie' (case-insensitive).
    2. Insert new feeding schedule, morning dosing reminder, and Friday water
       test tasks.
    3. For Saturday maintenance: update notes on any existing task whose name
       matches 'water change' or 'wymiana' (case-insensitive); if none found,
       insert a new Saturday Maintenance task.
    """
    # --- Delete old feeding tasks ---
    old_rows = cur.execute(
        """SELECT id, name FROM calendar_tasks
           WHERE LOWER(name)    LIKE '%feed%'
              OR LOWER(name_pl) LIKE '%feed%'
              OR LOWER(name)    LIKE '%karmienie%'
              OR LOWER(name_pl) LIKE '%karmienie%'"""
    ).fetchall()

    for row_id, row_name in old_rows:
        cur.execute("DELETE FROM calendar_tasks WHERE id = ?", (row_id,))
        print(f"  Deleted old feeding task (id={row_id}): {row_name}")
    if not old_rows:
        print("  No old feeding tasks matched the delete pattern.")

    # --- Insert new standard calendar tasks ---
    for t in NEW_CALENDAR_TASKS:
        cur.execute(
            """INSERT INTO calendar_tasks
                   (name, name_pl, color, recurrence_type, interval_days,
                    recurrence_days, start_date, end_date, amount, notes_pl, active)
               VALUES (?, ?, ?, ?, NULL, ?, ?, NULL, NULL, ?, 1)""",
            (
                t["name"], t["name_pl"], t["color"], t["recurrence_type"],
                json.dumps(t["recurrence_days"]),
                t["start_date"],
                t["notes_pl"],
            ),
        )
        print(f"  Added calendar task: {t['name']}")

    # --- Saturday maintenance: update existing or insert new ---
    existing_row = cur.execute(
        """SELECT id, name FROM calendar_tasks
           WHERE LOWER(name) LIKE '%water change%'
              OR LOWER(name) LIKE '%wymiana%'"""
    ).fetchone()

    sm = SATURDAY_MAINTENANCE
    if existing_row:
        cur.execute(
            "UPDATE calendar_tasks SET notes_pl = ? WHERE id = ?",
            (sm["notes_pl"], existing_row[0]),
        )
        print(
            f"  Updated Saturday maintenance notes on existing task "
            f"(id={existing_row[0]}): {existing_row[1]}"
        )
    else:
        cur.execute(
            """INSERT INTO calendar_tasks
                   (name, name_pl, color, recurrence_type, interval_days,
                    recurrence_days, start_date, end_date, amount, notes_pl, active)
               VALUES (?, ?, ?, ?, NULL, ?, ?, NULL, NULL, ?, 1)""",
            (
                sm["name"], sm["name_pl"], sm["color"], sm["recurrence_type"],
                json.dumps(sm["recurrence_days"]),
                sm["start_date"],
                sm["notes_pl"],
            ),
        )
        print("  Added new Saturday Maintenance calendar task.")


def migrate_fish(cur: sqlite3.Cursor) -> None:
    """
    Update fish qty and notes_pl by latin name.
    Logs a warning if a latin name is not found (does not insert — fish rows
    must already exist with full metadata from the original seed or manual entry).
    """
    for f in FISH_UPDATES:
        rows_affected = cur.execute(
            "UPDATE fish SET qty = ?, notes_pl = ? WHERE latin = ?",
            (f["qty"], f["notes_pl"], f["latin"]),
        ).rowcount
        if rows_affected:
            print(f"  Updated fish qty: {f['latin']} -> {f['qty']}")
        else:
            print(f"  WARNING: fish not found by latin name, skipping: {f['latin']}")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    db_path = find_db()
    print(f"DB: {db_path}\n")

    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("PRAGMA journal_mode=WAL")

    try:
        print("--- Supplies ---")
        supply_id_map = migrate_supplies(cur)

        print("\n--- Dosing Tasks ---")
        migrate_dosing_tasks(cur, supply_id_map)

        print("\n--- Calendar Tasks ---")
        migrate_calendar_tasks(cur)

        print("\n--- Fish ---")
        migrate_fish(cur)

        con.commit()
        print("\nMigration complete. All changes committed.")
    except Exception:
        con.rollback()
        print("\nERROR: exception raised — all changes rolled back.")
        raise
    finally:
        con.close()


if __name__ == "__main__":
    main()
