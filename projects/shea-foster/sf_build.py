"""Shea Foster documentary build (JxmyHighroller style: raw full-screen footage, hard cuts, real-audio beats,
white document cards, big white numbers, slow push-ins).

Stages:  python3 sf_build.py [plan] [video] [audio] [mux]
Shots are written in VOICEOVER time (seconds into voiceover/sf_vo_full.wav). Real-audio bites are inserted at
word boundaries; the narration pauses for them and `F()` maps voiceover time to final timeline time.
"""
import json, os, subprocess, sys
from multiprocessing import Pool
import numpy as np, cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_gfx as G

FPS, W, H = 30, 1920, 1080
P = os.path.dirname(os.path.abspath(__file__))
SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad/shea"
R = f"{SCR}/render"
DB, RL, AS, AI = f"{SCR}/dropbox", f"{SCR}/real", f"{SCR}/assets", f"{SCR}/ai"
NG, DL, FT, B12 = f"{RL}/ngtf_ep1.mp4", f"{RL}/day_in_life.mp4", f"{RL}/flotrack_fsu.mp4", f"{RL}/big12_xc_2021.mp4"
VO = f"{P}/voiceover/sf_vo_full.wav"
OLDSFX = "/home/user/YouTube-/projects/jon-drummond/sfx"
OUT = f"{P}/out/shea_foster_v1.mp4"
WORDS = json.load(open(f"{P}/voiceover/words.json"))[0]["words"]
VO_END = 332.52
TAIL = 2.5


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"FAILED {' '.join(cmd)[:300]}\n{r.stderr[-1500:]}")
    return r


def cut_after(word, approx):
    i = min((k for k, w in enumerate(WORDS) if w["w"] == word), key=lambda k: abs(WORDS[k]["s"] - approx))
    return round((WORDS[i]["e"] + WORDS[i + 1]["s"]) / 2, 3)


# ---------------------------------------------------------------- real-audio bites (source: NGTF "By The Grace of God" ep. 1)
PAD = 0.3
BITES = [  # name, cut (vo time), src, in, out
    ("sixth", cut_after("American.", 82.3), NG, 17.75, 29.95),
    ("news", cut_after("him.", 99.0), NG, 0.0, 11.95),
    ("world", cut_after("Jeep.", 106.5), NG, 49.35, 52.9),
    ("doctors", cut_after("rods.", 113.9), NG, 98.05, 104.85),
    ("surface", cut_after("athlete.", 194.2), NG, 199.5, 202.55),
]
BL = {b[0]: (b[4] - b[3]) + 2 * PAD for b in BITES}
CUTS = {b[1]: b for b in BITES}


def off(t):  # bites inserted at or before voiceover time t
    return sum(BL[b[0]] for b in BITES if b[1] <= t + 1e-6)


def F(t):
    return t + off(t)


END = F(VO_END) + TAIL

