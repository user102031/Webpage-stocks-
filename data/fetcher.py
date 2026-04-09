"""
Data fetcher — wraps yfinance calls with caching and graceful error handling.
All public functions return plain Python dicts/lists (JSON-serialisable).

Supports multi-market via `market` parameter (NO, SE, DK, FI).
"""

import logging
import math
import time
from datetime import datetime, timedelta
from typing import Optional

import yfinance as yf

from data import cache
from data.stocks import (
    OSLO_STOCKS, TICKER_MAP, ALL_TICKER_MAP,
    MARKET_CONFIG, get_stocks_for_market, get_ticker_map_for_market,
)

logger = logging.getLogger(__name__)


# ────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────

def _safe(val, default=None):
    """Return val if it is a real number, else default."""
    if val is None:
        return default
    try:
        if math.isnan(float(val)) or math.isinf(float(val)):
            return default
        return val
    except (TypeError, ValueError):
        return default


def _fmt_large(num) -> Optional[str]:
    """Format large numbers as e.g. '12.3B', '450M'."""
    if num is None:
        return None
    try:
        num = float(num)
        if num >= 1e12:
            return f"{num/1e12:.2f}T"
        if num >= 1e9:
            return f"{num/1e9:.2f}B"
        if num >= 1e6:
            return f"{num/1e6:.2f}M"
        if num >= 1e3:
            return f"{num/1e3:.2f}K"
        return f"{num:.2f}"
    except (TypeError, ValueError):
        return None


def _pct(val) -> Optional[float]:
    """Convert a decimal ratio (0.05) to percentage (5.0).
    yfinance is inconsistent: some fields come back already as percentages
    for certain exchange suffixes (.OL, .ST, etc.).  Values whose absolute
    magnitude exceeds 1 are assumed to already be in percentage form.
    """
    v = _safe(val)
    if v is None:
        return None
    if abs(v) > 1:          # e.g. 5.0 -> already 5 %, just round
        return round(float(v), 2)
    return round(float(v) * 100, 2)


def _yield_pct(val) -> Optional[float]:
    """Dividend yield normalised to percentage.
    dividendYield from yfinance can be 0.05 (decimal) OR 5.0 (already %).
    Dividend yields above ~50 % are unrealistic, so anything > 1 is treated
    as already being in percentage form.
    """
    v = _safe(val)
    if v is None:
        return None
    if v > 1:               # e.g. 5.0 -> 5 %
        return round(float(v), 2)
    return round(float(v) * 100, 2)


def _try_fast_info(tk):
    """Attempt to get basic price data from fast_info as a fallback."""
    try:
        fi = tk.fast_info
        if fi is None:
            return {}
        result = {}
        # fast_info attributes vary by yfinance version
        for attr, key in [
            ("last_price", "price"),
            ("previous_close", "prev_close"),
            ("market_cap", "market_cap"),
            ("currency", "currency"),
            ("fifty_day_average", "fifty_day_avg"),
            ("two_hundred_day_average", "two_hundred_day_avg"),
        ]:
            val = getattr(fi, attr, None)
            if val is not None:
                result[key] = val
        return result
    except Exception:
        return {}


# ────────────────────────────────────────────────────────────
# Single ticker quote / info
# ────────────────────────────────────────────────────────────

