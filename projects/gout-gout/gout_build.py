"""Gout Gout "Are His Times Real?" (from the Kejelcha build) (template: quincy_build.py) + PREMIUM layer (tools/premium.py): word-synced interview
subtitles, interview IDs, race clock / gap / timeline graphics, wipe headlines, cinematic transitions (stage trans).
Own score K1-K6 (ElevenLabs flow KGqVtCkMgtMtRbwXWnmK). Run: python3 kejelcha_build.py [shots concat trans audio mux]
Older header: Cinematic step-up (25 Nov 2026): tools/modern.py + tools/cinema.py
(letterbox, championship tracker, PB counter, versus split, scope), speed ramps, depth-pull photo stills, cinematic grade.
Voiceover: Erin Brown 2026 clone, A3b style (vo_lyles.mp3). Soundbites + EDL: edl_lyles.py.
Footage rules: no NCAA/ESPN broadcast, FloTrack/MileSplit, RunnerSpace, NBC, Olympic, Diamond League, World Athletics.
Run:  python3 projects/drew-hunter/hunter_build.py [stage ...]   stages: shots concat audio mux (default all); check
"""
import os, sys, json, math, subprocess, hashlib, difflib
import numpy as np
from PIL import Image, ImageFilter

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/gout-gout"
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, P)
import modern as K
import premium as PM
import cinema  # registers letterbox/tracker/counter/versus/scope in K.KINDS
import windfile  # v3 identity (28 Nov 2026): WIND FILE look, unique to this video (serif + mono, cyan/coral, streamlines, dials, drift chart)
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
CS = f"{SCR}/gout"; REAL = f"{CS}/clips"; R = f"{CS}/render"
for d in ("ov", "shots", "sfx", "tags"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/vo_gout.mp3"
OUT = f"{SCR}/output/Gout_2026.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/words.json"))[0]["words"]
_NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def _tok(w):
    t = "".join(ch for ch in w.lower() if ch.isalnum())
    return _NUMW[int(t)] if t.isdigit() and int(t) <= 20 else t
TOK = [_tok(x["w"]) for x in WORDS]
VO_END = WORDS[-1]["e"]
PART = {1: 0, 2: 26.55, 3: 70.63, 4: 105.4, 5: 133.45, 6: 153.33, 7: 180.19, 8: 200.49, 9: 247.6, 10: 315.91, 11: 332.99, 12: 358.03}   # vo_gout.mp3 (v4, 28 Nov 2026: eleven_multilingual_v2, accent from the voice sample; 11 = after the TikTok receipt, 12 = verdict)
_CUR = [0.0]
def A(phrase, after=None, end=False, win=45):
    """First match of `phrase` at/after the running cursor; tolerant of whisper misspellings."""
    t0 = _CUR[0] if after is None else after
    p = [_tok(x) for x in phrase.split() if _tok(x)]; tgt = " ".join(p); best = (0, None)
    for i in range(len(TOK) - len(p) + 1):   # exact match first (a fuzzy hit one word early would split mid-word)
        if WORDS[i]["s"] < t0 - 1e-6: continue
        if WORDS[i]["s"] > t0 + win: break
        if TOK[i:i + len(p)] == p:
            t = WORDS[i + len(p) - 1]["e"] if end else WORDS[i]["s"]
            if not end: _CUR[0] = t
            return t
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
TAGS = {}  # filled in edl_tuohy.py