# ---------------------------------------------------------------- graphics catalogue
FOSTER_TAG = "VIA 'BY THE GRACE OF GOD' (2024)"
GFX = {
    "4yrs_open": lambda: G.big("4 YEARS", "BANNED FOR BLOOD DOPING"),
    "c_old": lambda: G.comment("he too old", 160, 230),
    "c_on": lambda: G.comment("he on something", 1020, 420),
    "c_pass": lambda: G.comment("check his passport", 300, 680),
    "lt_foster": lambda: G.lower("SHEA FOSTER", "Cypress, Texas"),
    "lt_foster_slu": lambda: G.lower("SHEA FOSTER", "Southeastern Louisiana"),
    "headline": lambda: G.doc("USADA.org · October 30, 2026", "...imposing a four-year period of ineligibility on Foster for his "
                              "positive test for Roxadustat (FG-4592), a blood doping agent.",
                              ["four-year period of ineligibility", "blood doping agent."],
                              title="Shea Foster Receives Doping Sanction from CAS Arbitrator"),
    "feb21": lambda: G.big("FEBRUARY 2021", "SOUTHLAND CONFERENCE INDOOR CHAMPIONSHIPS", size=200),
    "mile": lambda: G.big("4:03.57", "WON THE MILE"),
    "3000": lambda: G.big("8:00.79", "WON THE 3000M"),
    "5000": lambda: G.big("13:40.36", "WON THE 5000M"),
    "3rec": lambda: G.big("3 EVENTS. 3 RECORDS.", "ONE WEEKEND", size=170),
    "6th": lambda: G.big("6TH · 13:32", "NCAA INDOOR 5000M · ALL-AMERICAN"),
    "harvey": lambda: G.big("2017", "HURRICANE HARVEY FLOODS THE FAMILY HOME · HE LEAVES SCHOOL TO WORK AS A VALET"),
    "walkon": lambda: G.big("WALK-ON", "SOUTHEASTERN LOUISIANA · 2019"),
    "tag_news": lambda: G.tag("NEWS REPORT"),
    "tag_ngtf": lambda: G.tag(FOSTER_TAG),
    "screws": lambda: G.big("8 SCREWS · 4 RODS", "SPINAL FUSION"),
    "27th": lambda: G.big("27TH", "NCAA CROSS COUNTRY · ALL-AMERICAN AGAIN"),
    "june": lambda: G.center("JUNE 2021", 70, y=930),
    "nov": lambda: G.center("NOVEMBER 2021", 70, y=930),
    "fall22": lambda: G.big("FALL 2022", "OKLAHOMA STATE · NO SHEA FOSTER", size=200),
    "noinj": lambda: G.center("NO INJURY.", 130),
    "noann": lambda: G.center("NO ANNOUNCEMENT.", 130),
    "nothing": lambda: G.center("NOTHING.", 130),
    "noanswer": lambda: G.big("NO ANSWER", "FANS ON THE MESSAGE BOARDS ASKED WHY"),
    "teammates": lambda: G.center("WHAT HIS FORMER TEAMMATES TOLD ME", 54, y=940, weight="Bold"),
    "illus": lambda: G.tag("ILLUSTRATION"),
    "epo": lambda: G.big("EPO", None, size=300),
    "notest": lambda: G.center("NO TEST.", 140),
    "noban": lambda: G.center("NO BAN.", 140),
    "nohead": lambda: G.center("NO HEADLINE.", 140),
    "trials": lambda: G.big("JULY 2024", "U.S. PARALYMPIC TRIALS · FIRST PARA RACE OF HIS LIFE", size=200),
    "358": lambda: G.big("3:58.74", "1500M · FASTEST AMERICAN EVER IN HIS CLASS (T38)"),
    "medical": lambda: G.big("WITHDREW", "REPORTED AS \"MEDICAL REASONS\""),
    "d1": lambda: G.doc("USADA.org · October 30, 2026", "Foster, 29, tested positive for Roxadustat as the result of a sample "
                        "collected at the U.S. Paralympic Team Trials on July 20, 2024.", ["tested positive for Roxadustat"]),
    "roxa": lambda: G.big("ROXADUSTAT", "MAKES YOUR BODY PRODUCE MORE EPO", size=210),
    "d2": lambda: G.doc("USADA.org · October 30, 2026", "The initial arbitrator, who also serves as a CAS arbitrator, had accepted "
                        "Foster’s argument that his positive test resulted from residual traces of a substance he used before "
                        "becoming subject to the World Anti-Doping Code.",
                        ["residual traces of a substance he used before becoming subject to the World Anti-Doping Code."]),
    "not1": lambda: G.center("NOT: \"I DIDN'T TAKE IT.\"", 100, y=380),
    "not2": lambda: G.center("BUT: \"I TOOK IT BEFORE IT COUNTED.\"", 100, y=560),
    "noviol": lambda: G.big("NO VIOLATION", "THE FIRST ARBITRATOR'S RULING"),
    "d3": lambda: G.doc("USADA.org · October 30, 2026", "After receiving the parties’ submissions, including new human excretion "
                        "data for the prohibited substance, the CAS arbitrator issued a decision more than a year later, imposing "
                        "a four-year period of ineligibility on Foster for his positive test for Roxadustat (FG-4592), a blood "
                        "doping agent.", ["new human excretion data", "four-year period of ineligibility"], size=46),
    "4yrs": lambda: G.big("4 YEARS", "COURT OF ARBITRATION FOR SPORT · OCTOBER 2026"),
    "d4": lambda: G.doc("USADA.org · October 30, 2026", "In addition, Foster has been disqualified from all competitive results "
                        "obtained on and after July 20, 2024 including forfeiture of any medals, points and prizes.",
                        ["disqualified from all competitive results"]),
    "d5": lambda: G.doc("USADA.org · October 30, 2026", "Foster did not participate in the appeal despite having the opportunity "
                        "and being encouraged to do so. ... Foster notified USADA of his intent to retire on May 12, 2025.",
                        ["did not participate in the appeal", "intent to retire"]),
    "howlong": lambda: G.center("HOW LONG?", 150),
    "redacted": lambda: G.big("REDACTED", "THE FULL CAS DECISION IS NOT PUBLIC"),
    "c_old2": lambda: G.comment("too old", 200, 250),
    "c_on2": lambda: G.comment("on something", 1100, 430),
    "c_pass2": lambda: G.comment("check his passport", 330, 700),
    "4yrs_end": lambda: G.big("4 YEARS", "BANNED FOR A BLOOD-DOPING DRUG"),
    "look": lambda: G.center("DOPIN' DON'T GOT A LOOK.", 120),
}

