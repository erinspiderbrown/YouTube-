"""The Greatest High School Runner Ever... Where Did She Go? (Katelyn Tuohy). Boling v2 style.
Copied from projects/abby-steiner/abby_build.py; only config, soundbites and EDL differ. No FloTrack/MileSplit footage.
- Voiceover: the user's one-take Dropbox recording, cleaned by clean_voiceover.py (cuts only inside measured silence,
  every year checked by check_vo.py). Parts 1-9 tagged in vo_words.json.
- Soundbites: NXN 2017 + NBNO 2018 race calls, Gatorade 2018, ESPN NCAA 2022, CITIUS going pro, her 2024 Trials and
  2025/2026 interviews (runnerspace, CITIUS, LetsRun). Photos: Wikimedia Commons (jenaragon94 CC BY 2.0, Joe Peacock CC BY-SA 4.0).
Every time in the EDL is cleaned-VO seconds; FT() maps it onto the final timeline.
Run:  python3 projects/katelyn-tuohy/tuohy_build.py [stage ...]   stages: shots concat audio mux (default all); check
"""
import os, sys, json, math, subprocess, hashlib, difflib
import numpy as np
from PIL import Image, ImageFilter

ROOT = "/home/user/YouTube-"; P = f"{ROOT}/projects/katelyn-tuohy"
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, f"{ROOT}/projects/katelyn-tuohy")
import kinetic as K
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad"
CS = f"{SCR}/tuohy"; REAL = f"{CS}/clips"; R = f"{CS}/render"
for d in ("ov", "shots", "sfx", "tags"): os.makedirs(f"{R}/{d}", exist_ok=True)
VO = f"{P}/tuohy_voiceover.wav"
OUT = f"{SCR}/output/Katelyn_Tuohy_Where_Did_She_Go.mp4"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
W, Hh, FPS = 1920, 1080, 24

# ------------------------------------------------------------------ voiceover words + phrase finder
WORDS = json.load(open(f"{P}/vo_words.json"))[0]["words"]
_NUMW = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
def _tok(w):
    t = "".join(ch for ch in w.lower() if ch.isalnum())
    return _NUMW[int(t)] if t.isdigit() and int(t) <= 20 else t
TOK = [_tok(x["w"]) for x in WORDS]
VO_END = WORDS[-1]["e"]
PART = {k: min(w["s"] for w in WORDS if w["part"] == k) for k in range(1, 10)}
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
TAGS = {}  # filled in edl_tuohy.py

# ------------------------------------------------------------------ soundbites (inserted; the voiceover pauses)
def snap(src, a, b):
    """Snap a soundbite to the clip's own word boundaries so no word is clipped."""
    try: segs = json.load(open(f"{CS}/tx_{src}.json"))
    except FileNotFoundError: return a, b
    ws = [w for s in segs for w in s.get("words", s.get("w", []))]
    st = [w["s"] for w in ws if w["s"] >= a - 0.4]; en = [w["e"] for w in ws if w["e"] <= b + 0.4]
    a2 = (min(st) - 0.12) if st else a; b2 = (max(en) + 0.3) if en else b
    return round(max(0, a2), 2), round(max(b2, a2 + 1), 2)

PAD = 0.3
from edl_tuohy import PRE_SB, SB_LIST, TAGS as _T, edl
TAGS.update(_T)
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
    _sb(); _CUR[0] = 0.0
    edl(A, S, O, stat, say, stack, name, stamp, chapter, PART)

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
    T2 = f"{ROOT}/projects/tebogo-rise/music"; N2 = f"{ROOT}/projects/ncaa-100m-champs/music"
    # one bed per mood: dark open -> hopeful come-up -> triumphant peak -> tense fall -> heavy last race -> sad disappearance -> reflective ending
    # dark open -> hopeful phenom -> tense weight -> triumphant NC State -> pro (hopeful) -> the slide -> sad disappearance -> tense comeback -> reflective end
    beds = [bed(f"{M1}/M1_cold-open-background.mp3", 0, Pt[2] + 0.4, 0.5, end, 1.0, 1.5),
            bed(f"{M1}/M2_sydney.mp3", Pt[2] - 0.2, Pt[3] + 0.4, 0.40, end, 0.6, 1.2),
            bed(f"{M1}/M4_coaching-ban.mp3", Pt[3] - 0.2, Pt[4] + 0.4, 0.40, end, 0.6, 1.2),
            bed(f"{T2}/triumph_drums_choir.mp3", Pt[4] - 0.2, Pt[5] + 0.4, 0.34, end, 0.4, 1.2),
            bed(f"{M1}/M2_sydney.mp3", Pt[5] - 0.2, Pt[6] + 0.4, 0.38, end, 0.6, 1.2, offset=40),
            bed(f"{M1}/M3_rule-paris-fallout.mp3", Pt[6] - 0.2, Pt[7] + 0.4, 0.42, end, 0.6, 1.5),
            bed(f"{N2}/tribute.mp3", Pt[7] - 0.2, Pt[8] + 0.4, 0.40, end, 0.8, 1.5),
            bed(f"{M1}/M4_coaching-ban.mp3", Pt[8] - 0.2, Pt[9] + 0.4, 0.40, end, 0.6, 1.5, offset=60),
            bed(f"{M1}/M5_verdict-ending.mp3", Pt[9] - 0.2, end, 0.48, end, 0.8, 3.5)]
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
