"""Did Candace Hill Finesse ASICS? Documentary edit on the user's own voiceover, in the approved Boling v2 style
(projects/matthew-boling/EDIT_STYLE.md). Copied from boling_build.py; only the config, soundbites and EDL differ.

- Voiceover: the user's 8 Dropbox takes, cleaned by clean_voiceover.py (flubs cut, long pauses shortened, no tempo change).
- Soundbites: the race call of the 10.98 (cold open), CNN, Trans World Sport, Gatorade, IAAF Inside Athletics,
  MileSplit "Stay Your Lane", the 2016 U20 race call, FloTrack 2021, 11Alive 2024. The voiceover pauses for each.
- Receipts: real articles (SI, Canadian Running, Footwear News/WWD, MileSplit, World Athletics, RunBlogRun) with the key
  line boxed in red, pushed in slowly (clips/art_*.mp4).

Every time in the EDL is raw voiceover seconds; FT() maps it onto the final timeline.
Run:  python3 projects/candace-hill/candace_build.py [stage ...]   stages: shots concat audio mux (default all); check
"""
import os, sys, json, math, subprocess, hashlib, difflib
import numpy as np
from PIL import Image, ImageFilter

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/candace-hill"
sys.path.insert(0, f"{ROOT}/tools")
import kinetic as K
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
CS = f"{SCR}/candace"; REAL = f"{CS}/clips"; R = f"{CS}/render"
for d in ("ov", "shots", "sfx", "tags"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/candace_voiceover.wav"
OUT = f"{SCR}/output/Did_Candace_Hill_Finesse_ASICS.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/vo_words.json"))[0]["words"]
_NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def _tok(w):
    t = "".join(ch for ch in w.lower() if ch.isalnum())
    return _NUMW[int(t)] if t.isdigit() and int(t) <= 20 else t
TOK = [_tok(x["w"]) for x in WORDS]
VO_END = WORDS[-1]["e"]
PART = {k: min(w["s"] for w in WORDS if w["part"] == k) for k in range(1, 9)}
_CUR = [0.0]
def A(phrase, after=None, end=False, win=45):
    """First match of `phrase` at/after the running cursor; tolerant of whisper misspellings."""
    t0 = _CUR[0] if after is None else after
    p = [_tok(x) for x in phrase.split() if _tok(x)]; tgt = " ".join(p); best = (0, None)
    for i in range(len(TOK) - len(p) + 1):
        if WORDS[i]["s"] < t0 - 1e-6: continue
        if WORDS[i]["s"] > t0 + win: break
        if TOK[i:i + len(p)] == p: best = (1, i); break
        r = difflib.SequenceMatcher(None, tgt, " ".join(TOK[i:i + len(p)])).ratio()
        if r >= 0.8: best = (r, i); break
        if r > best[0] + 0.02: best = (r, i)
    if best[0] < 0.6: raise KeyError(f"no match for {phrase!r} after {t0:.1f} (best {best[0]:.2f})")
    i = best[1]; t = WORDS[i + len(p) - 1]["e"] if end else WORDS[i]["s"]
    if not end: _CUR[0] = t
    return t

# ------------------------------------------------------------------ source credits
TAGS = {
    "c_1098_hs": "FLOTRACK · BROOKS PR · JUNE 20, 2015", "c_brooks": "YOUTH RUNNER · BROOKS PR 2015", "c_cnn": "CNN · 2015",
    "c_tws": "TRANS WORLD SPORT · 2016", "c_gatorade": "GATORADE PLAYER OF THE YEAR · 2015", "c_cali100": "WORLD YOUTH CHAMPS · CALI 2015",
    "c_cali200": "WORLD YOUTH CHAMPS · CALI 2015", "c_asics_ad": "ASICS", "c_stayyourlane": "MILESPLIT · STAY YOUR LANE · 2018",
    "c_insideath": "IAAF INSIDE ATHLETICS · 2016", "c_u20final": "WORLD U20 CHAMPS · BYDGOSZCZ 2016", "c_letsrun16": "LETSRUN · 2016",
    "c_ms_junior": "MILESPLIT · USATF JUNIORS 2017", "c_wa60": "WORLD ATHLETICS · 2018", "c_flo2021": "FLOTRACK · 2021",
    "c_trials21": "NBC · OLYMPIC TRIALS 2021", "c_semi24": "OLYMPIC TRIALS 2024 · SEMI-FINAL", "c_trials24": "NBC · OLYMPIC TRIALS 2024",
    "c_11alive": "11ALIVE NEWS · 2024", "c_150atl": "ATLANTA CITY GAMES · 2024", "c_fresh": "NFHS NETWORK · GEORGIA STATE 2014",
    "art_si_0": "SPORTS ILLUSTRATED · DEC 17, 2015", "art_si_1": "SPORTS ILLUSTRATED · DEC 17, 2015",
    "art_cr_h0": "CANADIAN RUNNING · DEC 18, 2015", "art_wwd_h0": "FOOTWEAR NEWS · DEC 2015",
    "art_ms_0": "MILESPLIT · OCT 27, 2015", "art_ms_1": "MILESPLIT · OCT 27, 2015",
    "art_wa_0": "WORLD ATHLETICS · MAY 2021", "art_wa_1": "WORLD ATHLETICS · MAY 2021", "art_wa_2": "WORLD ATHLETICS · MAY 2021",
    "art_rbr_h0": "RUNBLOGRUN · MARCH 2023", "art_rbr_h1": "RUNBLOGRUN · MARCH 2023",
}

