"""Neon motion graphics for the NCAA cross country documentary.

Same look as the Drummond doc (tools/neon.py background + bloom). The caller sets neon.PHOTOS and M.finish = neon.finish.
Every graphic is a function (t, dur) -> PIL image, registered in GRAPHICS.
Comment cards quote real YouTube comments (comment_receipts.json); usernames are never shown."""
import math, sys
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageDraw, ImageFilter
import mograph as M
from mograph import text, eo, eback, seg
import gfx
import neon as N
from neon import CYAN, PINK, ORANGE, WHITE, neon_photo

N.TAG = "XC//FILE"
background = N.background
W, H = 1920, 1080
GREY = (150, 156, 170)
GREEN = (60, 230, 140)
RED = (255, 60, 80)

def ph(name): return f"{N.PHOTOS}/{name}.jpg"

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def panel(d, box, col=CYAN, k=1.0, fill=(8, 10, 20, 225)):
    x0, y0, x1, y1 = box
    x1 = x0 + (x1 - x0) * k
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=col + (255,), width=3)
    d.rectangle([x0, y0, x0 + 8, y1], fill=col + (255,))

def kicker(d, t, s, x=110, y=96, col=ORANGE):
    k = eo(seg(t, 0, 0.4))
    d.text((x, y), s.upper(), font=N.mono(28), fill=col + (int(255 * k),))
    d.rectangle([x, y + 42, x + int(160 * eo(seg(t, 0.1, 0.5))), y + 47], fill=col)

def typed(s, t, t0, cps=40):
    n = int(max(0, t - t0) * cps)
    return s[:n]

def big(d, xy, s, size, col=WHITE, anchor="la", weight="Black"):
    d.text(xy, s, font=gfx.font(weight, size), fill=col, anchor=anchor)

# ------------------------------------------------------------------ cold open
def title_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "NCAA DI Cross Country Championships", 110, 300)
    big(d, (110, 370), typed("COLUMBIA, MISSOURI", t, 0.2, 30), 110)
    k = eo(seg(t, 0.8, 1.3))
    d.text((114, 520), "NOV 22 · 2025 · GANS CREEK", font=N.mono(40), fill=CYAN + (int(255 * k),))
    return im

RESULTS = [("1", "HABTOM SAMUEL", "ERI", "NEW MEXICO", 0.0), ("2", "ROCKY HANSEN", "USA", "WAKE FOREST", 2.9),
           ("3", "SOLOMON KIPCHOGE", "KEN", "WASHINGTON ST", 6.0), ("4", "BRIAN MUSAU", "KEN", "OKLAHOMA ST", 7.7),
           ("5", "FOUAD MESSAOUDI", "MAR", "OKLAHOMA ST", 9.2), ("6", "DENIS KIPNGETICH", "KEN", "OKLAHOMA ST", 10.6)]
FLAGCOL = {"ERI": (65, 170, 255), "USA": (255, 255, 255), "KEN": GREEN, "MAR": RED}

def results(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "2025 NCAA XC · Men's 10K · Official results")
    for i, (pos, name, nat, school, t0) in enumerate(RESULTS):
        k = eback(seg(t, t0 + 0.05, t0 + 0.45))
        if k <= 0: continue
        y = 200 + i * 128
        col = FLAGCOL[nat]
        panel(d, [110, y, 1810, y + 108], col if nat != "USA" else CYAN, min(1, k))
        if k > 0.6:
            big(d, (160, y + 54), pos, 70, ORANGE, "lm")
            big(d, (270, y + 54), name, 60, WHITE, "lm")
            d.rounded_rectangle([1240, y + 26, 1380, y + 82], 8, fill=col + (60,), outline=col + (255,), width=3)
            d.text((1310, y + 54), nat, font=N.mono(38), fill=col + (255,), anchor="mm")
            d.text((1420, y + 54), school, font=N.mono(30), fill=GREY + (255,), anchor="lm")
    return im

# ------------------------------------------------------------------ YouTube comment cards (real comments)
COMMENTS = {
    "c_guests": ("Should only be open to Americans. Not guests.", None),
    "c_30plus": ("What's crazy is that an Eritrean, that could easily be 30+ years old, with no birth certificate, from a corrupt government, takes the scholarship of an American…", None),
    "c_congrats": ("Congratulations to the African team representing Oklahoma state university", "59"),
    "c_corrupt": ("Disagree. A foreigner from a corrupt country, with no birth certificate, doesn't deserve to take a scholarship from an American, let alone an NCAA D1 title.", None),
    "c_imported": ("Almost all the athletes are imported from Africa and they have questionable birthdays…", None),
}