# ------------------------------------------------------------------ soundbites (inserted; the voiceover pauses)
SNAPLOG = []
def snap(src, a, b):
    """Snap a soundbite to whole SENTENCES (user, 28 Nov 2026: interviews cut off mid-sentence look tacky).
    Start at the start of the sentence that contains `a` (if it began <= 4 s earlier), end at the end of the sentence
    that contains `b` (if it ends <= 7 s later). Then keep the window clear of the neighbouring words."""
    try: segs = json.load(open(f"{CS}/tx/{src}.json"))
    except FileNotFoundError: return a, b
    if isinstance(segs, dict): segs = segs.get("segments", [])
    ws = sorted(({"w": w[0], "s": w[1], "e": w[2]} if isinstance(w, list) else w for s in segs for w in s.get("words", s.get("w", []))), key=lambda w: w["s"])
    idx = [i for i, w in enumerate(ws) if w["s"] >= a - 0.05 and w["e"] <= b + 0.05]
    if not idx: return a, b
    END = lambda w: w["w"].strip().endswith((".", "?", "!"))
    i0, i1 = idx[0], idx[-1]
    j = i0   # walk back to the sentence start
    while j > 0 and not END(ws[j - 1]) and ws[j]["s"] - ws[j - 1]["e"] < 0.6 and ws[i0]["s"] - ws[j - 1]["s"] <= 4.0: j -= 1
    if j == 0 or END(ws[j - 1]) or ws[j]["s"] - ws[j - 1]["e"] >= 0.6: i0 = j
    j = i1   # walk forward to the sentence end
    while j < len(ws) - 1 and not END(ws[j]) and ws[j + 1]["s"] - ws[j]["e"] < 0.6 and ws[j + 1]["e"] - ws[i1]["e"] <= 7.0: j += 1
    if END(ws[j]) or j == len(ws) - 1 or ws[j + 1]["s"] - ws[j]["e"] >= 0.6: i1 = j
    first, last = ws[i0], ws[i1]
    prev = ws[i0 - 1]["e"] if i0 > 0 else None; nxt = ws[i1 + 1]["s"] if i1 + 1 < len(ws) else None
    a2 = first["s"] - 0.15; b2 = last["e"] + 0.35
    if prev is not None: a2 = max(a2, (prev + first["s"]) / 2 if first["s"] - prev < 0.8 else prev + 0.4)
    if nxt is not None: b2 = min(b2, (last["e"] + nxt) / 2 if nxt - last["e"] < 0.9 else nxt - 0.45)
    a2 = min(a2, first["s"] - 0.03); b2 = max(b2, last["e"] + 0.08)
    SNAPLOG.append((src, a, b, round(a2, 2), round(b2, 2), " ".join(w["w"].strip() for w in ws[i0:i1 + 1])))
    return round(max(0, a2), 2), round(max(b2, a2 + 1), 2)

PAD = 0.05   # snap() already leaves the speaker's own pause at both ends; fades handle the edges
from edl_gout import PRE_SB, SB_LIST, TAGS as _T, edl
try: from edl_gout import SPLIT_AT
except ImportError: SPLIT_AT = {}
TAGS.update(_T)
SOUNDBITES = []
_VODB = None
def gap_point(t0):
    """The voiceover is split at a soundbite. Whisper start times run late/early, so never split at t0-0.25:
    pick the quietest 10 ms frame between the previous word's start and the phrase start (measured silence),
    so the last word before the soundbite is never clipped (user, 13 Nov 2026: no clipped words)."""
    global _VODB
    from safe_cuts import rms_db
    if _VODB is None:
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
        _VODB = rms_db(x, 16000)
    # quietest 80 ms stretch within [t0-0.7, t0+0.6]; whisper starts can be off either way
    i0, i1 = max(0, int((t0 - 1.2) / 0.01)), int((t0 + 0.5) / 0.01)
    seg = np.convolve(_VODB[i0:i1], np.ones(8) / 8, mode="valid")
    j = int(np.argmin(seg)) + 4
    return round((i0 + j) * 0.01, 3)
