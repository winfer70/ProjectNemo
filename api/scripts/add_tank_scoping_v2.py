#!/usr/bin/env python3
"""
add_tank_scoping_v2.py — Second tank-scoping migration for ProjectNemo.

Run via:
    docker exec nemo-api python scripts/add_tank_scoping_v2.py

Adds `tank_id` to feeding_schedule, feeding_log, feeding_pauses, and
calendar_tasks (missed by add_tank_scoping.py, which only covered
fish/plants/dosing_tasks/water_test_sessions/maintenance_tasks). Backfills
tank_id=1 on all existing rows - all data predates the second aquarium.

Safe to re-run: ALTER TABLE ADD COLUMN is skipped if the column already
exists; the UPDATE backfill only touches rows where tank_id IS NULL.
"""

import os
import sqlite3

DB_CANDIDATES = [
    "/app/data/nemo.db",
    "./data/nemo.db",
    "../data/nemo.db",
]

TANK_SCOPED_TABLES = ["feeding_schedule", "feeding_log", "feeding_pauses", "calendar_tasks"]


def find_db() -> str:
    for path in DB_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"nemo.db not found. Searched: {DB_CANDIDATES}")


def column_exists(cur: sqlite3.Cursor, table: str, column: str) -> bool:
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def main() -> None:
    db_path = find_db()
    print(f"Using DB: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for table in TANK_SCOPED_TABLES:
        if column_exists(cur, table, "tank_id"):
            print(f"  {table}.tank_id already exists - skipping ALTER TABLE")
        else:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN tank_id INTEGER")
            print(f"  Added {table}.tank_id")

        cur.execute(f"UPDATE {table} SET tank_id = 1 WHERE tank_id IS NULL")
        print(f"  Backfilled {cur.rowcount} row(s) in {table} to tank_id=1")

    # Tank 2 (Akwarium Salon) has no feeding schedule yet - seed one at the
    # same time as tank 1's, editable later.
    cur.execute("SELECT COUNT(*) FROM feeding_schedule WHERE tank_id = 2")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO feeding_schedule (tank_id, time_of_day, active) VALUES (2, '19:00', 1)"
        )
        print("  Seeded tank_id=2 feeding_schedule at 19:00")

    conn.commit()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
