"""
Norwegian Stock Universe — Oslo Børs tickers.
Each entry: ticker (yfinance format), company name, sector.

Corrections vs. original:
- GJF.OL    (was GJFS.OL  — Gjensidige)
- SRBANK.OL (was SCHA.OL  — SpareBank 1 SR-Bank)
- NONG.OL renamed to SpareBank 1 Nord-Norge (NONG = Nord-Norge)
- NOD.OL added for Nordic Semiconductor (correct Oslo Børs ticker)
- MING.OL relabelled as SpareBank 1 SMN (correct mapping)
- Removed: SRBNK.OL (invalid), SBANKEN.OL (delisted 2022),
           MHG.OL (old Mowi/Marine Harvest ticker, redundant),
           KAHOT.OL (Kahoot! taken private 2023),
           NO10.OL (not a valid ticker)
"""

OSLO_STOCKS = [
    # Energy
    {"ticker": "EQNR.OL",   "name": "Equinor",                    "sector": "Energy"},
    {"ticker": "AKERBP.OL", "name": "Aker BP",                    "sector": "Energy"},
    {"ticker": "VAR.OL",    "name": "Var Energi",                 "sector": "Energy"},
    {"ticker": "OKEA.OL",   "name": "OKEA",                       "sector": "Energy"},
    {"ticker": "PNOR.OL",   "name": "Panoro Energy",              "sector": "Energy"},
    {"ticker": "TGS.OL",    "name": "TGS",                        "sector": "Energy"},
    {"ticker": "PGS.OL",    "name": "PGS",                        "sector": "Energy"},
    {"ticker": "SDRL.OL",   "name": "Seadrill",                   "sector": "Energy"},
    {"ticker": "BORR.OL",   "name": "Borr Drilling",              "sector": "Energy"},
    {"ticker": "BWO.OL",    "name": "BW Offshore",                "sector": "Energy"},
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
    {"ticker": "HAVI.OL",   "name": "Havila Shipping",            "sector": "Industrials"},

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
    {"ticker": "OTEC.OL",   "name": "Ocean GeoLoop",              "sector": "Technology"},
    {"ticker": "NEXT.OL",   "name": "Next Biometrics",            "sector": "Technology"},
]

# Unique sectors for filter dropdowns
SECTORS = sorted(set(s["sector"] for s in OSLO_STOCKS))

# Build lookup by ticker
TICKER_MAP = {s["ticker"]: s for s in OSLO_STOCKS}
