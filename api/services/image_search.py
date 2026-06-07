"""Species image and metadata search — Wikipedia summary + Wikimedia Commons fallback."""
import logging
import urllib.parse

import httpx

logger = logging.getLogger("nemo.image_search")

WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "ProjectNemo/1.0"}


async def _commons_images(client: httpx.AsyncClient, query: str) -> list[dict]:
    images: list[dict] = []
    try:
        search_resp = await client.get(COMMONS_API, headers=HEADERS, params={
            "action": "query", "list": "search", "srsearch": query,
            "srnamespace": 6, "format": "json", "srlimit": 8,
        })
        if search_resp.status_code != 200:
            return images
        hits = search_resp.json().get("query", {}).get("search", [])
        titles_param = "|".join(h["title"] for h in hits[:6])
        if not titles_param:
            return images
        info_resp = await client.get(COMMONS_API, headers=HEADERS, params={
            "action": "query", "titles": titles_param,
            "prop": "imageinfo", "iiprop": "url|thumburl",
            "iiurlwidth": 400, "format": "json",
        })
        if info_resp.status_code == 200:
            pages = info_resp.json().get("query", {}).get("pages", {})
            for page in pages.values():
                info = (page.get("imageinfo") or [{}])[0]
                url = info.get("url", "")
                thumb = info.get("thumburl") or url
                if url:
                    images.append({"url": url, "source": "commons", "thumb": thumb})
    except Exception as exc:
        logger.debug("Wikimedia Commons search failed for %r: %s", query, exc)
    return images


async def search_species(query: str, species_type: str) -> dict:
    images: list[dict] = []
    scientific_name = query
    common_name = None
    wiki_extract = None
    wiki_url = None

    encoded = urllib.parse.quote(query.replace(" ", "_"))

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Wikipedia REST summary
        try:
            resp = await client.get(WIKI_SUMMARY.format(encoded), headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                wiki_extract = data.get("extract", "")[:500]
                wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page")
                titles = data.get("titles", {})
                common_name = titles.get("display") or data.get("displaytitle")
                if data.get("thumbnail"):
                    thumb = data["thumbnail"].get("source", "")
                    orig = data.get("originalimage", {}).get("source", thumb)
                    images.append({"url": orig, "source": "wikipedia", "thumb": thumb})
        except Exception as exc:
            logger.debug("Wikipedia summary failed for %r: %s", query, exc)

        # 2. Wikimedia Commons — try exact species name, then genus fallback
        is_genus_fallback = False
        if len(images) < 5:
            commons = await _commons_images(client, query)
            # If exact species returns nothing, try genus (first word) as fallback
            if not commons:
                parts = query.split()
                if len(parts) >= 2:
                    commons = await _commons_images(client, parts[0])
                    if commons:
                        is_genus_fallback = True
            for img in commons:
                if not any(i["url"] == img["url"] for i in images):
                    images.append(img)
                    if len(images) >= 6:
                        break

    return {
        "query": query,
        "scientific_name": scientific_name,
        "common_name": common_name,
        "wiki_extract": wiki_extract,
        "wiki_url": wiki_url,
        "images": images,
        "is_genus_fallback": is_genus_fallback,
    }
