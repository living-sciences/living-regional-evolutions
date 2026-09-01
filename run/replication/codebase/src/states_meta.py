"""State metadata for Blanchard-Katz (1992) replication.

51 units = 50 states + DC. Includes postal code, FIPS, Census division/region,
manufacturing-AHE start year (from the paper's data appendix, p.58), farm-state
flag (paper's >4% farm-earnings definition, used in Step 8), and Fig-2 regional
grouping.
"""

# postal: (name, fips, census_division, census_region, ahe_start, fig2_group)
# Census divisions (9) and regions (4) per U.S. Census Bureau.
STATES = {
    "AL": ("Alabama", "01", "East South Central", "South", 1949, "other"),
    "AK": ("Alaska", "02", "Pacific", "West", 1961, "oil"),
    "AZ": ("Arizona", "04", "Mountain", "West", 1949, "sunbelt"),
    "AR": ("Arkansas", "05", "West South Central", "South", 1949, "farm"),
    "CA": ("California", "06", "Pacific", "West", 1947, "sunbelt"),
    "CO": ("Colorado", "08", "Mountain", "West", 1951, "other"),
    "CT": ("Connecticut", "09", "New England", "Northeast", 1948, "newengland"),
    "DE": ("Delaware", "10", "South Atlantic", "South", 1947, "other"),
    "DC": ("District of Columbia", "11", "South Atlantic", "South", 1972, "other"),
    "FL": ("Florida", "12", "South Atlantic", "South", 1948, "sunbelt"),
    "GA": ("Georgia", "13", "South Atlantic", "South", 1949, "other"),
    "HI": ("Hawaii", "15", "Pacific", "West", 1961, "farm"),
    "ID": ("Idaho", "16", "Mountain", "West", 1950, "farm"),
    "IL": ("Illinois", "17", "East North Central", "Midwest", 1947, "rustbelt"),
    "IN": ("Indiana", "18", "East North Central", "Midwest", 1948, "rustbelt"),
    "IA": ("Iowa", "19", "West North Central", "Midwest", 1949, "farm"),
    "KS": ("Kansas", "20", "West North Central", "Midwest", 1949, "farm"),
    "KY": ("Kentucky", "21", "East South Central", "South", 1954, "coal"),
    "LA": ("Louisiana", "22", "West South Central", "South", 1950, "oil"),
    "ME": ("Maine", "23", "New England", "Northeast", 1948, "newengland"),
    "MD": ("Maryland", "24", "South Atlantic", "South", 1950, "midatlantic"),
    "MA": ("Massachusetts", "25", "New England", "Northeast", 1950, "newengland"),
    "MI": ("Michigan", "26", "East North Central", "Midwest", 1947, "rustbelt"),
    "MN": ("Minnesota", "27", "West North Central", "Midwest", 1947, "farm"),
    "MS": ("Mississippi", "28", "East South Central", "South", 1950, "other"),
    "MO": ("Missouri", "29", "West North Central", "Midwest", 1951, "other"),
    "MT": ("Montana", "30", "Mountain", "West", 1950, "farm"),
    "NE": ("Nebraska", "31", "West North Central", "Midwest", 1950, "farm"),
    "NV": ("Nevada", "32", "Mountain", "West", 1950, "sunbelt"),
    "NH": ("New Hampshire", "33", "New England", "Northeast", 1947, "newengland"),
    "NJ": ("New Jersey", "34", "Mid-Atlantic", "Northeast", 1947, "midatlantic"),
    "NM": ("New Mexico", "35", "Mountain", "West", 1949, "oil"),
    "NY": ("New York", "36", "Mid-Atlantic", "Northeast", 1947, "midatlantic"),
    "NC": ("North Carolina", "37", "South Atlantic", "South", 1950, "other"),
    "ND": ("North Dakota", "38", "West North Central", "Midwest", 1956, "farm"),
    "OH": ("Ohio", "39", "East North Central", "Midwest", 1952, "rustbelt"),
    "OK": ("Oklahoma", "40", "West South Central", "South", 1948, "oil"),
    "OR": ("Oregon", "41", "Pacific", "West", 1950, "other"),
    "PA": ("Pennsylvania", "42", "Mid-Atlantic", "Northeast", 1947, "coal"),
    "RI": ("Rhode Island", "44", "New England", "Northeast", 1947, "newengland"),
    "SC": ("South Carolina", "45", "South Atlantic", "South", 1949, "other"),
    "SD": ("South Dakota", "46", "West North Central", "Midwest", 1950, "farm"),
    "TN": ("Tennessee", "47", "East South Central", "South", 1948, "other"),
    "TX": ("Texas", "48", "West South Central", "South", 1949, "oil"),
    "UT": ("Utah", "49", "Mountain", "West", 1947, "other"),
    "VT": ("Vermont", "50", "New England", "Northeast", 1949, "newengland"),
    "VA": ("Virginia", "51", "South Atlantic", "South", 1950, "other"),
    "WA": ("Washington", "53", "Pacific", "West", 1947, "other"),
    "WV": ("West Virginia", "54", "South Atlantic", "South", 1951, "coal"),
    "WI": ("Wisconsin", "55", "East North Central", "Midwest", 1947, "farm"),
    "WY": ("Wyoming", "56", "Mountain", "West", 1950, "oil"),
}

# Employment coverage start per appendix: AK 1960, HI 1955 (FRED HINAN begins 1958).
EMP_START = {"AK": 1960, "HI": 1955}

# Farm states per paper Step 8 (>4% farm earnings): SD, ID, IA, MT, ND, WI, HI, AR, NE
FARM_STATES = ["SD", "ID", "IA", "MT", "ND", "WI", "HI", "AR", "NE"]

POSTALS = list(STATES.keys())

# 9 Census divisions -- note NJ/NY/PA are "Mid-Atlantic" (a division within Northeast).
def division(p): return STATES[p][2]
def region(p): return STATES[p][3]
def name(p): return STATES[p][0]
def fips(p): return STATES[p][1]
def ahe_start(p): return STATES[p][4]
def fig2_group(p): return STATES[p][5]