def _sb():
    keep = _CUR[0]; _CUR[0] = 0.0
    for ph, src, a, b, cr, *opt in SB_LIST:
        o = dict(opt[0]) if opt else {}
        if not o.pop("raw", 0): a, b = snap(src, a, b)   # raw: times checked by ear/medium.en, keep as given
        t = SPLIT_AT[ph[0]] if ph[0] in SPLIT_AT else gap_point(A(ph[0], PART[ph[1]] - 0.5, win=1e9))
        SOUNDBITES.append(dict(t=round(t, 3), src=src, ss=a, dur=round(b - a, 3), tag=cr, **o))
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
def number(t, dur, val, label, sub=""): O(t, dur, ("number", val, label, sub))
def title(t, dur, kicker, headline): O(t, dur, ("title", kicker, headline))
def name(t, dur, n, sub): O(t, dur, ("name", n, sub))
def quote(t, dur, text, who=""): O(t, dur, ("quote", text, who))
def date(t, dur, text, sub=""): O(t, dur, ("date", text, sub))
def chapter(t, num, ttl): O(t, 2.8, ("chapter", num, ttl))

def build_edl():
    _sb(); _CUR[0] = 0.0
    edl(A, S, O, number, title, name, quote, date, chapter, PART)

# ------------------------------------------------------------------ final timeline
def timeline():
    build_edl()
    vo_shots = sorted(SHOTS, key=lambda s: s["t"])
    for v in vo_shots:   # a cut placed just before a soundbite split would flash for a few frames: move it past the split
        for s in SOUNDBITES:
            if 0 < s["t"] - v["t"] < 0.8: v["t"] = s["t"] + 0.001
    for s in SOUNDBITES:   # after each soundbite the previous shot continues where it left off
        if any(abs(v["t"] - s["t"]) < 0.3 or (s["t"] < v["t"] < s["t"] + 0.6) for v in vo_shots): continue
        prev = max((v for v in vo_shots if v["t"] < s["t"]), key=lambda v: v["t"])
        cont = dict(prev); cont["t"] = s["t"] + 0.001; cont.pop("flash", None); cont.pop("punch", None)
        cont["ss"] = prev["ss"] + (s["t"] - prev["t"]) * prev.get("slow", 1)
        vo_shots.append(cont)
    vo_shots.sort(key=lambda s: s["t"])
    seq = [dict(T=0.0, src=PRE_SB[0], ss=PRE_SB[1] - PAD, tag=PRE_SB[3], sb=1, _sbend=PRE_SB[2], **(PRE_SB[4] if len(PRE_SB) > 4 else {}))]
    for v in vo_shots:
        d = dict(v); d["T"] = round(FT(v["t"]), 3); seq.append(d)
    for s in SOUNDBITES:
        seq.append(dict(T=round(SB_START(s), 3), src=s["src"], ss=round(s["ss"] - PAD, 3), tag=s["tag"], sb=1, _sbend=round(s["ss"] + s["dur"], 3),
                        **{k: s[k] for k in ("vsrc", "vss", "quote", "who", "crop", "name", "subs", "tr", "subfix") if k in s}))
    seq.sort(key=lambda x: x["T"])
    # no flash cuts: drop any non-soundbite shot shorter than 0.9 s (the previous shot runs on instead)
    keep = []
    for i, x in enumerate(seq):
        nxt = seq[i + 1]["T"] if i + 1 < len(seq) else 1e9
        if not x.get("sb") and nxt - x["T"] < 0.9 and keep: continue
        keep.append(x)
    seq = keep
    end = FT(VO_END) + 4.0; out = []
    if os.environ.get("TEST"):   # style test: stop at the start of part TEST (+2 s)
        end = FT(PART[int(os.environ["TEST"])]) + 2.0; seq = [x for x in seq if x["T"] < end - 0.3]
    # keep cuts every 2-5 s: split any non-soundbite shot longer than 6 s into parts, jumping ahead in the same clip
    split = []
    for i, x in enumerate(seq):
        t1 = seq[i + 1]["T"] if i + 1 < len(seq) else end
        d = t1 - x["T"]
        if x.get("sb") or d <= 6.0 or x["src"].startswith("ph_") or x["src"] in NOSPLIT: split.append(x); continue
        n = int(d // 3.5) + 1; step = d / n; L = CLIPLEN.get(x["src"], 0)
        for k in range(n):
            y = dict(x); y["T"] = round(x["T"] + k * step, 3)
            if k:
                y.pop("flash", None); y.pop("ramp", None)
                jump = 9.0 * k if L > x["ss"] + 9.0 * k + step + 2 else step * x.get("slow", 1) * k
                y["ss"] = round(x["ss"] + jump, 3); y["punch"] = 0.3 if k % 2 else None
                if y["punch"] is None: y.pop("punch")
            split.append(y)
    seq = split
    for i, x in enumerate(seq):
        t1 = seq[i + 1]["T"] if i + 1 < len(seq) else end
        if t1 - x["T"] < 0.3: continue
        out.append((x, t1))
    ov = []
    for a0, a1, spec in OVER:
        f0, f1 = FT(a0), FT(a1)
        for s in SOUNDBITES:
            if a0 < s["t"] < a1: f1 = min(f1, SB_START(s))
        if f0 < end - 0.3: ov.append((round(f0, 3), round(min(f1, end), 3), spec))
    SFXEV[:] = [(o0, o1, spec) for o0, o1, spec in ov if spec[0] in ("sfx", "amb")]
    ov = [o for o in ov if o[2][0] not in ("sfx", "amb")]
    return out, ov, end
SFXEV = []

CROPS = {}
BANNED = {"spot7": [(255, 270), (430, 452), (560, 582), (1152.5, 1176)]}   # Seven Spotlight inserts: 1968 Olympic board, Netflix Sprint, IOC, Netflix/Tokyo 2020
NOSPLIT = {"spot7", "citius_season", "emerole_fl", "btr_lyles", "nova"}   # fast-cut TV specials: never jump ahead inside them
CLIPLEN = {}
def _cliplen(src):
    try: return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{REAL}/{src}.mp4'],capture_output=True,text=True).stdout)
    except Exception: return 0
def _isvert(src):
    try:
        w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f"{REAL}/{src}.mp4"], capture_output=True, text=True).stdout.strip().split(",")[:2])
        return h > w
    except Exception: return False