def get_quote(ticker: str) -> dict:
    """
    Fetch a fast-expiring summary for one ticker.
    Returns a dict with price, change, dividend yield, P/E, etc.
    Falls back to fast_info if full .info fails.
    """
    cache_key = f"quote:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    meta = ALL_TICKER_MAP.get(ticker, TICKER_MAP.get(ticker, {}))
    result = {
        "ticker":         ticker,
        "name":           meta.get("name", ticker),
        "sector":         meta.get("sector", "Unknown"),
        "price":          None,
        "currency":       "NOK",
        "change_pct":     None,
        "dividend_yield": None,
        "pe_ratio":       None,
        "pb_ratio":       None,
        "eps":            None,
        "market_cap":     None,
        "market_cap_fmt": None,
        "week52_high":    None,
        "week52_low":     None,
        "volume":         None,
        "avg_volume":     None,
        "score":          None,
        "error":          None,
    }

    for attempt in range(2):
        try:
            tk   = yf.Ticker(ticker)
            info = tk.info or {}

            # If the dict has no useful data, try fast_info fallback
            if not info.get("regularMarketPrice") and not info.get("currentPrice"):
                fi = _try_fast_info(tk)
                if fi.get("price"):
                    result["price"]      = _safe(fi["price"])
                    result["currency"]   = fi.get("currency", "NOK")
                    result["market_cap"] = _safe(fi.get("market_cap"))
                    result["market_cap_fmt"] = _fmt_large(result["market_cap"])
                    # Still try to get more from info if available
                    result["dividend_yield"] = _yield_pct(info.get("dividendYield"))
                    result["pe_ratio"]       = _safe(info.get("trailingPE") or info.get("forwardPE"))
                    result["pb_ratio"]       = _safe(info.get("priceToBook"))
                    result["eps"]            = _safe(info.get("trailingEps"))
                    result["week52_high"]    = _safe(info.get("fiftyTwoWeekHigh"))
                    result["week52_low"]     = _safe(info.get("fiftyTwoWeekLow"))
                    result["volume"]         = _safe(info.get("volume"))
                    result["avg_volume"]     = _safe(info.get("averageVolume"))
                    result["score"]          = _compute_score(result)
                    break
                elif attempt == 0:
                    time.sleep(1.0)
                    continue

            result["price"]          = _safe(info.get("currentPrice") or info.get("regularMarketPrice"))
            result["currency"]       = info.get("currency", "NOK")
            result["change_pct"]     = _safe(info.get("regularMarketChangePercent"))
            result["dividend_yield"] = _yield_pct(info.get("dividendYield"))
            result["pe_ratio"]       = _safe(info.get("trailingPE") or info.get("forwardPE"))
            result["pb_ratio"]       = _safe(info.get("priceToBook"))
            result["eps"]            = _safe(info.get("trailingEps"))
            result["market_cap"]     = _safe(info.get("marketCap"))
            result["market_cap_fmt"] = _fmt_large(result["market_cap"])
            result["week52_high"]    = _safe(info.get("fiftyTwoWeekHigh"))
            result["week52_low"]     = _safe(info.get("fiftyTwoWeekLow"))
            result["volume"]         = _safe(info.get("volume"))
            result["avg_volume"]     = _safe(info.get("averageVolume"))
            result["score"]          = _compute_score(result)
            break  # success

        except Exception as exc:
            if attempt == 0:
                logger.info("Quote attempt 1 failed for %s, retrying... (%s)", ticker, exc)
                time.sleep(1.5)
            else:
                logger.warning("Quote fetch failed for %s: %s", ticker, exc)
                result["error"] = str(exc)

    cache.set(cache_key, result, ttl=cache.TTL_QUOTE)
    return result


def _compute_score(data: dict) -> Optional[int]:
    """
    Composite score 0-100 weighting dividend yield, P/E, and P/B.
    Higher = more attractive from a value-dividend perspective.
    """
    score = 0
    components = 0

    dy = data.get("dividend_yield")
    if dy is not None:
        score += min(dy / 10 * 40, 40)
        components += 1

    pe = data.get("pe_ratio")
    if pe is not None and pe > 0:
        score += max(0, min(30, (30 - pe) / 20 * 30))
        components += 1

    pb = data.get("pb_ratio")
    if pb is not None and pb > 0:
        score += max(0, min(30, (5 - pb) / 4 * 30))
        components += 1

    if components == 0:
        return None
    return round(score)


# ────────────────────────────────────────────────────────────
# Screener — all stocks (market-aware)
# ────────────────────────────────────────────────────────────

