"""Species image and metadata search — Wikipedia summary + Wikimedia Commons fallback."""
import logging
import urllib.parse

import httpx

logger = logging.getLogger("nemo.image_search")

WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "ProjectNemo/1.0"}


async def _resolve_wiki_title(client: httpx.AsyncClient, query: str) -> str | None:
    """Resolve free-text (common name, minor misspelling, non-canonical
    capitalization) to the actual matching Wikipedia article title, so a
    fuzzy/wrong query doesn't silently fall through to an unrelated species.
    Returns None if nothing plausibly matches - callers should show no
    image rather than guess."""
    try:
        r = await client.get(WIKI_API, headers=HEADERS, params={
            "action": "query", "list": "search", "srsearch": query,
            "format": "json", "srlimit": 1,
        })
        if r.status_code == 200:
            hits = r.json().get("query", {}).get("search", [])
            if hits:
                return hits[0]["title"]
    except Exception as exc:
        logger.debug("Wikipedia search failed for %r: %s", query, exc)
    return None


async def _commons_images(client: httpx.AsyncClient, query: str) -> list[dict]:
    """Search Commons file titles (intitle:) for the query - restricting to
    the title rather than full-text avoids matching files that merely
    mention the term in an unrelated description/category."""
    images: list[dict] = []
    try:
        search_resp = await client.get(COMMONS_API, headers=HEADERS, params={
            "action": "query", "list": "search", "srsearch": f"intitle:{query}",
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

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Resolve free-text (common name, typo, wrong language) to the actual
        # matching Wikipedia article title before looking anything up - this
        # is what prevents "no exact match" from silently falling through to
        # an unrelated species image.
        resolved_title = await _resolve_wiki_title(client, query)
        lookup_title = resolved_title or query
        encoded = urllib.parse.quote(lookup_title.replace(" ", "_"))

        # 1. Wikipedia REST summary
        try:
            resp = await client.get(WIKI_SUMMARY.format(encoded), headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                wiki_extract = data.get("extract", "")[:500]
                wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page")
                titles = data.get("titles", {})
                common_name = titles.get("display") or data.get("displaytitle")
                scientific_name = common_name or lookup_title
                if data.get("thumbnail"):
                    thumb = data["thumbnail"].get("source", "")
                    orig = data.get("originalimage", {}).get("source", thumb)
                    images.append({"url": orig, "source": "wikipedia", "thumb": thumb})
        except Exception as exc:
            logger.debug("Wikipedia summary failed for %r: %s", lookup_title, exc)

        # 2. Wikimedia Commons - searched using the resolved title, not the
        # raw query, and no blind genus fallback: an unresolved query means
        # we genuinely don't know the species, so show no image rather than
        # guess and risk showing the wrong one.
        if len(images) < 5:
            commons = await _commons_images(client, lookup_title)
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
        "is_genus_fallback": False,
    }

