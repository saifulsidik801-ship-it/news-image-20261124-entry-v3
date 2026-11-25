#!/usr/bin/env python3
"""news-image-20261124 v3 — one-day world news front page, Tuesday 24 November 2026.
Renders entry.png (1024x1024) with PIL. Every one of the 50 stories happened, or
was first reported, on 24 November 2026. Flat vector-style art drawn with PIL
primitives; no photographs, no real-person images, no text inside the art panels.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 14                      # side margin
CW = W - 2 * MX               # content width = 996

PAPER = (246, 241, 229)
PANEL = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (96, 88, 76)
RULE = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (22, 50, 79)
GOLD = (176, 132, 24)
GREEN = (31, 122, 77)
TEAL = (14, 124, 134)
PURPLE = (122, 42, 122)
GREY = (74, 74, 74)
LIGHT_LINE = (205, 196, 178)
LAND = (214, 196, 160)
LAND_EDGE = (120, 104, 78)

REGION_COLOR = {
    "Europe": (36, 86, 166), "Middle East": (194, 94, 30), "Africa": (31, 122, 77),
    "Asia": (142, 42, 142), "Oceania": (14, 124, 134), "Americas": (163, 22, 33),
    "World": (74, 74, 74),
}

STATUS_FILL = {"CONFIRMED": GREEN, "OFFICIAL": GOLD, "REPORTED": (70, 110, 150),
               "CLAIM": RED, "ONGOING": PURPLE}

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    for p in (FD + name, FN + name):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# ---------------------------------------------------------------- stories
# n, region, place, category, status, banner, headline, deck, source, glyph, lat, lon
HEROES = [
    dict(n=1, region="Asia", place="SHANGHAI", cat="POLITICS", status="OFFICIAL",
         banner="UNDER INVESTIGATION",
         headline="China probes Shanghai's party chief",
         deck="Xinhua: Politburo member Chen Jining, 62, is under investigation "
              "for \u201cserious violations\u201d.",
         source="Xinhua \u00b7 Reuters", glyph="building", lat=31.2, lon=121.5),
    dict(n=2, region="Americas", place="BROOKLYN, NEW YORK", cat="COURTS", status="CONFIRMED",
         banner="GUILTY \u00b7 10 OF 12 COUNTS",
         headline="US jury finds Huawei guilty",
         deck="Guilty of trade secrets, bank fraud and Iran sanctions breaches; "
              "the racketeering charge fails.",
         source="Reuters \u00b7 AP", glyph="gavel", lat=40.7, lon=-74.0),
    dict(n=3, region="Middle East", place="RIYADH", cat="WAR", status="CONFIRMED",
         banner="11 HURT",
         headline="Houthi drone hits Riyadh tower",
         deck="The PIF tower is hit a second time in a week; 11 are hurt, "
              "Saudi civil defence says.",
         source="Al Jazeera \u00b7 Saudi Civil Defence", glyph="tower", lat=24.7, lon=46.7),
]

# n, region, place, category, status, headline, deck, source, glyph, lat, lon
MIDS = [
    dict(n=4, region="Middle East", place="STRAIT OF HORMUZ", cat="SHIPPING", status="CLAIM",
         headline="Iran: three tankers hit mines in Hormuz",
         deck="IRGC says three tankers hit mines.",
         source="IRGC \u00b7 JMIC", glyph="ship", lat=26.5, lon=56.5),
    dict(n=5, region="Europe", place="KYIV", cat="WAR", status="CONFIRMED",
         headline="Zelensky owns ship strikes in two seas",
         deck="Kyiv confirms the Sparta II strikes.",
         source="Bloomberg", glyph="ship", lat=50.45, lon=30.52),
    dict(n=6, region="Europe", place="PARIS", cat="BUSINESS", status="OFFICIAL",
         headline="Sanofi to buy Insmed for $41bn",
         deck="Biggest pharma deal of the year.",
         source="Sanofi", glyph="pill", lat=48.85, lon=2.35),
    dict(n=7, region="Africa", place="DAKAR", cat="SPORT", status="OFFICIAL",
         headline="CAS hands Senegal back the AFCON title",
         deck="Court restores the 1-0 final win.",
         source="CAS \u00b7 AFP", glyph="trophy", lat=14.7, lon=-17.4),
    dict(n=8, region="Middle East", place="GAZA CITY", cat="WAR", status="CONFIRMED",
         headline="Israel kills Hamas security chief",
         deck="Naeem Abu Nahel dies in Gaza City.",
         source="Reuters", glyph="burst", lat=31.5, lon=34.5),
    dict(n=9, region="Middle East", place="BAGHDAD", cat="ENERGY", status="OFFICIAL",
         headline="Baghdad orders Kurdish oil takeover",
         deck="PM orders control of Kurdish oilfields.",
         source="Reuters \u00b7 The National", glyph="derrick", lat=35.5, lon=44.4),
    dict(n=10, region="Asia", place="ESKISEHIR", cat="DISASTER", status="OFFICIAL",
         headline="Turkish helicopter crash kills five",
         deck="An AS-532 goes down in training.",
         source="Turkish MoD", glyph="heli", lat=39.8, lon=30.5),
    dict(n=11, region="Asia", place="HANOI", cat="DISASTER", status="CONFIRMED",
         headline="Hanoi restaurant blast kills six",
         deck="Gas blast wrecks a hot-pot restaurant.",
         source="VnExpress", glyph="burst", lat=21.0, lon=105.85),
    dict(n=12, region="Americas", place="CARTAGENA", cat="CRIME", status="CONFIRMED",
         headline="Gunmen hold 25 hostage in Cartagena",
         deck="Gunmen seize a supermarket.",
         source="AP \u00b7 Reuters", glyph="building", lat=10.4, lon=-75.5),
    dict(n=13, region="Asia", place="ULLEUNGDO", cat="SECURITY", status="CONFIRMED",
         headline="Russian jets spark Korea air alert",
         deck="Fighters scrambled as jets enter.",
         source="Korea Herald", glyph="jet", lat=37.5, lon=130.9),
    dict(n=14, region="Americas", place="WALL STREET", cat="MARKETS", status="CONFIRMED",
         headline="Dow closes above 50,000",
         deck="First close past 50,000: 50,018.70.",
         source="AP \u00b7 CNBC", glyph="chart", lat=41.2, lon=-73.5),
    dict(n=15, region="Europe", place="KOUROU", cat="SPACE", status="CONFIRMED",
         headline="Ariane 6 lofts 36 Amazon satellites",
         deck="LE-04 lifts off at 11:14 UTC.",
         source="Arianespace", glyph="rocket", lat=5.2, lon=-52.8),
    dict(n=16, region="Europe", place="ENGLAND", cat="HEALTH", status="OFFICIAL",
         headline="Record 5,258 heat deaths in England",
         deck="Summer 2026 deadliest on record.",
         source="UKHSA", glyph="sun", lat=52.5, lon=-1.5),
]

# n, headline, source, glyph, region
LISTED = [
    (17, "UK sanctions Houthis and four officials", "Reuters", "gavel", "Europe"),
    (18, "Yemen: Houthis 60 km from Aden, ready to attack", "Reuters", "burst", "Middle East"),
    (19, "Yemen bus-strike toll rises to 25", "Saba", "burst", "Middle East"),
    (20, "Gaza meningitis alert: 272 cases in October", "Gaza health ministry", "cross", "Middle East"),
    (21, "Rebels name downed DR Congo plane", "BBC", "heli", "Africa"),
    (22, "Malaysia to send thousands of migrants to Myanmar", "AP", "building", "Asia"),
    (23, "Hasina plans return to Dhaka on 16 December", "Reuters", "building", "Asia"),
    (24, "Britain warns Ukraine suppliers on sabotage", "Reuters", "shield", "Europe"),
    (25, "Trump set to hit 16 economies with tariffs", "Reuters", "chart", "Americas"),
    (26, "France to build rare-earth stockpile", "Reuters", "gem", "Europe"),
    (27, "US paused joint ops with Ecuador", "Reuters", "shield", "Americas"),
    (28, "Army: lead azide must be detonated in Iowa", "Washington Post", "burst", "Americas"),
    (29, "Guterres marks 10 years of Colombia peace deal", "UN", "ribbon", "Americas"),
    (30, "Taiex posts record gain, closes at 40,122", "CNA", "chart", "Asia"),
    (31, "Solomons ends China security pact", "SMH", "building", "Oceania"),
    (32, "Nepal quake rattles border region", "USGS", "burst", "Asia"),
    (33, "Cobalt prices surge on Congo export ban", "Reuters", "chart", "Asia"),
    (34, "About 175 migrants missing off Senegal", "Reuters", "ship", "Africa"),
    (35, "Colombia blames ex-FARC for car bomb", "AP", "burst", "Americas"),
    (36, "PNG parliament votes on Bougainville", "The Conversation", "ballot", "Oceania"),
    (37, "Putin vows retaliation over refinery strikes", "Ukr Pravda", "burst", "Europe"),
    (38, "US recovers $8B, charges 800+ in anti-scam sweep", "DOJ", "gavel", "Americas"),
    (39, "Real Madrid hit PSV 5-1 in Champions League", "UEFA", "trophy", "Europe"),
    (40, "UNAIDS: 1.2m new HIV infections in 2025", "UNAIDS", "cross", "World"),
    (41, "Bitcoin falls below $60,000", "CoinDesk", "chart", "World"),
    (42, "UN: five women an hour killed by a partner or kin", "UNODC", "cross", "World"),
    (43, "Hungary's Magyar meets Zelensky in Uzhhorod", "Reuters", "building", "Europe"),
    (44, "Poland summons Russia's envoy over airspace", "Reuters", "jet", "Europe"),
    (45, "Germany first to get Ukraine's Delta system", "Kyiv Independent", "shield", "Europe"),
    (46, "Ebola workers evacuated after 3 days", "WHO", "cross", "Africa"),
    (47, "US measles deaths reach 14, cases near 6,000", "Ars Technica", "cross", "Americas"),
    (48, "Libya's Haftar visits Turkey for first time", "Reuters", "building", "Middle East"),
    (49, "Trump honours Giuliani with Medal of Freedom", "AP", "trophy", "Americas"),
    (50, "Venezuela reports $237.5bn public debt", "Reuters", "chart", "Americas"),
]

# (time UTC, event) — every time verified against the source
TIMELINE = [
    ("00:00", "Iran: three tankers hit mines"),
    ("01:00", "Hanoi restaurant blast"),
    ("06:30", "Sanofi deal, $41bn"),
    ("11:14", "Ariane 6 launch, 36 satellites"),
    ("15:47", "CAS restores Senegal's title"),
    ("17:18", "Putin vows retaliation"),
    ("20:00", "Real Madrid 5-1 PSV kick-off"),
]

NUMBERS = [
    ("11", "hurt in the Riyadh tower strike"),
    ("10 of 12", "counts: Huawei found guilty"),
    ("$41bn", "Sanofi buys Insmed"),
    ("50,018", "Dow's first close above 50,000"),
    ("5,258", "heat deaths, England record"),
    ("36", "Amazon satellites on Ariane 6"),
]

# Stories that are NOT on this page, with the day they actually belong to.
EXCLUSIONS = [
    ("COP31 ends", "22 Nov"),
    ("Nvidia / Huang", "23 Nov"),
    ("EU sanctions 22nd", "23 Nov"),
    ("ICJ Rohingya", "19 Nov"),
    ("Shenzhou-24", "25 Nov"),
    ("Pentagon / Canada", "23 Nov"),
    ("Megaspeed", "23 Nov"),
    ("Cikande fire", "21 Nov"),
    ("Indonesia VP", "23 Nov"),
    ("NATO space", "23 Nov"),
    ("Bukele Haiti", "23 Nov"),
    ("China spy sentence", "23 Nov"),
    ("Zelensky 4-party", "23 Nov"),
    ("Congo cobalt ban", "23 Nov"),
    ("Colombia car bomb", "23 Nov"),
    ("Yemen bus strike", "23 Nov"),
]

REGION_ORDER = ["Europe", "Middle East", "Africa", "Asia", "Oceania", "Americas", "World"]


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for s in HEROES + MIDS:
        counts[s["region"]] += 1
    for (_n, _h, _s, _g, r) in LISTED:
        counts[r] += 1
    return [(r, counts[r]) for r in REGION_ORDER]

# ---------------------------------------------------------------- text helpers

def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw):
    """Greedy wrap; returns list of lines that fit maxw."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(d, s, f, maxw, ellipsis="\u2026"):
    """Single line, truncated with an ellipsis if it does not fit."""
    if text_w(d, s, f) <= maxw:
        return s
    while s and text_w(d, s + ellipsis, f) > maxw:
        s = s[:-1]
    return s + ellipsis