def get_screener_data(market: str = "NO") -> list[dict]:
    """
    Return quotes for every stock in the given market.
    Results are cached as a whole for TTL_SCREENER seconds.
    """
    cache_key = f"screener:{market}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    stocks = get_stocks_for_market(market)
    results = []
    for i, stock in enumerate(stocks):
        ticker = stock["ticker"]
        if i > 0 and i % 5 == 0:
            time.sleep(0.8)
        try:
            q = get_quote(ticker)
            results.append(q)
        except Exception as exc:
            logger.warning("Screener skip %s: %s", ticker, exc)
            results.append({
                "ticker": ticker,
                "name":   stock["name"],
                "sector": stock["sector"],
                "error":  str(exc),
            })

    cache.set(cache_key, results, ttl=cache.TTL_SCREENER)
    return results


# ────────────────────────────────────────────────────────────
# Price history
# ────────────────────────────────────────────────────────────

PERIOD_MAP = {
    "1W": ("7d",  "1h"),
    "1M": ("1mo", "1d"),
    "3M": ("3mo", "1d"),
    "1Y": ("1y",  "1wk"),
    "5Y": ("5y",  "1mo"),
}


def get_price_history(ticker: str, period: str = "1Y") -> dict:
    """
    Return OHLCV history for charting.
    period: one of 1W, 1M, 3M, 1Y, 5Y
    """
    cache_key = f"history:{ticker}:{period}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    yf_period, interval = PERIOD_MAP.get(period, ("1y", "1d"))

    try:
        tk = yf.Ticker(ticker)
        df = tk.history(period=yf_period, interval=interval)

        if df is None or df.empty:
            result = {"ticker": ticker, "period": period, "data": [], "error": "No data"}
        else:
            df = df.reset_index()
            date_col = "Datetime" if "Datetime" in df.columns else "Date"
            result = {
                "ticker": ticker,
                "period": period,
                "data": [
                    {
                        "x": row[date_col].isoformat() if hasattr(row[date_col], "isoformat") else str(row[date_col]),
                        "o": round(float(row["Open"]),  2),
                        "h": round(float(row["High"]),  2),
                        "l": round(float(row["Low"]),   2),
                        "c": round(float(row["Close"]), 2),
                        "v": int(row["Volume"]),
                    }
                    for _, row in df.iterrows()
                ],
                "error": None,
            }
    except Exception as exc:
        logger.warning("History fetch failed for %s %s: %s", ticker, period, exc)
        result = {"ticker": ticker, "period": period, "data": [], "error": str(exc)}

    cache.set(cache_key, result, ttl=cache.TTL_HISTORY)
    return result


# ────────────────────────────────────────────────────────────
# Dividend history
# ────────────────────────────────────────────────────────────

def get_dividend_history(ticker: str) -> dict:
    """Return annual dividend totals for bar chart."""
    cache_key = f"dividends:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        tk = yf.Ticker(ticker)
        divs = tk.dividends

        if divs is None or divs.empty:
            result = {"ticker": ticker, "annual": [], "raw": [], "error": None}
        else:
            divs.index = divs.index.tz_localize(None) if divs.index.tzinfo else divs.index
            annual = (
                divs.groupby(divs.index.year)
                .sum()
                .reset_index()
                .rename(columns={"index": "year", "Dividends": "total"})
            )
            result = {
                "ticker": ticker,
                "annual": [
                    {"year": int(row["year"]), "total": round(float(row["total"]), 4)}
                    for _, row in annual.iterrows()
                ],
                "raw": [
                    {"date": str(idx.date()), "amount": round(float(val), 4)}
                    for idx, val in divs.items()
                ],
                "error": None,
            }
    except Exception as exc:
        logger.warning("Dividend fetch failed for %s: %s", ticker, exc)
        result = {"ticker": ticker, "annual": [], "raw": [], "error": str(exc)}

    cache.set(cache_key, result, ttl=cache.TTL_FINANCIALS)
    return result


# ────────────────────────────────────────────────────────────
# Financials: Income statement + Cash flow
# ────────────────────────────────────────────────────────────

