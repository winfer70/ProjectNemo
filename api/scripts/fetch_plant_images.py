#!/usr/bin/env python3
"""
fetch_plant_images.py — Fetch Wikipedia thumbnail images for plants missing an img URL.

Run via:
    docker exec nemo-api python scripts/fetch_plant_images.py

Queries Wikipedia API by latin name. Falls back to genus+species then genus-only
if the full name (including variety/cultivar) returns no image. Adds a short delay
between requests to avoid rate limiting. Updates img for all rows where img IS NULL.
"""
import sqlite3
import urllib.request
import urllib.parse
import json
import time

DB_PATH = "/app/data/nemo.db"
WIKI_API = "https://en.wikipedia.org/w/api.php"
THUMB_SIZE = 400
DELAY_S = 0.8


def _query_wiki(title: str) -> str | None:
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
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
        print(f"    warn: '{title}': {exc}")
    return None


def fetch_wikipedia_image(latin: str) -> str | None:
    """Try full latin, then genus+species, then genus only."""
    parts = latin.strip().split()

    candidates = [latin]
    if len(parts) >= 2:
        genus_species = f"{parts[0]} {parts[1]}"
        if genus_species != latin:
            candidates.append(genus_species)
    if len(parts) >= 1 and parts[0] not in ("cf.", "sp."):
        genus = parts[0]
        if genus not in candidates:
            candidates.append(genus)

    for title in candidates:
        time.sleep(DELAY_S)
        img = _query_wiki(title)
        if img:
            return img
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
            conn.commit()
            print(f"OK — {img_url[:80]}...")
            updated += 1
        else:
            print("no image found")

    conn.close()
    print(f"\nDone. Updated {updated}/{len(rows)} plants.")


if __name__ == "__main__":
    main()

