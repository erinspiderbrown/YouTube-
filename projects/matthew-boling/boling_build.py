"""The Downfall of Matthew Boling, v2: documentary edit on the user's own voiceover (no tempo change).

v2 (user notes on v1, 10 Nov 2026): "at least 8 minutes", "repetitive sound effects and transition noises,
two back to back", "not clipping when I'm making mistakes", "the neon stat graphic is not all that", "step up the editing".
- Voiceover v2: flubs/restarts cut (clean_voiceover.py MIST), words re-timed (vo_user_v2_words.json).
- Real soundbites play with their own sound (race calls, his dad, his coaches, Boling himself, CBS): the
  voiceover pauses for each one. That is where the extra length comes from. No padding or slowed voice.
- Graphics: tools/kinetic.py (animated slam-in numbers, kinetic words, lower thirds, stamps, chapter slates).
- Editing: punch-in on every number/key word, black-and-white on the low points, slow-mo finishes, chapter
  slates with a flash cut, small source credit instead of the HUD tag.
- Sound: one bed per chapter ducked under the voice; few SFX, varied, never closer than 3 s.

Every time in the EDL is raw voiceover seconds; FT() maps it onto the final timeline.
Run:  python3 projects/matthew-boling/boling_build.py [stage ...]   stages: shots concat audio mux (default all); check
"""
import os, sys, json, math, subprocess, hashlib, difflib
import numpy as np
from PIL import Image, ImageFilter

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/matthew-boling"
sys.path.insert(0, f"{ROOT}/tools")
import kinetic as K
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
BS = f"{SCR}/boling"; REAL = f"{BS}/real"; R = f"{BS}/render2"
for d in ("ov", "shots", "sfx", "tags"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/boling_voiceover_user_v2.wav"
OUT = f"{SCR}/output/Downfall_of_Matthew_Boling_v2.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/vo_user_v2_words.json"))[0]["words"]
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

# ------------------------------------------------------------------ soundbites (inserted; the voiceover pauses)
PAD = 0.3
PRE_SB = ("bdocshort", 184.6, 193.6, "FATHER · MARK BOLING")   # cold open: dad watching the 9.98 come up
SB_LIST = [  # (before phrase, src, a, b, credit)
    (("now the win", 1), "b998_cbs", 1.9, 19.35, "CBS MORNING NEWS · APRIL 2019"),
    (("he got the stick", 2), "bdocshort", 131.0, 143.95, "HEAD COACH · CHAD COLLIER"),
    (("he won gatorade", 2), "b4474", 168.6, 187.6, "FLOTRACK · TEXAS STATE 4X400"),
    (("so he committed", 2), "bdocshort", 74.3, 78.85, "FATHER · MARK BOLING"),
    (("his first year", 3), "bdocshort", 359.8, 377.7, "MATTHEW BOLING"),
    (("and for a minute", 3), "bncaa21", 30.0, 49.6, "ESPN · NCAA INDOORS 2021"),
    (("that was the first time", 3), "bdocshort", 334.2, 348.25, "HEAD COACH · CHAD COLLIER"),
    (("so he ain t slow", 4), "bsec22", 20.9, 34.45, "SEC NETWORK · 2022"),
    (("but outdoors", 5), "bncaa23", 16.2, 26.8, "ESPN · NCAA INDOORS 2023"),
    (("and man", 5), "bbudapest", 455.3, 470.3, "WORLD CHAMPIONSHIPS · BUDAPEST 2023"),
    (("he ran in heats", 5), "bbudapest", 530.9, 545.4, "WORLD CHAMPIONSHIPS · BUDAPEST 2023"),
    (("this the one everybody", 6), "bprobts", 80.7, 87.4, "MATTHEW BOLING · JANUARY 2024"),
    (("2025", "PART7"), "bdocshort", 410.7, 422.85, "FATHER · MARK BOLING"),
    (("he went viral", 8), "bdocshort", 207.7, 217.3, "UNIVERSITY OF GEORGIA"),
    (("so was this a downfall", 8), "bdocshort", 396.0, 409.2, "MATTHEW BOLING"),
]
SOUNDBITES = []
def _sb():
    keep = _CUR[0]; _CUR[0] = 0.0
    for ph, src, a, b, cr in SB_LIST:
        t = PART[7] - 0.25 if ph[1] == "PART7" else A(ph[0], PART[ph[1]] - 0.5, win=1e9) - 0.25
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
def S(t, src, ss=0.0, **o): SHOTS.append(dict(t=round(t, 3), src=src, ss=ss, **o))
def O(t, dur, spec): OVER.append((round(t, 3), round(t + dur, 3), spec))
def stat(t, dur, big, label, col="orange"): O(t, dur, ("stat", big, label, col))
def say(t, dur, text, col="white", pos="b", hi=None, size=130): O(t, dur, ("words", text, col, pos, hi, size))
def stack(t, dur, lines, col="orange"): O(t, dur, ("stack", lines, col))
def name(t, dur, n, sub, col="orange"): O(t, dur, ("name", n, sub, col))
def stamp(t, dur, text, col="red"): O(t, dur, ("stamp", text, col))
def chapter(t, num, title): O(t, 2.6, ("chapter", num, title, "orange"))