def get_financials(ticker: str) -> dict:
    """Return annual income statement and cash flow data."""
    cache_key = f"financials:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    result = {
        "ticker":   ticker,
        "annual":   [],
        "quarterly": [],
        "error":    None,
    }

    try:
        tk = yf.Ticker(ticker)

        def _parse_stmt(df):
            if df is None or df.empty:
                return []
            rows = []
            for col in df.columns:
                label = col.strftime("%Y") if hasattr(col, "strftime") else str(col)
                revenue     = _safe(df.loc["Total Revenue", col]) if "Total Revenue" in df.index else None
                net_income  = _safe(df.loc["Net Income", col])    if "Net Income"    in df.index else None
                rows.append({
                    "period":       label,
                    "revenue":      revenue,
                    "revenue_fmt":  _fmt_large(revenue),
                    "net_income":   net_income,
                    "ni_fmt":       _fmt_large(net_income),
                })
            return rows

        def _parse_cf(df):
            if df is None or df.empty:
                return {}
            fcf_map = {}
            for col in df.columns:
                label = col.strftime("%Y") if hasattr(col, "strftime") else str(col)
                fcf = None
                if "Free Cash Flow" in df.index:
                    fcf = _safe(df.loc["Free Cash Flow", col])
                elif "Operating Cash Flow" in df.index and "Capital Expenditure" in df.index:
                    op  = _safe(df.loc["Operating Cash Flow", col])
                    cap = _safe(df.loc["Capital Expenditure", col])
                    if op is not None and cap is not None:
                        fcf = op - abs(cap)
                fcf_map[label] = {"fcf": fcf, "fcf_fmt": _fmt_large(fcf)}
            return fcf_map

        ann_inc = _parse_stmt(tk.income_stmt)
        ann_cf  = _parse_cf(tk.cash_flow)

        for row in ann_inc:
            cf_data = ann_cf.get(row["period"], {})
            row.update(cf_data)

        result["annual"] = ann_inc

        # Quarterly
        q_inc = _parse_stmt(tk.quarterly_income_stmt)
        q_cf  = _parse_cf(tk.quarterly_cash_flow)
        for row in q_inc:
            cf_data = q_cf.get(row["period"], {})
            row.update(cf_data)
        result["quarterly"] = q_inc

    except Exception as exc:
        logger.warning("Financials fetch failed for %s: %s", ticker, exc)
        result["error"] = str(exc)

    cache.set(cache_key, result, ttl=cache.TTL_FINANCIALS)
    return result


# ────────────────────────────────────────────────────────────
# Dividend calendar (market-aware)
# ────────────────────────────────────────────────────────────

def get_dividend_calendar(market: str = "NO") -> list[dict]:
    """
    Collect upcoming ex-dividend and payment dates across the market.
    Returns list sorted by ex-date.
    """
    cache_key = f"calendar:{market}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    stocks = get_stocks_for_market(market)
    events = []
    today = datetime.utcnow().date()

    for i, stock in enumerate(stocks):
        ticker = stock["ticker"]
        if i > 0 and i % 5 == 0:
            time.sleep(0.8)
        try:
            tk = yf.Ticker(ticker)
            info = tk.info or {}

            ex_date_ts = info.get("exDividendDate")
            div_rate   = _safe(info.get("dividendRate"))
            div_yield  = _yield_pct(info.get("dividendYield"))

            if ex_date_ts:
                ex_date = datetime.utcfromtimestamp(ex_date_ts).date()
                if ex_date >= today:
                    events.append({
                        "ticker":    ticker,
                        "name":      stock["name"],
                        "sector":    stock["sector"],
                        "ex_date":   str(ex_date),
                        "div_rate":  div_rate,
                        "div_yield": div_yield,
                        "currency":  info.get("currency", MARKET_CONFIG.get(market, {}).get("currency", "NOK")),
                    })
        except Exception as exc:
            logger.debug("Calendar skip %s: %s", ticker, exc)

    events.sort(key=lambda e: e["ex_date"])
    cache.set(cache_key, events, ttl=cache.TTL_CALENDAR)
    return events


# ────────────────────────────────────────────────────────────
# Market summary (dashboard) — market-aware
# ────────────────────────────────────────────────────────────

