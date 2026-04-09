"""
Nordic Stock Analyzer — Flask Application
==========================================
Main entry point. Registers page routes and JSON API endpoints.
Supports multi-market switching (NO, SE, DK, FI).
"""

import logging
from flask import Flask, render_template, jsonify, request, abort

from data import fetcher
from data.stocks import (
    SECTORS, TICKER_MAP, ALL_TICKER_MAP,
    MARKET_CONFIG, get_sectors_for_market,
)

# -- Logging --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# -- App --
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def _get_market() -> str:
    """Read market from query param, default NO."""
    m = request.args.get("market", "NO").upper()
    return m if m in MARKET_CONFIG else "NO"


# ================================================================
# Page routes
# ================================================================

@app.route("/")
def dashboard():
    return render_template("index.html", page="dashboard")


@app.route("/screener")
def screener():
    market = _get_market()
    sectors = get_sectors_for_market(market)
    return render_template("screener.html", page="screener", sectors=sectors)


@app.route("/stock/<ticker>")
def stock_detail(ticker: str):
    ticker = ticker.upper()
    if ticker not in ALL_TICKER_MAP:
        abort(404)
    meta = ALL_TICKER_MAP[ticker]
    return render_template(
        "stock.html",
        page="stock",
        ticker=ticker,
        stock_name=meta["name"],
        sector=meta["sector"],
    )


@app.route("/calendar")
def dividend_calendar():
    return render_template("calendar.html", page="calendar")


@app.route("/watchlist")
def watchlist_page():
    return render_template("watchlist.html", page="watchlist")


# ================================================================
# JSON API endpoints
# ================================================================

@app.route("/api/summary")
def api_summary():
    market = _get_market()
    try:
        data = fetcher.get_market_summary(market)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_summary error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/screener")
def api_screener():
    market = _get_market()
    try:
        stocks = fetcher.get_screener_data(market)

        sector    = request.args.get("sector", "").strip()
        min_yield = request.args.get("min_yield", type=float)
        max_pe    = request.args.get("max_pe",    type=float)
        query     = request.args.get("q",         "").strip().lower()

        filtered = []
        for s in stocks:
            if sector and s.get("sector") != sector:
                continue
            if min_yield is not None and (s.get("dividend_yield") or 0) < min_yield:
                continue
            if max_pe is not None and (s.get("pe_ratio") or 0) > max_pe:
                continue
            if query and query not in s.get("ticker", "").lower() and query not in s.get("name", "").lower():
                continue
            filtered.append(s)

        return jsonify(filtered)
    except Exception as exc:
        logger.error("api_screener error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/quote/<ticker>")
def api_quote(ticker: str):
    ticker = ticker.upper()
    try:
        data = fetcher.get_quote(ticker)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_quote %s error: %s", ticker, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/detail/<ticker>")
def api_detail(ticker: str):
    ticker = ticker.upper()
    try:
        data = fetcher.get_stock_detail(ticker)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_detail %s error: %s", ticker, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/history/<ticker>")
def api_history(ticker: str):
    ticker = ticker.upper()
    period = request.args.get("period", "1Y").upper()
    try:
        data = fetcher.get_price_history(ticker, period)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_history %s error: %s", ticker, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/dividends/<ticker>")
def api_dividends(ticker: str):
    ticker = ticker.upper()
    try:
        data = fetcher.get_dividend_history(ticker)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_dividends %s error: %s", ticker, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/financials/<ticker>")
def api_financials(ticker: str):
    ticker = ticker.upper()
    try:
        data = fetcher.get_financials(ticker)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_financials %s error: %s", ticker, exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/calendar")
def api_calendar():
    market = _get_market()
    try:
        data = fetcher.get_dividend_calendar(market)
        return jsonify(data)
    except Exception as exc:
        logger.error("api_calendar error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/markets")
def api_markets():
    """Return market configuration for the frontend market switcher."""
    return jsonify(MARKET_CONFIG)


# ================================================================
# Error handlers
# ================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ================================================================
# Entry point
# ================================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
