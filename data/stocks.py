"""
Nordic Stock Universe — Oslo Børs, Nasdaq Stockholm, Nasdaq Copenhagen, Nasdaq Helsinki.
Each entry: ticker (yfinance format), company name, sector.

Supports multi-market switching via MARKET_CONFIG.
"""

# ────────────────────────────────────────────────────────────
# Market configurations
# ────────────────────────────────────────────────────────────

MARKET_CONFIG = {
    "NO": {
        "name": "Oslo Børs",
        "short_name": "OsloBørsen",
        "suffix": ".OL",
        "currency": "NOK",
        "flag": "\U0001F1F3\U0001F1F4",
        "timezone": "Europe/Oslo",
        "open_hour": 9, "open_min": 0,
        "close_hour": 16, "close_min": 30,
    },
    "SE": {
        "name": "Nasdaq Stockholm",
        "short_name": "Stockholmsbörsen",
        "suffix": ".ST",
        "currency": "SEK",
        "flag": "\U0001F1F8\U0001F1EA",
        "timezone": "Europe/Stockholm",
        "open_hour": 9, "open_min": 0,
        "close_hour": 17, "close_min": 30,
    },
    "DK": {
        "name": "Nasdaq Copenhagen",
        "short_name": "K\u00f8benhavnsb\u00f8rsen",
        "suffix": ".CO",
        "currency": "DKK",
        "flag": "\U0001F1E9\U0001F1F0",
        "timezone": "Europe/Copenhagen",
        "open_hour": 9, "open_min": 0,
        "close_hour": 17, "close_min": 0,
    },
    "FI": {
        "name": "Nasdaq Helsinki",
        "short_name": "Helsinkib\u00f6rsen",
        "suffix": ".HE",
        "currency": "EUR",
        "flag": "\U0001F1EB\U0001F1EE",
        "timezone": "Europe/Helsinki",
        "open_hour": 10, "open_min": 0,
        "close_hour": 18, "close_min": 30,
    },
}

# ────────────────────────────────────────────────────────────
# Norway — Oslo Børs (.OL)
# ────────────────────────────────────────────────────────────

OSLO_STOCKS = [
    # Energy
    {"ticker": "EQNR.OL",   "name": "Equinor",                    "sector": "Energy"},
    {"ticker": "AKERBP.OL", "name": "Aker BP",                    "sector": "Energy"},
    {"ticker": "VAR.OL",    "name": "Var Energi",                 "sector": "Energy"},
    {"ticker": "OKEA.OL",   "name": "OKEA",                       "sector": "Energy"},
    {"ticker": "TGS.OL",    "name": "TGS",                        "sector": "Energy"},
    {"ticker": "PGS.OL",    "name": "PGS",                        "sector": "Energy"},
    {"ticker": "BORR.OL",   "name": "Borr Drilling",              "sector": "Energy"},
    {"ticker": "FLNG.OL",   "name": "Flex LNG",                   "sector": "Energy"},
    {"ticker": "RECSI.OL",  "name": "REC Silicon",                "sector": "Energy"},

    # Financials
    {"ticker": "DNB.OL",    "name": "DNB Bank",                   "sector": "Financials"},
    {"ticker": "GJF.OL",    "name": "Gjensidige Forsikring",      "sector": "Financials"},
    {"ticker": "SRBANK.OL", "name": "SpareBank 1 SR-Bank",        "sector": "Financials"},
    {"ticker": "MING.OL",   "name": "SpareBank 1 SMN",            "sector": "Financials"},
    {"ticker": "NONG.OL",   "name": "SpareBank 1 Nord-Norge",     "sector": "Financials"},

    # Materials
    {"ticker": "NHY.OL",    "name": "Norsk Hydro",                "sector": "Materials"},
    {"ticker": "YAR.OL",    "name": "Yara International",         "sector": "Materials"},

    # Industrials
    {"ticker": "AKER.OL",   "name": "Aker ASA",                   "sector": "Industrials"},
    {"ticker": "SUBC.OL",   "name": "Subsea 7",                   "sector": "Industrials"},
    {"ticker": "AKSO.OL",   "name": "Aker Solutions",             "sector": "Industrials"},
    {"ticker": "FRO.OL",    "name": "Frontline",                  "sector": "Industrials"},
    {"ticker": "GOGL.OL",   "name": "Golden Ocean Group",         "sector": "Industrials"},
    {"ticker": "MPCC.OL",   "name": "MPC Container Ships",        "sector": "Industrials"},
    {"ticker": "WAWI.OL",   "name": "Wallenius Wilhelmsen",       "sector": "Industrials"},
    {"ticker": "BELCO.OL",  "name": "Belships",                   "sector": "Industrials"},
    {"ticker": "HAUTO.OL",  "name": "Höegh Autoliners",           "sector": "Industrials"},
    {"ticker": "2020.OL",   "name": "2020 Bulkers",               "sector": "Industrials"},

    # Consumer Staples / Food & Seafood
    {"ticker": "MOWI.OL",   "name": "Mowi",                       "sector": "Consumer Staples"},
    {"ticker": "SALM.OL",   "name": "SalMar",                     "sector": "Consumer Staples"},
    {"ticker": "LSG.OL",    "name": "Lerøy Seafood Group",        "sector": "Consumer Staples"},
    {"ticker": "ORK.OL",    "name": "Orkla",                      "sector": "Consumer Staples"},
    {"ticker": "AUSS.OL",   "name": "Austevoll Seafood",          "sector": "Consumer Staples"},

    # Communication Services
    {"ticker": "TEL.OL",    "name": "Telenor",                    "sector": "Communication Services"},

    # Real Estate
    {"ticker": "ENTRA.OL",  "name": "Entra",                      "sector": "Real Estate"},
    {"ticker": "OLT.OL",    "name": "Olav Thon Eiendomsselskap",  "sector": "Real Estate"},

    # Technology
    {"ticker": "NOD.OL",    "name": "Nordic Semiconductor",       "sector": "Technology"},
    {"ticker": "ATEA.OL",   "name": "Atea",                       "sector": "Technology"},
    {"ticker": "BOUVET.OL", "name": "Bouvet",                     "sector": "Technology"},
]