def get_market_summary(market: str = "NO") -> dict:
    """
    Return top-5 by yield, top-5 by lowest P/E, and a naive sentiment.
    """
    cache_key = f"market:summary:{market}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    all_stocks = get_screener_data(market)
    valid = [s for s in all_stocks if not s.get("error") and s.get("price")]

    by_yield = sorted(
        [s for s in valid if s.get("dividend_yield") is not None],
        key=lambda s: s["dividend_yield"],
        reverse=True,
    )[:5]

    by_pe = sorted(
        [s for s in valid if s.get("pe_ratio") is not None and s["pe_ratio"] > 0],
        key=lambda s: s["pe_ratio"],
    )[:5]

    changes = [s["change_pct"] for s in valid if s.get("change_pct") is not None]
    if changes:
        positive = sum(1 for c in changes if c > 0)
        sentiment_pct = round(positive / len(changes) * 100)
        sentiment = "Bullish" if sentiment_pct >= 55 else ("Bearish" if sentiment_pct <= 45 else "Neutral")
    else:
        sentiment_pct = 50
        sentiment = "Neutral"

    # Find proxy ticker for market chart (largest company)
    mkt_cfg = MARKET_CONFIG.get(market, MARKET_CONFIG["NO"])
    stocks = get_stocks_for_market(market)
    proxy_ticker = stocks[0]["ticker"] if stocks else "EQNR.OL"

    summary = {
        "top_yield":      by_yield,
        "top_value_pe":   by_pe,
        "sentiment":      sentiment,
        "sentiment_pct":  sentiment_pct,
        "total_stocks":   len(valid),
        "advancing":      sum(1 for c in changes if c > 0),
        "declining":      sum(1 for c in changes if c < 0),
        "unchanged":      sum(1 for c in changes if c == 0),
        "proxy_ticker":   proxy_ticker,
        "proxy_name":     stocks[0]["name"] if stocks else "Equinor",
        "market_name":    mkt_cfg["name"],
        "currency":       mkt_cfg["currency"],
    }

    cache.set(cache_key, summary, ttl=cache.TTL_SCREENER)
    return summary


# ────────────────────────────────────────────────────────────
# Single stock detail (combines quote + info)
# ────────────────────────────────────────────────────────────

def get_stock_detail(ticker: str) -> dict:
    """Full detail view for an individual stock page."""
    cache_key = f"detail:{ticker}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    meta  = ALL_TICKER_MAP.get(ticker, TICKER_MAP.get(ticker, {"name": ticker, "sector": "Unknown"}))
    quote = get_quote(ticker)

    try:
        tk   = yf.Ticker(ticker)
        info = tk.info or {}

        detail = {
            **quote,
            "description":     info.get("longBusinessSummary", ""),
            "website":         info.get("website", ""),
            "employees":       info.get("fullTimeEmployees"),
            "industry":        info.get("industry", meta.get("sector")),
            "country":         info.get("country", "Norway"),
            "beta":            _safe(info.get("beta")),
            "payout_ratio":    _pct(info.get("payoutRatio")),
            "current_ratio":   _safe(info.get("currentRatio")),
            "debt_to_equity":  _safe(info.get("debtToEquity")),
            "roe":             _pct(info.get("returnOnEquity")),
            "roa":             _pct(info.get("returnOnAssets")),
            "profit_margin":   _pct(info.get("profitMargins")),
            "gross_margin":    _pct(info.get("grossMargins")),
            "revenue_growth":  _pct(info.get("revenueGrowth")),
            "earnings_growth": _pct(info.get("earningsGrowth")),
            "analyst_target":  _safe(info.get("targetMeanPrice")),
            "recommendation":  info.get("recommendationKey", "").replace("-", " ").title(),
        }

    except Exception as exc:
        logger.warning("Detail fetch failed for %s: %s", ticker, exc)
        detail = {**quote, "error": str(exc)}

    cache.set(cache_key, detail, ttl=cache.TTL_QUOTE)
    return detail
