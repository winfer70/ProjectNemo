#!/usr/bin/env python3
"""
fetch_plant_images.py — Fetch Wikipedia thumbnail images for plants missing an img URL.

Run via:
    docker exec nemo-api python scripts/fetch_plant_images.py

Queries Wikipedia API by plant latin name. Updates img field for all rows where
img IS NULL or empty. Skips plants that already have an image.
"""
import sqlite3
import urllib.request
import urllib.parse
import json
import sys

DB_PATH = "/app/data/nemo.db"
WIKI_API = "https://en.wikipedia.org/w/api.php"
THUMB_SIZE = 400


def fetch_wikipedia_image(latin: str) -> str | None:
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": latin,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": THUMB_SIZE,
        "pilicense": "any",
    })
    url = f"{WIKI_API}?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ProjectNemo/1.0 aquarium-app"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                return thumb
    except Exception as exc:
        print(f"  WARNING: request failed for '{latin}': {exc}")
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    rows = c.execute(
        "SELECT id, name_en, latin FROM plants WHERE img IS NULL OR img = ''"
    ).fetchall()

    if not rows:
        print("All plants already have images. Nothing to do.")
        conn.close()
        return

    print(f"Fetching images for {len(rows)} plant(s)...\n")
    updated = 0
    for plant_id, name_en, latin in rows:
        if not latin:
            print(f"  SKIP id={plant_id} ({name_en}): no latin name")
            continue
        print(f"  [{plant_id}] {name_en} ({latin}) ... ", end="", flush=True)
        img_url = fetch_wikipedia_image(latin)
        if img_url:
            c.execute("UPDATE plants SET img = ? WHERE id = ?", (img_url, plant_id))
            print(f"OK — {img_url[:80]}...")
            updated += 1
        else:
            print("no image found")

    conn.commit()
    conn.close()
    print(f"\nDone. Updated {updated}/{len(rows)} plants.")


if __name__ == "__main__":
    main()
