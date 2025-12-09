import logging
import aiohttp
import urllib.parse

YAHOO_SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"
YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v6/finance/quote"

logger = logging.getLogger("trading_bot")


async def yahoo_search(query: str, limit: int = 20, timeout_s: int = 10):
    """
    Recherche hybride :
    - 1) suggestions Yahoo Finance (NVDA → NVIDIA CORP, etc.)
    - 2) si aucun résultat → fallback sur ticker exact via quote()
    """

    query = query.strip()
    if not query:
        return []

    headers = {
        "User-Agent": "Mozilla/5.0 (TradingBot; +https://example.com)",
        "Accept": "application/json"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # ----------------------------------------
        # 1) SEARCH auto-suggestions
        # ----------------------------------------
        try:
            async with session.get(
                YAHOO_SEARCH_URL,
                params={"q": query, "quotesCount": limit, "newsCount": 0},
                timeout=timeout_s,
            ) as r:

                if r.status == 200:
                    data = await r.json()
                    raw = data.get("quotes", [])

                    # suggestions trouvées → OK
                    if raw:
                        return [{
                            "symbol": x.get("symbol"),
                            "name": x.get("shortname") or x.get("longname") or "",
                            "exchange": x.get("exchDisp") or "",
                            "type": x.get("quoteType") or "",
                        } for x in raw][:limit]

        except Exception as e:
            logger.warning(f"[Yahoo Suggest Search] Error for {query}: {e}")

        # ----------------------------------------
        # 2) FALLBACK → TICKER EXACT
        # ----------------------------------------
        try:
            symbol = urllib.parse.quote_plus(query.upper())

            async with session.get(
                f"{YAHOO_QUOTE_URL}?symbols={symbol}",
                timeout=timeout_s,
            ) as r:

                if r.status != 200:
                    return []

                data = await r.json()
                raw = data.get("quoteResponse", {}).get("result", [])

                if not raw:
                    return []

                return [{
                    "symbol": x.get("symbol"),
                    "name": x.get("shortName") or x.get("longName") or "",
                    "exchange": x.get("fullExchangeName") or "",
                    "type": x.get("quoteType") or "",
                } for x in raw]

        except Exception as e:
            logger.warning(f"[Yahoo Exact Fallback] Error for {query}: {e}")

    return []