# ---------------------------------------------------------------- shots (voiceover time)
F20 = f"{AS}/team20_foster.png"; A20 = f"{AS}/team20_allblur.png"
AFR, FOS = (875, 351), (737, 350)


def I(path, kf, **o):
    return dict(kind="I", path=path, kf=kf, **o)


def V(src, ss, z=(1.0, 1.06), **o):
    return dict(kind="V", src=src, ss=ss, z=z, **o)


def B(**o):
    return dict(kind="B", **o)


def ov(a, b, key, dim=0.0):
    return (a, b, key, dim)


SHOTS = [
    # 01 cold open: one continuous move on the blurred team photo
    (0.0, I(A20, [(0.0, 603, 400, 1.0), (13.6, 603, 385, 1.12), (15.9, 470, 360, 1.5), (17.4, 700, 355, 1.6),
                  (20.0, *AFR, 3.0), (28.3, *AFR, 3.5), (32.95, *AFR, 3.8), (33.2, *FOS, 3.4, "whip"), (37.3, *FOS, 4.1)],
            swap=(33.08, F20), bw=[(28.3, 32.9)], flash=[33.15],
            ov=[ov(9.1, 13.4, "4yrs_open", 0.55), ov(24.4, 28.2, "c_old"), ov(25.4, 28.2, "c_on"), ov(26.8, 28.2, "c_pass"),
                ov(34.2, 37.2, "lt_foster")])),
    (37.3, I(f"{DB}/11.jpg", [(0, 590, 560, 1.0), (4, 590, 520, 1.08)], dark=0.55, ov=[ov(37.3, 40.8, "headline")])),
    (40.9, I(f"{AS}/ng_flex.png", [(0, 960, 540, 1.1), (3.9, 960, 520, 1.2)], bw=[(0, 999)])),
    # 02 I seen him run
    (44.8, I(f"{AS}/ng_podium.png", [(0, 960, 540, 1.1), (6.4, 960, 500, 1.22)], ov=[ov(44.8, 51.1, "feb21", 0.6)])),
    (51.2, I(f"{DB}/05.jpg", [(0, 600, 640, 1.0), (5.2, 600, 560, 1.12)], fit="contain", ov=[ov(53.2, 56.3, "lt_foster_slu")])),
    (56.4, V(B12, 13.0, (1.0, 1.08))),
    (61.4, V(FT, 69.6, (1.0, 1.12))),
    (64.6, I(f"{DB}/06.png", [(0, 578, 332, 1.0), (3.3, 578, 332, 1.1)], crop=(24, 1255, 1180, 1920))),
    (67.9, I(f"{AS}/ng_race.png", [(0, 960, 540, 1.1), (4.0, 1000, 500, 1.25)], ov=[ov(67.9, 69.1, "mile", 0.6), ov(69.2, 70.3, "3000", 0.6), ov(70.4, 71.8, "5000", 0.6)])),
    (71.9, B(ov=[ov(71.9, 75.4, "3rec")])),
    (75.5, I(f"{AS}/ng_bib.png", [(0, 960, 540, 1.0), (3.4, 960, 540, 1.1)])),
    (78.9, I(f"{AS}/ng_board.png", [(0, 960, 540, 1.05), (3.9, 900, 560, 1.2)], ov=[ov(80.6, 82.8, "6th", 0.6)])),
    (83.3, I(f"{DB}/18.png", [(0, 645, 700, 1.0), (4.9, 645, 640, 1.1)], fit="contain")),
    (88.2, B(ov=[ov(88.2, 93.3, "harvey")])),
    (93.4, I(f"{DB}/10.png", [(0, 492, 492, 1.0), (4.5, 492, 470, 1.1)], crop=(194, 1096, 1178, 2080), fit="contain",
             ov=[ov(93.4, 95.5, "walkon", 0.5)])),
    (97.9, V(FT, 38.0, (1.0, 1.06))),
    # 03 the crash   (news bite plays before this)
    (100.3, V(NG, 44.0, (1.0, 1.05))),
    (104.0, I(f"{AS}/ng_jeep.png", [(0, 960, 540, 1.0), (2.9, 960, 560, 1.15)])),
    (107.3, V(NG, 54.6, (1.0, 1.08))),
    (110.7, I(f"{DB}/13.webp", [(0, 623, 830, 1.0), (4.0, 623, 700, 1.15)], fit="contain", ov=[ov(112.4, 113.9, "screws", 0.6)])),
    (114.8, V(B12, 66.0, (1.0, 1.06), ov=[ov(120.4, 122.8, "27th", 0.55)])),
    (122.9, I(f"{AS}/team17_foster.png", [(0, 603, 395, 1.0), (3.0, 700, 330, 1.35)])),
    (125.9, I(f"{AS}/split_june_nov.png", [(0, 960, 540, 1.0), (3.3, 960, 540, 1.04)], ov=[ov(125.9, 127.3, "june"), ov(127.4, 129.1, "nov")])),
    (129.2, V(B12, 222.0, (1.0, 1.06), speed=0.6)),
    # 04 gone
    (131.4, I(f"{AS}/team17_foster.png", [(0, 700, 330, 1.35), (3.5, 702, 300, 1.7)], bw=[(0, 999)], fadeout=1.0)),
    (134.9, B(ov=[ov(134.9, 141.2, "fall22")])),
    (141.3, V(B12, 22.0, (1.05, 1.12), bw=True, dark=0.55, ov=[ov(141.3, 142.3, "noinj"), ov(142.4, 143.5, "noann"),
                                                                 ov(143.6, 144.4, "nothing")])),
    (144.5, I(f"{DB}/18.png", [(0, 645, 700, 1.0), (2.8, 645, 600, 1.15)], fit="contain", bw=[(0, 999)])),
    (147.3, B(ov=[ov(147.3, 152.5, "noanswer")])),
    (152.6, I(f"{AS}/team19_blur.png", [(0, 603, 393, 1.0), (7.9, 640, 300, 1.25)], bw=[(0, 999)], ov=[ov(154.7, 160.3, "teammates")])),
    (160.5, I(f"{AI}/room1.png", [(0, 640, 360, 1.0), (6.1, 420, 300, 1.35)], ov=[ov(160.5, 171.0, "illus")])),
    (166.6, I(f"{AI}/drawer1.png", [(0, 640, 360, 1.0), (3.4, 680, 560, 1.5), (5.3, 680, 560, 1.55), (7.8, 680, 560, 1.58)],
              flash=[171.9], ov=[ov(166.6, 174.3, "illus"), ov(170.0, 171.0, "epo", 0.35)])),
    (174.4, V(B12, 150.0, (1.0, 1.06), bw=True)),
    (178.3, I(f"{DB}/18.png", [(0, 645, 700, 1.15), (3.3, 645, 640, 1.25)], fit="contain", bw=[(0, 999)], fadeout=0.6)),
    (181.7, B(ov=[ov(181.7, 182.8, "notest"), ov(182.9, 183.8, "noban"), ov(183.9, 185.0, "nohead")])),
    # 05 Paralympics
    (188.7, V(DL, 4.0, (1.0, 1.06))),
    (191.6, I(f"{DB}/12.webp", [(0, 316, 450, 1.0), (2.8, 316, 400, 1.1)], fit="contain")),
    (195.3, V(NG, 384.0, (1.0, 1.06), ov=[ov(195.3, 199.9, "trials", 0.55)])),
    (200.8, V(NG, 396.0, (1.0, 1.06), ov=[ov(201.3, 204.0, "358", 0.55)])),
    (204.1, I(f"{DB}/11.jpg", [(0, 590, 720, 1.0), (2.3, 590, 700, 1.06)], fit="contain")),
    (206.4, I(f"{DB}/15.jpg", [(0, 317, 440, 1.0), (2.2, 317, 380, 1.12)], fit="contain")),
    (208.6, I(f"{DB}/16.jpg", [(0, 318, 191, 1.0), (2.2, 318, 191, 1.06)])),
    (210.8, I(f"{DB}/14.webp", [(0, 290, 512, 1.0), (3.3, 290, 450, 1.12)], fit="contain")),
    (214.1, I(f"{DB}/11.jpg", [(0, 590, 720, 1.0), (5.8, 590, 600, 1.18)], fit="contain", bw=[(0, 999)],
              ov=[ov(217.2, 219.8, "medical", 0.6)])),
    # 06 the truth
    (219.9, B()),
    (222.6, B(ov=[ov(222.6, 226.7, "d1")])),
    (226.8, B(ov=[ov(226.8, 228.0, "roxa")])),
    (228.1, V(B12, 88.0, (1.0, 1.08))),
    (232.8, V(NG, 458.0, (1.0, 1.08), speed=0.6)),
    (236.5, I(f"{AI}/drawer1.png", [(0, 680, 560, 1.4), (3.9, 680, 560, 1.55)], bw=[(0, 999)],
              ov=[ov(236.5, 240.3, "illus"), ov(236.5, 237.5, "epo", 0.35)])),
    (240.4, B(ov=[ov(240.4, 248.6, "d2")])),
    (248.7, B(ov=[ov(249.9, 255.2, "not1"), ov(252.1, 255.2, "not2")])),
    (255.3, B(ov=[ov(255.3, 258.9, "noviol")])),
    (259.0, B(ov=[ov(259.0, 265.6, "d3")])),
    (265.7, I(F20, [(0, *FOS, 3.0), (6.8, *FOS, 3.6)], bw=[(0, 999)], ov=[ov(270.9, 272.4, "4yrs", 0.6)])),
    (272.5, B(ov=[ov(272.5, 275.6, "d4")])),
    (275.7, B(ov=[ov(275.7, 279.8, "d5")])),
    # 07 my take
    (279.9, B(ov=[ov(280.0, 283.6, "howlong"), ov(283.7, 286.0, "redacted")])),
    (286.1, I(f"{AS}/ng_race.png", [(0, 960, 540, 1.1), (3.9, 1000, 480, 1.3)])),
    (288.0, I(f"{AS}/ng_osu.png", [(0, 960, 540, 1.05), (2.0, 960, 500, 1.15)])),
    (290.0, V(FT, 71.0, (1.05, 1.15))),
    (293.7, I(f"{DB}/05.jpg", [(0, 600, 600, 1.0), (3.2, 600, 560, 1.1)], fit="contain")),
    (296.9, I(f"{AI}/drawer1.png", [(0, 680, 560, 1.3), (5.8, 680, 560, 1.5)], bw=[(0, 999)], ov=[ov(296.9, 302.6, "illus")])),
    (302.7, I(A20, [(0, *AFR, 2.6), (11.9, *AFR, 3.3)], ov=[ov(310.8, 314.6, "c_old2"), ov(312.0, 314.6, "c_on2"),
                                                            ov(313.1, 314.6, "c_pass2")])),
    (314.7, I(F20, [(0, *FOS, 2.6), (9.7, *FOS, 3.6)], ov=[ov(318.9, 322.1, "4yrs_end", 0.6)])),
    (324.5, B(ov=[ov(324.5, 327.4, "look")])),
    (327.6, I(A20, [(0, 603, 385, 1.3), (5.0, 603, 400, 1.0), (7.5, 603, 400, 1.0)], fadeout=2.2)),
    (VO_END, B()),
]
BITE_SPEC = {
    "sixth": dict(ov=["tag_ngtf"]),
    "news": dict(ov=["tag_news"]),
    "world": dict(ov=["tag_ngtf"]),
    "doctors": dict(ov=["tag_ngtf"]),
    "surface": dict(ov=["tag_ngtf"]),
}


