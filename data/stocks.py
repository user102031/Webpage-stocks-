"""
Norwegian Stock Universe — Oslo Børs tickers.
Each entry: ticker (yfinance format), company name, sector.
"""

OSLO_STOCKS = [
    # Energy
    {"ticker": "EQNR.OL",   "name": "Equinor",                  "sector": "Energy"},
    {"ticker": "AKERBP.OL", "name": "Aker BP",                  "sector": "Energy"},
    {"ticker": "RECSI.OL",  "name": "REC Silicon",              "sector": "Energy"},
    {"ticker": "OKEA.OL",   "name": "OKEA",                     "sector": "Energy"},
    {"ticker": "PNOR.OL",   "name": "Panoro Energy",            "sector": "Energy"},
    {"ticker": "TGS.OL",    "name": "TGS",                      "sector": "Energy"},
    {"ticker": "PGS.OL",    "name": "PGS",                      "sector": "Energy"},
    {"ticker": "SDRL.OL",   "name": "Seadrill",                 "sector": "Energy"},
    {"ticker": "BORR.OL",   "name": "Borr Drilling",            "sector": "Energy"},
    {"ticker": "VAR.OL",    "name": "Var Energi",               "sector": "Energy"},

    # Financials
    {"ticker": "DNB.OL",    "name": "DNB Bank",                 "sector": "Financials"},
    {"ticker": "SCHA.OL",   "name": "Sparebank 1 SR-Bank",      "sector": "Financials"},
    {"ticker": "SRBNK.OL",  "name": "SpareBank 1 SMN",         "sector": "Financials"},
    {"ticker": "MING.OL",   "name": "SpareBank 1 Ringerike",   "sector": "Financials"},
    {"ticker": "SBANKEN.OL","name": "Sbanken",                  "sector": "Financials"},
    {"ticker": "GJFS.OL",   "name": "Gjensidige Forsikring",   "sector": "Financials"},

    # Materials / Industrials
    {"ticker": "NHY.OL",    "name": "Norsk Hydro",              "sector": "Materials"},
    {"ticker": "YAR.OL",    "name": "Yara International",       "sector": "Materials"},
    {"ticker": "AKER.OL",   "name": "Aker ASA",                 "sector": "Industrials"},
    {"ticker": "SUBC.OL",   "name": "Subsea 7",                 "sector": "Industrials"},
    {"ticker": "AKSO.OL",   "name": "Aker Solutions",           "sector": "Industrials"},
    {"ticker": "FRO.OL",    "name": "Frontline",                "sector": "Industrials"},
    {"ticker": "GOGL.OL",   "name": "Golden Ocean Group",       "sector": "Industrials"},
    {"ticker": "MHG.OL",    "name": "Mowi (Marine Harvest)",   "sector": "Consumer Staples"},
    {"ticker": "FLNG.OL",   "name": "Flex LNG",                 "sector": "Energy"},
    {"ticker": "HAVI.OL",   "name": "Havila Shipping",          "sector": "Industrials"},
    {"ticker": "KAHOT.OL",  "name": "Kahoot!",                  "sector": "Technology"},
    {"ticker": "NEXT.OL",   "name": "Next Biometrics",          "sector": "Technology"},

    # Consumer Staples / Food
    {"ticker": "MOWI.OL",   "name": "Mowi",                     "sector": "Consumer Staples"},
    {"ticker": "SALM.OL",   "name": "SalMar",                   "sector": "Consumer Staples"},
    {"ticker": "LSG.OL",    "name": "Lerøy Seafood Group",      "sector": "Consumer Staples"},
    {"ticker": "ORK.OL",    "name": "Orkla",                    "sector": "Consumer Staples"},
    {"ticker": "AUSS.OL",   "name": "Austevoll Seafood",        "sector": "Consumer Staples"},
    {"ticker": "BWO.OL",    "name": "BW Offshore",              "sector": "Energy"},

    # Telecom
    {"ticker": "TEL.OL",    "name": "Telenor",                  "sector": "Communication Services"},

    # Shipping / Transport
    {"ticker": "MPCC.OL",   "name": "MPC Container Ships",      "sector": "Industrials"},
    {"ticker": "2020.OL",   "name": "2020 Bulkers",             "sector": "Industrials"},
    {"ticker": "WAWI.OL",   "name": "Wallenius Wilhelmsen",     "sector": "Industrials"},
    {"ticker": "BELCO.OL",  "name": "Belships",                 "sector": "Industrials"},
    {"ticker": "HAUTO.OL",  "name": "Höegh Autoliners",        "sector": "Industrials"},

    # Real Estate
    {"ticker": "ENTRA.OL",  "name": "Entra",                    "sector": "Real Estate"},
    {"ticker": "OLT.OL",    "name": "Olav Thon Eiendomsselskap","sector": "Real Estate"},

    # Healthcare
    {"ticker": "NONG.OL",   "name": "Nordic Semiconductor",     "sector": "Technology"},
    {"ticker": "OTEC.OL",   "name": "Ocean Techno Group",       "sector": "Technology"},

    # Technology
    {"ticker": "ATEA.OL",   "name": "Atea",                     "sector": "Technology"},
    {"ticker": "BOUVET.OL", "name": "Bouvet",                   "sector": "Technology"},
    {"ticker": "OPERA.OL",  "name": "Opera",                    "sector": "Technology"},
    {"ticker": "NO10.OL",   "name": "Nordic Semiconductor",     "sector": "Technology"},
]

# Unique sectors for filter dropdowns
SECTORS = sorted(set(s["sector"] for s in OSLO_STOCKS))

# Build lookup by ticker
TICKER_MAP = {s["ticker"]: s for s in OSLO_STOCKS}