def draw_wrapped(d, x, y, s, f, maxw, fill, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading or int(f.size * 1.25)
    for line in wrap(d, s, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- flat vector art
# Every glyph draws a simple flat scene inside its box: sky, ground, one subject.
# No text inside art panels, no photographs, no real people.

def _sky(d, x, y, w, h, sky, ground=None):
    d.rectangle([x, y, x + w, y + h], fill=sky)
    if ground is not None:
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=ground)


def _star(d, cx, cy, r_out, r_in, n=8, fill=(255, 200, 60)):
    import math
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def draw_art(d, x, y, w, h, glyph):
    """Draw one flat illustration panel."""
    g = glyph
    if g == "building":
        _sky(d, x, y, w, h, (168, 205, 232), (90, 110, 130))
        d.rectangle([x + w * 0.10, y + h * 0.30, x + w * 0.30, y + h * 0.72], fill=(52, 72, 96))
        d.rectangle([x + w * 0.34, y + h * 0.15, x + w * 0.58, y + h * 0.72], fill=(34, 52, 78))
        d.rectangle([x + w * 0.62, y + h * 0.38, x + w * 0.86, y + h * 0.72], fill=(52, 72, 96))
        for bx in (0.10, 0.34, 0.62):
            for wy in (0.22, 0.38, 0.54):
                d.rectangle([x + w * (bx + 0.04), y + h * wy, x + w * (bx + 0.12), y + h * (wy + 0.08)],
                            fill=(255, 214, 90))
        d.ellipse([x + w * 0.78, y + h * 0.06, x + w * 0.92, y + h * 0.20], fill=(255, 214, 90))
    elif g == "gavel":
        _sky(d, x, y, w, h, (232, 214, 178), (120, 84, 48))
        d.rectangle([x + w * 0.20, y + h * 0.20, x + w * 0.80, y + h * 0.36], fill=(96, 60, 28))
        d.rectangle([x + w * 0.20, y + h * 0.20, x + w * 0.27, y + h * 0.36], fill=(70, 44, 22))
        d.rectangle([x + w * 0.73, y + h * 0.20, x + w * 0.80, y + h * 0.36], fill=(70, 44, 22))
        d.line([x + w * 0.50, y + h * 0.36, x + w * 0.72, y + h * 0.66], fill=(120, 76, 36), width=6)
        d.rectangle([x + w * 0.28, y + h * 0.66, x + w * 0.76, y + h * 0.76], fill=(70, 44, 22))
    elif g == "tower":
        _sky(d, x, y, w, h, (246, 190, 120), (70, 60, 80))
        d.rectangle([x + w * 0.40, y + h * 0.12, x + w * 0.58, y + h * 0.72], fill=(40, 48, 66))
        d.rectangle([x + w * 0.47, y + h * 0.02, x + w * 0.51, y + h * 0.12], fill=(40, 48, 66))
        for wy in (0.20, 0.36, 0.52):
            d.rectangle([x + w * 0.44, y + h * wy, x + w * 0.54, y + h * (wy + 0.07)],
                        fill=(255, 214, 90))
        d.ellipse([x + w * 0.70, y + h * 0.10, x + w * 0.82, y + h * 0.22], fill=(30, 30, 30))
        d.line([x + w * 0.70, y + h * 0.16, x + w * 0.60, y + h * 0.16], fill=(30, 30, 30), width=2)
        d.line([x + w * 0.82, y + h * 0.16, x + w * 0.92, y + h * 0.16], fill=(30, 30, 30), width=2)
        _star(d, x + w * 0.38, y + h * 0.20, w * 0.09, w * 0.04, 6, (255, 120, 40))
    elif g == "ship":
        _sky(d, x, y, w, h, (150, 196, 226), (16, 96, 128))
        d.polygon([(x + w * 0.14, y + h * 0.48), (x + w * 0.86, y + h * 0.48),
                   (x + w * 0.76, y + h * 0.70), (x + w * 0.24, y + h * 0.70)],
                  fill=(140, 40, 30))
        d.rectangle([x + w * 0.22, y + h * 0.34, x + w * 0.40, y + h * 0.48], fill=(240, 180, 40))
        d.rectangle([x + w * 0.44, y + h * 0.34, x + w * 0.62, y + h * 0.48], fill=(40, 90, 140))
        d.rectangle([x + w * 0.66, y + h * 0.36, x + w * 0.80, y + h * 0.48], fill=(240, 240, 240))
        d.line([x + w * 0.08, y + h * 0.78, x + w * 0.92, y + h * 0.78], fill=(255, 255, 255), width=3)
        d.line([x + w * 0.16, y + h * 0.88, x + w * 0.84, y + h * 0.88], fill=(255, 255, 255), width=3)
    elif g == "pill":
        _sky(d, x, y, w, h, (240, 240, 244), (200, 205, 215))
        d.rounded_rectangle([x + w * 0.16, y + h * 0.30, x + w * 0.84, y + h * 0.52],
                            radius=h * 0.11, fill=(220, 60, 50))
        d.rounded_rectangle([x + w * 0.50, y + h * 0.30, x + w * 0.84, y + h * 0.52],
                            radius=h * 0.11, fill=(255, 255, 255))
        d.ellipse([x + w * 0.20, y + h * 0.62, x + w * 0.34, y + h * 0.76], fill=(40, 120, 180))
        d.ellipse([x + w * 0.40, y + h * 0.66, x + w * 0.52, y + h * 0.78], fill=(40, 120, 180))
        d.ellipse([x + w * 0.58, y + h * 0.62, x + w * 0.72, y + h * 0.76], fill=(220, 60, 50))
    elif g == "trophy":
        _sky(d, x, y, w, h, (250, 226, 140), (176, 132, 24))
        d.polygon([(x + w * 0.30, y + h * 0.16), (x + w * 0.70, y + h * 0.16),
                   (x + w * 0.64, y + h * 0.48), (x + w * 0.36, y + h * 0.48)], fill=(212, 160, 30))
        d.arc([x + w * 0.12, y + h * 0.18, x + w * 0.34, y + h * 0.44], 90, 270, fill=(212, 160, 30), width=5)
        d.arc([x + w * 0.66, y + h * 0.18, x + w * 0.88, y + h * 0.44], -90, 90, fill=(212, 160, 30), width=5)
        d.rectangle([x + w * 0.46, y + h * 0.48, x + w * 0.54, y + h * 0.60], fill=(212, 160, 30))
        d.rectangle([x + w * 0.34, y + h * 0.60, x + w * 0.66, y + h * 0.68], fill=(212, 160, 30))
    elif g == "burst":
        _sky(d, x, y, w, h, (60, 52, 66), (40, 34, 44))
        _star(d, x + w * 0.50, y + h * 0.48, w * 0.34, w * 0.13, 9, (255, 150, 40))
        _star(d, x + w * 0.50, y + h * 0.48, w * 0.20, w * 0.08, 9, (255, 220, 80))
        _star(d, x + w * 0.22, y + h * 0.24, w * 0.08, w * 0.03, 6, (255, 200, 90))
        _star(d, x + w * 0.80, y + h * 0.28, w * 0.07, w * 0.03, 6, (255, 200, 90))
    elif g == "derrick":
        _sky(d, x, y, w, h, (238, 226, 200), (140, 110, 70))
        d.line([x + w * 0.50, y + h * 0.10, x + w * 0.30, y + h * 0.72], fill=(50, 44, 36), width=5)
        d.line([x + w * 0.50, y + h * 0.10, x + w * 0.70, y + h * 0.72], fill=(50, 44, 36), width=5)
        d.line([x + w * 0.40, y + h * 0.40, x + w * 0.60, y + h * 0.40], fill=(50, 44, 36), width=4)
        d.line([x + w * 0.36, y + h * 0.56, x + w * 0.64, y + h * 0.56], fill=(50, 44, 36), width=4)
        d.ellipse([x + w * 0.74, y + h * 0.52, x + w * 0.88, y + h * 0.70], fill=(20, 20, 20))
        d.polygon([(x + w * 0.81, y + h * 0.44), (x + w * 0.74, y + h * 0.54),
                   (x + w * 0.88, y + h * 0.54)], fill=(20, 20, 20))
    elif g == "heli":
        _sky(d, x, y, w, h, (150, 196, 226), (120, 140, 120))
        d.ellipse([x + w * 0.18, y + h * 0.38, x + w * 0.56, y + h * 0.64], fill=(60, 80, 100))
        d.polygon([(x + w * 0.52, y + h * 0.46), (x + w * 0.88, y + h * 0.40),
                   (x + w * 0.88, y + h * 0.50), (x + w * 0.54, y + h * 0.54)], fill=(60, 80, 100))
        d.line([x + w * 0.14, y + h * 0.34, x + w * 0.86, y + h * 0.34], fill=(30, 30, 30), width=4)
        d.line([x + w * 0.36, y + h * 0.34, x + w * 0.36, y + h * 0.38], fill=(30, 30, 30), width=3)
        d.ellipse([x + w * 0.22, y + h * 0.42, x + w * 0.32, y + h * 0.52], fill=(180, 220, 240))
        d.line([x + w * 0.24, y + h * 0.66, x + w * 0.52, y + h * 0.66], fill=(30, 30, 30), width=3)
    elif g == "jet":
        _sky(d, x, y, w, h, (150, 196, 226), (200, 210, 220))
        d.polygon([(x + w * 0.12, y + h * 0.50), (x + w * 0.62, y + h * 0.40),
                   (x + w * 0.88, y + h * 0.46), (x + w * 0.62, y + h * 0.58),
                   (x + w * 0.20, y + h * 0.58)], fill=(90, 100, 115))
        d.polygon([(x + w * 0.42, y + h * 0.40), (x + w * 0.52, y + h * 0.22),
                   (x + w * 0.58, y + h * 0.40)], fill=(70, 80, 95))
        d.polygon([(x + w * 0.40, y + h * 0.58), (x + w * 0.48, y + h * 0.74),
                   (x + w * 0.54, y + h * 0.58)], fill=(70, 80, 95))
        d.ellipse([x + w * 0.80, y + h * 0.16, x + w * 0.88, y + h * 0.24], fill=(255, 220, 90))
    elif g == "chart":
        _sky(d, x, y, w, h, (245, 245, 240), (220, 225, 220))
        d.line([x + w * 0.14, y + h * 0.80, x + w * 0.88, y + h * 0.80], fill=(60, 60, 60), width=3)
        d.line([x + w * 0.14, y + h * 0.14, x + w * 0.14, y + h * 0.80], fill=(60, 60, 60), width=3)
        pts = [(0.16, 0.62), (0.30, 0.55), (0.44, 0.60), (0.58, 0.38), (0.72, 0.44), (0.86, 0.22)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            d.line([x + w * ax, y + h * ay, x + w * bx, y + h * by], fill=(31, 122, 77), width=4)
        for (px, py) in pts:
            d.ellipse([x + w * px - 3, y + h * py - 3, x + w * px + 3, y + h * py + 3],
                      fill=(31, 122, 77))
    elif g == "rocket":
        _sky(d, x, y, w, h, (30, 44, 78), (20, 30, 56))
        d.ellipse([x + w * 0.14, y + h * 0.12, x + w * 0.20, y + h * 0.18], fill=(255, 255, 255))
        d.ellipse([x + w * 0.78, y + h * 0.22, x + w * 0.84, y + h * 0.28], fill=(255, 255, 255))
        d.ellipse([x + w * 0.66, y + h * 0.08, x + w * 0.70, y + h * 0.12], fill=(255, 255, 255))
        d.polygon([(x + w * 0.50, y + h * 0.10), (x + w * 0.62, y + h * 0.30),
                   (x + w * 0.60, y + h * 0.56), (x + w * 0.40, y + h * 0.56),
                   (x + w * 0.38, y + h * 0.30)], fill=(240, 240, 240))
        d.polygon([(x + w * 0.50, y + h * 0.10), (x + w * 0.58, y + h * 0.24),
                   (x + w * 0.42, y + h * 0.24)], fill=(200, 50, 40))
        d.polygon([(x + w * 0.40, y + h * 0.48), (x + w * 0.30, y + h * 0.66),
                   (x + w * 0.40, y + h * 0.60)], fill=(200, 50, 40))
        d.polygon([(x + w * 0.60, y + h * 0.48), (x + w * 0.70, y + h * 0.66),
                   (x + w * 0.60, y + h * 0.60)], fill=(200, 50, 40))
        d.polygon([(x + w * 0.44, y + h * 0.56), (x + w * 0.56, y + h * 0.56),
                   (x + w * 0.50, y + h * 0.78)], fill=(255, 150, 40))
    elif g == "sun":
        _sky(d, x, y, w, h, (252, 230, 150), (200, 160, 90))
        for i in range(8):
            import math
            a = math.pi * i / 4
            d.line([x + w * 0.50 + w * 0.30 * math.cos(a), y + h * 0.44 + h * 0.30 * math.sin(a),
                    x + w * 0.50 + w * 0.42 * math.cos(a), y + h * 0.44 + h * 0.42 * math.sin(a)],
                   fill=(230, 140, 30), width=4)
        d.ellipse([x + w * 0.32, y + h * 0.26, x + w * 0.68, y + h * 0.62], fill=(240, 160, 40))
    elif g == "cross":
        d.rectangle([x, y, x + w, y + h], fill=(31, 122, 77))
        d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.58, y + h * 0.82], fill=(255, 255, 255))
        d.rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.82, y + h * 0.58], fill=(255, 255, 255))
    elif g == "ribbon":
        _sky(d, x, y, w, h, (245, 240, 250), (220, 210, 230))
        d.polygon([(x + w * 0.50, y + h * 0.14), (x + w * 0.66, y + h * 0.34),
                   (x + w * 0.58, y + h * 0.52), (x + w * 0.42, y + h * 0.52),
                   (x + w * 0.34, y + h * 0.34)], fill=(142, 42, 142))
        d.polygon([(x + w * 0.42, y + h * 0.52), (x + w * 0.58, y + h * 0.52),
                   (x + w * 0.70, y + h * 0.82), (x + w * 0.56, y + h * 0.82),
                   (x + w * 0.50, y + h * 0.66), (x + w * 0.44, y + h * 0.82),
                   (x + w * 0.30, y + h * 0.82)], fill=(122, 32, 122))
    elif g == "flag":
        _sky(d, x, y, w, h, (200, 220, 240), (150, 170, 150))
        d.line([x + w * 0.24, y + h * 0.12, x + w * 0.24, y + h * 0.86], fill=(60, 60, 60), width=4)
        d.polygon([(x + w * 0.24, y + h * 0.12), (x + w * 0.82, y + h * 0.22),
                   (x + w * 0.24, y + h * 0.42)], fill=(179, 39, 30))
    elif g == "shield":
        _sky(d, x, y, w, h, (200, 220, 240), (170, 185, 200))
        d.polygon([(x + w * 0.22, y + h * 0.16), (x + w * 0.78, y + h * 0.16),
                   (x + w * 0.78, y + h * 0.48), (x + w * 0.50, y + h * 0.84),
                   (x + w * 0.22, y + h * 0.48)], fill=(36, 86, 166))
        d.line([x + w * 0.38, y + h * 0.46, x + w * 0.48, y + h * 0.58,
                x + w * 0.66, y + h * 0.30], fill=(255, 255, 255), width=5)
    elif g == "gem":
        _sky(d, x, y, w, h, (230, 240, 245), (190, 200, 210))
        d.polygon([(x + w * 0.20, y + h * 0.34), (x + w * 0.50, y + h * 0.16),
                   (x + w * 0.80, y + h * 0.34), (x + w * 0.50, y + h * 0.82)],
                  fill=(80, 190, 200))
        d.polygon([(x + w * 0.20, y + h * 0.34), (x + w * 0.50, y + h * 0.16),
                   (x + w * 0.50, y + h * 0.34)], fill=(140, 220, 230))
        d.polygon([(x + w * 0.80, y + h * 0.34), (x + w * 0.50, y + h * 0.16),
                   (x + w * 0.50, y + h * 0.34)], fill=(40, 150, 170))
        d.line([x + w * 0.20, y + h * 0.34, x + w * 0.80, y + h * 0.34], fill=(255, 255, 255), width=2)
    elif g == "ballot":
        _sky(d, x, y, w, h, (238, 230, 210), (190, 175, 150))
        d.polygon([(x + w * 0.30, y + h * 0.18), (x + w * 0.42, y + h * 0.34),
                   (x + w * 0.66, y + h * 0.10)], fill=(255, 255, 255), outline=(60, 60, 60))
        d.rectangle([x + w * 0.22, y + h * 0.44, x + w * 0.78, y + h * 0.80], fill=(150, 100, 50))
        d.rectangle([x + w * 0.38, y + h * 0.40, x + w * 0.62, y + h * 0.48], fill=(60, 40, 20))
        d.line([x + w * 0.30, y + h * 0.58, x + w * 0.70, y + h * 0.58], fill=(255, 255, 255), width=3)
        d.line([x + w * 0.30, y + h * 0.68, x + w * 0.58, y + h * 0.68], fill=(255, 255, 255), width=3)
    else:  # fallback: plain panel with a dot
        _sky(d, x, y, w, h, (200, 200, 200), (160, 160, 160))
        d.ellipse([x + w * 0.35, y + h * 0.35, x + w * 0.65, y + h * 0.65], fill=INK)