# ────────────────────────────────────────────────────────────
# Sweden — Nasdaq Stockholm (.ST)
# ────────────────────────────────────────────────────────────

STOCKHOLM_STOCKS = [
    # Financials
    {"ticker": "SEB-A.ST",    "name": "SEB",                       "sector": "Financials"},
    {"ticker": "SWED-A.ST",   "name": "Swedbank",                  "sector": "Financials"},
    {"ticker": "SHB-A.ST",    "name": "Handelsbanken",             "sector": "Financials"},
    {"ticker": "INVE-B.ST",   "name": "Investor AB",               "sector": "Financials"},

    # Industrials
    {"ticker": "VOLV-B.ST",   "name": "Volvo",                     "sector": "Industrials"},
    {"ticker": "SAND.ST",     "name": "Sandvik",                   "sector": "Industrials"},
    {"ticker": "ATCO-A.ST",   "name": "Atlas Copco",               "sector": "Industrials"},
    {"ticker": "ABB.ST",      "name": "ABB",                       "sector": "Industrials"},
    {"ticker": "ALFA.ST",     "name": "Alfa Laval",                "sector": "Industrials"},
    {"ticker": "SKF-B.ST",    "name": "SKF",                       "sector": "Industrials"},

    # Technology / Telecom
    {"ticker": "ERIC-B.ST",   "name": "Ericsson",                  "sector": "Technology"},
    {"ticker": "HEXA-B.ST",   "name": "Hexagon",                   "sector": "Technology"},
    {"ticker": "TELIA.ST",    "name": "Telia Company",             "sector": "Communication Services"},

    # Consumer
    {"ticker": "HM-B.ST",     "name": "H&M",                       "sector": "Consumer Discretionary"},
    {"ticker": "ESSITY-B.ST", "name": "Essity",                    "sector": "Consumer Staples"},

    # Materials
    {"ticker": "BOL.ST",      "name": "Boliden",                   "sector": "Materials"},

    # Healthcare
    {"ticker": "GETI-B.ST",   "name": "Getinge",                   "sector": "Healthcare"},

    # Real Estate
    {"ticker": "SAGA-B.ST",   "name": "Sagax",                     "sector": "Real Estate"},
]

# ────────────────────────────────────────────────────────────
# Denmark — Nasdaq Copenhagen (.CO)
# ────────────────────────────────────────────────────────────