# ------------------------------------------------------------------ soundbites (inserted; the voiceover pauses)
def snap(src, a, b):
    """Snap a soundbite to the clip's own word boundaries so no word is clipped."""
    try: segs = json.load(open(f"{CS}/tx/{src}.json"))
    except FileNotFoundError: return a, b
    ws = [w for s in segs for w in s["w"]]
    st = [w["s"] for w in ws if w["s"] >= a - 0.4]; en = [w["e"] for w in ws if w["e"] <= b + 0.4]
    a2 = (min(st) - 0.12) if st else a; b2 = (max(en) + 0.3) if en else b
    return round(max(0, a2), 2), round(max(b2, a2 + 1), 2)

PAD = 0.3
PRE_SB = ("c_1098_hs", 46.8, 57.4, "FLOTRACK BROADCAST · JUNE 20, 2015")   # cold open: "No, no, no... 10.98... national record"
SB_LIST = [  # ((before phrase, part), src, a, b, credit)
    (("six months later", 1), "c_tws", 41.3, 45.8, "CANDACE HILL · TRANS WORLD SPORT"),
    (("no high school girl", 2), "c_brooks", 33.0, 47.7, "CANDACE HILL · MINUTES AFTER THE 10.98"),
    (("that same summer", 2), "c_cnn", 69.25, 78.33, "CNN · 2015"),
    (("you know the only", 2), "c_gatorade", 107.3, 113.4, "GATORADE · 2015"),
    (("there is calling", 2), "c_gatorade", 42.2, 56.9, "COACH · GATORADE POY FILM"),
    (("ain t never say", 3), "c_stayyourlane", 176.2, 182.6, "CANDACE HILL · 2018"),
    (("so at 16", 3), "c_stayyourlane", 188.3, 201.2, "CANDACE HILL · 2018"),
    (("so at 16", 3), "c_stayyourlane", 206.4, 214.1, "CANDACE HILL · 2018"),
    (("the very", 4), "c_tws", 423.0, 438.1, "COACH TONY CARPENTER · 2016"),
    (("she still makes", 4), "c_stayyourlane", 251.3, 264.9, "CANDACE HILL · 2018"),
    (("then goes to the world", 4), "c_insideath", 219.2, 233.5, "CANDACE HILL · AFTER THE 2016 TRIALS"),
    (("so the talent", 4), "c_u20final", 56.1, 71.7, "EUROSPORT · WORLD U20 FINAL 2016"),
    (("but then", 4), "c_insideath", 266.0, 280.7, "CANDACE HILL · AGE 17"),
    (("in 2019 at usas", 4), "c_stayyourlane", 318.5, 327.8, "CANDACE HILL · 2018"),
    (("she started seeing", 5), "c_stayyourlane", 268.2, 278.7, "CANDACE HILL · 2018"),
    (("2021", 6), "c_stayyourlane", 516.0, 524.9, "CANDACE HILL · 2018"),
    (("july of 2021", 6), "c_flo2021", 84.0, 88.3, "FLOTRACK · 2021"),
    (("2024", 6), "c_11alive", 26.8, 42.4, "11ALIVE NEWS · MAY 2024"),
    (("but ain t nobody", 8), "c_ms_junior", 159.4, 167.6, "CANDACE HILL · 2017"),
    (("so which one", 8), "c_tws", 403.9, 421.4, "CANDACE HILL · 2016"),
]
SOUNDBITES = []
def _sb():
    keep = _CUR[0]; _CUR[0] = 0.0
    for ph, src, a, b, cr in SB_LIST:
        a, b = snap(src, a, b)
        t = A(ph[0], PART[ph[1]] - 0.5, win=1e9) - 0.25
        SOUNDBITES.append(dict(t=round(t, 3), src=src, ss=a, dur=round(b - a, 3), tag=cr))
    SOUNDBITES.sort(key=lambda s: s["t"]); _CUR[0] = keep
PRE = (PRE_SB[2] - PRE_SB[1]) + 2 * PAD + 0.6
def FT(t):
    sh = PRE
    for s in SOUNDBITES:
        if s["t"] <= t + 1e-6: sh += s["dur"] + 2 * PAD
    return t + sh
def SB_START(s):
    sh = PRE
    for o in SOUNDBITES:
        if o is s: break
        sh += o["dur"] + 2 * PAD
    return s["t"] + sh

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode: print(" ".join(map(str, cmd))[:1200]); print(r.stderr[-2500:]); raise SystemExit(1)
    return r

# ------------------------------------------------------------------ edit decision list (raw VO seconds)
SHOTS, OVER = [], []
def S(t, src, ss=0.0, **o):
    o.setdefault("tag", TAGS.get(src, "")); SHOTS.append(dict(t=round(t, 3), src=src, ss=ss, **o))
