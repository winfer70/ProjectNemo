#!/usr/bin/env python3
"""One-off: rename kh/gh units from 'ppm' to '°dKH'/'°dGH' on the live DB.

Run via:
    docker exec nemo-api python scripts/fix_kh_gh_units.py
"""
import os
import sqlite3

DB_CANDIDATES = ["/app/data/nemo.db", "./data/nemo.db", "../data/nemo.db"]


def find_db() -> str:
    for path in DB_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"nemo.db not found. Searched: {DB_CANDIDATES}")


def main() -> None:
    db_path = find_db()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE water_test_parameters SET unit = ? WHERE key = 'kh'", ("°dKH",))
    cur.execute("UPDATE water_test_parameters SET unit = ? WHERE key = 'gh'", ("°dGH",))
    conn.commit()
    print(list(cur.execute("SELECT key, unit FROM water_test_parameters WHERE key IN ('kh', 'gh')")))
    conn.close()


if __name__ == "__main__":
    main()
