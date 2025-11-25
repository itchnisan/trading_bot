import logging
import aiohttp
import asyncio
import urllib.parse

YAHOO_SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"
YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v6/finance/quote"

logger = logging.getLogger("trading_bot")

async def yahoo_search(query: str, limit: int = 25, timeout_s: int = 10):
    """
    Recherche via Yahoo Finance avec deux étapes :
    1) search endpoint (recherche générale)
    2) fallback sur quote endpoint pour symboles exacts
    Renvoie une liste de dicts: {symbol, shortname, exchange, type}
    """
    query = query.strip()
    if not query:
        return []

    params = {
        "q": query,
        "lang": "en-US",
        "region": "US",
        "quotesCount": limit,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; trading_bot/1.0; +https://example.com)",
        "Accept": "application/json, text/plain, */*"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # 1) try search endpoint
        try:
            async with session.get(YAHOO_SEARCH_URL, params=params, timeout=timeout_s) as r:
                text = await r.text()
                if r.status != 200:
                    logger.warning("Yahoo search returned status=%s for q=%s. Body: %s", r.status, query, text[:1000])
                else:
                    try:
                        data = await r.json()
                        quotes = data.get("quotes", [])
                        results = []
                        for item in quotes:
                            results.append({
                                "symbol": item.get("symbol"),
                                "shortname": item.get("shortname") or item.get("longname") or "",
                                "exchange": item.get("exchDisp") or "",
                                "type": item.get("quoteType") or "",
                            })
                        if results:
                            return results[:limit]
                    except Exception as ex:
                        logger.exception("Failed to parse Yahoo search JSON for q=%s: %s", query, ex)
        except asyncio.TimeoutError:
            logger.warning("Yahoo search timeout for q=%s", query)
        except Exception:
            logger.exception("Yahoo search exception for q=%s", query)

        # 2) fallback: si query semble être un ticker (ou même si non), tenter quote endpoint en majuscule
        try:
            symbols = urllib.parse.quote_plus(query.upper())
            quote_url = f"{YAHOO_QUOTE_URL}?symbols={symbols}"
            async with session.get(quote_url, timeout=timeout_s) as r:
                text = await r.text()
                if r.status == 200:
                    try:
                        data = await r.json()
                        result_map = data.get("quoteResponse", {}).get("result", [])
                        results = []
                        for item in result_map:
                            results.append({
                                "symbol": item.get("symbol"),
                                "shortname": item.get("shortName") or item.get("longName") or "",
                                "exchange": item.get("fullExchangeName") or item.get("exchange") or "",
                                "type": item.get("quoteType") or "",
                            })
                        if results:
                            return results[:limit]
                    except Exception:
                        logger.exception("Failed to parse Yahoo quote JSON for q=%s: %s", query, text[:1000])
                else:
                    logger.warning("Yahoo quote returned status=%s for q=%s. Body: %s", r.status, query, text[:1000])
        except Exception:
            logger.exception("Yahoo quote exception for q=%s", query)

    # nothing found
    return []