def O(t, dur, spec): OVER.append((round(t, 3), round(t + dur, 3), spec))
def stat(t, dur, big, label, col="orange"): O(t, dur, ("stat", big, label, col))
def say(t, dur, text, col="white", pos="b", hi=None, size=130): O(t, dur, ("words", text, col, pos, hi, size))
def stack(t, dur, lines, col="orange"): O(t, dur, ("stack", lines, col))
def name(t, dur, n, sub, col="orange"): O(t, dur, ("name", n, sub, col))
def stamp(t, dur, text, col="red"): O(t, dur, ("stamp", text, col))
def chapter(t, num, title): O(t, 2.6, ("chapter", num, title, "orange"))

def build_edl():
    _sb(); a = A; _CUR[0] = 0.0
    # 1 cold open ---------------------------------------------------------------------
    S(a("june"), "c_brooks", 6.7, amb=1); say(a("june"), 2.4, "JUNE 20, 2015", "white", "t")
    S(a("shoreline"), "c_cnn", 9.0); say(a("shoreline"), 2.0, "SHORELINE, WASHINGTON", "orange", "t", "SHORELINE,")
    S(a("a 16 year"), "c_gatorade", 20.0); say(a("16 year"), 1.8, "AGE 16", "orange", "t")
    S(a("10 98") - 0.1, "c_cnn", 26.9, punch=0.3); stat(a("10 98"), 2.4, "10.98", "100M · AGE 16", "orange")
    S(a("six months later"), "c_asics_ad", 1.0)
    S(a("asics hands"), "art_si_0", 0.0); stat(a("10 year pro"), 2.2, "10 YEARS", "PRO DEAL · ASICS", "gold")
    S(a("at 16 reportedly"), "art_ms_1", 1.5); say(a("six figures"), 1.6, "6 FIGURES A YEAR", "gold", "b", "FIGURES")
    stamp(a("no deductions"), 1.8, "NO DEDUCTIONS", "gold")
    S(a("and after that day"), "c_brooks", 28.1, slow=0.5, bw=1)
    S(a("she had never run"), "c_trials21", 10.0, bw=1); say(a("under 11"), 1.8, "NEVER UNDER 11 AGAIN", "red", "b", "NEVER")
    S(a("never made team"), "c_trials21", 190.0, bw=1, punch=1.2); say(a("never made team"), 2.6, "NO OLYMPIC OR WORLDS TEAM", "red", "b", "NO")
    S(a("never ran a personal"), "c_tws", 488.2, bw=1); say(a("never ran a personal"), 2.6, "NO PR · 100 OR 200", "red", "b", "NO PR")
    S(a("not once"), "c_gatorade", 211.7, bw=1, punch=0.2)
    S(a("so real talk"), "c_asics_ad", 47.4)
    S(a("the candace"), "c_asics_ad", 55.1, punch=0.6); say(a("the candace"), 2.6, "DID SHE FINESSE ASICS?", "orange", "c", "FINESSE", 150)
    S(a("let me tell"), "c_gatorade", 224.5)
    # 2 the fastest girl alive ------------------------------------------------------------
    S(PART[2] - 0.15, "c_gatorade", 28.0, flash=1); chapter(PART[2], "01", "THE FASTEST GIRL ALIVE")
    S(a("from conyers"), "c_tws", 74.5); name(a("from conyers"), 2.8, "CANDACE HILL", "CONYERS, GEORGIA · ROCKDALE COUNTY HS")
    S(a("roxdale county"), "c_fresh", 7.3, amb=1)
    S(a("and that 10 98"), "c_cnn", 26.9, punch=0.5)
    S(a("wasn t no fluke"), "c_cnn", 68.8); say(a("fluke"), 1.6, "NOT A FLUKE", "cyan", "c", "FLUKE")
    S(a("no high school girl"), "c_brooks", 22.8); say(a("11 seconds") - 0.3, 2.2, "FIRST HS GIRL UNDER 11", "gold", "b", "UNDER 11")
    S(a("that same summer"), "c_cali100", 4.6)
    S(a("world youth"), "c_cali100", 51.0, amb=1)
    S(a("and she win the 100"), "c_cali100", 97.3, punch=0.4); stat(a("win the 100") + 0.3, 2.2, "11.08", "100M · WORLD YOUTH GOLD", "gold")
    S(a("and the 200"), "c_cali200", 97.2); stat(a("2243"), 2.6, "22.43", "200M · WORLD YOUTH BEST", "gold")
    S(a("she won gatorade"), "c_gatorade", 139.8); say(a("she won gatorade"), 2.6, "GATORADE NATIONAL ATHLETE OF THE YEAR", "white", "b", "GATORADE", 110)
    S(a("as a sophomore"), "c_gatorade", 43.9); say(a("sophomore"), 1.4, "AS A SOPHOMORE", "orange", "t")
    S(a("you know the only"), "c_gatorade", 195.7)
    S(a("marion jones"), "c_gatorade", 203.7, punch=0.2); say(a("marion jones"), 2.0, "MARION JONES", "gold", "c", None, 170)
    S(a("there is calling"), "c_cnn", 3.0); say(a("fastest girl alive"), 2.2, "“THE FASTEST GIRL ALIVE”", "white", "b", "FASTEST")
    S(a("usc wanted"), "c_tws", 41.4); stack(a("usc wanted"), 3.6, ["USC", "FLORIDA", "EVERY BIG PROGRAM"], "cyan")
    # 3 the deal ------------------------------------------------------------------------
    S(PART[3] - 0.15, "c_asics_ad", 26.1, flash=1); chapter(PART[3], "02", "THE DEAL")
    say(a("december") + 1.0, 2.4, "DECEMBER 17, 2015", "white", "t")
    S(a("candace hill signs"), "art_si_0", 0.5)
    S(a("she was 16"), "art_cr_h0", 1.0); stat(a("16 years"), 2.4, "16", "YOUNGEST US TRACK PRO EVER", "orange")
    S(a("the youngest") + 0.6, "c_asics_ad", 37.7)
    S(a("ain t never say"), "c_asics_ad", 30.0)
    S(a("but miles"), "art_ms_1", 0.0); stack(a("six figures"), 3.6, ["6 FIGURES A YEAR", "10 YEARS", "NO REDUCTIONS"], "gold")
    S(a("her agency never"), "art_ms_1", 7.0); say(a("her agency never"), 1.8, "NEVER CONFIRMED", "white", "b", "NEVER")
    S(a("now here go"), "c_trials24", 98.7)
    S(a("most track contracts"), "c_trials24", 106.5); say(a("reduction clause") - 0.2, 1.5, "REDUCTION CLAUSE", "red", "c", "REDUCTION")
    S(a("you don t run fast"), "c_semi24", 29.6, amb=1); stack(a("you don t run fast"), 3.6, ["DON'T RUN FAST", "DON'T RANK", "DON'T MAKE THE TEAM"], "red")
    S(a("they cut your pay"), "c_stayyourlane", 389.9, bw=1); stamp(a("they cut your pay") + 0.3, 1.6, "PAY CUT")
    S(a("reportedly"), "art_ms_1", 9.0); say(a("none of that"), 1.6, "NOT CANDACE", "gold", "c")
    S(a("and it ran"), "art_wwd_h0", 1.0); stat(a("2025"), 2.4, "2025", "THE DEAL RUNS THROUGH", "gold")
    S(a("till she was"), "c_asics_ad", 41.6); say(a("26 years"), 1.6, "UNTIL AGE 26", "white", "t")
    S(a("plus they said"), "art_si_1", 0.0); say(a("college") - 0.2, 1.8, "+ COLLEGE PAID FOR", "cyan", "b", "COLLEGE")
    S(a("so at 16"), "c_tws", 206.9)
    S(a("before she even"), "c_gatorade", 59.9)
    S(a("she was set up"), "c_asics_ad", 51.3, punch=1.0); stat(a("at least 10") + 0.2, 2.2, "10 YEARS", "SET UP AT 16", "gold")
    # 4 the fall-off --------------------------------------------------------------------
    S(PART[4] - 0.15, "c_letsrun16", 8.0, flash=1); chapter(PART[4], "03", "THE FALL-OFF")
    say(a("2016"), 1.6, "2016", "white", "t", None, 150)
    S(a("the olympic year"), "c_insideath", 135.0)
    S(a("candace is 17"), "c_letsrun16", 20.0); say(a("17"), 1.2, "AGE 17", "orange", "t")
    S(a("she missed about"), "c_stayyourlane", 389.9, bw=1); stat(a("four months"), 2.4, "4 MONTHS", "OF TRAINING · MISSED", "red")
    S(a("she still makes"), "c_letsrun16", 40.0)
    S(a("13th"), "c_letsrun16", 60.0, bw=1); stack(a("13th"), 3.0, ["13TH · 100M", "14TH · 200M"], "red")
    S(a("then goes to the world"), "c_u20final", 24.3, amb=1)
    S(a("win gold"), "c_u20final", 86.0, punch=0.3); stat(a("1107"), 2.4, "11.07", "WORLD U20 GOLD · 2016", "gold")
    S(a("so the talent"), "c_u20final", 79.5)
    S(a("but then"), "c_ms_junior", 31.7, bw=1)
    S(a("it just stops"), "c_wa60", 13.2, bw=1); stamp(a("stops"), 1.4, "STOPPED")
    S(a("2017"), "c_ms_junior", 8.7, bw=1); say(a("2017"), 1.3, "2017", "white", "c", None, 170)
    S(a("2018"), "c_wa60", 22.9, bw=1); say(a("2018"), 1.3, "2018", "white", "c", None, 170)
    S(a("2019"), "c_stayyourlane", 408.1, bw=1); say(a("2019"), 1.3, "2019", "white", "c", None, 170)
    S(a("no personal best"), "c_stayyourlane", 335.5, bw=1); stamp(a("no personal best") + 0.2, 1.4, "NO PR")
    S(a("in 2019 at usas"), "c_stayyourlane", 244.9, bw=1); stack(a("14th in the 100"), 3.2, ["14TH · 100M", "14TH · 200M", "2019 USAs"], "red")
    S(a("and she s going through"), "c_stayyourlane", 27.2)
    S(a("by 2023"), "c_tws", 140.7); stat(a("five different"), 2.4, "5", "COACHING CHANGES BY 2023", "red")
    # 5 the part nobody saw -------------------------------------------------------------
    S(PART[5] - 0.15, "c_stayyourlane", 408.1, flash=1); chapter(PART[5], "04", "THE PART NOBODY SAW")
    S(a("in 2021"), "art_wa_0", 0.0)
    S(a("she said i have"), "art_wa_1", 0.0)
    S(a("and she said"), "art_wa_1", 6.0); say(a("second guessing"), 2.2, "“SECOND-GUESSING MYSELF”", "white", "b", "SECOND-GUESSING")
    S(a("she started seeing"), "art_wa_2", 0.0); say(a("therapist"), 1.6, "THERAPY", "cyan", "t")
    S(a("some of your emotional"), "c_stayyourlane", 400.0, bw=1)
    S(a("if your mind"), "c_tws", 24.8); say(a("your body"), 2.4, "“YOUR BODY QUICKLY FOLLOWS SUIT”", "white", "b", "BODY")
    # 6 so close ------------------------------------------------------------------------
    S(PART[6] - 0.15, "c_flo2021", 43.7, flash=1, amb=1); chapter(PART[6], "05", "SO CLOSE")
    S(a("she finally looks"), "c_flo2021", 47.2, amb=1)
    S(a("july of 2021"), "c_asics_ad", 33.8); say(a("july of 2021"), 2.0, "JULY 2021 · CALIFORNIA", "white", "t", "2021")
    S(a("she runs 10 99"), "c_asics_ad", 37.7, punch=0.6); stat(a("10 99"), 2.4, "10.99", "UNDER 11 · FIRST TIME SINCE 2015", "cyan")
    S(a("under 11"), "c_tws", 57.9); say(a("first time in six years"), 2.0, "FIRST TIME IN 6 YEARS", "gold", "b", "6 YEARS")
    S(a("but the win"), "c_asics_ad", 8.7, bw=1); stat(a("2 5"), 2.6, "+2.5", "WIND · LEGAL LIMIT +2.0", "red")
    S(a("the legal limit"), "c_asics_ad", 12.6, bw=1)
    S(a("when dated"), "c_asics_ad", 16.4, bw=1); stamp(a("when dated"), 1.6, "WIND-AIDED")
    S(a("it don t count"), "c_asics_ad", 22.2, bw=1); say(a("it don t count"), 1.4, "DOESN'T COUNT", "red", "c")
    S(a("that same summer"), "c_trials21", 3.3, amb=1); say(a("olympic trials"), 2.0, "2021 OLYMPIC TRIALS", "white", "t", "2021")
    S(a("make the finals"), "c_trials21", 10.0, amb=1)
    t9 = a("make the finals", end=True) + 0.25   # NBC board: 9 finalists, Hill 9th in 11.23 (the user's "8." was cut from the VO)
    S(t9, "c_trials21", 190.0); say(t9 + 0.1, 2.4, "9TH OF 9 · 11.23", "red", "t", "9TH")
    S(a("then she moved") + 1.2, "c_stayyourlane", 27.2); name(a("dennis"), 2.6, "DENNIS SHAVER", "COACH · BATON ROUGE", "orange")
    S(a("with pros like"), "art_rbr_h0", 0.0)
    S(a("and she was back"), "art_rbr_h1", 2.0); say(a("pre med"), 1.6, "PRE-MED", "cyan", "c")
    S(a("2024"), "c_150atl", 2.0, amb=1)
    S(a("olympic trials"), "c_trials24", 98.7, amb=1); say(a("olympic trials"), 1.8, "2024 OLYMPIC TRIALS", "white", "t", "2024")
    S(a("she makes the 100"), "c_semi24", 51.0, punch=0.6); say(a("final again"), 1.6, "FINAL AGAIN", "orange", "b")
    S(a("7th") - 0.1, "c_trials24", 146.0, amb=1); stat(a("7th"), 2.4, "7TH", "2024 TRIALS FINAL · 11.00", "orange")
    S(a("11 flat"), "c_trials24", 153.9, bw=1)
    S(a("that s how close") - 1.4, "c_semi24", 62.8, punch=1.4); stat(a("that s how close") - 1.4, 2.8, "0.01", "FROM UNDER 11 AGAIN", "red")
    # 7 the receipts --------------------------------------------------------------------
    S(PART[7] - 0.15, "c_cnn", 26.9, flash=1, bw=1); chapter(PART[7], "06", "THE RECEIPTS")
    S(a("legal sub"), "c_trials21", 16.7, bw=1); stat(a("zero"), 2.4, "0", "LEGAL SUB-11s SINCE SIGNING", "red")
    S(a("olympic teams"), "c_trials24", 169.7, bw=1); stat(a("zero"), 2.4, "0", "OLYMPIC TEAMS", "red")
    S(a("world championship"), "c_trials21", 76.7, bw=1); stat(a("zero"), 2.4, "0", "WORLD CHAMPIONSHIP TEAMS", "red")
    S(a("personal best is"), "art_rbr_h0", 3.0); stat(a("zero"), 2.4, "0", "100/200 PRs SINCE AGE 16", "red")
    S(a("her best 100"), "c_1098_hs", 36.0, slow=0.5, tag="FLASHBACK · JUNE 20, 2015"); stat(a("10 98"), 2.4, "10.98", "STILL HER BEST · AGE 16", "orange")
    S(a("her best 200"), "c_cali200", 183.6, tag="FLASHBACK · CALI 2015"); stat(a("2243"), 2.2, "22.43", "STILL HER BEST · AGE 16", "orange")
    S(a("and that deal"), "art_rbr_h1", 0.0); say(a("three years left"), 2.4, "3 YEARS LEFT · 2023", "gold", "b", "3 YEARS")
    # 8 did she finesse asics? ----------------------------------------------------------
    S(PART[8] - 0.15, "c_asics_ad", 55.1, flash=1); chapter(PART[8], "07", "DID SHE FINESSE ASICS?")
    S(a("if look at it"), "art_ms_1", 4.0)
    S(a("candace got the bag"), "c_asics_ad", 26.1); say(a("got the bag"), 0.95, "GOT THE BAG", "gold", "c", "BAG", 170)
    S(a("10 years reportedly"), "art_wwd_h0", 4.0); stack(a("10 years reportedly"), 3.0, ["10 YEARS", "NO REDUCTIONS (REPORTED)"], "gold")
    S(a("and the time"), "c_letsrun16", 60.0, bw=1); say(a("never came"), 1.8, "NEVER CAME BACK", "red", "b", "NEVER")
    S(a("that s what"), "c_asics_ad", 49.3); stamp(a("finesse"), 2.0, "FINESSE", "gold")
    S(a("but ain t nobody"), "c_cnn", 26.9)
    S(a("they saw a 16"), "c_1098_hs", 38.0, amb=1, slow=0.6)
    S(a("made a bet"), "art_si_0", 4.0)
    S(a("candace ain t quit"), "c_150atl", 34.5); stat(a("two olympic"), 2.4, "2", "OLYMPIC TRIALS FINALS", "cyan")
    S(a("she went back"), "c_tws", 206.9)
    S(a("she fought through"), "art_wa_1", 4.0)
    S(a("so which one"), "c_gatorade", 211.7); O(a("the candidates"), 6.0, ("endq", "DID SHE FINESSE ASICS?", "OR DID ASICS LOSE THE BET?"))
    S(a("and if you"), "c_cnn", 44.9)
    say(a("would have signed"), 2.6, "WOULD YOU HAVE SIGNED?", "orange", "c", "SIGNED?")
    S(a("y all let me know") - 0.3, "c_cali100", 245.6)