CLIPLEN.update({os.path.splitext(f)[0]: _cliplen(os.path.splitext(f)[0]) for f in os.listdir(REAL) if f.endswith('.mp4')})
VERT = {os.path.splitext(f)[0] for f in os.listdir(REAL) if f.endswith(".mp4") and _isvert(os.path.splitext(f)[0])}
GRADE = ("colorbalance=rs=-0.03:gs=-0.01:bs=0.04:rh=0.03:gh=0.01:bh=-0.02,eq=contrast=1.09:saturation=1.02:gamma=0.98,"
         "vignette=angle=PI/5,unsharp=5:5:0.6")   # cinematic grade: teal shadows / warm highlights, soft vignette, no grain
def ov_mov(spec, dur):
    p = f"{R}/ov/{hashlib.md5(json.dumps([spec, round(dur, 3)]).encode()).hexdigest()[:12]}.mov"
    if not os.path.exists(p): K.render(spec, dur, p)
    return p

SUBFIX = [("Solway", "Sawe"), ("Sawi", "Sawe"), ("Kejelcher", "Kejelcha"), ("Kajelcher", "Kejelcha"), ("Kejalcha", "Kejelcha"), ("Kejelja", "Kejelcha"),
          ("Gao", "Gout"), ("Galco", "Gout"), ("Dae", "Di"), ("Shepherd", "Sheppard"), ("SOP20", "sub-20"), ("1975", "19.75"), ("1967", "19.67"), ("1967.", "19.67.")]
