"""Motion graphics for the Oscar Pistorius documentary (same neon look as jd_mograph).

Two moods:
- neon cards (synthwave background, bloom) for the career, the legal fight and the numbers;
- quiet cards (near-black, no grid, slow fades, no pop-ins) for everything about the night of
  14 Feb 2013, Reeva Steenkamp and her family.
The caller sets neon.PHOTOS to the Commons photo folder and M.finish = neon.finish."""
import sys
sys.path.insert(0, "/home/user/YouTube-/tools")
from PIL import Image, ImageDraw
import mograph as M
from mograph import header, text, eo, eback, seg, ORANGE, RED, WHITE, GREY, DIM
import gfx
import neon as N
from neon import CYAN, neon_photo

N.TAGLINE = "OP//ARCHIVE"
background = N.background
M.BG = N.BG
W, H = 1920, 1080

def ph(name):
    return f"{N.PHOTOS}/{name}.jpg"

def quiet_bg(t):
    """Near-black with a faint cold glow: used for the respectful cards."""
    im = Image.new("RGB", (W, H), (4, 5, 9))
    d = ImageDraw.Draw(im, "RGBA")
    for r in range(9, 0, -1):
        a = int(5 * (10 - r) / 9)
        d.ellipse([960 - r * 120, 540 - r * 70, 960 + r * 120, 540 + r * 70], fill=(30, 50, 70, a))
    return im

def fade_in_out(t, dur, a=0.6, b=0.6):
    return min(eo(seg(t, 0, a)), 1 - seg(t, dur - b, dur))

def ctext(d, y, s, size, col, weight="Black", k=1.0):
    text(d, (960, y), s, size, col, weight, anchor="mm", alpha=k)

# ------------------------------------------------------------------ cold open
def date_open(t, dur):
    """'Valentine's Day 2013. Pretoria, South Africa. Sun ain't even up yet.'"""
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.8, 0.5)
    ctext(d, 430, "14 FEBRUARY 2013", 110, WHITE, k=k)
    ctext(d, 530, "PRETORIA · SOUTH AFRICA", 40, CYAN, "Bold", k=k * eo(seg(t, 0.8, 1.6)))
    k2 = k * eo(seg(t, 6.0, 6.6))  # "Sun ain't even up yet" (VO 6.16)
    ctext(d, 640, "BEFORE SUNRISE", 34, GREY, "Bold", k=k2)
    return im