# ------------------------------------------------------------------ final timeline
def timeline():
    build_edl()
    vo_shots = sorted(SHOTS, key=lambda s: s["t"])
    for s in SOUNDBITES:   # after each soundbite the previous shot continues where it left off
        if any(abs(v["t"] - s["t"]) < 0.3 or (s["t"] < v["t"] < s["t"] + 0.6) for v in vo_shots): continue
        prev = max((v for v in vo_shots if v["t"] < s["t"]), key=lambda v: v["t"])
        cont = dict(prev); cont["t"] = s["t"] + 0.001; cont.pop("flash", None); cont.pop("punch", None)
        cont["ss"] = prev["ss"] + (s["t"] - prev["t"]) * prev.get("slow", 1)
        vo_shots.append(cont)
    vo_shots.sort(key=lambda s: s["t"])
    seq = [dict(T=0.0, src=PRE_SB[0], ss=PRE_SB[1] - PAD, tag=PRE_SB[3], sb=1)]
    for v in vo_shots:
        d = dict(v); d["T"] = round(FT(v["t"]), 3); seq.append(d)
    for s in SOUNDBITES:
        seq.append(dict(T=round(SB_START(s), 3), src=s["src"], ss=round(s["ss"] - PAD, 3), tag=s["tag"], sb=1))
    seq.sort(key=lambda x: x["T"])
    end = FT(VO_END) + 4.0; out = []
    for i, x in enumerate(seq):
        t1 = seq[i + 1]["T"] if i + 1 < len(seq) else end
        if t1 - x["T"] < 0.3: continue
        out.append((x, t1))
    ov = []
    for a0, a1, spec in OVER:
        f0, f1 = FT(a0), FT(a1)
        for s in SOUNDBITES:
            if a0 < s["t"] < a1: f1 = min(f1, SB_START(s))
        ov.append((round(f0, 3), round(min(f1, end), 3), spec))
    return out, ov, end

