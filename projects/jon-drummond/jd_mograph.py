"""Motion graphics for the Jon Drummond documentary (same dark/orange HUD look as tools/mograph.py)."""
import math, sys, os
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageDraw
import mograph as M
from mograph import background, header, text, eo, eback, seg, pin, Proj, draw_map, _load, arc, ORANGE, RED, WHITE, GREY, DIM, BG
import gfx

W, H = 1920, 1080

def _box(d, x, y, w, h, k, col=ORANGE):
    d.rectangle([x, y, x + w * k, y + h], fill=(20, 21, 26), outline=col, width=3)

def profile(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.1, 0.6))
    text(d, (160, 300), "SUBJECT FILE", 30, ORANGE, "Bold", alpha=k)
    d.rectangle([160, 350, 160 + 900 * eo(seg(t, 0.2, 0.8)), 356], fill=ORANGE)
    f = gfx.font("Black", 150)
    name = "JON DRUMMOND"[: int(12 * eo(seg(t, 0.3, 1.1)))]
    d.text((160, 380), name, font=f, fill=WHITE)
    for i, (lab, val) in enumerate([("ROLE", "US 4x100 RELAY CAPTAIN"), ("HONORS", "OLYMPIC GOLD MEDALIST"), ("HOMETOWN", "PHILADELPHIA, PA")]):
        kk = eo(seg(t, 1.0 + i * 0.35, 1.4 + i * 0.35))
        text(d, (160, 600 + i * 80), lab, 26, GREY, "Bold", alpha=kk)
        text(d, (420, 594 + i * 80), val, 38, WHITE, "Black", alpha=kk)
    return im

def delay_clock(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    cx, cy, r = 960, 520, 250
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=DIM, width=10)
    frac = min(1, t / max(1, dur - 0.6))
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=ORANGE, width=14)
    mins = int(58 * eo(frac))
    text(d, (cx, cy - 30), f"{mins:02d}:00", 120, WHITE, "Black", anchor="mm")
    text(d, (cx, cy + 70), "MEET STOPPED", 30, GREY, "Bold", anchor="mm")
    header(d, t, "Worlds · Paris 2003", "Damn near a hour")
    return im

def case_stamp(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.0, 0.5))
    x, y = 560, 220
    d.rectangle([x, y, x + 800, y + 640], fill=(232, 228, 218))
    for i in range(9):
        d.rectangle([x + 70, y + 160 + i * 44, x + 70 + (600 if i % 3 else 420) * k, y + 172 + i * 44], fill=(170, 165, 155))
    text(d, (x + 70, y + 60), "ANTI-DOPING DECISION", 40, (30, 30, 30), "Black")
    text(d, (x + 70, y + 110), "CASE: J. DRUMMOND · 2014", 24, (90, 90, 90), "Bold")
    ks = seg(t, 0.9, 1.1)
    if ks > 0:
        sc = 1.8 - 0.8 * eo(ks)
        st = Image.new("RGBA", (700, 260), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 10, 690, 250], radius=20, outline=RED, width=14)
        sd.text((350, 95), "8 YEARS", font=gfx.font("Black", 110), fill=RED, anchor="mm")
        sd.text((350, 195), "BANNED", font=gfx.font("Black", 64), fill=RED, anchor="mm")
        st = st.rotate(-10, expand=True, resample=Image.BICUBIC)
        st = st.resize((int(st.width * sc), int(st.height * sc)))
        im.alpha_composite(st, (960 - st.width // 2, 560 - st.height // 2)) if im.mode == "RGBA" else im.paste(st, (960 - st.width // 2, 560 - st.height // 2), st)
    return im

def title_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.2, 1.0))
    text(d, (960, 380), "A TRACK & FIELD STORY", 30, ORANGE, "Bold", anchor="mm", alpha=k)
    f = gfx.font("Black", 170)
    s = "JON DRUMMOND"
    n = int(len(s) * eo(seg(t, 0.3, 1.3)))
    d.text((960, 500), s[:n], font=f, fill=WHITE, anchor="mm")
    d.rectangle([960 - 520 * eo(seg(t, 1.0, 1.8)), 600, 960 + 520 * eo(seg(t, 1.0, 1.8)), 606], fill=ORANGE)
    text(d, (960, 660), "THE SHOWMAN WHO WOULDN'T LEAVE", 44, WHITE, "Bold", anchor="mm", alpha=eo(seg(t, 1.4, 2.0)))
    return im

