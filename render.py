#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page (1024x1024 PNG).

Build-time renderer for the make.fun news-image-20261122 entry.
Draws a retro-newspaper front page with 50 verified stories, a UTC
timeline strip, an explicit date check and a sources line.
Run:  python3 render.py   ->  writes entry.png next to this file.
The graded entrypoint (main.py) only copies entry.png to the output
directory; it does not draw anything.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"
DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (29, 78, 137)
DARK = (32, 32, 34)
GREY = (90, 86, 78)
RULE = (120, 112, 96)


def load_font(name, size):
    """Try Noto first, fall back to DejaVu, then PIL's default."""
    for base in (FONT_DIR, DEJAVU_DIR):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: load_font("NotoSerif-Bold.ttf", s)
SERIF = lambda s: load_font("NotoSerif-Regular.ttf", s)
SANS_B = lambda s: load_font("NotoSans-Bold.ttf", s)
SANS = lambda s: load_font("NotoSans-Regular.ttf", s)

# (region, lead, detail, source) -- every story first reported
# on Sunday 22 November 2026; see MODEL.md for the source of each.
STORIES = [
    ("CLIMATE", "COP31 COLLAPSES",
     "UN summit in Antalya ends with no deal on fossil fuels.", "CNN"),
    ("CLIMATE", "LONGEST COP EVER",
     "Two days into overtime; first big breakdown since 2009.", "CNN"),
    ("CLIMATE", "GUTERRES: 'DEEPLY DISAPPOINTING'",
     "UN chief condemns the failure as 194 nations split.", "UN"),
    ("THE GULF & MIDDLE EAST", "IRAN HITS BAHRAIN SITE",
     "Iranian projectiles hit a civilian plant in Sitra; 2 hurt.", "Reuters"),
    ("THE GULF & MIDDLE EAST", "TANKERS HIT AT HORMUZ",
     "Two tankers struck near the strait; a third burned Friday.", "UKMTO"),
    ("THE GULF & MIDDLE EAST", "US BLOCKADE, DAY 130",
     "Saturday was day 130 of the US naval blockade of Iran.", "AP"),
    ("THE GULF & MIDDLE EAST", "TRUMP: IRAN WANTS A DEAL",
     "Trump says Tehran seeks a deal; he wants it permanent.", "AP"),
    ("THE GULF & MIDDLE EAST", "GAZA STRIKE WOUNDS ONE",
     "Israeli airstrike in north Gaza leaves one critically hurt.", "AP"),
    ("THE GULF & MIDDLE EAST", "SETTLERS TORCH CARS",
     "Settlers burn 12 cars in 4 villages; Israel opens inquiry.", "AP"),
    ("THE GULF & MIDDLE EAST", "EISENKOT: 'JEWISH TERRORISM'",
     "Opposition leader condemns settler attacks as talks stall.", "AP"),
    ("THE GULF & MIDDLE EAST", "EISENKOT COURTS LIKUD",
     "PM-designate invites Likud into coalition talks.", "AP"),
    ("THE GULF & MIDDLE EAST", "YEMEN FIRE EXCHANGED",
     "Saudis and Houthis trade fire; 149 Houthis hit, army says.", "AP"),
    ("UKRAINE WAR", "DRONES HIT SHIP IN LIBYA",
     "Suspected Ukrainian sea drones hit a Russian corvette.", "AP"),
    ("UKRAINE WAR", "FLATS HIT NEAR KYIV",
     "Drone hits Dymer flats; 2 killed, 4 hurt, 14 missing.", "AP"),
    ("UKRAINE WAR", "MISSILE HITS KRYVYI RIH",
     "Strike on Zelenskyy's home town kills two; 60 are hurt.", "AP"),
    ("UKRAINE WAR", "RUSSIAN SHIP STILL BURNING",
     "Sanctioned ship Sparta II burns a day after a drone hit.", "Reuters"),
    ("UKRAINE WAR", "MISSILES LAND IN POLAND",
     "Missiles land amid drills; NATO calls it a violation.", "AP"),
    ("UKRAINE WAR", "RUSSIA REVIVES OLD DEMANDS",
     "Moscow seizes on a US offer to restate Cold War-era terms.", "AP"),
    ("UKRAINE WAR", "DRONES HIT KHARTOUM",
     "Strikes damage a UN building in Khartoum, staff inside.", "Reuters"),
    ("EUROPE", "UK-EU CLOSER TIES",
     "Easier food trade, youth mobility, linked carbon markets.", "UK govt"),
    ("EUROPE", "DENMARK EXPELS RUSSIAN",
     "Official expelled after a plot to kill a rapper is foiled.", "AP"),
    ("EUROPE", "POLAND: TWO MURDER PLOTS",
     "Warsaw says Russia twice tried to kill the rapper.", "AP"),
    ("EUROPE", "SPAIN VOTE LOOMS",
     "Spain heads for uncertainty before its 29 November vote.", "AP"),
    ("EUROPE", "FRANCE STRIKES, WEEK SIX",
     "Wage strikes enter a sixth week; police respond in Paris.", "AP"),
    ("ASIA & PACIFIC", "INDONESIA FACTORY FIRE",
     "Cikande candy factory blaze kills 3; 37 workers missing.", "AP"),
    ("ASIA & PACIFIC", "QUAKE HITS INDONESIA",
     "A 7.2-magnitude quake strikes; no tsunami warning issued.", "AP"),
    ("ASIA & PACIFIC", "LAHORE CHOKES",
     "Lahore again tops world pollution ranking; AQI over 500.", "AP"),
    ("ASIA & PACIFIC", "NEPAL PM HEADS TO DELHI",
     "PM Shah to raise border issues on his first India visit.", "AP"),
    ("ASIA & PACIFIC", "CHINA-JAPAN STRAIN",
     "Ties fray over Taiwan and critical minerals.", "AP"),
    ("ASIA & PACIFIC", "EU-INDONESIA TRADE DEAL",
     "Decade of talks ends; tariffs scrapped on 98.5% of goods.", "AP"),
    ("AFRICA", "NIGERIA BOAT SINKS",
     "Mourners' boat capsizes in Bayelsa; at least 24 dead.", "Al Jazeera"),
    ("AFRICA", "ROHINGYA WELCOME VERDICT",
     "Refugees welcome the UN court genocide ruling on Myanmar.", "AP"),
    ("AFRICA", "BURHAN VOWS TO FIGHT ON",
     "Sudan's army chief plays down RSF gains in Blue Nile.", "AP"),
    ("AFRICA", "MLAMBO-NGCUKA DIES AT 71",
     "Ex-South African deputy president and UN Women chief dies.", "AP"),
    ("THE AMERICAS", "'EL CHAPO ISIDRO' SEIZED",
     "Cartel boss seized in Sinaloa; 11 killed, four soldiers.", "AP"),
    ("THE AMERICAS", "FBI PROBES 2ND BREACH",
     "FBI probes hack of crime database, the second in months.", "AP"),
    ("THE AMERICAS", "TRUMP ON FBI HACK",
     "Trump: breach 'not good' but may offer benefits.", "AP"),
    ("THE AMERICAS", "SALVADORANS KILLED IN HAITI",
     "Troops killed handling explosives; first mission deaths.", "AP"),
    ("THE AMERICAS", "LEBANON SEIZES EXPLOSIVES",
     "Army arrests three over 264 kg of trafficked explosives.", "AP"),
    ("THE AMERICAS", "PAKISTAN FEUD KILLS 7",
     "Seven dead as a forest feud turns to gunfire.", "AP"),
    ("TECH & SCIENCE", "BEPICOLOMBO AT MERCURY",
     "ESA-JAXA craft in orbit after 8 years; thruster glitch.", "Reuters"),
    ("TECH & SCIENCE", "SIGNAL BLOCKS AI SNOOPS",
     "Messenger blocks AI assistants from reading private chats.", "Reuters"),
    ("TECH & SCIENCE", "NO RULES FOR ROBOT WEAPONS",
     "UN talks on robot weapons end with no binding rules.", "AP"),
    ("TECH & SCIENCE", "AFGHAN WOMEN GO DIGITAL",
     "Afghan women turn to online work as in-person jobs dry up.", "AP"),
    ("SPORT", "LIVERPOOL 4-0 MAN UTD",
     "Yoro off after 8 min; Szoboszlai, Wirtz, Ngumoha, Munoz net.", "NBC"),
    ("SPORT", "BOCA LIFT SUDAMERICANA",
     "Boca Juniors beat Atletico Mineiro 2-0 to win the final.", "AP"),
    ("SPORT", "ATALANTA 4-4 INTER",
     "Atalanta fight back from 2-4 down in a Serie A thriller.", "AP"),
    ("SPORT", "GEORGIA INTO SEC FINAL",
     "No. 1 Georgia beat South Carolina 34-6 to reach the title game.", "AP"),
    ("SPORT", "INDIANA STUNNED IN OT",
     "No. 6 Indiana fall 27-24 at Washington; playoff hopes dented.", "AP"),
    ("SPORT", "TCU SACKS DYKES",
     "TCU fires coach Sonny Dykes four years after a title-game run.", "AP"),
]