def plan():
    ts = [s[0] for s in SHOTS]
    bounds = sorted(set(ts + list(CUTS) + [VO_END + TAIL]))
    segs = []
    for x, y in zip(bounds, bounds[1:]):
        if x in CUTS:
            b = CUTS[x]
            fs = x + off(x) - BL[b[0]]
            segs.append(dict(kind="BITE", name=b[0], src=b[2], ss=b[3] - PAD, fs=fs, fe=fs + BL[b[0]], **BITE_SPEC[b[0]]))
        k = max(i for i, t in enumerate(ts) if t <= x + 1e-6)
        if x in CUTS and y - x < 0.7 and y in ts:   # sliver after a bite: start the next shot early instead
            k = ts.index(y)
        segs.append(dict(kind="SHOT", shot=k, t0=ts[k], lo=x - ts[k], fs=x + off(x), fe=y + off(x)))
    for i, s in enumerate(segs):
        s["i"] = i
        s["f0"], s["f1"] = round(s["fs"] * FPS), round(s["fe"] * FPS)
    return segs


# ---------------------------------------------------------------- rendering
_gcache = {}


def gfx(key):
    if key not in _gcache:
        os.makedirs(f"{R}/gfx", exist_ok=True)
        p = f"{R}/gfx/{key}.png"
        if not os.path.exists(p):
            GFX[key]().save(p)
        a = np.asarray(Image.open(p).convert("RGBA"), np.float32) / 255
        _gcache[key] = (a[..., :3] * a[..., 3:], a[..., 3:])
    return _gcache[key]