COPENHAGEN_STOCKS = [
    # Healthcare / Pharma
    {"ticker": "NOVO-B.CO",   "name": "Novo Nordisk",              "sector": "Healthcare"},
    {"ticker": "COLO-B.CO",   "name": "Coloplast",                 "sector": "Healthcare"},
    {"ticker": "GN.CO",       "name": "GN Store Nord",             "sector": "Healthcare"},
    {"ticker": "DEMANT.CO",   "name": "Demant",                    "sector": "Healthcare"},

    # Consumer
    {"ticker": "CARL-B.CO",   "name": "Carlsberg",                 "sector": "Consumer Staples"},
    {"ticker": "PNDORA.CO",   "name": "Pandora",                   "sector": "Consumer Discretionary"},

    # Financials
    {"ticker": "DANSKE.CO",   "name": "Danske Bank",               "sector": "Financials"},
    {"ticker": "TRYG.CO",     "name": "Tryg",                      "sector": "Financials"},
    {"ticker": "JYSK.CO",     "name": "Jyske Bank",                "sector": "Financials"},

    # Industrials / Shipping
    {"ticker": "MAERSK-B.CO", "name": "A.P. M\u00f8ller-M\u00e6rsk", "sector": "Industrials"},
    {"ticker": "DSV.CO",      "name": "DSV",                       "sector": "Industrials"},
    {"ticker": "VWS.CO",      "name": "Vestas Wind Systems",       "sector": "Industrials"},
    {"ticker": "FLS.CO",      "name": "FLSmidth",                  "sector": "Industrials"},

    # Energy
    {"ticker": "ORSTED.CO",   "name": "\u00d8rsted",               "sector": "Energy"},

    # Technology
    {"ticker": "NETC.CO",     "name": "Netcompany",                "sector": "Technology"},
    {"ticker": "SIM.CO",      "name": "SimCorp",                   "sector": "Technology"},
]

# ────────────────────────────────────────────────────────────
# Finland — Nasdaq Helsinki (.HE)
# ────────────────────────────────────────────────────────────

HELSINKI_STOCKS = [
    # Industrials
    {"ticker": "KNEBV.HE",   "name": "KONE",                      "sector": "Industrials"},
    {"ticker": "WRT1V.HE",   "name": "W\u00e4rtsil\u00e4",       "sector": "Industrials"},
    {"ticker": "METSO.HE",   "name": "Metso",                     "sector": "Industrials"},
    {"ticker": "CGCBV.HE",   "name": "Cargotec",                  "sector": "Industrials"},

    # Financials
    {"ticker": "SAMPO.HE",   "name": "Sampo",                     "sector": "Financials"},
    {"ticker": "NDA-FI.HE",  "name": "Nordea",                    "sector": "Financials"},

    # Technology / Telecom
    {"ticker": "NOKIA.HE",   "name": "Nokia",                     "sector": "Technology"},
    {"ticker": "ELISA.HE",   "name": "Elisa",                     "sector": "Communication Services"},

    # Consumer Staples
    {"ticker": "KESBV.HE",   "name": "Kesko",                     "sector": "Consumer Staples"},

    # Materials / Forest
    {"ticker": "UPM.HE",     "name": "UPM-Kymmene",               "sector": "Materials"},
    {"ticker": "STERV.HE",   "name": "Stora Enso",                "sector": "Materials"},

    # Healthcare
    {"ticker": "ORNBV.HE",   "name": "Orion",                     "sector": "Healthcare"},

    # Energy
    {"ticker": "FORTUM.HE",  "name": "Fortum",                    "sector": "Energy"},
    {"ticker": "NESTE.HE",   "name": "Neste",                     "sector": "Energy"},

    # Real Estate
    {"ticker": "KOJAMO.HE",  "name": "Kojamo",                    "sector": "Real Estate"},
]

# ────────────────────────────────────────────────────────────
# All markets map
# ────────────────────────────────────────────────────────────

MARKET_STOCKS = {
    "NO": OSLO_STOCKS,
    "SE": STOCKHOLM_STOCKS,
    "DK": COPENHAGEN_STOCKS,
    "FI": HELSINKI_STOCKS,
}


def get_stocks_for_market(market: str) -> list[dict]:
    """Return stock list for a given market code."""
    return MARKET_STOCKS.get(market, OSLO_STOCKS)


def get_sectors_for_market(market: str) -> list[str]:
    """Return sorted unique sectors for a market."""
    stocks = get_stocks_for_market(market)
    return sorted(set(s["sector"] for s in stocks))


def get_ticker_map_for_market(market: str) -> dict:
    """Return ticker lookup dict for a market."""
    stocks = get_stocks_for_market(market)
    return {s["ticker"]: s for s in stocks}


# Default (backwards-compatible) — Oslo
SECTORS = sorted(set(s["sector"] for s in OSLO_STOCKS))
TICKER_MAP = {s["ticker"]: s for s in OSLO_STOCKS}

# Build a global ticker map across ALL markets for stock detail pages
ALL_TICKER_MAP = {}
for _market_stocks in MARKET_STOCKS.values():
    for _s in _market_stocks:
        ALL_TICKER_MAP[_s["ticker"]] = _s
