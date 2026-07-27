"""Curated dataset of the world's principal space agencies.

Kept as plain Python (not the database) so the dashboard works identically on
every deployment after a simple `git pull` — no migration, no fixtures, and no
dependency on the server's outbound network access.

Budgets are approximate annual figures in **millions of USD**, compiled from
public government and agency sources; several (notably CNSA) are best-available
estimates. Treat them as indicative, not audited.
"""

WORLD_AGENCIES = [
    # acronym, full name, country, region, annual budget (USD millions), founded
    {"acr": "NASA",       "name": "National Aeronautics and Space Administration", "country": "United States",         "region": "North America", "budget": 24875, "founded": 1958},
    {"acr": "CNSA",       "name": "China National Space Administration",           "country": "China",                 "region": "Asia",          "budget": 11000, "founded": 1993},
    {"acr": "ESA",        "name": "European Space Agency",                         "country": "Europe (multinational)","region": "Europe",        "budget": 8300,  "founded": 1975},
    {"acr": "Roscosmos",  "name": "Roscosmos State Corporation",                   "country": "Russia",                "region": "Eurasia",       "budget": 3400,  "founded": 1992},
    {"acr": "CNES",       "name": "National Centre for Space Studies",             "country": "France",                "region": "Europe",        "budget": 3200,  "founded": 1961},
    {"acr": "DLR",        "name": "German Aerospace Center",                       "country": "Germany",               "region": "Europe",        "budget": 2500,  "founded": 1969},
    {"acr": "JAXA",       "name": "Japan Aerospace Exploration Agency",            "country": "Japan",                 "region": "Asia",          "budget": 2100,  "founded": 2003},
    {"acr": "ASI",        "name": "Italian Space Agency",                          "country": "Italy",                 "region": "Europe",        "budget": 2100,  "founded": 1988},
    {"acr": "ISRO",       "name": "Indian Space Research Organisation",            "country": "India",                 "region": "Asia",          "budget": 1600,  "founded": 1969},
    {"acr": "KARI",       "name": "Korea Aerospace Research Institute",            "country": "South Korea",           "region": "Asia",          "budget": 720,   "founded": 1989},
    {"acr": "UKSA",       "name": "UK Space Agency",                               "country": "United Kingdom",        "region": "Europe",        "budget": 700,   "founded": 2010},
    {"acr": "CSA",        "name": "Canadian Space Agency",                         "country": "Canada",                "region": "North America", "budget": 430,   "founded": 1990},
    {"acr": "MBRSC",      "name": "Mohammed bin Rashid Space Centre",              "country": "United Arab Emirates",  "region": "Middle East",   "budget": 410,   "founded": 2006},
    {"acr": "ASA",        "name": "Australian Space Agency",                       "country": "Australia",             "region": "Oceania",       "budget": 260,   "founded": 2018},
    {"acr": "Azercosmos", "name": "Space Agency of the Republic of Azerbaijan",    "country": "Azerbaijan",            "region": "Asia",          "budget": 230,   "founded": 2010},
    {"acr": "BRIN",       "name": "National Research and Innovation Agency (ex-LAPAN)", "country": "Indonesia",        "region": "Asia",          "budget": 220,   "founded": 1963},
    {"acr": "PhilSA",     "name": "Philippine Space Agency",                       "country": "Philippines",           "region": "Asia",          "budget": 150,   "founded": 2019},
    {"acr": "ASAL",       "name": "Algerian Space Agency",                         "country": "Algeria",               "region": "Africa",        "budget": 100,   "founded": 2002},
    {"acr": "ISA",        "name": "Israeli Space Agency",                          "country": "Israel",                "region": "Middle East",   "budget": 90,    "founded": 1983},
    {"acr": "SANSA",      "name": "South African National Space Agency",           "country": "South Africa",          "region": "Africa",        "budget": 84,    "founded": 2010},
    {"acr": "SSAU",       "name": "State Space Agency of Ukraine",                 "country": "Ukraine",               "region": "Eurasia",       "budget": 80,    "founded": 1992},
    {"acr": "CONAE",      "name": "National Space Activities Commission",          "country": "Argentina",             "region": "South America", "budget": 64,    "founded": 1991},
    {"acr": "EgSA",       "name": "Egyptian Space Agency",                         "country": "Egypt",                 "region": "Africa",        "budget": 50,    "founded": 2018},
    {"acr": "TUA",        "name": "Turkish Space Agency",                          "country": "Türkiye",               "region": "Middle East",   "budget": 50,    "founded": 2018},
    {"acr": "SUPARCO",    "name": "Space & Upper Atmosphere Research Commission",  "country": "Pakistan",              "region": "Asia",          "budget": 45,    "founded": 1961},
    {"acr": "GGPEN",      "name": "National Space Program Management Office",       "country": "Angola",                "region": "Africa",        "budget": 30,    "founded": 2013},
    {"acr": "AEM",        "name": "Mexican Space Agency",                          "country": "Mexico",                "region": "North America", "budget": 30,    "founded": 2010},
    {"acr": "NSSA",       "name": "National Space Science Agency",                 "country": "Bahrain",               "region": "Middle East",   "budget": 25,    "founded": 2014},
    {"acr": "KSA",        "name": "Kenya Space Agency",                            "country": "Kenya",                 "region": "Africa",        "budget": 20,    "founded": 2017},
    {"acr": "AEB",        "name": "Brazilian Space Agency",                        "country": "Brazil",                "region": "South America", "budget": 17,    "founded": 1994},
    {"acr": "ISA-IR",     "name": "Iranian Space Agency",                          "country": "Iran",                  "region": "Middle East",   "budget": 10,    "founded": 2004},
    {"acr": "ABAE",       "name": "Bolivarian Agency for Space Activities",        "country": "Venezuela",             "region": "South America", "budget": 7,     "founded": 2007},
    {"acr": "ZINGSA",     "name": "Zimbabwe National Geospatial & Space Agency",   "country": "Zimbabwe",              "region": "Africa",        "budget": 7,     "founded": 2018},
    {"acr": "CONIDA",     "name": "National Commission for Aerospace Research",    "country": "Peru",                  "region": "South America", "budget": 2,     "founded": 1974},
]