def build_edl():
    _sb(); a = A; _CUR[0] = 0.0
    T19, TST, TPA, TGA = "REGION MEET · APRIL 27, 2019", "TEXAS 6A STATE · MAY 2019", "PAN AM U20 · SAN JOSÉ 2019", "UNIVERSITY OF GEORGIA"
    # 1 cold open ---------------------------------------------------------------------
    S(a("april"), "b998_flo", 0.0, tag="HOUSTON · " + T19, amb=1); say(a("april"), 2.6, "APRIL 27, 2019", "white", "t")
    S(a("houston"), "b998_dctf", 1.0, tag=T19, amb=1)
    S(a("straight jesuit"), "b998_flo", 2.3, tag=T19, amb=1); say(a("straight jesuit"), 2.0, "STRAKE JESUIT · SENIOR", "orange", "t", "STRAKE JESUIT")
    S(a("and runs") + 0.25, "b998_flo", 4.8, tag=T19, amb=1, slow=0.5)
    S(a("998 in high school"), "b998_dctf", 23.3, tag=T19, punch=0.4); stat(a("998 in high school"), 2.6, "9.98", "100M · IN HIGH SCHOOL", "orange")
    S(a("now the win"), "b998_flo", 15.0, tag=T19, amb=1); stat(a("way over"), 3.4, "+4.2", "WIND · LEGAL LIMIT +2.0", "red")
    S(a("it ain t matter"), "b998_flo", 21.0, tag=T19, amb=1); say(a("ain t matter"), 1.5, "DIDN'T MATTER", "orange", "c")
    S(a("by the next morning"), "b998_cbs", 22.0, tag="CBS MORNING NEWS · 2019")
    S(a("espn"), "b998_cbs", 26.0, tag="CBS MORNING NEWS · 2019"); stack(a("espn"), 3.6, ["ESPN", "CBS · FOX", "SPORTS ILLUSTRATED"], "cyan")
    S(a("everybody calling"), "b998_cbs", 9.0, tag="CBS MORNING NEWS · 2019", punch=1.0); say(a("white lightning"), 1.8, "“WHITE LIGHTNING”", "white", "c")
    S(a("people saying"), "b998_cbs", 13.0, tag="CBS MORNING NEWS · 2019"); say(a("usain bolt"), 2.0, "THE NEXT USAIN BOLT?", "orange", "b", "BOLT?")
    S(a("his name was"), "b998_cbs", 18.4, tag="TEAM USA · 2019", punch=0.9); name(a("matthew"), 2.0, "MATTHEW BOLING", "STRAKE JESUIT · HOUSTON, TX")
    S(a("and seven years later"), "bdocshort", 360.5, tag=TGA); say(a("seven years later"), 2.4, "7 YEARS LATER", "white", "t")
    S(a("what happened"), "bdocshort", 404.5, tag=TGA, bw=1); say(a("what happened"), 2.4, "WHAT HAPPENED?", "orange", "c", "HAPPENED?", 170)
    # 2 the hype was real ---------------------------------------------------------------
    S(PART[2] - 0.15, "bdocshort", 115.5, tag="STRAKE JESUIT", flash=1); chapter(PART[2], "01", "THE HYPE WAS REAL")
    S(a("matt was not"), "bdocshort", 173.5, tag="STRAKE JESUIT"); say(a("not a"), 1.8, "NOT A FLUKE", "cyan", "c", "FLUKE")
    S(a("that same season"), "b1013", 40.0, tag=TST, amb=1)
    S(a("he ran 10") - 0.3, "b1013", 132.5, tag=TST, amb=1, punch=1.2); stat(a("he ran 10") + 0.4, 3.0, "10.13", "LEGAL WIND", "cyan")
    say(a("that was the us"), 2.6, "US HIGH SCHOOL RECORD", "gold", "b", "RECORD")
    S(a("he won a long jump"), "bdocshort", 14.4, tag="HOUSTON"); stat(a("jumping 26"), 2.4, "26 FT", "LONG JUMP · STATE CHAMP", "cyan")
    S(a("and then he anchored"), "b4474", 140.0, tag=TST + " · 4X400", amb=1); say(a("anchored"), 1.8, "4X400 ANCHOR", "orange", "t", "ANCHOR")
    S(a("he got the stick"), "b4474", 156.0, tag=TST + " · 4X400", amb=1, punch=1.0); stat(a("20 meters"), 2.0, "20+ M", "BEHIND AT THE HANDOFF", "red")
    S(a("and ran a 44") - 0.2, "b4474", 160.0, tag=TST + " · 4X400", amb=1); stat(a("and ran a 44") + 0.4, 3.0, "44.74", "ANCHOR SPLIT", "gold")
    S(a("he won gatorade"), "bdocshort", 346.5, tag="STRAKE JESUIT"); say(a("he won gatorade"), 2.8, "GATORADE NATIONAL ATHLETE OF THE YEAR", "white", "b", "GATORADE", 110)
    S(a("pan am"), "bpanam", 2.0, tag=TPA); stat(a("four gold"), 2.2, "4 GOLD", "PAN AM U20 CHAMPIONSHIPS", "gold")
    S(a("100 200"), "bpanam", 60.0, tag=TPA); stack(a("100 200"), 4.0, ["100M · 200M", "4X100 · 4X400", "U20 WORLD RECORDS"], "gold")
    S(a("oh and a nickname"), "bpanam", 100.0, tag=TPA); say(a("oh and a nickname"), 2.2, "“WHITE LIGHTNING”", "white", "t")
    S(a("he didn t want"), "bpanam", 118.0, tag=TPA); say(a("he didn t want"), 2.8, "HE DIDN'T LIKE IT", "orange", "b", "DIDN'T")
    S(a("he just wanted to run"), "bdocshort", 158.0, tag="HOUSTON")
    S(a("committed to georgia"), "bdocshort", 230.0, tag=TGA); say(a("committed to georgia"), 2.4, "COMMITTED: GEORGIA", "red", "t", "GEORGIA")
    S(a("something crazy") - 1.2, "bdocshort", 389.0, tag=TGA)
    # 3 georgia -------------------------------------------------------------------------
    S(PART[3] - 0.15, "bdocshort", 202.0, tag=TGA, flash=1); chapter(PART[3], "02", "GEORGIA")
    S(a("covid"), "bdocshort", 288.5, tag=TGA, bw=1); stamp(a("covid") + 0.3, 1.8, "SEASON CANCELLED")
    S(a("2021"), "bncaa21", 2.0, tag="NCAA INDOOR · FAYETTEVILLE 2021", amb=1)
    S(a("20 19") - 0.2, "bncaa21", 84.0, tag="NCAA INDOOR · FAYETTEVILLE 2021", punch=0.3); stat(a("20 19"), 3.0, "20.19", "NCAA INDOOR CHAMPION · 200M", "gold")
    S(a("and for a minute"), "bncaa21", 42.0, tag="NCAA INDOOR · FAYETTEVILLE 2021", slow=0.6); say(a("right on schedule"), 1.8, "RIGHT ON SCHEDULE", "white", "b", "SCHEDULE")
    S(a("then the olympic trials"), "btrials21", 28.0, tag="OLYMPIC TRIALS · EUGENE 2021", amb=1)
    S(a("he goes out"), "btrials21", 98.0, tag="OLYMPIC TRIALS · 100M SEMIS", amb=1)
    S(a("14th") - 0.1, "btrials21", 110.0, tag="OLYMPIC TRIALS · 100M SEMIS", bw=1, punch=0.2); stat(a("14th"), 2.2, "14TH", "100M SEMIS · OUT", "red")
    S(a("and then the 200"), "btrials21", 248.0, tag="OLYMPIC TRIALS · 200M SEMIS", amb=1)
    S(a("one spot"), "btrials21", 262.0, tag="OLYMPIC TRIALS · 200M SEMIS", bw=1, punch=0.2); stat(a("one spot") - 0.6, 3.0, "9TH", "1 SPOT FROM THE FINAL", "red")
    S(a("that was the first time"), "bdocshort", 362.0, tag=TGA, bw=1); say(a("this ain t high school"), 2.6, "THIS AIN'T HIGH SCHOOL NO MORE", "white", "b", "NO MORE")
    # 4 he actually got faster ----------------------------------------------------------
    S(PART[4] - 0.15, "bdocshort", 397.0, tag=TGA, flash=1); chapter(PART[4], "03", "HE GOT FASTER")
    S(a("2022") + 0.2, "bdocshort", 305.0, tag="GEORGIA · 2022", punch=1.2); stat(a("runs 9") + 0.3, 3.0, "9.98", "AGAIN · LEGAL WIND", "cyan")
    S(a("and a couple"), "b1992", 0.5, tag="GEORGIA TECH INVITATIONAL · 2022", amb=1)
    S(a("1992") - 0.2, "b1992", 25.5, tag="GEORGIA TECH INVITATIONAL · 2022", amb=1, punch=0.3); stat(a("1992"), 2.8, "19.92", "200M · APRIL 23, 2022", "gold")
    S(a("he won the sec"), "bsec22", 35.5, tag="SEC CHAMPIONSHIPS · 2022"); say(a("he won the sec"), 1.8, "SEC CHAMPION", "gold", "t", "CHAMPION")
    say(a("took second"), 1.8, "2ND AT NCAAs", "white", "t")
    S(a("so he ain t slow"), "b1992", 42.5, tag="WORLD RANKINGS · 2022")
    stack(a("sub 10"), 3.0, ["SUB-10", "SUB-20"], "cyan")
    S(a("at usa"), "bdocshort", 375.0, tag=TGA, bw=1); stat(a("at usa") + 0.4, 2.4, "6TH", "USATF 200M · 2022", "red")
    S(a("america"), "btrials21", 57.0, tag="HAYWARD FIELD · EUGENE"); say(a("top 10"), 3.0, "TOP 10 IN THE WORLD", "white", "b", "WORLD")
    S(a("still be staying"), "btrials21", 230.0, tag="HAYWARD FIELD · EUGENE", bw=1); say(a("still be staying"), 1.8, "...STILL HOME", "red", "c")
    say(a("that deep"), 1.4, "THAT DEEP", "orange", "t")
    # 5 the switch ----------------------------------------------------------------------
    S(PART[5] - 0.15, "bncaa23", 52.0, tag="NCAA INDOOR · ALBUQUERQUE 2023", flash=1, amb=1); chapter(PART[5], "04", "THE SWITCH")
    S(a("title in the 200") , "bncaa23", 72.0, tag="NCAA INDOOR · ALBUQUERQUE 2023", punch=0.5); stat(a("title in the 200") + 0.3, 2.6, "20.12", "NCAA INDOOR CHAMPION · AGAIN", "gold")
    S(a("but outdoors"), "bdocshort", 404.0, tag=TGA, bw=1); stamp(a("make the finals"), 1.6, "NO FINAL")
    S(a("so he tried"), "bdocshort", 389.0, tag=TGA); say(a("the 400"), 1.6, "THE 400", "orange", "c", "400", 180)
    S(a("at usa s"), "bdocshort", 317.0, tag=TGA); stat(a("sixth again"), 2.4, "6TH", "USATF 400M · 45.17", "orange")
    S(a("relay pool"), "bbudapest", 86.0, tag="WORLD CHAMPIONSHIPS · BUDAPEST 2023", amb=1); say(a("budapest"), 1.8, "BUDAPEST WORLDS", "cyan", "t", "BUDAPEST")
    S(a("and man"), "bbudapest", 470.3, tag="BUDAPEST 2023 · MIXED 4X400 FINAL", amb=1); stat(a("third leg"), 2.2, "3RD LEG", "MIXED 4X400 · USA", "cyan")
    S(a("gold medal") , "bbudapest", 655.0, tag="BUDAPEST 2023 · MIXED 4X400 FINAL", punch=0.4); stat(a("gold medal"), 2.6, "3:08.80", "GOLD · WORLD RECORD", "gold")
    S(a("he ran in heats"), "bbudapest", 600.0, tag="BUDAPEST 2023", amb=1); say(a("they won that too"), 1.6, "GOLD AGAIN", "gold", "b")
    S(a("so on paper"), "bbudapest", 826.0, tag="BUDAPEST 2023 · RESULTS", punch=1.2); say(a("two time"), 2.6, "2-TIME WORLD CHAMPION", "gold", "c", "WORLD CHAMPION", 150)
    S(a("that september"), "bprobts", 117.0, tag="PRO · 2024"); say(a("skips his last year"), 2.4, "TURNS PRO · SEPT 2023", "orange", "t", "PRO")
    S(a("moves to south"), "bprobts", 150.0, tag="PRO · SOUTH CAROLINA"); name(a("coach"), 2.6, "ALLEYNE FRANCIQUE", "NEW COACH · SOUTH CAROLINA")
    S(a("saying he"), "bprobts", 255.0, tag="PRO · SOUTH CAROLINA"); say(a("world stage"), 1.6, "THE WORLD STAGE", "cyan", "b", "WORLD")
    # 6 paris ---------------------------------------------------------------------------
    S(PART[6] - 0.15, "bprobts", 186.0, tag="2024 SEASON", flash=1); chapter(PART[6], "05", "PARIS")
    S(a("this the one everybody"), "b998_flo", 3.0, tag="FLASHBACK · 2019", bw=1)
    S(a("he runs"), "bprobts", 208.0, tag="2024 SEASON", amb=1, punch=0.6); stat(a("44"), 3.0, "44.84", "400M PR · JULY 2024", "gold")
    S(a("world indoor"), "bprobts", 296.0, tag="2024 SEASON", amb=1); stack(a("world indoor"), 3.4, ["WORLD INDOORS · SILVER", "WORLD RELAYS · GOLD"], "gold")
    S(a("then the trials"), "btrials21", 15.0, tag="HAYWARD FIELD · EUGENE", blur=1); say(a("then the trials"), 2.0, "2024 OLYMPIC TRIALS", "orange", "c", "TRIALS", 150)
    S(a("in the 400"), "btrials21", 40.0, tag="HAYWARD FIELD · EUGENE")
    S(a("finishes eighth") - 0.1, "btrials21", 64.0, tag="HAYWARD FIELD · EUGENE", bw=1, punch=0.2); stat(a("finishes eighth"), 2.8, "8TH", "400M FINAL · LAST", "red")
    S(a("in the 200"), "btrials21", 280.0, tag="HAYWARD FIELD · EUGENE", bw=1); stat(a("9th"), 2.2, "9TH", "200M · NO FINAL", "red")
    S(a("and they don t pick"), "bdocshort", 368.0, tag=TGA, bw=1); stamp(a("pairs") - 0.1, 2.4, "NO PARIS")
    # 7 now -----------------------------------------------------------------------------
    S(PART[7] - 0.15, "bgst", 120.0, tag="GRAND SLAM TRACK · PHILADELPHIA 2025", flash=1, amb=1); chapter(PART[7], "06", "NOW")
    stat(a("7th"), 2.4, "7TH", "200M · 20.87", "red")
    S(a("5th") - 0.2, "bgst", 190.0, tag="GRAND SLAM TRACK · PHILADELPHIA 2025", amb=1); stat(a("5th"), 2.0, "5TH", "400M", "orange")
    S(a("that year"), "bdocshort", 303.0, tag="2026"); say(a("that year"), 4.0, "2026", "cyan", "t", "2026", 150)
    stat(a("45"), 3.0, "45.51", "400M · JULY 10, 2026", "white")
    S(a("the kid that ran"), "b998_flo", 5.0, tag="FLASHBACK · 2019", bw=1, slow=0.5); stat(a("at 18"), 1.8, "9.98", "AT 18", "orange")
    S(a("his best 100"), "b998_dctf", 24.0, tag="FLASHBACK · 2019", punch=0.8); stat(a("still"), 2.6, "9.98", "STILL HIS BEST 100", "cyan")
    # 8 so is it really a downfall ------------------------------------------------------
    S(PART[8] - 0.15, "bdocshort", 420.0, tag=TGA, flash=1); chapter(PART[8], "07", "A DOWNFALL?")
    S(a("is a two time"), "bbudapest", 655.0, tag="BUDAPEST 2023"); say(a("is a two time"), 2.4, "2-TIME WORLD CHAMPION", "gold", "b", "WORLD CHAMPION")
    S(a("he ran sub 10"), "b1992", 25.0, tag="ATLANTA · 2022"); stack(a("he ran sub 10"), 3.0, ["SUB-10", "SUB-20"], "cyan")
    S(a("most people"), "bprobts", 318.0, tag="PRO · 2024")
    S(a("but that ain t"), "b998_cbs", 2.0, tag="CBS MORNING NEWS · 2019")
    S(a("he was promised"), "b998_cbs", 18.4, tag="TEAM USA · 2019", punch=1.4); say(a("usain bolt"), 2.0, "“THE NEXT USAIN BOLT”", "orange", "c", "BOLT”")
    S(a("he went viral"), "b998_cbs", 6.0, tag="CBS MORNING NEWS · 2019"); stat(a("wasn t even legal"), 2.4, "+4.2", "TAILWIND · NOT LEGAL", "red")
    S(a("before he ever"), "bdocshort", 230.0, tag=TGA)
    S(a("measured against"), "b998_flo", 2.6, tag="REGION MEET · 2019", bw=1); say(a("one clip"), 2.6, "1 CLIP", "orange", "c", "CLIP", 190)
    S(a("the hardest team"), "btrials21", 57.0, tag="HAYWARD FIELD · EUGENE"); say(a("the hardest team"), 2.8, "THE HARDEST TEAM TO MAKE", "white", "b", "HARDEST")
    S(a("sixth in america"), "btrials21", 232.0, tag="HAYWARD FIELD · EUGENE"); stat(a("sixth in america"), 3.2, "6TH IN THE US", "= TOP 10 IN THE WORLD", "orange")
    S(a("so was this a downfall"), "bdocshort", 404.0, tag=TGA); O(a("so was this a downfall"), 8.0, ("endq", "A DOWNFALL?", "OR TOO MUCH HYPE?"))
    S(a("let me know") - 0.3, "bdocshort", 418.5, tag=TGA)
    S(a("and if you was"), "b998_cbs", 18.6, tag="2019"); say(a("hype train"), 3.4, "WERE YOU ON THE HYPE TRAIN?", "orange", "b", "HYPE TRAIN?")

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
