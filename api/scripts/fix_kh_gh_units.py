#!/usr/bin/env python3
"""One-off: rename kh/gh units from 'ppm' to '°dKH'/'°dGH' on the live DB,
convert their min/max thresholds from ppm to the degree scale (1 °dKH/°dGH
= 17.848 ppm CaCO3), and recompute out_of_range on any already-logged
kh/gh readings so their status reflects the corrected range.

Run via:
    docker exec nemo-api python scripts/fix_kh_gh_units.py
"""
import os
import sqlite3

DB_CANDIDATES = ["/app/data/nemo.db", "./data/nemo.db", "../data/nemo.db"]
PPM_PER_DEGREE = 17.848

NEW_RANGES = {
    "kh": (2.2, 6.7),
    "gh": (7.0, 14.0),
}


def find_db() -> str:
    for path in DB_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"nemo.db not found. Searched: {DB_CANDIDATES}")


def main() -> None:
    db_path = find_db()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for key, unit in (("kh", "°dKH"), ("gh", "°dGH")):
        min_safe, max_safe = NEW_RANGES[key]
        cur.execute(
            "UPDATE water_test_parameters SET unit = ?, min_safe = ?, max_safe = ? WHERE key = ?",
            (unit, min_safe, max_safe, key),
        )
        cur.execute("SELECT id FROM water_test_parameters WHERE key = ?", (key,))
        param_id = cur.fetchone()[0]

        cur.execute("SELECT id, value FROM water_test_readings WHERE parameter_id = ?", (param_id,))
        rows = cur.fetchall()
        for reading_id, value in rows:
            oor = value < min_safe or value > max_safe
            cur.execute("UPDATE water_test_readings SET out_of_range = ? WHERE id = ?", (int(oor), reading_id))
        print(f"  {key}: unit={unit} range={min_safe}-{max_safe}, recomputed {len(rows)} reading(s)")

    conn.commit()
    print(list(cur.execute("SELECT key, unit, min_safe, max_safe FROM water_test_parameters WHERE key IN ('kh', 'gh')")))
    conn.close()


if __name__ == "__main__":
    main()