GRADE = "eq=contrast=1.07:saturation=1.1:gamma=0.98,colorbalance=rs=-0.02:bs=0.03:rh=0.03,vignette=PI/5"
def ov_mov(spec, dur):
    p = f"{R}/ov/{hashlib.md5(json.dumps([spec, round(dur, 3)]).encode()).hexdigest()[:12]}.mov"
    if not os.path.exists(p): K.render(spec, dur, p)
    return p

def tag_png(tag):
    p = f"{R}/tags/{hashlib.md5(tag.encode()).hexdigest()[:10]}.png"
    if not os.path.exists(p): K.source(1.0, 99, tag).save(p + ".tmp.png"); os.replace(p + ".tmp.png", p)
    return p

def render_shot(i, sh, T1, OV):
    out = f"{R}/shots/{i:04d}.mp4"; T0 = sh["T"]
    dur = (round(T1 * FPS) - round(T0 * FPS)) / FPS
    mine = [o for o in OV if o[0] < T1 - 0.05 and o[1] > T0 + 0.05]
    key = json.dumps([sh, dur, GRADE, mine, 3], sort_keys=True, default=str); stamp_ = f"{out}.key"
    if os.path.exists(out) and os.path.exists(stamp_) and open(stamp_).read() == key: return out
    src = sh["src"]; slow = sh.get("slow", 1.0); sb = sh.get("sb")
    ins = ["-ss", f"{max(0, sh['ss']):.3f}", "-t", f"{dur * slow + 0.2:.3f}", "-i", f"{REAL}/{src}.mp4"]
    if sb:
        base = (f"[0:v]setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,"
                f"eq=contrast=1.04:saturation=1.05,tpad=stop_mode=clone:stop_duration=30")
    else:
        p = sh.get("punch"); z = f"(1+0.035*t/{dur:.3f}"
        if p is not None: z += f"+0.13*min(1,max(0,(t-{p:.3f})/0.12))"
        z += ")"
        base = (f"[0:v]setpts={1 / slow:.4f}*(PTS-STARTPTS),scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                f"scale='trunc(1920*{z}/2)*2':-2:eval=frame,crop=1920:1080,setsar=1,{GRADE},tpad=stop_mode=clone:stop_duration=60")
        if sh.get("bw"): base += ",hue=s=0,eq=contrast=1.15:brightness=-0.03"
        if sh.get("blur"): base += ",gblur=sigma=18,eq=brightness=-0.12"
        if sh.get("flash"): base += ",eq=brightness='if(lt(t,0.1),0.6*(1-t/0.1),0)':eval=frame"
    vf = [base + ",fps=24,format=yuva420p[b0]"]; k = 0
    if not sb or True:
        k = 1; ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", tag_png(sh.get("tag", ""))]
        vf.append(f"[1:v]format=rgba[o1];[b0][o1]overlay=0:0:enable='lt(t,{min(dur, 3.5):.3f})'[b1]")
    for (o0, o1, spec) in mine:
        a_ = max(0, o0 - T0); b_ = min(dur, o1 - T0)
        if b_ - a_ < 0.2: continue
        mov = ov_mov(spec, o1 - o0); k += 1
        ins += ["-ss", f"{max(0, T0 - o0):.3f}", "-i", mov]
        vf.append(f"[{k}:v]setpts=PTS-STARTPTS+{a_:.3f}/TB,format=rgba[o{k}];[b{k - 1}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a_:.3f},{b_:.3f})'[b{k}]")
    vf.append(f"[b{k}]format=yuv420p[v]")
    ins += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]; amap = f"{k + 1}:a"
    vol = 1.0 if sb else (0.16 if sh.get("amb") else 0.0)
    if vol > 0:
        hp = ",loudnorm=I=-17:TP=-2:LRA=11" if sb else ",highpass=f=120"
        at = "" if slow == 1 else f",atempo={max(0.5, slow):.3f}"
        vf.append(f"[0:a]aresample=48000{at},volume={vol}{hp},apad=whole_dur={dur:.3f}[a]"); amap = "[a]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(vf), "-map", "[v]", "-map", amap,
           "-t", f"{dur:.3f}", "-r", "24", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-ar", "48000", "-ac", "2", out]
    run(cmd); open(stamp_, "w").write(key); return out

