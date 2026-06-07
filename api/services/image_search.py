"""Species image and metadata search — Wikipedia summary + Wikimedia Commons fallback."""
import logging
import urllib.parse

import httpx

logger = logging.getLogger("nemo.image_search")

WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
COMMONS_SEARCH = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "ProjectNemo/1.0"}


async def search_species(query: str, species_type: str) -> dict:
    images: list[dict] = []
    scientific_name = query
    common_name = None
    wiki_extract = None
    wiki_url = None

    encoded = urllib.parse.quote(query.replace(" ", "_"))

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Wikipedia REST summary (fast, has thumbnail for well-known species)
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

        # 2. Wikimedia Commons — works for species even when Wikipedia has no thumbnail
        if len(images) < 5:
            try:
                # Search for image files matching the query
                search_resp = await client.get(COMMONS_SEARCH, headers=HEADERS, params={
                    "action": "query", "list": "search", "srsearch": query,
                    "srnamespace": 6, "format": "json", "srlimit": 8,
                })
                if search_resp.status_code == 200:
                    hits = search_resp.json().get("query", {}).get("search", [])
                    titles_param = "|".join(h["title"] for h in hits[:6])
                    if titles_param:
                        info_resp = await client.get(COMMONS_SEARCH, headers=HEADERS, params={
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
                                if url and not any(i["url"] == url for i in images):
                                    images.append({"url": url, "source": "commons", "thumb": thumb})
                                    if len(images) >= 6:
                                        break
            except Exception as exc:
                logger.debug("Wikimedia Commons search failed for %r: %s", query, exc)

    return {
        "query": query,
        "scientific_name": scientific_name,
        "common_name": common_name,
        "wiki_extract": wiki_extract,
        "wiki_url": wiki_url,
        "images": images,
    }
