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


# ---------------------------------------------------------------------------
# Factual space-history milestones. Focus on the rise of developing nations in
# space, anchored by the major global firsts for context. Kept static so the
# timeline is rich and identical on every deployment.
#   kind: 'global'      -> landmark world firsts (teal)
#         'developing'  -> milestones for developing nations (amber)
#         'landmark'    -> especially historic firsts (terracotta)
# ---------------------------------------------------------------------------
TIMELINE_EVENTS = [
    {"year": 1957, "when": "Oct 1957", "kind": "global",     "tag": "USSR",
     "title": "Sputnik 1 opens the Space Age",
     "text": "The Soviet Union launches the first artificial satellite, kicking off the space race and the era of orbital technology."},
    {"year": 1961, "when": "Apr 1961", "kind": "global",     "tag": "USSR",
     "title": "First human in orbit",
     "text": "Yuri Gagarin becomes the first person to orbit the Earth aboard Vostok 1."},
    {"year": 1969, "when": "1969",      "kind": "developing", "tag": "India",
     "title": "ISRO is founded",
     "text": "India establishes the Indian Space Research Organisation, betting that a developing nation can build space technology for development."},
    {"year": 1969, "when": "Jul 1969", "kind": "global",     "tag": "USA",
     "title": "Apollo 11 lands on the Moon",
     "text": "Humans walk on another world for the first time as the United States lands two astronauts on the lunar surface."},
    {"year": 1970, "when": "Apr 1970", "kind": "developing", "tag": "China",
     "title": "China reaches orbit — Dong Fang Hong 1",
     "text": "China becomes the fifth nation to launch its own satellite, broadcasting a patriotic anthem from orbit."},
    {"year": 1975, "when": "Apr 1975", "kind": "developing", "tag": "India",
     "title": "India's first satellite, Aryabhata",
     "text": "Named after the ancient astronomer, Aryabhata is India's first satellite, launched with Soviet help while ISRO built its own rockets."},
    {"year": 1980, "when": "Jul 1980", "kind": "landmark",   "tag": "India",
     "title": "India launches its own rocket to orbit",
     "text": "The SLV-3 places Rohini RS-1 in orbit, making India the sixth nation able to reach space with an indigenous launch vehicle."},
    {"year": 1988, "when": "1988",      "kind": "developing", "tag": "Brazil · China",
     "title": "The China–Brazil satellite partnership (CBERS)",
     "text": "Two developing giants agree to jointly build Earth-observation satellites — a landmark of South–South space cooperation."},
    {"year": 1999, "when": "Oct 1999", "kind": "developing", "tag": "Brazil · China",
     "title": "CBERS-1 reaches orbit",
     "text": "The first China–Brazil Earth Resources Satellite launches, delivering imagery used across agriculture and the environment."},
    {"year": 2008, "when": "Oct 2008", "kind": "landmark",   "tag": "India",
     "title": "Chandrayaan-1 discovers water on the Moon",
     "text": "India's first lunar probe finds evidence of water molecules on the Moon — a major scientific result on a modest budget."},
    {"year": 2009, "when": "Feb 2009", "kind": "developing", "tag": "Iran",
     "title": "Iran launches its own satellite, Omid",
     "text": "Iran becomes the ninth nation to place a domestically built satellite in orbit using a domestically built rocket."},
    {"year": 2013, "when": "Feb 2013", "kind": "developing", "tag": "Azerbaijan",
     "title": "Azerbaijan's first satellite, Azerspace-1",
     "text": "Azerbaijan enters the space club with a communications satellite serving Europe, Africa and Central Asia."},
    {"year": 2014, "when": "Sep 2014", "kind": "landmark",   "tag": "India",
     "title": "India reaches Mars on the first try",
     "text": "The Mars Orbiter Mission (Mangalyaan) makes India the first nation to reach Mars orbit on its maiden attempt — and the first in Asia."},
    {"year": 2017, "when": "2017",      "kind": "developing", "tag": "Ghana · Multiple",
     "title": "A wave of first satellites",
     "text": "Nations from Ghana to Bangladesh build and deploy their first satellites, many via university and CubeSat programs."},
    {"year": 2018, "when": "2018",      "kind": "developing", "tag": "Kenya · Egypt · Türkiye",
     "title": "New space agencies stand up",
     "text": "Egypt, Türkiye, Zimbabwe and others formally establish national space agencies, signalling long-term ambition."},
    {"year": 2019, "when": "Aug 2019", "kind": "developing", "tag": "Philippines",
     "title": "The Philippine Space Agency is created",
     "text": "PhilSA is founded to coordinate a national program built on the Diwata microsatellites."},
    {"year": 2020, "when": "Nov 2020", "kind": "global",     "tag": "China",
     "title": "China returns lunar samples",
     "text": "Chang'e 5 brings Moon rocks back to Earth — the first lunar sample return in over four decades."},
    {"year": 2021, "when": "Feb 2021", "kind": "landmark",   "tag": "UAE",
     "title": "The UAE reaches Mars with Hope",
     "text": "The Emirates Mars Mission enters orbit, making the UAE the first Arab nation — and fifth entity ever — to reach Mars."},
    {"year": 2021, "when": "May 2021", "kind": "landmark",   "tag": "China",
     "title": "China lands a rover on Mars",
     "text": "The Zhurong rover touches down, making China the second nation to operate a rover on the Martian surface."},
    {"year": 2023, "when": "Apr 2023", "kind": "developing", "tag": "Kenya",
     "title": "Kenya's first operational satellite, Taifa-1",
     "text": "Kenya launches a domestically designed Earth-observation satellite to support agriculture and disaster response."},
    {"year": 2023, "when": "Aug 2023", "kind": "landmark",   "tag": "India",
     "title": "Chandrayaan-3 lands near the lunar south pole",
     "text": "India becomes the first nation ever to land near the Moon's south pole — and the fourth to soft-land on the Moon at all."},
    {"year": 2024, "when": "2024",      "kind": "developing", "tag": "Global South",
     "title": "The frontier keeps widening",
     "text": "More developing nations launch satellites, join lunar programs and grow ground-station networks — space is now a genuinely global endeavour."},
]