_TL = None
def TL():
    global _TL
    if _TL is None: _TL = timeline()
    return _TL

def stage_overlays():
    from concurrent.futures import ProcessPoolExecutor
    shots, ov, end = TL(); todo = {}
    for o0, o1, spec in ov:
        p = f"{R}/ov/{hashlib.md5(json.dumps([spec, round(o1 - o0, 3)]).encode()).hexdigest()[:12]}.mov"
        if not os.path.exists(p): todo[p] = (spec, o1 - o0)
    with ProcessPoolExecutor(8) as ex: list(ex.map(_rend, [(s, d, p) for p, (s, d) in todo.items()]))
    for sh, _ in shots: tag_png(sh.get("tag", ""))
    print("overlays", len(todo), "new of", len(ov))
def _rend(a): K.render(a[0], a[1], a[2])

def stage_shots():
    from concurrent.futures import ThreadPoolExecutor
    stage_overlays()
    shots, ov, end = TL(); todo = list(enumerate(shots))
    only = os.environ.get("ONLY")
    if only: a, b = map(int, only.split("-")); todo = [x for x in todo if a <= x[0] <= b]
    with ThreadPoolExecutor(6) as ex: list(ex.map(lambda a: render_shot(a[0], a[1][0], a[1][1], ov), todo))
    print("shots", len(todo), "of", len(shots), "end", round(end, 1))