# ---------------------------------------------------------------- world map
# Coarse continent outlines (lon, lat). Stylised, not surveyed.

CONTINENTS = {
    "NA": [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-105, 73),
           (-95, 80), (-85, 76), (-80, 73), (-76, 62), (-70, 58), (-65, 60),
           (-60, 55), (-55, 52), (-60, 47), (-65, 45), (-70, 42), (-75, 39),
           (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-88, 30), (-90, 21),
           (-94, 17), (-92, 15), (-87, 13), (-83, 9), (-79, 9), (-82, 13),
           (-86, 13), (-91, 14), (-96, 16), (-101, 18), (-105, 20), (-108, 23),
           (-112, 28), (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-128, 52),
           (-135, 58), (-145, 60), (-152, 58), (-158, 58), (-165, 60)],
    "SA": [(-79, 9), (-77, 5), (-79, 0), (-81, -5), (-80, -8), (-77, -12),
           (-75, -15), (-70, -18), (-70, -23), (-70, -28), (-71, -33), (-73, -37),
           (-73, -42), (-74, -46), (-71, -50), (-69, -52), (-66, -55), (-65, -52),
           (-66, -47), (-64, -42), (-60, -38), (-57, -34), (-52, -32), (-48, -28),
           (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-38, -4), (-44, -3),
           (-50, 0), (-53, 4), (-57, 6), (-61, 9), (-65, 11), (-70, 12),
           (-75, 11), (-77, 8)],
    "AF": [(-6, 35), (-1, 35), (3, 37), (10, 37), (11, 34), (15, 32), (20, 32),
           (25, 32), (30, 31), (32, 31), (34, 28), (36, 24), (37, 20), (39, 17),
           (41, 13), (44, 11), (48, 11), (51, 11), (46, 6), (42, 2), (41, -2),
           (40, -6), (39, -10), (37, -14), (35, -18), (33, -22), (32, -26),
           (30, -30), (27, -33), (22, -35), (19, -34), (17, -32), (15, -28),
           (13, -22), (12, -16), (12, -10), (10, -4), (9, 0), (9, 4), (4, 6),
           (-2, 5), (-7, 4), (-12, 7), (-16, 12), (-17, 15), (-17, 20), (-16, 24),
           (-14, 28), (-10, 31)],
    "EUAS": [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (0, 46), (2, 48),
             (4, 50), (6, 53), (8, 55), (8, 57), (10, 58), (12, 56), (18, 56),
             (21, 55), (23, 57), (24, 59), (26, 60), (28, 61), (30, 62), (32, 64),
             (35, 66), (40, 68), (45, 68), (50, 69), (55, 69), (60, 70), (65, 71),
             (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77),
             (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 72),
             (135, 72), (140, 72), (145, 72), (150, 70), (155, 70), (160, 69),
             (165, 68), (170, 67), (175, 66), (178, 65), (178, 62), (175, 60),
             (170, 60), (165, 60), (162, 59), (158, 55), (155, 52), (150, 55),
             (145, 55), (142, 52), (140, 48), (138, 45), (135, 43), (132, 43),
             (130, 42), (127, 40), (126, 38), (122, 38), (121, 33), (120, 28),
             (118, 25), (115, 22), (110, 20), (108, 18), (106, 10), (104, 9),
             (101, 8), (99, 7), (98, 10), (96, 15), (94, 17), (92, 21),
             (90, 22), (88, 22), (86, 20), (83, 18), (80, 15), (78, 10),
             (76, 8), (74, 13), (72, 20), (70, 22), (68, 23), (66, 25),
             (63, 25), (60, 25), (57, 26), (55, 27), (52, 26), (50, 29),
             (49, 30), (51, 28), (54, 27), (56, 26), (57, 24), (59, 22),
             (58, 20), (55, 17), (52, 15), (50, 14), (48, 14), (46, 12),
             (44, 13), (43, 13), (42, 15), (40, 16), (39, 18), (38, 20),
             (37, 22), (35, 24), (34, 27), (33, 29), (32, 31), (30, 32),
             (28, 33), (26, 34), (23, 35), (20, 36), (18, 36), (16, 38),
             (14, 38), (12, 38), (10, 37), (8, 37), (5, 36), (2, 36),
             (-1, 35), (-5, 35), (-8, 34)],
    "AU": [(113, -22), (114, -28), (115, -33), (118, -35), (122, -34), (126, -32),
           (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (143, -39),
           (146, -39), (149, -37), (151, -35), (153, -32), (153, -28), (151, -24),
           (149, -20), (146, -19), (143, -15), (142, -11), (141, -13), (138, -15),
           (136, -15), (135, -12), (132, -12), (130, -13), (127, -14), (124, -15),
           (121, -17), (118, -20), (114, -22)],
}

