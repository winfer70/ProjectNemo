"""Species image search — Wikipedia REST API first, SearXNG fallback."""
import logging
import urllib.parse

import httpx

from config import settings

logger = logging.getLogger("nemo.image_search")

WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"


async def search_species(query: str, species_type: str) -> dict:
    images: list[dict] = []
    scientific_name = None
    common_name = None
    wiki_extract = None
    wiki_url = None

    encoded = urllib.parse.quote(query.replace(" ", "_"))
    wiki_url_req = WIKI_API.format(encoded)

    async with httpx.AsyncClient(timeout=8.0) as client:
        # 1. Wikipedia summary
        try:
            resp = await client.get(wiki_url_req, headers={"User-Agent": "ProjectNemo/1.0"})
            if resp.status_code == 200:
                data = resp.json()
                wiki_extract = data.get("extract", "")[:500]
                wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page")
                if data.get("thumbnail"):
                    thumb_src = data["thumbnail"].get("source", "")
                    orig_src = data.get("originalimage", {}).get("source", thumb_src)
                    images.append({"url": orig_src, "source": "wikipedia", "thumb": thumb_src})
                titles = data.get("titles", {})
                common_name = titles.get("display") or data.get("displaytitle")
                scientific_name = query
        except Exception as exc:
            logger.debug("Wikipedia lookup failed for %r: %s", query, exc)

        # 2. SearXNG image search
        if settings.searxng_url:
            try:
                search_q = f"{query} aquarium {species_type}"
                params = {"q": search_q, "format": "json", "categories": "images"}
                resp = await client.get(f"{settings.searxng_url}/search", params=params)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    for r in results[:6]:
                        img_src = r.get("img_src") or r.get("thumbnail_src")
                        if img_src and not any(i["url"] == img_src for i in images):
                            images.append({"url": img_src, "source": "searxng", "thumb": r.get("thumbnail_src")})
                            if len(images) >= 6:
                                break
            except Exception as exc:
                logger.debug("SearXNG lookup failed for %r: %s", query, exc)

    return {
        "query": query,
        "scientific_name": scientific_name,
        "common_name": common_name,
        "wiki_extract": wiki_extract,
        "wiki_url": wiki_url,
        "images": images,
    }