def stage_concat():
    shots, ov, end = TL(); lst = f"{R}/concat.txt"
    open(lst, "w").write("".join(f"file '{R}/shots/{i:04d}.mp4'\n" for i in range(len(shots))))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/picture.mp4"])
    print("concat", run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/picture.mp4"]).stdout.strip(), "END", round(end, 2))

# ------------------------------------------------------------------ audio
def vo_track(end):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    SR = 48000; parts = [np.zeros((int(PRE * SR), 2), np.float32)]; last = 0
    for s in SOUNDBITES:
        cut = int(s["t"] * SR); parts.append(x[last:cut]); parts.append(np.zeros((int((s["dur"] + 2 * PAD) * SR), 2), np.float32)); last = cut
    parts.append(x[last:]); y = np.concatenate(parts)
    y = np.concatenate([y, np.zeros((max(0, int(end * SR) - len(y)), 2), np.float32)])[:int(end * SR)]
    p = f"{R}/vo_full.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", p], input=y.tobytes(), check=True)
    return p

def make_sfx(kind, seed):
    import sounds
    p = f"{R}/sfx/{kind}_{seed}.wav"
    if not os.path.exists(p):
        if kind == "decode": sounds.ui_sound("decode", p, seed)
        else: sounds.trans_sound(kind, p, seed)
    return p