def load_img(path, crop=None):
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop(crop)
    return np.asarray(im)


def ease(u):
    u = min(1, max(0, u))
    return u * u * (3 - 2 * u)


def ease_whip(u):
    u = min(1, max(0, u))
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def kf_at(kf, t):
    if t <= kf[0][0]:
        return kf[0][1:4], False
    for a, b in zip(kf, kf[1:]):
        if t <= b[0]:
            whip = len(b) > 4 and b[4] == "whip"
            u = (t - a[0]) / max(1e-6, b[0] - a[0])
            e = ease_whip(u) if whip else ease(u)
            return tuple(a[i] + (b[i] - a[i]) * e for i in (1, 2, 3)), whip and 0.02 < u < 0.98
    return kf[-1][1:4], False


def warp(img, cx, cy, s, fit):
    h, w = img.shape[:2]
    if fit == "cover":  # keep the frame filled
        half_w, half_h = W / 2 / s, H / 2 / s
        cx = min(max(cx, half_w), w - half_w) if w > 2 * half_w else w / 2
        cy = min(max(cy, half_h), h - half_h) if h > 2 * half_h else h / 2
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))


def grade(fr, bw=False, dark=0.0):
    f = fr.astype(np.float32)
    if bw:
        g = f @ np.float32([0.299, 0.587, 0.114])
        g = np.clip((g - 128) * 1.15 + 128, 0, 255)
        f = np.repeat(g[..., None], 3, 2)
    if dark:
        f *= (1 - dark)
    return f