# Display nudges (dx, dy) in px for pins that would collide on the small map.
# Fan-out computed so every neighbouring pair is >= ~15px apart (pin dia 14).
PIN_NUDGE = {
    1: (6, -12),    # Shanghai, away from Hanoi
    2: (-14, -10),  # Brooklyn, away from Wall Street
    3: (2, -20),    # Riyadh, above Baghdad
    4: (22, -10),   # Hormuz, east of Baghdad
    5: (10, -14),   # Kyiv, up-right
    6: (-18, -2),   # Paris, west over the Atlantic
    8: (2, 16),     # Gaza City, down
    9: (16, 2),     # Baghdad, east
    10: (-16, 4),   # Eskisehir, west
    13: (13, -8),   # Ulleungdo, away from Shanghai
    14: (12, 8),    # Wall Street, down-right
    16: (-6, -16),  # England, up
}


def draw_map(d, x, y, w, h):
    """Filled continent map with numbered pins for the 16 hero/mid stories."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    lon0, lon1, lat0, lat1 = -170.0, 190.0, -58.0, 78.0
    s = min(w / (lon1 - lon0), h / (lat1 - lat0))
    ox = x + (w - (lon1 - lon0) * s) / 2
    oy = y + (h - (lat1 - lat0) * s) / 2

    def proj(lon, lat):
        return (ox + (lon - lon0) * s, oy + (lat1 - lat) * s)

    for poly in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
    for st in HEROES + MIDS:
        px, py = proj(st["lon"], st["lat"])
        dx, dy = PIN_NUDGE.get(st["n"], (0, 0))
        # leader line when nudged
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=REGION_COLOR[st["region"]], width=1)
            px, py = px + dx, py + dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r],
                  fill=REGION_COLOR[st["region"]], outline=(255, 255, 255), width=1)
        f = SANS_B(8)
        label = str(st["n"])
        tw = d.textlength(label, font=f)
        d.text((px - tw / 2, py - 5), label, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout

def section_masthead(d, y):
    f_kick = SANS_B(11)
    kick = "ONE DAY  \u00b7  FIFTY STORIES  \u00b7  EVERY WIRE CHECKED"
    tw = d.textlength(kick, font=f_kick)
    d.text(((W - tw) / 2, y + 1), kick, font=f_kick, fill=RED)
    y += 16
    f_date = SERIF_B(34)
    date = "TUESDAY 24 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, y), date, font=f_date, fill=INK)
    y += 44
    f_sub = SERIF_I(13)
    sub = "The world in one day \u2014 every story happened, or was first reported, on 24 November 2026."
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, y), sub, font=f_sub, fill=MUTED)
    y += 18
    d.rectangle([MX, y, MX + CW, y + 3], fill=INK)
    y += 5
    d.rectangle([MX, y, MX + CW, y + 1], fill=INK)
    y += 4
    return y


def section_numbers(d, y):
    cell_w = CW / len(NUMBERS)
    f_num = SERIF_B(17)
    f_lab = SANS(9)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + i * cell_w
        d.text((cx + 6, y), num, font=f_num, fill=RED if i == 0 else INK)
        yy = y + 23
        for line in wrap(d, lab, f_lab, cell_w - 12):
            d.text((cx + 6, yy), line, font=f_lab, fill=MUTED)
            yy += 11
        if i:
            d.line([cx, y + 2, cx, y + 36], fill=LIGHT_LINE, width=1)
    y += 42
    d.line([MX, y, MX + CW, y], fill=LIGHT_LINE, width=1)
    y += 3
    return y


def _hero_card_height(d, hero, card_w):
    art_h = 68
    tw = card_w - 16
    hl = wrap(d, hero["headline"], SERIF_B(17), tw)
    dl = wrap(d, hero["deck"], SANS(11), tw)
    return (6 + art_h + 5 + 13 + 3 + len(hl) * 22 + 4 + len(dl) * 14 + 4 + 12 + 6,
            hl, dl)


def section_heroes(d, y):
    gap = 10
    card_w = (CW - 2 * gap) / 3
    heights = [_hero_card_height(d, h, card_w)[0] for h in HEROES]
    card_h = max(heights)
    for i, hero in enumerate(HEROES):
        x = MX + i * (card_w + gap)
        _h, hl, dl = _hero_card_height(d, hero, card_w)
        d.rectangle([x, y, x + card_w, y + card_h], fill=PANEL, outline=LIGHT_LINE)
        d.rectangle([x, y, x + card_w, y + 4], fill=REGION_COLOR[hero["region"]])
        cy = y + 4
        draw_art(d, x + 1, cy + 1, card_w - 2, 68, hero["glyph"])
        # number badge on the art
        r = 11
        bx, by = x + 14, cy + 14
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=REGION_COLOR[hero["region"]],
                  outline=(255, 255, 255), width=2)
        f_nb = SANS_B(11)
        lab = str(hero["n"])
        tw = d.textlength(lab, font=f_nb)
        d.text((bx - tw / 2, by - 7), lab, font=f_nb, fill=(255, 255, 255))
        cy += 68 + 6
        f_ban = SANS_B(10)
        d.text((x + 8, cy), hero["banner"], font=f_ban,
               fill=STATUS_FILL[hero["status"]])
        d.text((x + card_w - 8 - d.textlength(hero["place"], font=f_ban), cy),
               hero["place"], font=f_ban, fill=MUTED)
        cy += 15
        f_cat = SANS_B(9)
        d.text((x + 8, cy), hero["cat"], font=f_cat, fill=MUTED)
        cy += 13
        for line in hl:
            d.text((x + 8, cy), line, font=SERIF_B(17), fill=INK)
            cy += 22
        cy += 2
        for line in dl:
            d.text((x + 8, cy), line, font=SANS(11), fill=INK)
            cy += 14
        cy += 2
        d.text((x + 8, cy), hero["source"], font=SANS(9.5), fill=MUTED)
    return y + card_h + 8


def section_mids(d, y):
    gap = 10
    col_w = (CW - 2 * gap) / 3
    strip_h = 38
    pitch = 40
    cells = [(m, False) for m in MIDS]  # 13 mids + 1 explainer cell
    for row in range(5):
        for col in range(3):
            idx = row * 3 + col
            x = MX + col * (col_w + gap)
            yy = y + row * pitch
            if idx < len(MIDS):
                m = MIDS[idx]
                d.rectangle([x, yy, x + col_w, yy + strip_h], fill=PANEL, outline=LIGHT_LINE)
                draw_art(d, x + 1, yy + 1, 36, strip_h - 2, m["glyph"])
                r = 8
                bx, by = x + 11, yy + 10
                d.ellipse([bx - r, by - r, bx + r, by + r],
                          fill=REGION_COLOR[m["region"]], outline=(255, 255, 255), width=1)
                f_nb = SANS_B(8)
                lab = str(m["n"])
                tw = d.textlength(lab, font=f_nb)
                d.text((bx - tw / 2, by - 5), lab, font=f_nb, fill=(255, 255, 255))
                tx = x + 44
                twd = col_w - 48
                head = fit_text(d, m["headline"], SANS_B(12), twd)
                d.text((tx, yy + 4), head, font=SANS_B(12), fill=INK)
                deck = fit_text(d, m["deck"] + " \u00b7 " + m["source"].split(" \u00b7 ")[0],
                                SANS(10), twd)
                d.text((tx, yy + 21), deck, font=SANS(10), fill=MUTED)
            elif idx == len(MIDS):
                # DATE RULE explainer fills the remaining cells of the last row
                span_w = col_w * (3 - col) + gap * (3 - col - 1)
                d.rectangle([x, yy, x + span_w, yy + strip_h], fill=(255, 244, 214),
                            outline=GOLD)
                d.text((x + 8, yy + 3), "DATE RULE", font=SANS_B(10), fill=RED)
                d.text((x + 8, yy + 15),
                       "Every story here happened, or was first reported, on 24 Nov 2026.",
                       font=SANS(9), fill=INK)
                d.text((x + 8, yy + 26),
                       "Stories from 23 or 25 Nov were left out \u2014 see DATE CHECK below.",
                       font=SANS(9), fill=INK)
                break
    return y + 5 * pitch + 6


def section_map_timeline(d, y, row_h=150):
    map_w = 500
    tl_x = MX + map_w + 10
    tl_w = CW - map_w - 10
    # map
    f_t = SANS_B(11)
    d.text((MX, y), "WHERE IT HAPPENED", font=f_t, fill=INK)
    counts = region_counts()
    rc = "  \u00b7  ".join("%s %d" % (r.replace("Middle East", "Mideast"), c)
                           for r, c in counts)
    f_rc = SANS(8)
    d.text((MX + map_w - d.textlength(rc, font=f_rc), y + 2), rc, font=f_rc, fill=MUTED)
    draw_map(d, MX, y + 18, map_w, row_h - 18)
    # timeline
    d.text((tl_x, y), "THE DAY IN UTC", font=f_t, fill=INK)
    yy = y + 20
    for t, ev in TIMELINE:
        d.text((tl_x, yy), t, font=SANS_B(11), fill=RED)
        d.text((tl_x + 46, yy), ev, font=SANS(11), fill=INK)
        yy += 18
    return y + row_h + 8


def section_datecheck(d, y):
    f_t = SANS_B(11)
    items = "  \u00b7  ".join("%s (%s)" % (name, when) for name, when in EXCLUSIONS)
    txt = ("Left out \u2014 they belong to another day: " + items)
    lines = wrap(d, txt, SANS(9.5), CW - 16)
    box_h = 6 + 14 + 2 + len(lines) * 13 + 6
    d.rectangle([MX, y, MX + CW, y + box_h], fill=(255, 244, 214), outline=GOLD)
    d.text((MX + 8, y + 6), "DATE CHECK \u2014 NOT TODAY", font=f_t, fill=RED)
    yy = y + 22
    for line in lines:
        d.text((MX + 8, yy), line, font=SANS(9.5), fill=MUTED)
        yy += 13
    return y + box_h + 6


def section_list(d, y):
    f_t = SANS_B(12)
    d.text((MX, y), "THE REST OF THE DAY \u00b7 STORIES 17\u201350", font=f_t, fill=INK)
    y += 16
    d.line([MX, y, MX + CW, y], fill=INK, width=1)
    y += 4
    gap = 10
    col_w = (CW - gap) / 2
    pitch = 12
    left = LISTED[:17]
    right = LISTED[17:]
    for col, items in enumerate((left, right)):
        x = MX + col * (col_w + gap)
        for i, (n, head, src, glyph, region) in enumerate(items):
            yy = y + i * pitch
            f_nb = SANS_B(9.5)
            d.text((x, yy), str(n), font=f_nb, fill=REGION_COLOR[region])
            draw_art(d, x + 20, yy, 12, 12, glyph)
            f_h = SANS_B(9.5)
            f_s = SANS(9)
            src_w = d.textlength(src, font=f_s)
            head_w = col_w - 20 - 16 - 6 - src_w - 8
            head = fit_text(d, head, f_h, head_w)
            d.text((x + 36, yy), head, font=f_h, fill=INK)
            d.text((x + col_w - src_w, yy), src, font=f_s, fill=MUTED)
    return y + 17 * pitch + 6


def section_footer(d, y):
    d.line([MX, y, MX + CW, y], fill=INK, width=1)
    y += 5
    f_f = SANS(9)
    txt = ("All 50 stories happened, or were first reported, on Tuesday 24 November 2026  \u00b7  "
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Xinhua \u00b7 UNAIDS \u00b7 UN \u00b7 WHO \u00b7 UKHSA \u00b7 CAS")
    tw = d.textlength(txt, font=f_f)
    d.text(((W - tw) / 2, y), txt, font=f_f, fill=MUTED)
    return y + 11


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8
    y = section_masthead(d, y)
    y = section_numbers(d, y)
    y = section_heroes(d, y)
    y = section_mids(d, y)
    y = section_map_timeline(d, y)
    y = section_datecheck(d, y)
    y = section_list(d, y)
    y = section_footer(d, y)
    print("final y =", y, "of", H, "-> slack", H - y)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes,", img.size)
