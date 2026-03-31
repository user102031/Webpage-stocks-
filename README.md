# OsloBørsen — Norwegian Stock Analyzer

A professional, Bloomberg-inspired dividend stock screener and analyzer focused on **Oslo Børs** (Norwegian Stock Exchange).

![Dark Mode UI](https://img.shields.io/badge/UI-Dark%20Mode-0f0f1a?style=flat-square&labelColor=1c1c35&color=4f46e5)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

---

## Features

| Feature | Description |
|---|---|
| **Stock Screener** | Full Oslo Børs table with sortable columns, filters (sector, min yield, max P/E), and real-time search |
| **Individual Stock Pages** | Interactive price chart (1W → 5Y), dividend history, revenue/net income/FCF charts, company info |
| **Dividend Calendar** | Timeline of upcoming ex-dividend dates across the Norwegian stock universe |
| **Market Dashboard** | Sentiment indicator, top-5 yield, top-5 value, sector breakdown, live market status |
| **Composite Score** | 0–100 score combining dividend yield + P/E + P/B for quick value-dividend ranking |
| **Watchlist** | Add/remove stocks — persisted in browser `localStorage`, no login required |
| **Tooltips** | Beginner-friendly explanations for every financial metric |
| **Caching** | File + memory cache with per-TTL expiry (5 min quotes, 6 hr financials) to avoid API hammering |

---

## Tech Stack

- **Backend:** Python / Flask
- **Data:** [yfinance](https://github.com/ranaroussi/yfinance) (primary)
- **Frontend:** HTML + [Tailwind CSS](https://tailwindcss.com/) (CDN) + vanilla JavaScript
- **Charts:** [ApexCharts](https://apexcharts.com/) (CDN)
- **Fonts:** Inter + JetBrains Mono (Google Fonts)

---

## Quick Start

### 1. Clone & enter directory

```bash
git clone <repo-url>
cd Webpage-stocks-
```

### 2. Create virtual environment

```bash
python3 -m venv .venv            # Linux / macOS
source .venv/bin/activate        # Linux / macOS

py -m venv .venv              # Windows
.venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### 5. Production (Gunicorn)

```bash
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

---

## Project Structure

```
Webpage-stocks-/
├── app.py                  # Flask app — routes + API endpoints
├── requirements.txt
├── README.md
│
├── data/
│   ├── __init__.py
│   ├── stocks.py           # Oslo Børs ticker universe (~50 stocks)
│   ├── cache.py            # Memory + file cache with TTL
│   └── fetcher.py          # yfinance wrappers + data helpers
│
├── templates/
│   ├── base.html           # Dark-mode base layout (nav, watchlist panel, footer)
│   ├── index.html          # Dashboard / market overview
│   ├── screener.html       # Stock screener with filters + sortable table
│   ├── stock.html          # Individual stock detail page
│   ├── calendar.html       # Dividend calendar (timeline + table)
│   └── 404.html
│
└── static/
    ├── css/
    │   └── custom.css      # Component styles (cards, inputs, skeletons, charts)
    └── js/
        └── main.js         # Watchlist, tooltips, mobile nav, market status
```

---

## API Endpoints

All endpoints return JSON and are consumed by the frontend via `fetch()`.

| Method | Path | Description |
|---|---|---|
| GET | `/api/summary` | Market dashboard data |
| GET | `/api/screener` | All stocks with key metrics. Query params: `sector`, `min_yield`, `max_pe`, `q` |
| GET | `/api/quote/<ticker>` | Single ticker quote |
| GET | `/api/detail/<ticker>` | Full stock detail |
| GET | `/api/history/<ticker>?period=1Y` | Price history. Periods: `1W`, `1M`, `3M`, `1Y`, `5Y` |
| GET | `/api/dividends/<ticker>` | Annual dividend history |
| GET | `/api/financials/<ticker>` | Income statement + cash flow |
| GET | `/api/calendar` | Upcoming ex-dividend dates |

---

## Supported Tickers (Oslo Børs)

Energy: EQNR, AKERBP, VAR, OKEA, TGS, PGS, SDRL, BORR, FLNG, RECSI
Financials: DNB, SCHA, SRBNK, GJFS
Materials: NHY, YAR
Industrials: AKER, SUBC, AKSO, FRO, GOGL, MPCC, WAWI, BELCO, HAUTO
Consumer Staples: MOWI, SALM, LSG, ORK, AUSS
Communication: TEL
Technology: ATEA, BOUVET, KAHOT, OPERA
Real Estate: ENTRA, OLT

> Easily extend by adding entries to `data/stocks.py`.

---

## Configuration & Caching

Cache TTLs are defined in `data/cache.py`:

| Cache Type | TTL |
|---|---|
| Live quotes | 5 minutes |
| Screener results | 10 minutes |
| Price history | 2 hours |
| Financials / dividends | 6 hours |
| Dividend calendar | 1 hour |

Cache is stored in `.cache/` directory (auto-created). Delete this folder to force fresh data.

---

## Expanding to Nordic / European Markets

To add Swedish (STO), Danish (CPH), or Finnish (HEL) stocks:

1. Add tickers to `data/stocks.py` (yfinance format: `TICKER.ST`, `TICKER.CO`, `TICKER.HE`)
2. Add new sectors if needed — they auto-populate in the screener filter

---

## Disclaimer

Data is sourced from Yahoo Finance via yfinance and may be delayed up to 15 minutes. This application is for **informational purposes only** and does not constitute financial advice. Always do your own research before investing.