def sub_words(src, ss, dur, end=None, fix=None):
    """Clip transcript words inside [ss, min(ss+dur, end)] -> [(word, t0, t1)] relative to the shot start.
    fix: [(old phrase, new phrase)] applied to consecutive words (whisper mishears), plus the global SUBFIX."""
    try: segs = json.load(open(f"{CS}/tx/{src}.json"))
    except FileNotFoundError: return []
    lim = min(ss + dur, end + 0.15) if end else ss + dur
    ws = [[w["w"].strip(), round(w["s"] - ss, 2), round(w["e"] - ss, 2)] for sg in segs for w in sg["words"]
          if w["s"] >= ss - 0.05 and w["s"] <= lim and w["w"].strip()]
    def norm(x): return "".join(c for c in x.lower() if c.isalnum())
    for old, new in list(fix or []) + SUBFIX:
        ot = [norm(x) for x in old.split()]; i = 0
        while i <= len(ws) - len(ot):
            if [norm(w[0]) for w in ws[i:i + len(ot)]] == ot:
                trail = "".join(c for c in ws[i + len(ot) - 1][0] if not c.isalnum() and c not in "'")[-1:]
                nw = new.rstrip(".,!?") + trail
                if nw != ws[i][0] or len(ot) > 1: ws[i] = [nw, ws[i][1], ws[i + len(ot) - 1][2]]; del ws[i + 1:i + len(ot)]
            i += 1
    return [tuple(w) for w in ws]

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
    vsb = sb and sh.get("vsrc")   # audio-only soundbite: her voice over clean B-roll with the words on screen
    if vsb:
        asrc, ass = src, sh["ss"]; src = sh["vsrc"]; sb = None; sh = dict(sh, ss=sh.get("vss", 0.0), _asrc=asrc, _ass=ass)
    rp = sh.get("ramp")
    tin = (rp[0] + (dur - rp[0]) * rp[1]) if rp else dur * slow
    for b0, b1 in BANNED.get(src, ()):   # Netflix/Olympic/IOC inserts inside TV specials: never render them
        if sh["ss"] < b1 and sh["ss"] + tin > b0: raise SystemExit(f"shot {i} uses banned footage: {src} {sh['ss']:.1f}-{sh['ss'] + tin:.1f} overlaps {b0}-{b1}")
    L_ = CLIPLEN.get(src, 0)
    if L_ and sh["ss"] + tin > L_ - 0.1: sh = dict(sh, ss=max(0.0, L_ - tin - 0.3))   # never seek past the clip's end (empty shot = broken timestamps)
    ins = ["-ss", f"{max(0, sh['ss']):.3f}", "-t", f"{tin + 0.2:.3f}", "-i", f"{REAL}/{src}.mp4"]
    DL = (sh.get("crop") or CROPS.get(src, "")) + ("," if (sh.get("crop") or CROPS.get(src)) else "")   # crop away burned-in UI / boxes
    FILL = "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080"
    if src in VERT:
        FILL = ("split[vf1][vf2];[vf1]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=40,eq=brightness=-0.25[vbg];"
                "[vf2]scale=-2:1080:flags=lanczos[vfg];[vbg][vfg]overlay=(W-w)/2:0")
    if sb:
        base = (f"[0:v]setpts=PTS-STARTPTS,{DL}{FILL},setsar=1,"
                f"eq=contrast=1.04:saturation=1.05,tpad=stop_mode=clone:stop_duration=30")
    else:
        p = sh.get("punch"); z = f"(1+0.035*t/{dur:.3f}"
        if p is not None: z += f"+0.06*min(1,max(0,(t-{p:.3f})/0.6))"
        z += ")"
        sp = (f"setpts='if(lt(T,{rp[0]:.3f}),PTS-STARTPTS,({rp[0]:.3f}+(T-{rp[0]:.3f})/{rp[1]:.3f})/TB)'" if rp else f"setpts={1 / slow:.4f}*(PTS-STARTPTS)")
        base = (f"[0:v]{sp},{DL}{FILL},"
                f"scale='trunc(1920*{z}/2)*2':-2:eval=frame:flags=lanczos,crop=1920:1080,setsar=1,{GRADE},tpad=stop_mode=clone:stop_duration=60")
        if sh.get("bw"): base += ",hue=s=0.15,eq=contrast=1.08:brightness=-0.02"   # muted, not full B&W
        if sh.get("blur"): base += ",gblur=sigma=18,eq=brightness=-0.12"
        if sh.get("flash"): base += ",fade=t=in:st=0:d=0.35"   # soft fade-in from black instead of a white flash
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
    if sh.get("name"):
        mov = ov_mov(("iname",) + tuple(sh["name"]), min(dur, 5.0)); k += 1; ins += ["-i", mov]
        vf.append(f"[{k}:v]setpts=PTS-STARTPTS,format=rgba[o{k}];[b{k - 1}][o{k}]overlay=0:0:eof_action=pass[b{k}]")
    if sh.get("subs"):
        ws = sub_words(sh.get("_asrc", src), sh.get("_ass", sh["ss"]), dur, sh.get("_sbend"), sh.get("subfix"))
        if ws:
            mov = ov_mov(("subs", ws), dur); k += 1; ins += ["-i", mov]
            vf.append(f"[{k}:v]setpts=PTS-STARTPTS,format=rgba[o{k}];[b{k - 1}][o{k}]overlay=0:0:eof_action=pass[b{k}]")
    if vsb and sh.get("quote"):
        mov = ov_mov(("quote", sh["quote"], sh.get("who", "")), dur); k += 1; ins += ["-i", mov]
        vf.append(f"[{k}:v]setpts=PTS-STARTPTS,format=rgba[o{k}];[b{k - 1}][o{k}]overlay=0:0:eof_action=pass[b{k}]")
    vf.append(f"[b{k}]format=yuv420p[v]")
    ins += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]; amap = f"{k + 1}:a"
    if vsb:
        ins += ["-ss", f"{max(0, ass):.3f}", "-t", f"{dur + 0.2:.3f}", "-i", f"{REAL}/{asrc}.mp4"]
        vf.append(f"[{k + 2}:a]aresample=48000,loudnorm=I=-17:TP=-2:LRA=11,afade=t=in:d=0.15,afade=t=out:st={max(0, dur - 0.45):.3f}:d=0.45,apad=whole_dur={dur:.3f}[a]"); amap = "[a]"
    vol = 1.0 if sb else (0.16 if sh.get("amb") else 0.0)
    if vol > 0:
        hp = ",loudnorm=I=-17:TP=-2:LRA=11" if sb else ",highpass=f=120"
        at = "" if slow == 1 else f",atempo={max(0.5, slow):.3f}"
        fd = f",afade=t=in:d=0.15,afade=t=out:st={max(0, dur - 0.45):.3f}:d=0.45" if sb else ""
        vf.append(f"[0:a]aresample=48000{at},volume={vol}{hp}{fd},apad=whole_dur={dur:.3f}[a]"); amap = "[a]"
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