def video_frames(src, ss, n, speed=1.0):
    vf = f"setpts=PTS/{speed},fps={FPS}," if speed != 1 else f"fps={FPS},"
    vf += f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{n / FPS * speed + 1:.3f}", "-i", src, "-an",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        yield last if last is not None else np.zeros((H, W, 3), np.uint8)
    p.stdout.close(); p.wait()


def in_ranges(t, rs):
    return any(a <= t < b for a, b in rs)


def render_seg(seg):
    out = f"{R}/segs/{seg['i']:03d}.mp4"
    n = seg["f1"] - seg["f0"]
    if os.path.exists(out) or n <= 0:
        return out
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                            "-threads", "2", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    if seg["kind"] == "BITE":
        frames = video_frames(seg["src"], seg["ss"], n)
        for j, fr in enumerate(frames):
            lt = j / FPS
            z = 1.0 + 0.04 * lt / (n / FPS)
            f = grade(warp(fr, W / 2, H / 2, z, "cover"))
            for key in seg["ov"]:
                c, a = gfx(key)
                f = f * (1 - a) + c * 255
            enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    else:
        sh = SHOTS[seg["shot"]][1]
        t0 = SHOTS[seg["shot"]][0]
        nxt = SHOTS[seg["shot"] + 1][0] if seg["shot"] + 1 < len(SHOTS) else VO_END + TAIL
        shot_len = nxt - t0
        kind = sh["kind"]
        if kind == "I":
            img = load_img(sh["path"], sh.get("crop"))
            img2 = load_img(sh["swap"][1], sh.get("crop")) if "swap" in sh else None
            h, w = img.shape[:2]
            base = max(W / w, H / h) if sh.get("fit", "cover") == "cover" else min(W / w, H / h)
        elif kind == "V":
            frames = video_frames(sh["src"], sh["ss"] + seg["lo"] * sh.get("speed", 1.0), n, sh.get("speed", 1.0))
        for j in range(n):
            lt = seg["lo"] + j / FPS          # local time in the shot
            vt = t0 + lt                     # voiceover time
            if kind == "B":
                f = np.zeros((H, W, 3), np.float32)
            elif kind == "I":
                src = img2 if img2 is not None and vt >= sh["swap"][0] else img
                (cx, cy, z), whip = kf_at(sh["kf"], lt)
                if whip:  # motion blur: average sub-frames along the move
                    acc = np.zeros((H, W, 3), np.float32)
                    for q in range(6):
                        (qx, qy, qz), _ = kf_at(sh["kf"], lt + (q - 2.5) / FPS / 3)
                        acc += warp(src, qx, qy, base * qz, sh.get("fit", "cover"))
                    fr = acc / 6
                else:
                    fr = warp(src, cx, cy, base * z, sh.get("fit", "cover"))
                f = grade(fr, in_ranges(lt, sh.get("bw", [])) or in_ranges(vt, sh.get("bw", [])), sh.get("dark", 0))
            else:
                fr = next(frames)
                z0, z1 = sh["z"]
                z = z0 + (z1 - z0) * lt / shot_len
                f = grade(warp(fr, W / 2, H / 2, z, "cover"), sh.get("bw", False), sh.get("dark", 0))
            for a_, b_, key, dim in sh.get("ov", []):
                if a_ <= vt < b_:
                    k_in = min(1, (vt - a_) * FPS / 4 + 0.25)
                    k_out = min(1, (b_ - vt) * FPS / 3)
                    al = max(0, min(k_in, k_out))
                    if dim:
                        f *= 1 - dim * al
                    c, a = gfx(key)
                    f = f * (1 - a * al) + c * 255 * al
            for ft in sh.get("flash", []):
                d = vt - ft
                if 0 <= d < 0.3:
                    k = 1 - d / 0.3
                    f = f * (1 - 0.85 * k) + 255 * 0.85 * k
            fo = sh.get("fadeout")
            if fo and shot_len - lt < fo:
                f *= max(0, (shot_len - lt) / fo)
            enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    os.replace(out + ".tmp.mp4", out)
    return out