def bed(path, t0, t1, vol, end, fin=1.5, fout=2.5, offset=0.0):
    out = f"{R}/bed_{os.path.basename(path)}_{t0:.1f}.wav"; L = t1 - t0; dl = int(t0 * 1000)
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", str(offset), "-i", path, "-t", f"{L:.2f}", "-af",
         f"volume={vol},afade=t=in:st=0:d={fin},afade=t=out:st={max(0, L - fout):.2f}:d={fout},adelay={dl}|{dl},apad=whole_dur={end:.2f}",
         "-ar", "48000", "-ac", "2", out]); return out

def sfx_plan(shots, ov):
    """Few hits, varied, never closer than 3 s, nothing on plain cuts or soundbites."""
    cand = []
    for j, (o0, o1, spec) in enumerate(ov):
        k = spec[0]
        if k == "chapter": cand.append((o0 - 0.05, "zoom", 0.42, 3))
        elif k == "stamp": cand.append((o0 - 0.03, "glitch", 0.34, 3))
        elif k == "stat": cand.append((o0 - 0.06, ("streak", "pixel", "scan", "grid")[j % 4], 0.13, 2))
        elif k == "endq": cand.append((o0 - 0.05, "zoom", 0.3, 3))
    cand.sort(key=lambda c: (c[0], -c[3])); out, last = [], -9
    for t, kind, g, pri in cand:
        if t - last < (6.0 if pri == 2 else 3.0): continue
        out.append((t, make_sfx(kind, 40 + len(out) * 7), g)); last = t
    return out

def stage_audio():
    shots, ov, end = TL(); vo = vo_track(end)
    M1 = f"{ROOT}/projects/jon-drummond/music"; Pt = {k: FT(v) for k, v in PART.items()}
    beds = [bed(f"{M1}/M1_cold-open-background.mp3", 0, Pt[2] + 0.4, 0.5, end, 1.0, 1.5),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", Pt[2] - 0.2, Pt[4] + 0.4, 0.42, end, 0.6, 1.5),
            bed(f"{M1}/M4_coaching-ban.mp3", Pt[4] - 0.2, Pt[6] + 0.4, 0.42, end, 0.6, 1.5),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", Pt[6] - 0.2, Pt[8] + 0.4, 0.42, end, 0.6, 1.5, offset=60),
            bed(f"{M1}/M5_verdict-ending.mp3", Pt[8] - 0.2, end, 0.48, end, 0.8, 3.5)]
    S_ = sfx_plan(shots, ov)
    ins, fl = [], []; nb = len(beds); base = 2 + nb
    for j, (t, path, g) in enumerate(S_):
        ins += ["-i", path]; d = int(max(0, t) * 1000)
        fl.append(f"[{j + base}:a]volume={g},afade=t=out:st=1.2:d=0.5,adelay={d}|{d},aformat=sample_rates=48000:channel_layouts=stereo[s{j}]")
    bed_in = "".join(f"[{2 + j}:a]" for j in range(nb)); mix_in = "".join(f"[s{j}]" for j in range(len(S_)))
    fc = ";".join(fl) + (";" if fl else "") + \
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[pic];" \
        f"{bed_in}amix=inputs={nb}:normalize=0[music];[vo][pic]amix=inputs=2:normalize=0[key0];[key0]asplit=2[key][keyout];" \
        f"[music][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=450[duck];" \
        f"[keyout][duck]{mix_in}amix=inputs={2 + len(S_)}:normalize=0:duration=first,alimiter=limit=0.95[out]"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-vn", "-af", f"aresample=48000:async=1:first_pts=0,apad=whole_dur={end:.2f}",
         "-t", f"{end:.2f}", "-ac", "2", "-c:a", "pcm_s16le", f"{R}/pic_audio.wav"])
    run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", f"{R}/pic_audio.wav"] + sum((["-i", b] for b in beds), []) + ins +
        ["-filter_complex", fc, "-map", "[out]", "-t", f"{end:.2f}", "-ar", "48000", f"{R}/mix.wav"])
    print("audio", len(S_), "sfx")

def stage_mux():
    shots, ov, end = TL()
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/picture.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", f"{end:.2f}", "-movflags", "+faststart", OUT])
    print("wrote", OUT)

def stage_check():
    shots, ov, end = TL()
    print("shots", len(shots), "overlays", len(ov), "end", round(end, 1), "=", f"{int(end // 60)}:{end % 60:04.1f}", "soundbites", len(SOUNDBITES))
    for sh, t1 in shots: print(f"{sh['T']:7.2f}-{t1:7.2f} {'SB ' if sh.get('sb') else '   '}{sh['src']:10s} {sh.get('ss', 0):7.1f} {sh.get('tag', '')}")
    for o in ov: print(f"  OV {o[0]:7.2f}-{o[1]:7.2f} {o[2][:3]}")

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")