def trans_cuts():
    shots, ov, end = TL(); cuts = []
    for i, (sh, t1) in enumerate(shots):
        if i == 0: continue
        k = sh.get("tr", "blur" if sh.get("sb") else ("dip" if shots[i - 1][0].get("sb") else None))   # smooth in AND out of every interview
        if k == "none": k = None
        if k: cuts.append((sh["T"], k))
    for o0, o1, spec in ov:
        if spec[0] == "chapter": cuts.append((o0, "leak"))
    cuts = sorted({round(c, 2): (c, k) for c, k in cuts}.values())
    clean = []
    for c, k in cuts:
        if clean and c - clean[-1][0] < 1.2: continue
        clean.append((c, k))
    return clean

def stage_trans():
    """Cinematic transitions on chosen cuts (shot opt tr=kind; soundbites 'blur' in and 'dip' out, chapters 'leak')."""
    clean = trans_cuts()
    PM.apply_transitions(f"{R}/picture.mp4", f"{R}/picture_tr.mp4", clean)
    print("transitions", len(clean))

def vo_track(end):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)
    SR = 48000; parts = [np.zeros((int(PRE * SR), 2), np.float32)]; last = 0
    for s in SOUNDBITES:
        cut = int(s["t"] * SR); parts.append(x[last:cut]); parts.append(np.zeros((int((s["dur"] + 2 * PAD) * SR), 2), np.float32)); last = cut
    parts.append(x[last:]); y = np.concatenate(parts)
    if os.environ.get("TEST"): y = y[:int(end * SR)].copy(); y[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))[:, None]
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
    if t0 >= end - 0.5: return None
    t1 = min(t1, end)
    out = f"{R}/bed_{os.path.basename(path)}_{t0:.1f}.wav"; L = t1 - t0; dl = int(t0 * 1000)
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", str(offset), "-i", path, "-t", f"{L:.2f}", "-af",
         f"volume={vol},afade=t=in:st=0:d={fin},afade=t=out:st={max(0, L - fout):.2f}:d={fout},adelay={dl}|{dl},apad=whole_dur={end:.2f}",
         "-ar", "48000", "-ac", "2", out]); return out