def make_assets():
    p = f"{AS}/split_june_nov.png"
    if not os.path.exists(p):
        a = Image.open(f"{DB}/13.webp").convert("RGB")
        b = Image.open(f"{AS}/team17_foster.png").convert("RGB").crop((520, 120, 900, 700))
        canvas = Image.new("RGB", (W, H), (0, 0, 0))
        for k, im in enumerate((a, b)):
            s = min(940 / im.width, H / im.height)
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
            canvas.paste(im, (k * 960 + (960 - im.width) // 2, (H - im.height) // 2))
        canvas.save(p)


def stage_plan():
    segs = plan()
    json.dump(segs, open(f"{R}/plan.json", "w"), indent=0)
    for s in segs:
        lab = s.get("name") or SHOTS[s["shot"]][1].get("path", SHOTS[s["shot"]][1].get("src", "black")).split("/")[-1]
        print(f"{s['i']:3d} {s['kind']:4s} {s['fs']:7.2f}-{s['fe']:7.2f} ({s['fe'] - s['fs']:5.2f}s) {lab}")
    print("END", round(END, 2), "segments", len(segs))


def stage_video():
    os.makedirs(f"{R}/segs", exist_ok=True)
    make_assets()
    for k in GFX:  # pre-render graphics once (workers then just load them)
        gfx(k)
    segs = plan()
    with Pool(3) as pool:
        for k, o in enumerate(pool.imap_unordered(render_seg, segs)):
            if k % 10 == 0:
                print("seg", k, "/", len(segs), flush=True)
    lst = f"{R}/segs.txt"
    open(lst, "w").write("".join(f"file '{R}/segs/{s['i']:03d}.mp4'\n" for s in segs if s["f1"] > s["f0"]))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/base.mp4"])
    print("base", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/base.mp4"]).stdout.strip())


# ---------------------------------------------------------------- audio
SFX = [  # (voiceover time, file, gain)
    (0.0, "sub-boom", 0.45), (9.1, "rubber-stamp", 0.5), (32.95, "whoosh", 0.7), (33.1, "sub-boom", 1.0),
    (37.3, "newspaper-rip", 0.45), (44.8, "sub-boom", 0.4), (71.9, "sub-boom", 0.45), (112.4, "sub-boom", 0.5),
    (134.9, "sub-boom", 0.5), (170.0, "sub-boom", 0.6), (171.9, "shutter", 0.9), (181.7, "rubber-stamp", 0.45),
    (182.9, "rubber-stamp", 0.45), (183.9, "rubber-stamp", 0.45), (217.2, "sub-boom", 0.45), (220.1, "sub-boom", 1.0),
    (222.6, "newspaper-rip", 0.4), (255.3, "rubber-stamp", 0.7), (270.9, "sub-boom", 0.9), (283.7, "rubber-stamp", 0.5),
    (318.9, "sub-boom", 0.7), (324.5, "sub-boom", 0.6),
]
HEART = [(16.0, 28.3, 0.85), (302.7, 314.6, 0.5)]   # heartbeat loops (voiceover time)
# music: (file, file_offset, start_final, end_final, gain)
def music_plan():
    s4 = F(131.4)
    return [("M1_dark", 0.0, 0.0, F(17.0), 0.30),
            ("M1_dark", 17.0, F(33.1), s4 + 1.5, 0.26),
            ("M2_verdict", 0.0, s4, min(END, s4 + 178.0), 0.26),
            ("M1_dark", 95.0, s4 + 175.0, END, 0.26)]


def stage_audio():
    os.makedirs(f"{R}/aud", exist_ok=True)
    inputs, fc = [], []
    k = 0
    # voiceover pieces
    cuts = sorted(CUTS)
    pieces = list(zip([0.0] + cuts, cuts + [VO_END + 0.5]))
    vo = []
    for a, b in pieces:
        inputs += ["-i", VO]
        ms = int(round(F(a) * 1000)) if a else 0
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={a}:{b},asetpts=PTS-STARTPTS,adelay={ms}|{ms}[v{k}]")
        vo.append(f"[v{k}]"); k += 1
    for name, cut, src, s, e in BITES:
        f = f"{R}/aud/{name}.wav"
        if not os.path.exists(f):
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(s), "-t", str(e - s), "-i", src, "-vn", "-ac", "2", "-ar", "48000",
                 "-af", "afade=t=in:d=0.08,afade=t=out:st=%.2f:d=0.15,loudnorm=I=-17:TP=-2:LRA=8" % (e - s - 0.15), f])
        inputs += ["-i", f]
        ms = int(round((cut + off(cut) - BL[name] + PAD) * 1000))
        fc.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[v{k}]")
        vo.append(f"[v{k}]"); k += 1
    fc.append(f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0,apad=whole_dur={END:.3f},asplit=2[vo][sc]")
    mus = []
    for name, fo, a, b, g in music_plan():
        inputs += ["-i", f"{P}/music/{name}.mp3"]
        ln = b - a; ms = int(a * 1000)
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={fo}:{fo + ln:.2f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=1.5,afade=t=out:st={max(0, ln - 2):.2f}:d=2,volume={g},adelay={ms}|{ms}[m{k}]")
        mus.append(f"[m{k}]"); k += 1
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,equalizer=f=220:t=q:w=1.1:g=-3[mbus]")
    fc.append("[mbus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=25:release=450:makeup=1[mduck]")
    fx = []
    for t, name, g in SFX:
        d = f"{P}/sfx" if os.path.exists(f"{P}/sfx/{name}.mp3") else OLDSFX
        inputs += ["-i", f"{d}/{name}.mp3"]; ms = int(F(t) * 1000)
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for a, b, g in HEART:
        inputs += ["-stream_loop", "-1", "-i", f"{P}/sfx/heartbeat.mp3"]; ms = int(F(a) * 1000); ln = F(b) - F(a)
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{ln:.2f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=1,afade=t=out:st={ln - 0.6:.2f}:d=0.6,volume={g},adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    fc.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    fc.append(f"[vo][mduck][fx]amix=inputs=3:normalize=0,atrim=0:{END:.3f},afade=t=out:st={END - 2.5:.2f}:d=2.5,"
              f"loudnorm=I=-14:TP=-1:LRA=9,aresample=48000[out]")
    open(f"{R}/audio.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/audio.txt", "-map", "[out]", "-c:a", "pcm_s16le",
                                                    f"{R}/mix.wav"])
    print("mix", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/mix.wav"]).stdout.strip())


def stage_mux():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/base.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-vf", "noise=alls=4:allf=t,fade=in:st=0:d=0.6,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", OUT])
    print("wrote", OUT)


if __name__ == "__main__":
    os.makedirs(R, exist_ok=True)
    for s in sys.argv[1:] or ["plan", "video", "audio", "mux"]:
        print("==", s, flush=True)
        globals()["stage_" + s]()