PHL, ODESSA, FTW = (-75.165, 39.953), (-102.367, 31.846), (-97.33, 32.75)

def route_map(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    proj = Proj(-107, -70, 26, 44, box=(200, 180, 1880, 1040))
    draw_map(d, _load("us_states.json"), proj, hi={"Pennsylvania": eo(seg(t, 0.2, 0.7)), "Texas": eo(seg(t, 1.6, 2.2))}, hi_fill=(70, 46, 30))
    pin(d, proj(*PHL), 0.3, t, "Philadelphia", "Overbrook High · same school as Wilt", side="left")
    arc(d, proj(*PHL), proj(*ODESSA), eo(seg(t, 1.2, 2.2)), bend=0.15)
    pin(d, proj(*ODESSA), 2.1, t, "Odessa, TX", "JUCO", side="right")
    arc(d, proj(*ODESSA), proj(*FTW), eo(seg(t, 2.8, 3.4)), bend=-0.3)
    pin(d, proj(*FTW), 3.3, t, "TCU", "Fort Worth, TX", side="right")
    header(d, t, "Born 1968", "The come-up")
    return im

def medals(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Relays · 4x100", "Made his name")
    items = [("'93", "WORLD GOLD", "TIED THE WORLD RECORD", ORANGE), ("'96", "OLYMPIC SILVER", "ATLANTA", (190, 190, 200)), ("'99", "WORLD GOLD", "SEVILLE", ORANGE)]
    for i, (yr, a, b, col) in enumerate(items):
        k = eback(seg(t, 0.4 + i * 0.5, 0.8 + i * 0.5))
        if k <= 0: continue
        x = 300 + i * 500; y = 600
        r = 110 * k
        d.ellipse([x - r, y - r, x + r, y + r], fill=(26, 27, 33), outline=col, width=8)
        text(d, (x, y), yr, int(80 * min(1, k)), col, "Black", anchor="mm")
        text(d, (x, y + 150), a, 38, WHITE, "Black", anchor="mt", alpha=min(1, k))
        text(d, (x, y + 200), b, 24, GREY, "Bold", anchor="mt", alpha=min(1, k))
    return im

def team_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Sydney 2000 · Olympic final", "USA 4x100")
    names = [("JON DRUMMOND", "CAPTAIN"), ("BERNARD WILLIAMS", ""), ("BRIAN LEWIS", ""), ("MAURICE GREENE", "")]
    for i, (n, tag) in enumerate(names):
        k = eo(seg(t, 0.4 + i * 0.25, 0.8 + i * 0.25))
        if k <= 0: continue
        y = 380 + i * 140; x = 160 + int((1 - k) * -80)
        d.rectangle([x, y, x + 12, y + 100], fill=ORANGE if tag else WHITE)
        text(d, (x + 40, y + 10), f"LEG {i + 1}", 24, GREY, "Bold", alpha=k)
        text(d, (x + 40, y + 40), n, 54, WHITE, "Black", alpha=k)
        if tag: text(d, (x + 40 + 640, y + 52), tag, 30, ORANGE, "Black", alpha=k)
    kg = eback(seg(t, 2.0, 2.5))
    if kg > 0:
        r = 140 * kg; d.ellipse([1500 - r, 600 - r, 1500 + r, 600 + r], fill=ORANGE)
        text(d, (1500, 600), "GOLD", int(60 * min(1, kg)), (20, 20, 20), "Black", anchor="mm")
    return im

def medal_stand(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Sydney 2000 · Medal stand", "On camera")
    for i, (lab, h) in enumerate([("2", 180), ("1", 260), ("3", 130)]):
        k = eo(seg(t, 0.3 + i * 0.15, 0.8 + i * 0.15)); x = 560 + i * 280
        d.rectangle([x, 900 - h * k, x + 260, 900], fill=(30, 32, 38), outline=ORANGE if lab == "1" else GREY, width=3)
        text(d, (x + 130, 900 - h * k + 40), lab, 70, ORANGE if lab == "1" else GREY, "Black", anchor="mm", alpha=k)
    text(d, (960, 330), "MEDALS PRESENTED BY HENRY KISSINGER", 34, WHITE, "Bold", anchor="mm", alpha=eo(seg(t, 1.0, 1.5)))
    return im

def emails(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "After Sydney", "The backlash")
    n0, n1 = 125, 200
    v = int(n0 + (n1 - n0) * eo(seg(t, 0.4, 2.4)))
    text(d, (960, 520), f"{n0}–{v}", 190, WHITE, "Black", anchor="mm")
    text(d, (960, 650), "EMAILS A DAY", 50, ORANGE, "Black", anchor="mm", alpha=eo(seg(t, 0.6, 1.0)))
    for i in range(14):  # falling envelopes
        ph = (t * 0.6 + i / 14) % 1
        x = 120 + (i * 137) % 1700; y = -60 + ph * 1200
        d.rectangle([x, y, x + 70, y + 46], outline=(80, 84, 94), width=3); d.line([(x, y), (x + 35, y + 26), (x + 70, y)], fill=(80, 84, 94), width=3)
    if t > 2.6:
        text(d, (960, 760), "SOME OF 'EM WAS RACIAL", 40, RED, "Black", anchor="mm", alpha=eo(seg(t, 2.6, 3.0)))
    return im

def rep_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Reputation", "After Sydney")
    for i, w in enumerate(["SHOWMAN", "REBEL", "DON'T FOLLOW THE SCRIPT"]):
        k = eback(seg(t, 0.4 + i * 0.45, 0.8 + i * 0.45))
        if k <= 0: continue
        y = 420 + i * 160
        f = gfx.font("Black", int(110 * min(1.1, k)) if i < 2 else int(70 * min(1.1, k)))
        d.text((160, y), w, font=f, fill=ORANGE if i == 2 else WHITE)
    return im

def rule_explainer(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "The false start rule", "How it changed")
    cols = [("BEFORE 2003", "Every sprinter gets\none false start\nof they own", GREY, 0.3),
            ("2003 · IAAF", "1st false start charged\nto the WHOLE field.\nWhoever jumps next: OUT", ORANGE, dur * 0.35),
            ("2010", "One false start\nand you out.\nNo warnin'.", RED, dur * 0.7)]
    for i, (h, body, col, t0) in enumerate(cols):
        k = eo(seg(t, t0, t0 + 0.6))
        if k <= 0: continue
        x = 140 + i * 570; y = 360 + int((1 - k) * 60)
        d.rectangle([x, y, x + 520, y + 520], fill=(22, 23, 28), outline=col, width=4)
        d.rectangle([x, y, x + 520, y + 14], fill=col)
        text(d, (x + 40, y + 50), h, 48, col, "Black", alpha=k)
        for j, line in enumerate(body.split("\n")):
            text(d, (x + 40, y + 160 + j * 64), line, 38, WHITE, "Bold", alpha=k)
    return im

def paris_pin(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = M.eio(seg(t, 0, 1.4))
    v = M.lerp_view((-15, 30, 35, 62), (-2, 8, 45.5, 51.5), k)
    proj = Proj(*v, box=(400, 150, 1880, 1040))
    draw_map(d, _load("world.json"), proj, hi={"France": eo(seg(t, 0.5, 1.2))}, hi_fill=(70, 46, 30))
    pin(d, proj(2.35, 48.86), 1.3, t, "Paris", "Worlds · Aug 2003 · 100m quarterfinal", side="left")
    header(d, t, "August 2003", "World Championships")
    return im

def false_start(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    fl = max(0, 1 - t / 0.25)
    if fl > 0: d.rectangle([0, 0, W, H], fill=(229, 57, 53, int(160 * fl)))
    k = eback(seg(t, 0.05, 0.35))
    f = gfx.font("Black", int(190 * min(1.1, k + 0.01)))
    d.text((960, 470), "FALSE START", font=f, fill=RED, anchor="mm")
    text(d, (960, 640), "DRUMMOND · DISQUALIFIED", 50, WHITE, "Black", anchor="mm", alpha=eo(seg(t, 0.5, 0.9)))
    return im

def quote_card(t, dur, kicker, lines, sub=None):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    text(d, (160, 300), kicker.upper(), 30, ORANGE, "Bold", alpha=eo(seg(t, 0.1, 0.5)))
    d.rectangle([160, 350, 160 + 140 * eo(seg(t, 0.2, 0.6)), 356], fill=ORANGE)
    text(d, (130, 330), "“", 220, (60, 62, 70), "Black")
    for i, ln in enumerate(lines):
        k = eo(seg(t, 0.4 + i * 0.4, 0.9 + i * 0.4))
        text(d, (180 + int((1 - k) * 40), 420 + i * 92), ln, 66, WHITE if i < len(lines) - 1 else ORANGE, "Black", alpha=k)
    if sub: text(d, (180, 420 + len(lines) * 92 + 30), sub, 28, GREY, "Bold", alpha=eo(seg(t, 1.6, 2.0)))
    return im

def fallout(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Paris 2003 · fallout", "What happened next")
    steps = [("IAAF", "Deadline for USA Track & Field to act"), ("RELAY", "Drummond to be pulled off it"), ("OUT", "Rest of Worlds · rest of the season")]
    for i, (a, b) in enumerate(steps):
        k = eo(seg(t, 0.4 + i * 0.9, 0.9 + i * 0.9))
        if k <= 0: continue
        y = 400 + i * 170
        d.ellipse([160, y, 220, y + 60], fill=ORANGE if i < 2 else RED)
        if i < 2: d.line([(190, y + 60), (190, y + 170)], fill=DIM, width=6)
        text(d, (260, y - 4), a, 48, WHITE, "Black", alpha=k)
        text(d, (260, y + 50), b.upper(), 28, GREY, "Bold", alpha=k)
    return im

def bolt_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "2010 rule", "One and done")
    k = eback(seg(t, 0.3, 0.8))
    f = gfx.font("Black", int(150 * min(1.1, k + 0.01)))
    d.text((960, 470), "1 FALSE START", font=f, fill=WHITE, anchor="mm")
    text(d, (960, 600), "= YOU OUT", 80, RED, "Black", anchor="mm", alpha=eo(seg(t, 0.7, 1.1)))
    if t > dur * 0.5:
        kk = eo(seg(t, dur * 0.5, dur * 0.5 + 0.5))
        d.rectangle([560, 720, 560 + 800 * kk, 800], fill=(22, 23, 28), outline=ORANGE, width=3)
        if kk > 0.8: text(d, (960, 760), "USAIN BOLT · DQ'D IN A WORLD FINAL · 2011", 30, ORANGE, "Black", anchor="mm")
    return im

def chapter(name, num):
    def fn(t, dur):
        im = background(t); d = ImageDraw.Draw(im, "RGBA")
        k = eo(seg(t, 0.1, 0.7))
        text(d, (960, 430), f"CHAPTER {num}", 34, ORANGE, "Bold", anchor="mm", alpha=k)
        f = gfx.font("Black", 140); n = int(len(name) * eo(seg(t, 0.3, 1.2)))
        d.text((960, 540), name[:n], font=f, fill=WHITE, anchor="mm")
        d.rectangle([960 - 300 * eo(seg(t, 0.8, 1.4)), 630, 960 + 300 * eo(seg(t, 0.8, 1.4)), 636], fill=ORANGE)
        return im
    return fn

def london(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "London 2012", "Back in the building")
    for i, (a, b) in enumerate([("RELAY COACH", "TEAM USA · LONDON OLYMPICS"), ("PERSONAL COACH", "TYSON GAY"), ("US WOMEN'S 4x100", "SET A WORLD RECORD")]):
        k = eo(seg(t, 0.5 + i * 0.6, 1.0 + i * 0.6))
        if k <= 0: continue
        y = 400 + i * 170
        d.rectangle([160, y, 172, y + 110], fill=ORANGE)
        text(d, (200, y + 4), a, 30, GREY, "Bold", alpha=k)
        text(d, (200, y + 44), b, 56, WHITE, "Black", alpha=k)
    return im

def gay_case(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Tyson Gay · 2013", "The tests")
    for i in range(3):
        k = eback(seg(t, 0.4 + i * 0.35, 0.8 + i * 0.35))
        if k <= 0: continue
        x = 300 + i * 260; y = 560; r = 90 * k
        d.ellipse([x - r, y - r, x + r, y + r], fill=(26, 27, 33), outline=RED, width=6)
        text(d, (x, y), "+", int(90 * min(1, k)), RED, "Black", anchor="mm")
    text(d, (300, 720), "3 FAILED TESTS", 48, WHITE, "Black", alpha=eo(seg(t, 1.6, 2.0)))
    for i, s in enumerate(["RESULTS WIPED FROM JULY 2012", "OLYMPIC RELAY SILVER RETURNED", "BAN CUT TO 1 YEAR · \"SUBSTANTIAL ASSISTANCE\""]):
        k = eo(seg(t, 2.2 + i * 0.5, 2.6 + i * 0.5))
        text(d, (1100, 450 + i * 110), s, 30, ORANGE if i == 2 else WHITE, "Black", alpha=k)
    return im

def ruling(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "December 17, 2014", "The ruling")
    for i, s in enumerate(["HAD BANNED PEDs", "WAS MOVIN' 'EM", "WAS GIVIN' 'EM TO ATHLETES", "HELPED TYSON USE BANNED STUFF · 2012"]):
        k = eo(seg(t, 0.4 + i * 0.6, 0.8 + i * 0.6))
        if k <= 0: continue
        y = 400 + i * 130
        d.rectangle([160, y + 10, 190, y + 40], outline=RED, width=4)
        if k > 0.8: d.line([(165, y + 25), (175, y + 35), (190, y + 12)], fill=RED, width=5)
        text(d, (220, y), s, 50, WHITE, "Black", alpha=k)
    text(d, (160, 940), "INDEPENDENT PANEL FINDINGS · DRUMMOND SAID THE ACCUSATIONS WAS FALSE", 24, GREY, "Bold", alpha=eo(seg(t, 2.8, 3.2)))
    return im

def sanction(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eback(seg(t, 0.1, 0.5))
    f = gfx.font("Black", int(260 * min(1.05, k + 0.01)))
    d.text((560, 520), "8", font=f, fill=RED, anchor="mm")
    text(d, (560, 700), "YEARS", 70, WHITE, "Black", anchor="mm", alpha=min(1, k))
    for i, s in enumerate(["NO COACHIN'", "NO TRAININ'", "NO ADVISIN' ATHLETES", "NO USATF OR IAAF EVENTS"]):
        kk = eo(seg(t, 0.8 + i * 0.5, 1.2 + i * 0.5))
        y = 360 + i * 110
        d.line([(980, y + 30), (1020, y + 30)], fill=RED, width=8)
        text(d, (1050, y), s, 52, WHITE, "Black", alpha=kk)
    return im

def same_year(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.2, 0.7))
    d.rectangle([0, 0, 960 * k, H], fill=(28, 24, 18))
    text(d, (480, 470), "HALL OF FAME", 80, ORANGE, "Black", anchor="mm", alpha=k)
    text(d, (480, 560), "TEXAS TRACK & FIELD COACHES", 28, WHITE, "Bold", anchor="mm", alpha=k)
    k2 = eo(seg(t, 0.9, 1.4))
    d.rectangle([1920 - 960 * k2, 0, 1920, H], fill=(36, 14, 14))
    text(d, (1440, 470), "8-YEAR BAN", 80, RED, "Black", anchor="mm", alpha=k2)
    text(d, (1440, 560), "ANTI-DOPING SANCTION", 28, WHITE, "Bold", anchor="mm", alpha=k2)
    k3 = eback(seg(t, 1.8, 2.2))
    if k3 > 0:
        r = 120 * k3
        d.ellipse([960 - r, 820 - r, 960 + r, 820 + r], fill=WHITE)
        text(d, (960, 820), "2014", int(64 * min(1, k3)), (20, 20, 20), "Black", anchor="mm")
        text(d, (960, 140), "SAME YEAR", 60, WHITE, "Black", anchor="mm", alpha=min(1, k3))
    return im

def now_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Where he at now", "Back home")
    for i, (a, b) in enumerate([("BAN ENDED", "DECEMBER 2022"), ("LISTED AS", "PASTOR · PHILADELPHIA")]):
        k = eo(seg(t, 0.5 + i * 0.7, 1.0 + i * 0.7))
        y = 430 + i * 200
        d.rectangle([160, y, 172, y + 130], fill=ORANGE)
        text(d, (200, y + 4), a, 30, GREY, "Bold", alpha=k)
        text(d, (200, y + 50), b, 70, WHITE, "Black", alpha=k)
    return im

def end_line(t, dur):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    k = eo(seg(t, 0.4, 1.4))
    text(d, (960, 500), "ELEVEN YEARS LATER…", 50, ORANGE, "Bold", anchor="mm", alpha=k)
    text(d, (960, 590), "THE SPORT LET GO OF HIM.", 80, WHITE, "Black", anchor="mm", alpha=eo(seg(t, 1.2, 2.2)))
    if t > dur - 1.2:
        fade = (dur - t) / 1.2
        im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, fade))
    return im

GRAPHICS = {
    "profile": profile, "delay_clock": delay_clock, "case_stamp": case_stamp, "title": title_card,
    "route_map": route_map, "medals": medals, "team": team_card, "medal_stand": medal_stand, "emails": emails,
    "rep": rep_card, "rule": rule_explainer, "paris": paris_pin, "false_start": false_start, "fallout": fallout,
    "bolt": bolt_card, "london": london, "gay_case": gay_case, "ruling": ruling, "sanction": sanction,
    "same_year": same_year, "now": now_card, "end": end_line,
    "ch_sydney": chapter("SYDNEY 2000", "II"), "ch_paris": chapter("PARIS 2003", "III"), "ch_fall": chapter("THE FALL", "IV"),
    "q_spirit": lambda t, d: quote_card(t, d, "His statement · in my words", ["His spirit was broke…", "'cause all he ever wanted", "was to entertain the fans."]),
    "q_regret": lambda t, d: quote_card(t, d, "USA Track & Field", ["“Regrettable.”"], "PROMISED A WHOLE CONDUCT POLICY FOR ATHLETES"),
    "q_mj": lambda t, d: quote_card(t, d, "The reaction", ["Spain's federation: kick him out.", "Michael Johnson:", "embarrassed to be American."]),
    "q_ceo": lambda t, d: quote_card(t, d, "USA Track & Field CEO", ["“Deeply disappointed.”"], "SAID THEY HAD NO KNOWLEDGE OF WHAT DRUMMOND WAS DOIN'"),
}
