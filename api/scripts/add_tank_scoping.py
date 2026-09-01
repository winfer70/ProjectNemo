#!/usr/bin/env python3
"""
add_tank_scoping.py — One-time migration script for ProjectNemo.

Run via:
    docker exec nemo-api python scripts/add_tank_scoping.py

What this script does:
  1. Adds a `tank_id` column to fish, plants, dosing_tasks, water_test_sessions,
     maintenance_tasks (nullable, SQLite ALTER TABLE ADD COLUMN).
  2. Backfills tank_id=1 on every existing row in those tables - all data
     predates the second aquarium, so it all belongs to tank 1 (Akwarium).
  3. Creates the plant_health_events table (normally SQLAlchemy's
     create_all() on startup would do this for a brand-new table, but this
     script creates it explicitly so a single migration run covers
     everything in one step).

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

TANK_SCOPED_TABLES = ["fish", "plants", "dosing_tasks", "water_test_sessions", "maintenance_tasks"]

PLANT_HEALTH_EVENTS_DDL = """
CREATE TABLE IF NOT EXISTS plant_health_events (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id),
    tank_id INTEGER,
    deficiency_key VARCHAR(30) NOT NULL,
    source VARCHAR(20) NOT NULL DEFAULT 'manual',
    confidence FLOAT,
    photo_hash VARCHAR(64),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    notes TEXT,
    corrected_deficiency_key VARCHAR(30),
    correction_notes TEXT,
    treatment_notes TEXT,
    detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    treated_at DATETIME
)
"""


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

    cur.execute(PLANT_HEALTH_EVENTS_DDL)
    print("  plant_health_events table ready")

    conn.commit()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