SFXD = f"{P}/sfx"   # real ambience + SFX (ElevenLabs sound effects v3, flow FG4WsvGEsPROQNhXYEBS), 28 Nov 2026
def sfx_plan(shots, ov):
    """User, 28 Nov 2026 (v3 review): the whip/whoosh noises happened "too consistently... too repetitive". Most cuts and
    transitions are now SILENT. A sound only lands on: interview entrances, chapter cards, rgb glitches, data graphics,
    and explicit EDL cues. Whooshes >= 7 s apart, never the same file twice in a row, softer."""
    shot_at = {round(sh["T"], 2): sh for sh, _ in shots}
    cand = []
    for c, k in trans_cuts():
        sh = shot_at.get(round(c, 2), {})
        if k == "rgb": cand.append((c - 0.1, "glitch", 0.20, 2, "w"))
        elif sh.get("sb") or k == "leak": cand.append((c - 0.3, "whoosh_deep", 0.20, 2, "w"))
    for o0, o1, spec in ov:
        k = spec[0]
        if k == "chapter": cand.append((o0 + 0.05, "boom", 0.34, 3, "b"))
        elif k in ("board", "drift"): cand.append((o0 + 0.25, "data_ticks", 0.16, 1, "d"))
        elif k == "stamp": cand.append((o0, "shutters", 0.28, 3, "s"))
    for o0, o1, spec in SFXEV:
        if spec[0] == "sfx": cand.append((o0, spec[1], spec[2] if len(spec) > 2 else 0.35, 9, "x"))
    cand.sort(key=lambda c: (-c[3], c[0])); kept = []
    for t, nm, g, pri, grp in cand:
        if t < 0 or any(abs(t - u) < 2.5 for u, *_ in kept): continue
        if grp == "w" and any(abs(t - u) < 7.0 for u, _, _, _, gg in kept if gg == "w"): continue
        kept.append((t, nm, g, pri, grp))
    kept.sort(); out = []; rot = {"whoosh_deep": ["whoosh_deep1", "whoosh_deep3", "whoosh_fast2", "whoosh_deep2", "whoosh_fast1", "whoosh_fast3"]}; last = None; i = 0
    for t, nm, g, pri, grp in kept:
        if nm in rot:
            opts = [x for x in rot[nm] if x != last]; nm2 = opts[i % len(opts)]; i += 1
        else: nm2 = nm
        last = nm2; out.append((t, f"{SFXD}/{nm2}.mp3", g))
    return out

def amb_beds(end):
    """Room tone of the story: a low stadium bed under everything, plus wind/rain/heartbeat/clock beds from ("amb", name, vol) cues."""
    b = [bed(f"{SFXD}/amb_stadium.mp3", 0, end, 0.10, end, 2.0, 3.0)]
    for o0, o1, spec in SFXEV:
        if spec[0] == "amb": b.append(bed(f"{SFXD}/{spec[1]}.mp3", o0, o1, spec[2] if len(spec) > 2 else 0.2, end, 1.2, 1.5))
    return [x for x in b if x]