# (approx UTC time, moment) -- times are first-report times, approximate.
TIMELINE = [
    ("~03:00", "Drones hit UN building, Khartoum"),
    ("~07:00", "BepiColombo burn cut short"),
    ("09:31", "ESA confirms Mercury orbit"),
    ("~11:00", "Drone hits flats near Kyiv"),
    ("~13:00", "'El Chapo Isidro' captured"),
    ("~15:00", "COP31 collapses, no deal"),
    ("15:24", "Nigeria boat toll hits 24"),
    ("~18:30", "Liverpool 4-0 Man Utd"),
]

SOURCES = ("AP, Reuters, CNN, Al Jazeera, Le Monde, WSJ, ESA, UN, "
           "UKMTO, NEMA, NBC, UK government")


def wrap(draw, text, font, width):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def column_height(draw, stories, col_w, lead_f, body_f, region_f, lh, gap):
    """Total pixels a column of stories needs, region headers included."""
    total, last_region = 0, None
    for region, lead, detail, _src in stories:
        if region != last_region:
            total += 16
            last_region = region
        total += len(wrap(draw, lead, lead_f, col_w)) * lh
        total += len(wrap(draw, detail, body_f, col_w)) * lh
        total += gap
    return total


def draw_globe(draw, box):
    """Flat illustration: a cracked globe under a hot sun."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    r = 58
    for k in range(12):
        ang = math.pi * 2 * k / 12
        x_a = cx + int(math.cos(ang) * (r + 8))
        y_a = cy + int(math.sin(ang) * (r + 8))
        x_b = cx + int(math.cos(ang) * (r + 20))
        y_b = cy + int(math.sin(ang) * (r + 20))
        draw.line([x_a, y_a, x_b, y_b], fill=RED, width=4)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 214, 226),
                 outline=NAVY, width=3)
    for dx in (-30, 0, 30):
        draw.arc([cx - r + dx, cy - r, cx + r + dx, cy + r],
                 start=270, end=90, fill=NAVY, width=2)
        draw.arc([cx - r + dx, cy - r, cx + r + dx, cy + r],
                 start=90, end=270, fill=NAVY, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    draw.ellipse([cx - 40, cy - 36, cx - 8, cy - 6], fill=(94, 148, 84))
    draw.ellipse([cx + 6, cy + 8, cx + 40, cy + 38], fill=(94, 148, 84))
    draw.ellipse([cx - 16, cy + 16, cx + 12, cy + 40], fill=(120, 170, 100))
    draw.line([cx - 36, cy - 48, cx - 16, cy - 18, cx - 30, cy + 6,
               cx - 6, cy + 32, cx - 18, cy + 52], fill=RED, width=4)
    draw.text((cx, y1 - 14), "THE WORLD, DIVIDED",
              font=SANS_B(11), fill=RED, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26
    cw = W - 2 * mx  # 972

    # ---- masthead ----
    d.text((W // 2, 26), "ONE DAY  ·  THE WHOLE WORLD  ·  50 STORIES",
           font=SANS_B(13), fill=GREY, anchor="ma")
    d.text((W // 2, 48), "THE SUNDAY GLOBE",
           font=SERIF_B(60), fill=INK, anchor="ma")
    d.line([mx, 116, W - mx, 116], fill=INK, width=3)
    d.line([mx, 121, W - mx, 121], fill=INK, width=1)
    d.text((mx, 130), "SUNDAY 22 NOVEMBER 2026",
           font=SANS_B(15), fill=RED, anchor="la")
    d.text((W - mx, 130), "ANTALYA · BENGHAZI · BAHRAIN · KYIV · MEXICO CITY",
           font=SANS_B(12), fill=INK, anchor="ra")

    # ---- lead story ----
    ly = 158
    d.text((mx, ly), "CLIMATE TALKS COLLAPSE",
           font=SERIF_B(44), fill=INK, anchor="la")
    d.text((mx, ly + 50), "COP31 ends with no deal as the EU rejects a pact",
           font=SERIF(20), fill=INK, anchor="la")
    d.text((mx, ly + 76), "that never mentions fossil fuels",
           font=SERIF(20), fill=INK, anchor="la")
    standfirst = ("After two weeks in Antalya and two days of overtime, nearly 200 "
                  "nations walked away without an overarching climate agreement — "
                  "the longest COP in history.")
    y = ly + 106
    for line in wrap(d, standfirst, SANS(13), 600):
        d.text((mx, y), line, font=SANS(13), fill=INK, anchor="la")
        y += 17
    draw_globe(d, (660, 158, 998, 316))
    d.line([mx, 322, W - mx, 322], fill=RULE, width=1)

    # ---- stories header ----
    d.rectangle([mx, 332, W - mx, 360], fill=DARK)
    d.text((mx + 10, 338), "THE DAY IN 50 STORIES",
           font=SANS_B(14), fill=PAPER, anchor="la")
    d.text((W - mx - 10, 338), "ALL FIRST REPORTED SUNDAY 22 NOVEMBER 2026",
           font=SANS_B(11), fill=PAPER, anchor="ra")

    # ---- story columns (auto-fit the type size) ----
    col_w = 304
    col_x = [mx, mx + col_w + 30, mx + 2 * (col_w + 30)]
    per_col = [17, 17, 16]
    top, bottom_limit = 370, 876
    avail = bottom_limit - top
    chosen = None
    for size, lh in ((11, 13), (10.5, 12.5), (10, 12), (9.5, 11.5)):
        lead_f, body_f = SANS_B(size), SANS(size)
        region_f = SANS_B(max(9, size - 1))
        idx = 0
        heights = []
        for ci in range(3):
            chunk = STORIES[idx:idx + per_col[ci]]
            idx += per_col[ci]
            heights.append(column_height(d, chunk, col_w, lead_f, body_f,
                                         region_f, lh, 2))
        if max(heights) <= avail:
            chosen = (size, lh, lead_f, body_f, region_f)
            print("fit at story font %.1f, line height %.1f; col heights %s"
                  % (size, lh, heights))
            break
    assert chosen, "no story font size fits"
    size, lh, lead_f, body_f, region_f = chosen
    idx = 0
    for ci in range(3):
        x = col_x[ci]
        y = top
        last_region = None
        for _ in range(per_col[ci]):
            region, lead, detail, _src = STORIES[idx]
            idx += 1
            if region != last_region:
                d.text((x, y), region, font=region_f, fill=RED, anchor="la")
                d.line([x, y + 12, x + col_w, y + 12], fill=RULE, width=1)
                y += 16
                last_region = region
            num = "%02d" % idx
            for ln in wrap(d, "%s  %s" % (num, lead), lead_f, col_w):
                d.text((x, y), ln, font=lead_f, fill=INK, anchor="la")
                y += lh
            for ln in wrap(d, detail, body_f, col_w):
                d.text((x, y), ln, font=body_f, fill=INK, anchor="la")
                y += lh
            y += 2
        assert y <= bottom_limit + 1, "column %d overflowed" % ci

    # ---- timeline strip ----
    ty = 880
    d.rectangle([mx, ty, W - mx, ty + 66], fill=NAVY)
    d.text((mx + 10, ty + 6), "THE DAY IN UTC — FIRST REPORTS (TIMES APPROXIMATE)",
           font=SANS_B(11), fill=(255, 255, 255), anchor="la")
    cell_w = cw // 4
    for i, (t, moment) in enumerate(TIMELINE):
        cx = mx + (i % 4) * cell_w + 10
        cy = ty + 24 + (i // 4) * 22
        d.text((cx, cy), t, font=SANS_B(10), fill=(255, 214, 90), anchor="la")
        d.text((cx + 52, cy), moment, font=SANS(10),
               fill=(255, 255, 255), anchor="la")

    # ---- footer: date check + sources ----
    fy = 958
    d.line([mx, fy, W - mx, fy], fill=INK, width=2)
    d.text((W // 2, fy + 8),
           "DATE CHECK: All 50 stories were first reported on Sunday 22 November 2026.",
           font=SANS_B(12), fill=INK, anchor="ma")
    d.text((W // 2, fy + 28),
           "Sources: " + SOURCES + ".",
           font=SANS(10), fill=GREY, anchor="ma")
    d.text((W // 2, fy + 44),
           "50 stories · 7 regions · 10 fields · The Sunday Globe",
           font=SANS_B(10), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote %s (%d bytes, %d stories)" % (out, size, len(STORIES)))
    assert size <= 1048576, "PNG over 1 MiB"
    assert len(STORIES) == 50


if __name__ == "__main__":
    main()