def comment_card(key):
    txt, likes = COMMENTS[key]
    def fn(t, dur):
        im = background(t); d = ImageDraw.Draw(im, "RGBA")
        kicker(d, t, "Real comment · official NCAA race video · Nov 2025", col=PINK)
        k = eback(seg(t, 0.1, 0.5))
        bx, by, bw = 230, 330, 1460
        f = gfx.font("SemiBold", 52)
        lines = wrap(d, txt, f, bw - 260)
        bh = 150 + 70 * len(lines)
        if k > 0:
            hh = bh * min(1, k)
            d.rounded_rectangle([bx, by, bx + bw, by + hh], 18, fill=(18, 18, 22, 245), outline=PINK + (255,), width=3)
            if k > 0.8:
                d.ellipse([bx + 50, by + 50, bx + 140, by + 140], fill=(70, 72, 84))
                d.rounded_rectangle([bx + 180, by + 58, bx + 480, by + 92], 8, fill=(60, 62, 72))  # hidden username
                pass
                shown = typed(" ".join(lines), t, 0.6, 55); n = 0
                for i, l in enumerate(lines):
                    part = shown[n:n + len(l)]; n += len(l) + 1
                    d.text((bx + 180, by + 120 + i * 70), part, font=f, fill=WHITE)
                if likes:
                    d.text((bx + 180, by + bh - 50), f"LIKES: {likes}", font=N.mono(30), fill=GREY + (255,))
        d.text((W // 2, 1000), "USERNAME HIDDEN · TEXT UNEDITED", font=N.mono(22), fill=GREY + (160,), anchor="mm")
        return im
    return fn

# ------------------------------------------------------------------ "no rule broken"
def legal(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Eligibility check · 2025 NCAA XC")
    items = ["AGE LIMIT VIOLATED", "ELIGIBILITY RULE BROKEN", "NCAA BYLAW BROKEN"]
    for i, s in enumerate(items):
        k = eo(seg(t, 0.3 + i * 0.9, 0.7 + i * 0.9))
        if k <= 0: continue
        y = 260 + i * 150
        panel(d, [110, y, 1250, y + 112], CYAN, k)
        if k > 0.7:
            big(d, (160, y + 56), s, 52, WHITE, "lm")
            big(d, (1190, y + 56), "NO", 60, GREEN, "rm")
    k = eback(seg(t, 3.4, 3.8))
    if k > 0:
        s = 0.6 + 0.4 * min(1.1, k)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle([1340, 360, 1800, 600], 20, outline=GREEN + (255,), width=12)
        dl.text((1570, 480), "LEGAL", font=gfx.font("Black", int(110 * s)), fill=GREEN + (255,), anchor="mm")
        lay = lay.rotate(-9, center=(1570, 480))
        im.paste(lay, (0, 0), lay)
    return im

# ------------------------------------------------------------------ 1977
def cover1977(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.0, 0.5))
    x0, y0, w, h = 560, 120, 800, 840
    if k > 0:
        hh = int(h * min(1, k))
        d.rectangle([x0, y0, x0 + w, y0 + hh], fill=(236, 230, 214))
        N.NOBLOOM.append((x0, y0, x0 + w, y0 + hh))
        if k > 0.9:
            d.rectangle([x0, y0, x0 + w, y0 + 150], fill=(180, 30, 30))
            d.text((x0 + w // 2, y0 + 75), "TRACK & FIELD NEWS", font=gfx.font("Black", 64), fill=(255, 255, 255), anchor="mm")
            d.text((x0 + w // 2, y0 + 200), "APRIL 1977", font=N.mono(34), fill=(40, 40, 40), anchor="mm")
            hl = typed("FOREIGNERS\nDOMINATE\nNCAA", t, 0.9, 18)
            for i, l in enumerate(hl.split("\n")):
                d.text((x0 + w // 2, y0 + 360 + i * 150), l, font=gfx.font("Black", 112), fill=(20, 20, 20), anchor="mm")
            d.text((x0 + w // 2, y0 + h - 40), "COVER HEADLINE · RECREATED", font=N.mono(22), fill=(110, 110, 110), anchor="mm")
    return im

def rono_stats(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    neon_photo(im, ph("p_rono"), 470, 520, 700, t, 0.0, ORANGE, "Henry Rono", "Washington State", crop=(0.5, 0.4, 0.95))
    kicker(d, t, "NCAA XC champion", 900, 220)
    for i, yr in enumerate(["'76", "'77", "'79"]):
        k = eback(seg(t, 0.6 + i * 1.2, 1.0 + i * 1.2))
        if k > 0: big(d, (900 + i * 300, 300), yr, int(150 * min(1.05, k)), WHITE)
    k = eo(seg(t, 4.8, 5.3))
    if k > 0:
        panel(d, [900, 600, 1810, 820], CYAN, k)
        if k > 0.7:
            n = int(4 * eo(seg(t, 5.0, 5.8)))
            big(d, (950, 640), f"{n} WORLD RECORDS", 74, WHITE)
            d.text((954, 745), "IN 81 DAYS · 1978 · STILL IN COLLEGE", font=N.mono(32), fill=CYAN + (255,))
    return im

def fifty_years(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.2, 2.5))
    d.line([(200, 560), (200 + 1520 * k, 560)], fill=ORANGE, width=8)
    big(d, (200, 620), "1977", 80, WHITE, "la")
    if k > 0.95: big(d, (1720, 620), "2025", 80, WHITE, "ra")
    big(d, (960, 330), "50 YEARS", 150, ORANGE, "mm")
    k2 = eo(seg(t, 4.3, 4.8))
    if k2 > 0:
        d.text((960, 830), "SOMEBODY BEEN MAD THE WHOLE TIME", font=N.mono(40), fill=PINK + (int(255 * k2),), anchor="mm")
    return im

# ------------------------------------------------------------------ Kipchoge / age
def kipchoge_file(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Subject file · Fall 2024")
    big(d, (110, 190), typed("SOLOMON KIPCHOGE", t, 0.2, 30), 110)
    rows = [("SCHOOL", "TEXAS TECH (LATER WASHINGTON STATE)"), ("CLASS", "FRESHMAN"), ("HALF MARATHON", "59:37 · LILLE 2023")]
    for i, (a, b) in enumerate(rows):
        k = eo(seg(t, 0.9 + i * 0.4, 1.3 + i * 0.4))
        if k > 0:
            d.text((114, 400 + i * 90), a, font=N.mono(30), fill=GREY + (int(255 * k),))
            big(d, (480, 392 + i * 90), b, 46, WHITE)
    k = eback(seg(t, 2.6, 3.1))
    if k > 0:
        d.text((1500, 820), "AGE", font=N.mono(40), fill=ORANGE + (255,), anchor="mm")
        big(d, (1500, 680), "28", int(260 * min(1.05, k)), ORANGE, "mm")
    return im

def age_limit(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "College admissions · age limit")
    k = eback(seg(t, 2.3, 2.8))
    if k > 0 and t > 2.3: big(d, (960, 340), "NONE", int(220 * min(1.05, k)), GREEN, "mm")
    for i, a in enumerate(["18", "28", "58"]):
        kk = eback(seg(t, 4.6 + i * 0.6, 5.0 + i * 0.6))
        if kk <= 0: continue
        x = 480 + i * 480
        panel(d, [x - 180, 600, x + 180, 900], CYAN, min(1, kk))
        if kk > 0.7:
            big(d, (x, 720), a, 130, WHITE, "mm")
            d.text((x, 850), "WELCOME", font=N.mono(30), fill=GREEN + (255,), anchor="mm")
    return im

def eligibility(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "NCAA rule · before 2026 · same for everybody")
    rows = [("4", "SEASONS OF COMPETITION"), ("5", "YEARS TO USE THEM"), ("→", "CLOCK STARTS WHEN YOU ENROLL")]
    for i, (a, b) in enumerate(rows):
        k = eback(seg(t, (1.4, 2.8, 4.4)[i], (1.4, 2.8, 4.4)[i] + 0.4))
        if k <= 0: continue
        y = 250 + i * 210
        panel(d, [110, y, 1810, y + 170], ORANGE if i < 2 else CYAN, min(1, k))
        if k > 0.7:
            big(d, (230, y + 85), a, 110, ORANGE if i < 2 else CYAN, "mm")
            big(d, (360, y + 85), b, 70, WHITE, "lm")
    return im

def same_rule(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Same rule · who uses it")
    items = [("2-YEAR CHURCH MISSION", 3.0), ("MILITARY FIRST", 5.7), ("EXTRA COVID YEAR", 7.6)]
    for i, (s, t0) in enumerate(items):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 240 + i * 150
        panel(d, [110, y, 1100, y + 115], CYAN, k)
        if k > 0.7:
            big(d, (160, y + 58), s, 54, WHITE, "lm")
            d.text((1060, y + 58), "AMERICANS: OK", font=N.mono(28), fill=GREEN + (255,), anchor="rm")
    k = eback(seg(t, 9.8, 10.3))
    if k > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle([1180, 380, 1820, 640], 20, outline=ORANGE + (255,), width=10)
        dl.text((1500, 470), "\"INSPIRING", font=gfx.font("Black", 78), fill=ORANGE + (255,), anchor="mm")
        dl.text((1500, 560), "COMEBACK\"", font=gfx.font("Black", 78), fill=ORANGE + (255,), anchor="mm")
        lay = lay.rotate(-6, center=(1500, 510))
        im.paste(lay, (0, 0), lay)
    return im

def quote_card(kick, quote, who, col=ORANGE, photo=None, crop=(0.5, 0.4, 0.95)):
    def fn(t, dur):
        im = background(t); d = ImageDraw.Draw(im, "RGBA")
        kicker(d, t, kick, col=col)
        x = 110
        if photo:
            neon_photo(im, ph(photo), 420, 560, 620, t, 0.0, col, who, None, crop=crop)
            x = 800
        f = gfx.font("Black", 70)
        lines = wrap(d, quote, f, 1810 - x)
        shown = typed(quote, t, 0.5, 34); n = 0
        for i, l in enumerate(lines):
            part = shown[n:n + len(l)]; n += len(l) + 1
            d.text((x, 290 + i * 92), part, font=f, fill=WHITE)
        if not photo:
            k = eo(seg(t, 1.2, 1.6))
            if k > 0: d.text((x, 330 + len(lines) * 92), "— " + who.upper(), font=N.mono(36), fill=col + (int(255 * k),))
        d.text((x - 10, 90), "“", font=gfx.font("Black", 200), fill=col + (120,))
        return im
    return fn

def third_place(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "2025 NCAA XC · Men's 10K")
    k = eback(seg(t, 0.2, 0.7))
    if k > 0: big(d, (960, 430), "3RD", int(260 * min(1.05, k)), ORANGE, "mm")
    k2 = eo(seg(t, 0.9, 1.3))
    if k2 > 0:
        d.text((960, 640), "SOLOMON KIPCHOGE · WASHINGTON STATE", font=N.mono(44), fill=WHITE + (int(255 * k2),), anchor="mm")
        d.text((960, 720), "28:40.1", font=N.mono(44), fill=CYAN + (int(255 * k2),), anchor="mm")
    k3 = eback(seg(t, 3.6, 4.0))
    if k3 > 0: big(d, (960, 870), "BY THE RULES", int(84 * min(1.05, k3)), GREEN, "mm")
    return im

# ------------------------------------------------------------------ better situation
def offer(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "The offer")
    items = ["FREE TUITION", "HOUSING", "FOOD", "MEDICAL", "REAL COACHING", "A DEGREE · FOR LIFE"]
    starts = [2.1, 3.6, 4.4, 5.0, 5.8, 6.9]
    for i, (s, t0) in enumerate(zip(items, starts)):
        k = eo(seg(t, t0, t0 + 0.3))
        if k <= 0: continue
        col_ = i % 2; row = i // 2
        x = 110 + col_ * 860; y = 220 + row * 220
        panel(d, [x, y, x + 800, y + 170], GREEN, k)
        if k > 0.7:
            d.text((x + 50, y + 85), "✓", font=N.mono(80), fill=GREEN + (255,), anchor="lm")
            big(d, (x + 150, y + 85), s, 58, WHITE, "lm")
    return im

def pipeline(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Why now")
    rows = [("RECRUITING SERVICES", "e.g. SCHOLARBOOK → TIMES + VIDEO TO COACHES", 1.8),
            ("SAT / ACT", "REQUIREMENT DROPPED · PERMANENT IN 2023", 6.4),
            ("SCHOLARSHIPS", "NOW COVER THE FULL COST OF ATTENDANCE", 10.1)]
    for i, (a, b, t0) in enumerate(rows):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 230 + i * 230
        panel(d, [110, y, 1810, y + 190], CYAN, k)
        if k > 0.7:
            big(d, (160, y + 60), a, 66, WHITE, "lm")
            d.text((164, y + 140), b, font=N.mono(32), fill=CYAN + (255,), anchor="lm")
    return im

def share(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Foreign-born runners · one recent NCAA XC final · LetsRun count")
    for i, (lab, pct, t0) in enumerate([("MEN", 43, 1.3), ("WOMEN", 38, 3.6)]):
        k = eo(seg(t, t0, t0 + 1.0))
        cx = 560 + i * 800; cy = 560; r = 250
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 44, 60), width=40)
        if k > 0:
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * pct / 100 * k, fill=ORANGE if i == 0 else CYAN, width=40)
            big(d, (cx, cy - 10), f"{int(pct * k)}%", 140, WHITE, "mm")
            d.text((cx, cy + 100), lab, font=N.mono(40), fill=GREY + (255,), anchor="mm")
    return im

def went_got(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.0, 0.4))
    if k > 0: big(d, (960, 420), "THEY DIDN'T SNEAK IN.", int(96 * min(1.05, k)), WHITE, "mm")
    k2 = eback(seg(t, 1.9, 2.3))
    if k2 > 0: big(d, (960, 600), "THEY GOT RECRUITED.", int(110 * min(1.05, k2)), ORANGE, "mm")
    return im

# ------------------------------------------------------------------ the hate
def two_groups(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Two kinds of mad")
    for i, (a, b, col, t0) in enumerate([("1 · COACHES", "WANT THE RULES CHANGED", CYAN, 0.2), ("2 · A CROWD ONLINE", "GOING AFTER THE ATHLETES", PINK, 1.6)]):
        k = eback(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        x = 110 + i * 870
        panel(d, [x, 300, x + 830, 760], col, min(1, k))
        if k > 0.7:
            big(d, (x + 50, 400), a, 64, col)
            for j, l in enumerate(wrap(d, b, gfx.font("Black", 58), 720)):
                big(d, (x + 50, 520 + j * 80), l, 58, WHITE)
    return im

def imported(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.0, 0.35))
    if k > 0: big(d, (960, 470), "IMPORTED.", int(230 * min(1.05, k)), PINK, "mm")
    k2 = eo(seg(t, 1.0, 1.4))
    if k2 > 0: d.text((960, 680), "LIKE THEY CARGO.", font=N.mono(56), fill=WHITE + (int(255 * k2),), anchor="mm")
    return im

def no_rule(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Searching the comments for a rule")
    panel(d, [110, 220, 1810, 340], CYAN, eo(seg(t, 0.1, 0.5)))
    q = typed("eligibility rule OR bylaw OR age violation", t, 0.4, 30)
    d.text((170, 280), "> " + q, font=N.mono(44), fill=WHITE, anchor="lm")
    k = eback(seg(t, 2.2, 2.6))
    if k > 0: big(d, (960, 520), "0 RESULTS", int(150 * min(1.05, k)), PINK, "mm")
    tags = [("AGE · NO PROOF", 5.6), ("THEIR COUNTRY", 7.8), ("\"DON'T BELONG\"", 9.4)]
    for i, (s, t0) in enumerate(tags):
        kk = eo(seg(t, t0, t0 + 0.3))
        if kk > 0:
            x = 200 + i * 540
            d.rounded_rectangle([x, 720, x + 480, 820], 14, outline=PINK + (255,), width=4, fill=(30, 8, 16, 220))
            d.text((x + 240, 770), s, font=N.mono(36), fill=WHITE, anchor="mm")
    return im

def sports_grid(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "International athletes in college sports")
    sp = [("BASKETBALL", 4.6), ("TENNIS", 5.2), ("GOLF", 5.8), ("SWIMMING", 6.4), ("SPRINTS", 7.1), ("DISTANCE", 12.5)]
    for i, (s, t0) in enumerate(sp):
        k = eback(seg(t, t0, t0 + 0.35))
        if k <= 0: continue
        col_ = i % 3; row = i // 3
        x = 140 + col_ * 560; y = 240 + row * 340
        hot = i == 5
        panel(d, [x, y, x + 520, y + 280], PINK if hot else CYAN, min(1, k))
        if k > 0.7:
            big(d, (x + 260, y + 110), s, 56, WHITE, "mm")
            d.text((x + 260, y + 205), "THE OUTRAGE" if hot else "QUIET", font=N.mono(32), fill=(PINK if hot else GREY) + (255,), anchor="mm")
    return im

# ------------------------------------------------------------------ doping
def cases(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "The real cases · no hiding them")
    rows = [("NOV 2024 · TULANE", "12TH AT NATIONALS WHILE PROVISIONALLY SUSPENDED IN KENYA", 0.3),
            ("SPRING 2025 · TCU", "KENYAN ATHLETE PULLED FROM NATIONALS OVER A PROVISIONAL SUSPENSION", 7.0)]
    for i, (a, b, t0) in enumerate(rows):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 260 + i * 300
        panel(d, [110, y, 1810, y + 240], PINK, k)
        if k > 0.7:
            big(d, (160, y + 70), a, 64, PINK, "lm")
            for j, l in enumerate(wrap(d, b, N.mono(36), 1560)):
                d.text((164, y + 140 + j * 46), l, font=N.mono(36), fill=WHITE)
    return im

def category_a(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "World Athletics · Category A · highest doping risk")
    fed = ["KENYA", "ETHIOPIA", "NIGERIA", "UKRAINE", "BAHRAIN", "BELARUS"]
    for i, s in enumerate(fed):
        k = eo(seg(t, 1.6 + i * 0.25, 1.9 + i * 0.25))
        if k <= 0: continue
        x = 110 + (i % 3) * 570; y = 220 + (i // 3) * 130
        panel(d, [x, y, x + 530, y + 100], PINK if i == 0 else CYAN, k)
        if k > 0.7: big(d, (x + 40, y + 50), s, 54, WHITE, "lm")
    k = eo(seg(t, 10.0, 10.5))
    if k > 0:
        panel(d, [110, 520, 1810, 700], ORANGE, k)
        if k > 0.7:
            big(d, (160, 575), "3+ SURPRISE OUT-OF-COMPETITION TESTS", 56, WHITE, "lm")
            d.text((164, 650), "IN THE 10 MONTHS BEFORE AN OLYMPICS OR WORLDS · PARIS 2024 AVG: ~7 PER KENYAN/ETHIOPIAN ATHLETE", font=N.mono(25), fill=ORANGE + (255,), anchor="lm")
    return im

def usa_not(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "World Athletics · Category A")
    k = eback(seg(t, 0.1, 0.5))
    if k > 0: big(d, (960, 420), "USA", int(220 * min(1.05, k)), WHITE, "mm")
    k2 = eo(seg(t, 1.2, 1.6))
    if k2 > 0: d.text((960, 640), "NOT ON THE LIST", font=N.mono(80), fill=GREEN + (int(255 * k2),), anchor="mm")
    return im

def tests_compare(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Who gets looked at")
    for i in range(7):
        k = eback(seg(t, 1.3 + i * 0.25, 1.6 + i * 0.25))
        if k <= 0: continue
        x = 200 + i * 110
        d.rounded_rectangle([x, 560 - 220 * min(1, k), x + 70, 560], 30, outline=PINK + (255,), width=6, fill=(255, 46, 99, 60))
    big(d, (550, 640), "TESTED A LOT", 56, PINK, "mm")
    k = eo(seg(t, 3.3, 3.8))
    if k > 0:
        x = 1330
        d.rounded_rectangle([x, 340, x + 70, 560], 30, outline=CYAN + (int(255 * k),), width=6)
        big(d, (x + 35, 640), "TESTED LESS", 56, CYAN, "mm")
    k2 = eo(seg(t, 7.4, 7.9))
    if k2 > 0:
        d.text((960, 820), "MORE TESTS → MORE CATCHES", font=N.mono(48), fill=WHITE + (int(255 * k2),), anchor="mm")
        d.text((960, 890), "ILLUSTRATION", font=N.mono(22), fill=GREY + (160,), anchor="mm")
    return im

def exum(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "2003 · The Exum files · former USOC drug-control director")
    for i in range(10):
        k = eo(seg(t, 0.1 + i * 0.08, 0.4 + i * 0.08))
        if k <= 0: continue
        x, y = 200 + i * 10, 620 - i * 26
        d.rectangle([x, y, x + 560, y + 30], fill=(232, 228, 218, int(255 * k)), outline=(120, 120, 120))
    N.NOBLOOM.append((190, 380, 860, 660))
    k = eo(seg(t, 3.4, 3.9))
    if k > 0:
        big(d, (480, 760), f"{int(30000 * eo(seg(t, 3.4, 4.6))):,}", 90, WHITE, "mm")
        d.text((480, 840), "PAGES", font=N.mono(36), fill=GREY + (255,), anchor="mm")
    rows = [("100+", "U.S. POSITIVE TESTS · 1988–2000", 8.3), ("STILL", "ALLOWED TO COMPETE", 13.2), ("19", "OLYMPIC MEDALS WON BY THEM", 15.8)]
    for i, (a, b, t0) in enumerate(rows):
        kk = eo(seg(t, t0, t0 + 0.4))
        if kk <= 0: continue
        y = 280 + i * 190
        panel(d, [980, y, 1810, y + 160], ORANGE, kk)
        if kk > 0.7:
            big(d, (1030, y + 80), a, 76, ORANGE, "lm")
            d.text((1260, y + 80), b, font=N.mono(28), fill=WHITE, anchor="lm")
    return im

def lewis(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    neon_photo(im, ph("p_lewis"), 430, 520, 680, t, 0.0, CYAN, "Carl Lewis", "USA", crop=(0.5, 0.35, 0.85))
    kicker(d, t, "1988 U.S. Olympic Trials · per the Exum files", 860, 200)
    rows = [("POSITIVE", "PSEUDOEPHEDRINE · EPHEDRINE · PHENYLPROPANOLAMINE", 0.6),
            ("RULING", "CLEARED ON APPEAL", 3.8), ("SEOUL 1988", "WON GOLD", 5.8),
            ("PUBLIC", "15 YEARS LATER", 14.5)]
    for i, (a, b, t0) in enumerate(rows):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 300 + i * 150
        panel(d, [860, y, 1810, y + 120], ORANGE if i != 3 else PINK, k)
        if k > 0.7:
            d.text((900, y + 34), a, font=N.mono(28), fill=GREY + (255,))
            fb = gfx.font("Black", 31 if i == 0 else 52)
            d.text((900, y + 66), b, font=fb, fill=WHITE)
    k = eo(seg(t, 8.0, 8.5))
    if k > 0: d.text((1335, 930), "LEWIS DENIED WRONGDOING · USOC & IAAF: CLEARING FOLLOWED THE RULES", font=N.mono(21), fill=GREY + (int(230 * k),), anchor="mm")
    return im

def informants(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Aug 2024 · WADA vs USADA")
    k = eo(seg(t, 0.2, 0.6))
    panel(d, [110, 220, 1810, 560], PINK, k)
    if k > 0.7:
        big(d, (160, 300), "WADA: AT LEAST 3 CASES, 2011–2014", 60, WHITE, "lm")
        for j, l in enumerate(["ATHLETES WITH SERIOUS VIOLATIONS KEPT COMPETING FOR YEARS", "WHILE WORKING AS UNDERCOVER INFORMANTS · WADA NOT NOTIFIED"]):
            d.text((164, 400 + j * 60), l, font=N.mono(32), fill=PINK + (255,))
    k2 = eo(seg(t, 9.4, 9.8))
    if k2 > 0:
        panel(d, [110, 620, 1810, 820], CYAN, k2)
        if k2 > 0.7:
            big(d, (160, 690), "USADA: IT HELPED CATCH BIGGER FISH", 56, WHITE, "lm")
            d.text((164, 770), "SAYS THE INTEL LED TO CRIMINAL CHARGES", font=N.mono(30), fill=CYAN + (255,))
    return im

def knighton(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    neon_photo(im, ph("p_knighton2"), 420, 520, 660, t, 0.0, ORANGE, "Erriyon Knighton", "USA", crop=(0.5, 0.5, 1.0), aspect=0.84)
    rows = [("MAR 2024", "POSITIVE · TRENBOLONE (STEROID)", 0.1), ("JUN 2024", "CLEARED · \"CONTAMINATED MEAT\"", 1.2),
            ("AUG 2024", "RAN THE PARIS OLYMPICS · 4TH", 2.6), ("SEP 2025", "CAS · 4-YEAR BAN", 4.4)]
    for i, (a, b, t0) in enumerate(rows):
        k = eo(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 230 + i * 165
        panel(d, [860, y, 1810, y + 135], PINK if i == 3 else CYAN, k)
        if k > 0.7:
            d.text((900, y + 36), a, font=N.mono(30), fill=GREY + (255,))
            big(d, (900, y + 72), b, 46, WHITE)
    return im

def double_standard(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.1, 0.5))
    if k > 0:
        panel(d, [80, 200, 930, 900], PINK, min(1, k))
        if k > 0.7:
            big(d, (505, 300), "KENYAN FAILS", 66, PINK, "mm")
            for j, l in enumerate(["\"ALL THEM", "KENYANS IS", "DIRTY.\""]):
                big(d, (505, 470 + j * 110), l, 84, WHITE, "mm")
    k2 = eback(seg(t, 4.0, 4.4))
    if k2 > 0:
        panel(d, [990, 200, 1840, 900], CYAN, min(1, k2))
        if k2 > 0.7:
            big(d, (1415, 300), "AMERICAN FAILS", 66, CYAN, "mm")
            for j, (l, t0) in enumerate([("AN APPEAL", 5.2), ("AN EXPLANATION", 6.1), ("A HERBAL SUPPLEMENT", 7.2), ("A STEAK", 8.8)]):
                kk = eo(seg(t, t0, t0 + 0.3))
                if kk > 0: big(d, (1415, 440 + j * 110), l, 66, WHITE, "mm")
    return im

def cheaters(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.0, 0.4))
    if k > 0: big(d, (960, 300), "CHEATERS IS CHEATERS.", int(100 * min(1.05, k)), WHITE, "mm")
    for i, (s, t0) in enumerate([("KENYA GOT SOME", 1.8), ("AMERICA GOT SOME", 3.1), ("EVERY COUNTRY DO", 4.3)]):
        kk = eo(seg(t, t0, t0 + 0.3))
        if kk > 0: d.text((960, 470 + i * 90), s, font=N.mono(52), fill=CYAN + (int(255 * kk),), anchor="mm")
    k2 = eback(seg(t, 5.5, 5.9))
    if k2 > 0: big(d, (960, 850), "ONLY ONE SIDE GETS THE WHOLE COUNTRY BLAMED", int(56 * min(1.05, k2)), PINK, "mm")
    return im

# ------------------------------------------------------------------ the rule change
def five_in_five(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Summer 2026 · NCAA Division I")
    k = eback(seg(t, 0.3, 0.7))
    if k > 0: big(d, (960, 330), "5-IN-5", int(200 * min(1.05, k)), ORANGE, "mm")
    rows = [("5 YEARS OF ELIGIBILITY · 5 YEARS TO USE IT", 3.9), ("INTERNATIONAL CLOCK STARTS AT 19", 9.4)]
    for i, (s, t0) in enumerate(rows):
        kk = eo(seg(t, t0, t0 + 0.4))
        if kk <= 0: continue
        y = 540 + i * 160
        panel(d, [210, y, 1710, y + 125], CYAN if i == 0 else PINK, kk)
        if kk > 0.7: big(d, (960, y + 62), s, 54, WHITE, "mm")
    return im

def old_rules(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.0, 0.4))
    if k > 0: big(d, (960, 400), "YOU DON'T WRITE A NEW RULE", int(88 * min(1.05, k)), WHITE, "mm")
    k2 = eback(seg(t, 3.2, 3.6))
    if k2 > 0: big(d, (960, 560), "UNLESS THE OLD RULES ALLOWED IT.", int(88 * min(1.05, k2)), GREEN, "mm")
    return im

def clock(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "Under 5-in-5")
    y = 520
    d.line([(160, y), (1760, y)], fill=(70, 76, 96), width=6)
    def xa(age): return 160 + (age - 17) / 13 * 1600
    k = eo(seg(t, 0.2, 1.5))
    d.line([(xa(19), y), (xa(19) + (xa(24) - xa(19)) * k, y)], fill=GREEN, width=16)
    for a in (18, 19, 24, 28):
        d.line([(xa(a), y - 30), (xa(a), y + 30)], fill=WHITE, width=4)
        d.text((xa(a), y + 70), str(a), font=N.mono(44), fill=WHITE, anchor="mm")
    d.text(((xa(19) + xa(24)) / 2, y - 80), "5-YEAR WINDOW", font=N.mono(36), fill=GREEN + (255,), anchor="mm")
    k2 = eback(seg(t, 0.6, 1.0))
    if k2 > 0:
        d.text((xa(28), y - 140), "28-YEAR-OLD FRESHMAN", font=N.mono(34), fill=PINK + (255,), anchor="mm")
        big(d, (xa(28), y - 60), "X", 80, PINK, "mm")
    k3 = eo(seg(t, 2.6, 3.0))
    if k3 > 0:
        d.text((xa(18.5), y + 170), "KENYAN WHO ARRIVES AT 18 OR 19: STILL 5 YEARS", font=N.mono(36), fill=GREEN + (int(255 * k3),), anchor="lm")
    k4 = eback(seg(t, 7.7, 8.1))
    if k4 > 0: big(d, (960, 900), "THE RULE HITS AGE. NOT WHERE YOU'RE FROM.", int(60 * min(1.05, k4)), ORANGE, "mm")
    return im

# ------------------------------------------------------------------ this season
def matchup(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "2026 Big 12 XC · Oct 31 · 6K")
    for i, (pos, name, nat, school, col, t0) in enumerate([("1", "JANE HEDENGREN", "USA", "BYU", CYAN, 0.2), ("2", "BILLAH JEPKIRUI", "KEN", "OKLAHOMA STATE", GREEN, 2.8)]):
        k = eback(seg(t, t0, t0 + 0.4))
        if k <= 0: continue
        y = 260 + i * 200
        panel(d, [110, y, 1810, y + 160], col, min(1, k))
        if k > 0.7:
            big(d, (180, y + 80), pos, 90, ORANGE, "lm")
            big(d, (320, y + 80), name, 74, WHITE, "lm")
            d.text((1760, y + 80), f"{nat} · {school}", font=N.mono(34), fill=col + (255,), anchor="rm")
    k = eo(seg(t, 3.6, 4.0))
    if k > 0 and t > 3.6: d.text((960, 740), "MARGIN: 10 SECONDS", font=N.mono(48), fill=WHITE + (int(255 * k),), anchor="mm")
    return im

def nov21(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    kicker(d, t, "NCAA DI Cross Country Championships")
    k = eback(seg(t, 0.1, 0.5))
    if k > 0: big(d, (960, 330), "NOV 21", int(220 * min(1.05, k)), ORANGE, "mm")
    k2 = eo(seg(t, 0.8, 1.2))
    if k2 > 0: d.text((960, 500), "TERRE HAUTE, INDIANA · LAVERN GIBSON COURSE", font=N.mono(44), fill=WHITE + (int(255 * k2),), anchor="mm")
    for i, (c, col, t0) in enumerate([("USA", WHITE, 3.6), ("KEN", GREEN, 4.2), ("ERI", (65, 170, 255), 4.8), ("MAR", RED, 5.5)]):
        kk = eback(seg(t, t0, t0 + 0.3))
        if kk <= 0: continue
        x = 420 + i * 360
        d.rounded_rectangle([x - 140, 620, x + 140, 740], 12, outline=col + (255,), width=5, fill=col + (40,))
        d.text((x, 680), c, font=N.mono(60), fill=col + (255,), anchor="mm")
    k3 = eback(seg(t, 8.0, 8.4))
    if k3 > 0: big(d, (960, 880), "SAME LINE. SAME COURSE. SAME RULES.", int(64 * min(1.05, k3)), CYAN, "mm")
    return im

def what_rule(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.0, 0.4))
    if k > 0:
        d.text((960, 300), "\"IMPORTED\"   ·   \"NO BIRTH CERTIFICATE\"", font=N.mono(52), fill=PINK + (int(255 * k),), anchor="mm")
    k2 = eback(seg(t, 7.0, 7.4))
    if k2 > 0: big(d, (960, 540), "WHAT RULE DID THEY BREAK?", int(110 * min(1.05, k2)), WHITE, "mm")
    return im

def end_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.2, 0.6))
    if k > 0: big(d, (960, 300), "THE RUNNERS JUST RAN.", int(110 * min(1.05, k)), WHITE, "mm")
    k2 = eo(seg(t, 1.5, 2.0))
    if k2 > 0:
        panel(d, [560, 480, 1360, 620], ORANGE, k2)
        if k2 > 0.7: big(d, (960, 550), "SUBSCRIBE", 80, WHITE, "mm")
        d.text((960, 700), "NATIONALS · NOV 21 · TERRE HAUTE", font=N.mono(40), fill=CYAN + (int(255 * k2),), anchor="mm")
    k3 = eo(seg(t, 3.0, 3.5))
    if k3 > 0:
        d.text((960, 900), "SOURCES & PHOTO CREDITS IN THE DESCRIPTION · COMMENTS SHOWN ARE REAL, USERNAMES HIDDEN", font=N.mono(22), fill=GREY + (int(220 * k3),), anchor="mm")
    return im

GRAPHICS = {
    "title_card": title_card, "results": results, "legal": legal, "cover1977": cover1977, "rono_stats": rono_stats,
    "fifty_years": fifty_years, "kipchoge_file": kipchoge_file, "age_limit": age_limit, "eligibility": eligibility,
    "same_rule": same_rule, "third_place": third_place, "offer": offer, "pipeline": pipeline, "share": share,
    "went_got": went_got, "two_groups": two_groups, "imported": imported, "no_rule": no_rule, "sports_grid": sports_grid,
    "cases": cases, "category_a": category_a, "tests_compare": tests_compare, "exum": exum, "lewis": lewis,
    "informants": informants, "knighton": knighton, "double_standard": double_standard, "cheaters": cheaters,
    "five_in_five": five_in_five, "old_rules": old_rules, "clock": clock, "matchup": matchup, "nov21": nov21,
    "what_rule": what_rule, "end_card": end_card, "usa_not": usa_not,
    "dunkley": quote_card("Fitz Dunkley · Jamaican Olympic silver medalist", "The same rule that's called \"inspiring\" for Americans becomes \"unfair\" when an international athlete benefits from it.", "Fitz Dunkley", ORANGE),
    "eyestone": quote_card("Ed Eyestone · BYU men's coach · Deseret News", "I'd be embarrassed to have seven foreigners on the team.", "Ed Eyestone", CYAN, photo="p_eyestone", crop=(0.5, 0.4, 1.0)),
    "smith": quote_card("Dave Smith · Oklahoma State coach · reply to critics", "Change the rulebook… or shut up and coach.", "Dave Smith, Oklahoma State", GREEN),
}
for k in COMMENTS: GRAPHICS[k] = comment_card(k)