def stage_audio():
    shots, ov, end = TL(); vo = vo_track(end)
    M1 = f"{ROOT}/projects/jon-drummond/music"; Pt = {k: FT(v) for k, v in PART.items()}
    T2 = f"{ROOT}/projects/tebogo-rise/music"; N2 = f"{ROOT}/projects/ncaa-100m-champs/music"
    # dark open -> rising kid -> familiar (tense) -> freshman dominance (triumph) -> first cracks (dark) -> they all fell off (sad) -> the difference (hopeful) -> NCAAs (tense) -> reflective end
    # the video (dark) -> Bronxville (light) -> the rise (tense build) -> the deal (dark) -> body breaks (sad) -> Salazar falls (tense) -> the ban -> now (hopeful) -> end
    # fall (dark) -> Trenton (light) -> 16 (light) -> rise (tense build) -> cracks (tense) -> doubt (sad) -> the fall (dark/tense)
    # -> comeback (tense) -> silence (dark) -> answer (warm) -> end (reflective)
    # dark open -> prodigy/USC/43.45 (rise) -> chokes (dark) -> gold (tense) -> switch + Paris (dark) -> comeback (hope/dark)
    # -> soft + Japan (tense) -> verdict (reflective)
    # Cooper rise: cold open (dark) -> Justin/record/1:42 (rise) -> Nike + Tokyo (tense) -> 2026 run (triumph) -> respect/senior (reflective) -> end
    # Lyles: its own score (ElevenLabs music v2.5, flow 5b7OvkCR2GzFbi91MiPX, N1-N7), one track per mood
    MU = f"{P}/music"   # Gout Gout: own score G1-G6 (flow FG4WsvGEsPROQNhXYEBS)
    beds = [bed(f"{MU}/G1_case.mp3", 0, Pt[2] + 0.4, 0.56, end, 1.0, 1.5),
            bed(f"{MU}/G2_ipswich.mp3", Pt[2] - 0.2, Pt[3] + 0.4, 0.50, end, 0.8, 1.5),
            bed(f"{MU}/G3_hype.mp3", Pt[3] - 0.2, Pt[4] + 0.4, 0.52, end, 0.8, 1.5),
            bed(f"{MU}/G4_evidence.mp3", Pt[4] - 0.2, Pt[8] + 0.4, 0.52, end, 0.8, 1.2),
            bed(f"{MU}/G5_sydney.mp3", Pt[8] - 0.2, Pt[10] + 0.4, 0.54, end, 0.8, 1.5),
            bed(f"{MU}/G6_verdict.mp3", Pt[10] - 0.2, end, 0.55, end, 0.8, 3.5)]
    beds = [b for b in beds if b] + amb_beds(end)
    S_ = sfx_plan(shots, ov)
    ins, fl = [], []; nb = len(beds); base = 2 + nb
    for j, (t, path, g) in enumerate(S_):
        ins += ["-i", path]; d = int(max(0, t) * 1000)
        fl.append(f"[{j + base}:a]volume={g},adelay={d}|{d},aformat=sample_rates=48000:channel_layouts=stereo[s{j}]")
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
    pic = f"{R}/picture_tr.mp4" if os.path.exists(f"{R}/picture_tr.mp4") else f"{R}/picture.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", f"{end:.2f}", "-movflags", "+faststart", OUT])
    print("wrote", OUT)

def stage_check():
    shots, ov, end = TL()
    print("shots", len(shots), "overlays", len(ov), "end", round(end, 1), "=", f"{int(end // 60)}:{end % 60:04.1f}", "soundbites", len(SOUNDBITES))
    for sh, t1 in shots: print(f"{sh['T']:7.2f}-{t1:7.2f} {'SB ' if sh.get('sb') else '   '}{sh['src']:10s} {sh.get('ss', 0):7.1f} {sh.get('tag', '')}")
    for o in ov: print(f"  OV {o[0]:7.2f}-{o[1]:7.2f} {o[2][:3]}")

if __name__ == "__main__":
    st = sys.argv[1:] or ["shots", "concat", "trans", "audio", "mux"]
    for s in st: globals()[f"stage_{s}"]()
    print("DONE")