def door(t, dur):
    """Quiet: a closed door outline, four small marks appearing one by one. No gunshot sounds."""
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.8, 0.6)
    c = tuple(int(v * k) for v in (150, 160, 175))
    x0, y0, x1, y1 = 800, 190, 1120, 900
    d.rectangle([x0, y0, x1, y1], outline=c, width=4)
    d.rectangle([x0 + 30, y0 + 30, x1 - 30, y0 + 330], outline=tuple(v // 2 for v in c), width=2)
    d.rectangle([x0 + 30, y0 + 370, x1 - 30, y1 - 30], outline=tuple(v // 2 for v in c), width=2)
    d.ellipse([x1 - 60, 540, x1 - 40, 560], outline=c, width=3)
    for i, (px, py) in enumerate([(930, 470), (990, 520), (955, 585), (1015, 640)]):
        if t > 5.4 + i * 0.35:
            kk = k * eo(seg(t, 5.4 + i * 0.35, 5.7 + i * 0.35))
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(220, 220, 230, int(255 * kk)))
    text(d, (160, 860), "A LOCKED BATHROOM DOOR", 30, GREY, "Bold", alpha=k * eo(seg(t, 1.0, 1.6)))
    return im

def profile(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    text(d, (160, 300), "SUBJECT FILE", 30, ORANGE, "Bold", alpha=eo(seg(t, 0.1, 0.6)))
    d.rectangle([160, 350, 160 + 900 * eo(seg(t, 0.2, 0.8)), 356], fill=ORANGE)
    f = gfx.font("Black", 118)
    name = "OSCAR PISTORIUS"[: int(15 * eo(seg(t, 0.3, 1.2)))]
    d.text((160, 385), name, font=f, fill=WHITE)
    neon_photo(im, ph("Oscar_Pistorius_in_Warsaw_cropped_"), 1530, 520, 620, t, 0.35, CYAN, "Oscar Pistorius", "Photo · Warsaw", crop=(0.5, 0.45, 0.95))
    d = ImageDraw.Draw(im, "RGBA")
    for i, (lab, val) in enumerate([("KNOWN AS", "THE BLADE RUNNER"), ("SPORT", "SPRINTING · 400M"), ("COUNTRY", "SOUTH AFRICA")]):
        kk = eo(seg(t, 1.0 + i * 0.35, 1.4 + i * 0.35))
        text(d, (160, 600 + i * 80), lab, 26, GREY, "Bold", alpha=kk)
        text(d, (420, 594 + i * 80), val, 38, WHITE, "Black", alpha=kk)
    return im

def title_card(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.2, 1.0))
    text(d, (960, 380), "A TRACK & FIELD STORY", 30, ORANGE, "Bold", anchor="mm", alpha=k)
    f = gfx.font("Black", 170); s = "THE BLADE RUNNER"
    d.text((960, 500), s[: int(len(s) * eo(seg(t, 0.3, 1.3)))], font=f, fill=WHITE, anchor="mm")
    w = 600 * eo(seg(t, 1.0, 1.8))
    d.rectangle([960 - w, 600, 960 + w, 606], fill=ORANGE)
    text(d, (960, 660), "OSCAR PISTORIUS", 44, WHITE, "Bold", anchor="mm", alpha=eo(seg(t, 1.4, 2.0)))
    return im

def chapter(name, num):
    def fn(t, dur):
        im = background(t); d = ImageDraw.Draw(im, "RGBA")
        text(d, (960, 430), f"CHAPTER {num}", 34, ORANGE, "Bold", anchor="mm", alpha=eo(seg(t, 0.1, 0.7)))
        f = gfx.font("Black", 140)
        d.text((960, 540), name[: int(len(name) * eo(seg(t, 0.3, 1.2)))], font=f, fill=WHITE, anchor="mm")
        w = 300 * eo(seg(t, 0.8, 1.4))
        d.rectangle([960 - w, 630, 960 + w, 636], fill=ORANGE)
        return im
    return fn

# ------------------------------------------------------------------ early life
def born(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Johannesburg, South Africa", "Born 1986")
    k = eback(seg(t, 0.5, 0.9))
    if k > 0:
        r = 150 * k
        d.ellipse([960 - r, 600 - r, 960 + r, 600 + r], outline=CYAN, width=8, fill=(8, 12, 24))
        text(d, (960, 600), "1986", int(96 * min(1, k)), WHITE, "Black", anchor="mm")
    return im

def fibula(t, dur):
    """Simple lower-leg diagram: tibia + fibula, fibula highlighted 'missing', then '11 months'."""
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Fibular hemimelia", "Born without the fibula")
    x = 620; k = eo(seg(t, 0.4, 1.2))
    d.rounded_rectangle([x - 40, 330, x + 40, 360], 14, outline=WHITE, width=5)  # knee
    d.rounded_rectangle([x - 26, 360, x + 6, 360 + 520 * k], 10, outline=WHITE, width=5)  # tibia
    kf = seg(t, 1.4, 2.0)
    col = (255, 46, 99, int(255 * (0.4 + 0.6 * abs(((t * 1.6) % 2) - 1)))) if kf > 0 else (0, 0, 0, 0)
    for yy in range(372, 860, 26):  # dashed fibula outline = missing bone
        d.line([(x + 30, yy), (x + 30, yy + 14)], fill=col, width=5)
    if kf > 0:
        text(d, (x + 70, 600), "FIBULA", 34, (255, 46, 99), "Black", alpha=kf)
        text(d, (x + 70, 645), "THE OUTSIDE BONE OF THE LOWER LEG", 24, GREY, "Bold", alpha=kf)
    k2 = eo(seg(t, 5.3, 5.9))
    if k2 > 0:
        d.rectangle([1180, 420, 1180 + 600 * k2, 700], fill=(8, 10, 22), outline=CYAN, width=3)
        if k2 > 0.8:
            text(d, (1220, 450), "11 MONTHS OLD", 54, WHITE, "Black")
            text(d, (1220, 530), "BOTH LEGS AMPUTATED", 32, CYAN, "Bold")
            text(d, (1220, 580), "BELOW THE KNEE", 32, CYAN, "Bold")
    return im

def sheila(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.8, 0.6)
    ctext(d, 460, "SHEILA PISTORIUS", 84, WHITE, k=k)
    ctext(d, 560, "HIS MOTHER · DIED MARCH 2002", 34, CYAN, "Bold", k=k * eo(seg(t, 0.6, 1.3)))
    ctext(d, 630, "OSCAR WAS 15", 30, GREY, "Bold", k=k * eo(seg(t, 1.6, 2.2)))
    return im

# ------------------------------------------------------------------ the fight to run
def ban(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "IAAF ruling · January 2008", "The blade ban")
    for i, s in enumerate(["CARBON-FIBRE BLADES", "RULED AN ADVANTAGE"]):
        text(d, (160, 400 + i * 90), s, 64, WHITE, "Black", alpha=eo(seg(t, 0.4 + i * 0.5, 0.9 + i * 0.5)))
    ks = seg(t, 3.6, 3.85)
    if ks > 0:
        sc = 1.8 - 0.8 * eo(ks)
        st = Image.new("RGBA", (760, 240), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 10, 750, 230], radius=20, outline=RED, width=14)
        sd.text((380, 90), "BANNED", font=gfx.font("Black", 110), fill=RED, anchor="mm")
        sd.text((380, 185), "FROM ABLE-BODIED RACES", font=gfx.font("Black", 38), fill=RED, anchor="mm")
        st = st.rotate(-8, expand=True, resample=Image.BICUBIC)
        st = st.resize((int(st.width * sc), int(st.height * sc)))
        im.paste(st, (1300 - st.width // 2, 720 - st.height // 2), st)
    return im

def cas(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Court of Arbitration for Sport · May 2008", "Ban overturned")
    k = eback(seg(t, 0.4, 0.8))
    if k > 0:
        d.rectangle([160, 420, 160 + 1100 * min(1, k), 560], fill=(8, 12, 24), outline=CYAN, width=4)
        if k > 0.8: text(d, (200, 455), "NO PROOF THE BLADES GAVE AN EDGE", 54, WHITE, "Black")
    text(d, (160, 620), "CLEARED TO RACE ABLE-BODIED ATHLETES", 36, CYAN, "Bold", alpha=eo(seg(t, 1.4, 2.0)))
    return im

# ------------------------------------------------------------------ cracks
def guns(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    k = eo(seg(t, 0.2, 0.8))
    text(d, (960, 470), "THE GUNS", 150, WHITE, "Black", anchor="mm", alpha=k)
    text(d, (960, 600), "HE WAS BIG ON FIREARMS", 38, ORANGE, "Bold", anchor="mm", alpha=eo(seg(t, 2.2, 2.8)))
    return im

def tashas(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "January 2013 · Johannesburg", "Tasha's, Melrose Arch")
    items = [("A PISTOL WENT OFF", "UNDER THE TABLE WHERE HE SAT"), ("RESTAURANT FULL OF PEOPLE", "CHILDREN AT THE NEXT TABLE")]
    for i, (a, b) in enumerate(items):
        t0 = 0.6 if i == 0 else 6.6
        kk = eo(seg(t, t0, t0 + 0.5))
        if kk <= 0: continue
        y = 420 + i * 200
        d.rectangle([160, y, 172, y + 120], fill=ORANGE if i == 0 else CYAN)
        text(d, (200, y + 4), a, 56, WHITE, "Black", alpha=kk)
        text(d, (200, y + 74), b, 30, GREY, "Bold", alpha=kk)
    return im

def countdown(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.5, 0.6)
    ctext(d, 470, "ONE MONTH LATER", 46, GREY, "Bold", k=k)
    ctext(d, 570, "14 FEBRUARY 2013", 110, WHITE, k=k * eo(seg(t, 0.7, 1.4)))
    return im

# ------------------------------------------------------------------ the night (quiet)
def feb14(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.7, 0.5)
    ctext(d, 540, "14 FEBRUARY 2013", 120, WHITE, k=k)
    return im

def night(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.8, 0.8)
    ctext(d, 470, "SILVER WOODS ESTATE", 70, WHITE, k=k)
    ctext(d, 560, "PRETORIA · BEFORE DAWN", 34, CYAN, "Bold", k=k * eo(seg(t, 0.8, 1.5)))
    return im

def night_plain(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.8, 0.8)
    ctext(d, 540, "NO ONE ELSE WAS IN THAT HOUSE", 60, WHITE, k=k)
    return im

def account(t, dur):
    """His version, as he testified. Plain text, no stamps."""
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.5, 0.6)
    text(d, (220, 260), "HIS ACCOUNT · AS HE TOLD IT IN COURT", 30, CYAN, "Bold", alpha=k)
    d.rectangle([220, 310, 220 + 160 * k, 314], fill=CYAN)
    lines = [(0.4, "Woke up in the night"), (2.0, "Heard a noise in the bathroom"), (3.6, "Thought it was an intruder"),
             (6.2, "Grabbed his gun, without his legs on"), (8.2, "Fired because he was scared")]
    for i, (t0, s) in enumerate(lines):
        kk = k * eo(seg(t, t0, t0 + 0.6))
        text(d, (220, 380 + i * 92), s.upper(), 54, WHITE, "Black", alpha=kk)
    return im

def end_card(t, dur):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    k = eo(seg(t, 0.4, 1.6))
    text(d, (960, 500), "REEVA STEENKAMP", 96, WHITE, "Black", anchor="mm", alpha=k)
    text(d, (960, 600), "19 AUGUST 1983 – 14 FEBRUARY 2013", 36, GREY, "Bold", anchor="mm", alpha=eo(seg(t, 1.2, 2.2)))
    if t > dur - 1.4:
        im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, (dur - t) / 1.4))
    return im

# ------------------------------------------------------------------ trial & appeals
def verdict1(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "12 September 2014 · Judge Thokozile Masipa", "The verdict")
    rows = [("MURDER", "NOT GUILTY", GREY, 0.3), ("CULPABLE HOMICIDE", "GUILTY", ORANGE, 0.9)]
    for i, (a, b, col, t0) in enumerate(rows):
        kk = eo(seg(t, t0, t0 + 0.5))
        if kk <= 0: continue
        y = 420 + i * 170
        d.rectangle([160, y, 160 + 1240 * kk, y + 130], fill=(8, 10, 22), outline=col, width=3)
        text(d, (200, y + 30), a, 58, WHITE, "Black", alpha=kk)
        text(d, (1340, y + 36), b, 52, col, "Black", anchor="ra", alpha=kk)
    text(d, (160, 800), "CULPABLE HOMICIDE ≈ MANSLAUGHTER", 32, CYAN, "Bold", alpha=eo(seg(t, 2.0, 2.6)))
    return im

def sca_rule(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Supreme Court of Appeal · 3 December 2015", "Guilty of murder")
    lines = [(0.6, "FOUR SHOTS INTO A TINY TOILET CUBICLE", WHITE), (4.4, "SOMEONE BEHIND THAT DOOR COULD DIE", WHITE),
             (6.6, "WHO HE THOUGHT IT WAS DOESN'T MATTER", CYAN)]
    for i, (t0, s, col) in enumerate(lines):
        kk = eo(seg(t, t0, t0 + 0.6))
        text(d, (160 + int((1 - kk) * 40), 400 + i * 110), s, 54, col, "Black", alpha=kk)
    text(d, (160, 780), "LEGAL TERM: DOLUS EVENTUALIS · THE RULING, IN PLAIN WORDS", 26, GREY, "Bold", alpha=eo(seg(t, 7.6, 8.2)))
    return im

def six_vs_15(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Sentence for murder · July 2016", "6 years")
    for i, (n, lab, col, t0) in enumerate([(6, "WHAT MASIPA GAVE HIM", ORANGE, 0.3), (15, "SOUTH AFRICA'S MINIMUM FOR MURDER", CYAN, 0.9)]):
        kk = eo(seg(t, t0, t0 + 0.9))
        y = 430 + i * 190
        d.rectangle([160, y, 160 + 100 * n * kk, y + 110], fill=col)
        text(d, (180 + 100 * n * kk, y + 20), f"{n} YRS", 64, WHITE, "Black", alpha=kk)
        text(d, (160, y + 124), lab, 26, GREY, "Bold", alpha=kk)
    return im

def y13(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Supreme Court of Appeal · 24 November 2017", "Sentence more than doubled")
    k = eback(seg(t, 0.1, 0.5))
    f = gfx.font("Black", int(220 * min(1.05, k + 0.01)))
    d.text((960, 560), "13 YRS 5 MOS", font=f, fill=WHITE, anchor="mm")
    text(d, (960, 740), "THE 15-YEAR MINIMUM, LESS TIME SERVED", 34, CYAN, "Bold", anchor="mm", alpha=eo(seg(t, 0.8, 1.4)))
    return im

def release(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Parole denied March 2023 · granted November 2023", "Released")
    k = eback(seg(t, 0.3, 0.7))
    f = gfx.font("Black", int(150 * min(1.05, k + 0.01)))
    d.text((960, 560), "5 JANUARY 2024", font=f, fill=WHITE, anchor="mm")
    text(d, (960, 700), "WALKED OUT OF PRISON ON PAROLE", 38, CYAN, "Bold", anchor="mm", alpha=eo(seg(t, 0.9, 1.5)))
    return im

def parole(t, dur):
    im = background(t); d = ImageDraw.Draw(im, "RGBA")
    header(d, t, "Parole conditions", "On parole until 2029")
    rows = [(2.6, "ANGER MANAGEMENT"), (4.0, "PROGRAMMES ON VIOLENCE AGAINST WOMEN"), (6.5, "NO ALCOHOL"), (7.6, "NO TALKING TO THE MEDIA")]
    for i, (t0, s) in enumerate(rows):
        kk = eo(seg(t, t0, t0 + 0.5))
        if kk <= 0: continue
        y = 400 + i * 120
        d.rectangle([160, y + 14, 196, y + 50], outline=CYAN, width=4)
        if kk > 0.8: d.line([(166, y + 32), (178, y + 44), (196, y + 18)], fill=CYAN, width=5)
        text(d, (230, y), s, 52, WHITE, "Black", alpha=kk)
    return im

def june_quote(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.6, 0.7)
    text(d, (220, 300), "JUNE STEENKAMP · REEVA'S MOTHER · 2023", 30, CYAN, "Bold", alpha=k)
    text(d, (190, 330), "“", 220, (60, 62, 70), "Black", alpha=k)
    for i, s in enumerate(["The family…", "are the ones serving", "a life sentence."]):
        kk = k * eo(seg(t, 0.4 + i * 0.5, 1.0 + i * 0.5))
        text(d, (240, 440 + i * 100), s, 76, WHITE, "Black", alpha=kk)
    return im

def four_shots(t, dur):
    im = quiet_bg(t); d = ImageDraw.Draw(im, "RGBA")
    k = fade_in_out(t, dur, 0.6, 0.7)
    rows = [(0.2, "EVEN IF HE THOUGHT IT WAS AN INTRUDER", GREY, 40), (1.6, "FOUR SHOTS", WHITE, 110),
            (2.6, "THROUGH A LOCKED DOOR", WHITE, 70), (4.4, "IS NOT AN ACCIDENT", CYAN, 70)]
    for i, (t0, s, col, sz) in enumerate(rows):
        ctext(d, [330, 470, 590, 720][i], s, sz, col, k=k * eo(seg(t, t0, t0 + 0.6)))
    return im

GRAPHICS = {
    "date_open": date_open, "door": door, "profile": profile, "title": title_card, "born": born, "fibula": fibula,
    "sheila": sheila, "ban": ban, "cas": cas, "guns": guns, "tashas": tashas, "countdown": countdown,
    "feb14": feb14, "night": night, "night_plain": night_plain, "account": account, "end": end_card,
    "verdict1": verdict1, "sca_rule": sca_rule, "six_vs_15": six_vs_15, "y13": y13, "release": release,
    "parole": parole, "june_quote": june_quote, "four_shots": four_shots,
    "ch_fight": chapter("THE FIGHT TO RUN", "II"), "ch_cracks": chapter("THE CRACKS", "III"),
    "ch_trial": chapter("THE TRIAL", "IV"), "ch_after": chapter("AFTER", "V"),
}
