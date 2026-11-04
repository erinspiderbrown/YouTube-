"""Podcast-style edit pipeline: Montverde video.

Stages (each cached in render/):
  1. plan     - keep-ranges from word timestamps, shots + framing, timeline
  2. aroll    - render each A-roll shot (crop/punch-in + grade) and inserts
  3. broll    - render B-roll inserts (stock clips / photo Ken Burns) + graphics PNGs
  4. compose  - concat base, overlay B-roll + graphics
  5. audio    - voice edit + cleanup, music bed w/ ducking, SFX, loudness
  6. mux      - final.mp4
"""
import json, os, subprocess, sys, wave, math
from concurrent.futures import ThreadPoolExecutor
import numpy as np

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(S, "scripts"))
import gfx, cards, mograph, hud, sounds
import transitions as TR
import cv2
from deshadow import deshadow

F, B, A, R = (os.path.join(S, d) for d in ("dropbox1/files", "broll", "assets", "render"))
os.makedirs(R, exist_ok=True)
FPS = 24
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:600]); print(r.stderr[-2000:]); raise SystemExit(1)

def fr(t):  # snap to frame grid
    return round(t * FPS) / FPS

# ---------------------------------------------------------------- 1. plan
MUSIC_GAIN = 1   # user: dark suspense bed, low under the voice (synthesized)
CUT_END = 599.95   # user: cut everything after "this doping shit is a joke"
ALL_WORDS = [w for seg in json.load(open(os.path.join(S, "work/main.json"))) for w in seg["words"]]
words = [w for w in ALL_WORDS if w["s"] < CUT_END]
import re as _re
SWEAR = _re.compile(r"\b(shit|fuck\w*|motherfuck\w*|nigga\w*|bitch\w*)\b", _re.I)
SWEARS = [(w["s"], w["e"]) for w in words if SWEAR.search(w["w"])]
GAP, PRE, POST = 0.45, 0.10, 0.16
ranges = []
cur = [words[0]["s"], words[0]["e"]]
for w in words[1:]:
    if w["s"] - cur[1] > GAP:
        ranges.append(cur); cur = [w["s"], w["e"]]
    else:
        cur[1] = w["e"]
ranges.append(cur)
ranges = [[max(0, s - PRE), e + POST] for s, e in ranges]
for i in range(1, len(ranges)):  # no overlaps
    if ranges[i][0] < ranges[i - 1][1]:
        mid = (ranges[i][0] + ranges[i - 1][1]) / 2
        ranges[i - 1][1] = mid; ranges[i][0] = mid

# split long ranges into shots (angle change on continuous audio) at word gaps
MAXSHOT = 8.0
shots = []
for s, e in ranges:
    inner = [w for w in words if s <= w["s"] and w["e"] <= e]
    start = s
    while e - start > MAXSHOT + 3:
        target = start + MAXSHOT
        cands = [(abs(a["e"] - target), (a["e"] + b["s"]) / 2) for a, b in zip(inner, inner[1:])
                 if start + 3 < a["e"] < e - 3 and b["s"] - a["e"] > 0.12]
        if not cands: break
        cut = min(cands)[1]
        shots.append([start, cut, False]); start = cut
    shots.append([start, e, True])   # True = ends at a real time-cut

# framing: (crop_w, cx, cy) in 4K coords; cycle changes on every shot
FRAMES = {"W": (3840, 1920, 1080), "M": (3072, 1650, 1130), "C": (2560, 1478, 1080)}
CYCLE = ["C", "M", "C", "W"]
shot_items = []
for i, (s, e, tc) in enumerate(shots):
    shot_items.append({"type": "aroll", "src": [s, e], "frame": CYCLE[i % len(CYCLE)]})

TITLE_AFTER, INTERVIEW_AFTER = 30.56, 236.99
TITLE_DUR = 3.0
timeline = []
for it in shot_items:
    timeline.append(it)
    if abs(it["src"][1] - POST - TITLE_AFTER) < 0.3:
        timeline.append({"type": "title", "dur": TITLE_DUR})
    if abs(it["src"][1] - POST - INTERVIEW_AFTER) < 0.3:
        timeline.append({"type": "interview", "src": [0.30, 14.0]})
timeline.append({"type": "end", "dur": 4.0})
assert sum(t["type"] == "title" for t in timeline) == 1, "title anchor not found"
assert sum(t["type"] == "interview" for t in timeline) == 1, "interview anchor not found"

t = 0.0
for it in timeline:
    d = it["dur"] if "dur" in it else it["src"][1] - it["src"][0]
    it["frames"] = max(1, round(d * FPS)); it["out"] = t; t += it["frames"] / FPS
TOTAL = t

def O(src):
    """Map a source time to output time."""
    best = None
    for it in timeline:
        if it["type"] != "aroll": continue
        s, e = it["src"]
        if s <= src <= e: return it["out"] + (src - s)
        if src < s and best is None: best = it["out"]
    return best if best is not None else TOTAL

# ---------------------------------------------------------------- creative spec (source times)
BROLL = [  # (src_start, src_end, kind, source, offset)  kind: stock | mg (motion graphic)
    (3.38, 5.16, "stock", "sweep", 3),
    (10.66, 14.2, "mg", "florida_map", None),
    (20.5, 23.68, "stock", "start_line", 2),
    (24.42, 26.82, "stock", "plane", 1),
    (26.82, 30.56, "stock", "lab_tubes", 1),
    (41.9, 46.3, "mg", "stepper", None),
    (46.62, 53.0, "stock", "suit_laptop", 3),
    (65.94, 71.78, "stock", "pour_glass", 0),
    (71.78, 77.04, "stock", "warmup", 1),
    (94.38, 99.78, "stock", "lab_gloves", 1),
    (105.6, 108.6, "stock", "women_track", 1),
    (128.26, 134.6, "stock", "campus2", 3),
    (140.4, 147.5, "stock", "newspaper", 1),
    (150.07, 163.0, "mg", "definition", None),
    (178.4, 183.6, "stock", "judge_doc", 1),
    (191.13, 197.33, "mg", "relationship", None),
    (197.5, 201.31, "stock", "campus1", 3),
    (205.11, 209.69, "stock", "gavel", 1),
    (218.39, 222.49, "stock", "start_line", 8),
    (226.31, 237.0, "mg", "deal_timeline", None),
    (245.44, 250.0, "stock", "blocks3", 2),
    (263.18, 278.0, "mg", "jadco_vs_aiu", None),
    (303.14, 312.34, "mg", "africa_target", None),
    (332.2, 337.26, "stock", "lab_drops", 2),
    (348.94, 356.0, "mg", "world_routes", None),
    (387.7, 393.06, "mg", "converge", None),
    (393.24, 397.8, "stock", "campus2", 14),
    (415.18, 426.3, "mg", "gw1516", None),
    (437.58, 443.0, "stock", "lightning", 4.4),
    (449.4, 458.4, "mg", "tracker3", None),
    (464.19, 468.99, "stock", "women_track", 1),
    (479.35, 489.07, "mg", "tracker4", None),
    (494.87, 499.13, "stock", "male_track", 1),
    (499.29, 503.75, "stock", "women_track", 6),
    (505.05, 518.0, "mg", "team_grid", None),
    (549.57, 556.89, "stock", "pour_bottle", 9),
    (556.89, 561.15, "stock", "blocks1", 2),
    (580.53, 590.63, "stock", "laptop", 1),
]
TRANSITIONS = ["whip", "zoom", "glitch", "whip", "flash", "zoom"]   # cycled across inserts
GERALD = dict(name="Gerald Phiri", sub="Former Montverde track coach")
ISSAM = dict(name="Issam Asinga", sub="Sprinter · Suriname")
ADAEJAH = dict(name="Adaejah Hodge", sub="Sprinter · British Virgin Islands")
CARDS = [  # first mention of each person only
    (14.3, 18.9, GERALD, "coach_mouth.jpg", None, None),
    (56.4, 62.2, ISSAM, "issam_270.jpg", ("SUSPENDED", None, 1.6), "Photo: Oscar Muñoz Badilla"),
    (103.3, 105.6, ADAEJAH, "hodge_flag.jpg", None, None),
]
KEYWORDS = [  # (src_time, text, dur, pos)
    (1.9, "Swept under\nthe rug", 2.6, "left"),
    (8.3, "Almost\n2 years", 2.2, "left"),
    (16.5, "Allegedly", 2.0, "left"),
    (34.2, "Everybody\non the team", 2.4, "left"),
    (47.9, "New company", 2.2, "left"),
    (68.4, "Clear. Tasteless.\nOdorless.", 3.2, "left"),
    (117.2, "These kids\nare cooked", 2.2, "left"),
    (138.8, "Nobody's\ntalking about it", 2.4, "left"),
    (205.2, "Sue the\nschool", 2.4, "left"),
    (197.5, "Well-funded\nboarding school", 3.0, "left"),
    (250.2, "Same substance.\nSame coach.", 3.2, "right"),
    (329.9, "Target\ntesting", 2.4, "left"),
    (437.6, "Lightning\nstriking twice", 2.6, "left"),
    (551.0, "Water bottles\nat practice", 3.0, "left"),
]
PUNCH_EXTRA = [6.28, 24.42, 39.08, 83.46, 91.18, 101.48, 109.3, 173.67, 214.95, 240.78, 289.0,
               343.64, 357.26, 405.94, 520.0, 563.69, 593.47]   # emphasis beats with no graphic
LOWER_THIRDS = []
DISCLAIMER = "Commentary & opinion · Claims about the coach and school are allegations"

def stage_plan():
    plan = {"total": TOTAL, "timeline": timeline}
    json.dump(plan, open(os.path.join(R, "plan.json"), "w"), indent=1)
    n_cuts = sum(1 for s in shots if s[2]) - 1
    print(f"shots={len(shots)} time-cuts={n_cuts} total={TOTAL:.1f}s (source 699.3s)")

# ---------------------------------------------------------------- 2. aroll
GRADE = ("curves=master='0/0.02 0.18/0.21 0.42/0.5 0.7/0.72 0.85/0.8 1/0.9',"
         "eq=saturation=1.12,colorbalance=rm=0.015:bm=-0.015:rs=0.01:bs=-0.01")
STOCK_GRADE = "eq=contrast=1.06:saturation=1.08,colorbalance=rm=0.02:bm=-0.02"

SOFA_Y = 0.72 * 2160  # top of the sofa back, 4K coords
FACES = np.array(json.load(open(os.path.join(S, "work/faces.json"))))
FACE_MED = np.median(FACES[:, 1:3], axis=0)

def face_at(s, e):
    m = FACES[(FACES[:, 0] >= s) & (FACES[:, 0] <= e)]
    fx, fy = (np.median(m[:, 1:3], axis=0) if len(m) else FACE_MED)
    return fx * 3840, fy * 2160

def crop_rect(code, src=None):
    w = FRAMES[code][0]; h = w * 9 // 16
    if code == "W": return w, h, 0, 0
    fx, fy = face_at(*src) if src else (FACE_MED[0] * 3840, FACE_MED[1] * 2160)
    lead = 0.08 * w  # a little look-room to his left side of frame
    cx = fx + lead
    x = int(min(max(0, cx - w / 2), 3840 - w)); y = int(min(max(0, fy - 0.55 * h), 2160 - h))
    return w, h, x & ~1, y & ~1

def enc(out):
    return ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-video_track_timescale", "12288", out]

def render_item(i):
    it = timeline[i]; out = os.path.join(R, f"item_{i:03d}.mp4")
    if os.path.exists(out): return
    d = it["frames"] / FPS
    if it["type"] == "aroll":
        w, h, x, y = crop_rect(it["frame"], it["src"])
        fx, _ = face_at(*it["src"])
        face_x = (fx - x) / w * 1920
        sofa_y = (SOFA_Y - y) / h * 1080
        mask = cv2.resize(cv2.imread(os.path.join(A, "lightmask.png"))[y:y + h, x:x + w], (1920, 1080),
                          interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{it['src'][0]:.3f}", "-t", f"{d + 0.5:.3f}",
                                "-i", os.path.join(F, "main.mov"), "-vf",
                                f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,fps={FPS},{GRADE}",
                                "-frames:v", str(it["frames"]), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                               stdout=subprocess.PIPE)
        encp = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", "1920x1080", "-r", str(FPS), "-i", "-", "-vf", "unsharp=5:5:0.3"] + enc(out),
                                stdin=subprocess.PIPE)
        fsz = 1920 * 1080 * 3; nfr = 0; last = None; dstate = {}
        while nfr < it["frames"]:
            buf = dec.stdout.read(fsz)
            if len(buf) < fsz:
                buf = last  # source ran short: hold last frame
                if buf is None: break
            last = buf
            fr_ = np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3)
            fixed, _ = deshadow(fr_, sofa_y, face_x, state=dstate)
            fixed = (fixed.astype(np.float32) * mask[..., ::-1]).astype(np.uint8)
            encp.stdin.write(fixed.tobytes()); nfr += 1
        dec.stdout.close(); dec.wait(); encp.stdin.close(); encp.wait()
    elif it["type"] == "interview":
        tag = os.path.join(R, "g_interview_tag.png")
        gfx.caption_tag("Issam Asinga · post-race interview", tag)
        fc = (f"[0:v]scale=1920:1080:flags=lanczos,fps={FPS},{STOCK_GRADE},unsharp=5:5:0.5[v];"
              f"[v][1:v]overlay,format=yuv420p,trim=end_frame={it['frames']}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{it['src'][0]:.3f}", "-i", os.path.join(F, "interview.mp4"),
             "-loop", "1", "-i", tag, "-filter_complex", fc, "-map", "[o]", "-frames:v", str(it["frames"])] + enc(out))
    elif it["type"] in ("title", "end"):
        png = os.path.join(R, f"g_{it['type']}.png")
        if it["type"] == "title":
            gfx.title_card("The Montverde Academy doping scandal", "Swept under\nthe rug", png, DISCLAIMER)
            bg, off = os.path.join(B, "blocks3.mp4"), 1
        else:
            gfx.title_card("What do you think?", "Let me know\nin the comments", png)
            bg, off = os.path.join(B, "fl_city.mp4"), 2
        fc = (f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps={FPS},"
              f"eq=brightness=-0.28:saturation=0.75,boxblur=10:1,vignette=angle=PI/3,setpts=PTS*1.4[bg];"
              f"[1:v]format=rgba,fade=in:st=0.1:d=0.35:alpha=1[t];[bg][t]overlay,"
              f"fade=in:st=0:d=0.2,format=yuv420p,trim=end_frame={it['frames']}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(off), "-i", bg, "-loop", "1", "-i", png,
             "-filter_complex", fc, "-map", "[o]", "-frames:v", str(it["frames"])] + enc(out))

def stage_aroll():
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(render_item, range(len(timeline))))
    lst = os.path.join(R, "concat.txt")
    with open(lst, "w") as f:
        for i in range(len(timeline)): f.write(f"file 'item_{i:03d}.mp4'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
         os.path.join(R, "base.mp4")])

# ---------------------------------------------------------------- 3. broll + graphics
def broll_events():
    ev = []
    for i, (s0, e0, kind, src, opt) in enumerate(BROLL):
        o0, o1 = fr(O(s0)), fr(O(e0))
        if o1 - o0 < 0.8: print("skip short broll", src, s0); continue
        ev.append({"start": o0, "dur": o1 - o0, "kind": kind, "src": src, "opt": opt,
                   "trans": TRANSITIONS[len(ev) % len(TRANSITIONS)]})
    return ev

def transition(raw, out, kind, n):
    """Bake entry/exit transition into an insert clip's first/last frames."""
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", raw, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    encp = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
                             "-r", str(FPS), "-i", "-"] + enc(out), stdin=subprocess.PIPE)
    fsz = 1920 * 1080 * 3; rng = np.random.default_rng(7)
    IN, OUT = 6, 5
    for i in range(n):
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz: break
        f = np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3)
        p_in = 1 - i / IN if i < IN else 0             # 1 -> 0 during entry
        p_out = (i - (n - OUT)) / OUT if i >= n - OUT else 0   # 0 -> 1 during exit
        p = max(p_in, p_out)
        if p > 0:
            if kind == "whip":
                sgn = 1 if p_in else -1
                f = np.roll(f, int(sgn * 1920 * 0.28 * p ** 1.5), axis=1)
                k = int(2 + 140 * p) | 1
                f = cv2.blur(f, (k, 1))
            elif kind == "zoom":
                z = 1 + (0.35 if p_in else 0.25) * p ** 1.3
                M = cv2.getRotationMatrix2D((960, 540), 0, z)
                acc = np.zeros_like(f, np.float32)
                for j in range(4):  # cheap zoom blur
                    Mj = cv2.getRotationMatrix2D((960, 540), 0, z * (1 + 0.025 * j * p))
                    acc += cv2.warpAffine(f, Mj, (1920, 1080), borderMode=cv2.BORDER_REFLECT)
                f = (acc / 4).astype(np.uint8)
            elif kind == "glitch":
                g = f.copy(); sh = int(40 * p)
                g[..., 0] = np.roll(f[..., 0], sh, axis=1); g[..., 2] = np.roll(f[..., 2], -sh, axis=1)
                for _ in range(int(10 * p) + 1):
                    y0 = rng.integers(0, 1000); hgt = rng.integers(10, 90)
                    g[y0:y0 + hgt] = np.roll(g[y0:y0 + hgt], int(rng.integers(-160, 160) * p), axis=1)
                f = g
            elif kind == "flash":
                w = p ** 1.4 if p_in else p ** 2 * 0.7
                f = (f.astype(np.float32) * (1 - w) + 255 * w).astype(np.uint8)
        encp.stdin.write(np.ascontiguousarray(f).tobytes())
    dec.stdout.close(); dec.wait(); encp.stdin.close(); encp.wait()

def render_broll(i, b):
    out = os.path.join(R, f"ins_{i:02d}_{b['src']}.mp4")
    if os.path.exists(out): return out
    n = round(b["dur"] * FPS)
    raw = os.path.join(R, f"raw_broll_{i:02d}.mp4")
    if b["kind"] == "stock":
        src = os.path.join(B, b["src"] + ".mp4")
        # gentle push-in on every stock shot so nothing sits static
        fc = (f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,"
              f"fps={FPS},{STOCK_GRADE},tpad=stop_mode=clone:stop_duration=10,"
              f"zoompan=z='1+0.08*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS},"
              f"vignette=angle=PI/6,format=yuv420p,trim=end_frame={n}[o]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(b["opt"]), "-i", src, "-filter_complex", fc,
             "-map", "[o]", "-frames:v", str(n)] + enc(raw))
    else:
        mograph.render(mograph.GRAPHICS[b["src"]], b["dur"], raw)
    os.replace(raw, out)
    return out

def gfx_events():
    ev = []
    for i, (s, text, d, pos) in enumerate(KEYWORDS):
        p = os.path.join(R, f"hud_{i:02d}.mov")
        if not os.path.exists(p): hud.render(text, i + 1, d, pos, p, seed=i)
        ev.append({"start": fr(O(s)), "dur": d, "mov": p, "kind": "kw"})
    for i, (s, name, sub, d) in enumerate(LOWER_THIRDS):
        p = os.path.join(R, f"g_lt_{i:02d}.png"); gfx.lower_third(name, sub, p)
        ev.append({"start": fr(O(s)), "dur": d, "png": p, "kind": "lt"})
    return ev

def card_events():
    ev = []
    for i, (s0, s1, person, photo, stamp, credit) in enumerate(CARDS):
        o0, o1 = fr(O(s0)), fr(O(s1))
        out = os.path.join(R, f"card_{i:02d}.mov")
        if not os.path.exists(out):
            cards.render(dict(person, photo=photo, path=os.path.join(F, photo), dur=o1 - o0,
                              stamp=stamp, credit=credit), out)
        ev.append({"start": o0, "dur": o1 - o0, "file": out, "stamp_t": stamp[2] if stamp else None})
    return ev

def boundaries(bev):
    """Every cut between different sources (A-roll/base <-> insert, insert <-> insert, base items)."""
    eps = 0.5 / FPS
    ins = sorted(bev, key=lambda b: b["start"])
    out = {}
    def src_at(t):
        for b in ins:
            if b["start"] - eps <= t < b["start"] + b["dur"] - eps: return b
        return None
    for b in ins:
        for T in (b["start"], b["start"] + b["dur"]):
            out[round(T * FPS)] = (src_at(T - 1 / FPS), src_at(T + eps))
    for it in timeline:
        if it["type"] in ("title", "interview", "end"):
            for T in (it["out"], it["out"] + it["frames"] / FPS):
                k = round(T * FPS)
                if k not in out and src_at(T) is None and 0 < T < TOTAL - 0.5: out[k] = (None, None)
    return [(k / FPS, a, b) for k, (a, b) in sorted(out.items())]

def _grab(path, offset, length, times):
    """Frames of a source at absolute times, clamped to the source's own range."""
    loc = [min(max(t - offset, 0), length - 1 / FPS) for t in times]
    t0, t1 = min(loc), max(loc)
    n = round((t1 - t0) * FPS) + 2
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", path, "-frames:v", str(n),
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    fr_ = np.frombuffer(r.stdout, np.uint8).reshape(-1, 1080, 1920, 3)
    return [fr_[min(len(fr_) - 1, round((t - t0) * FPS))] for t in loc]

def render_transitions(bev, files):
    fmap = {id(b): f for b, f in zip(bev, files)}
    base = os.path.join(R, "base.mp4")
    ev = []
    for j, (T, A, B) in enumerate(boundaries(bev)):
        kind = TR.KINDS[j % len(TR.KINDS)]
        out = os.path.join(R, f"tr_{j:03d}_{kind}.mp4")
        times = [T + (i - 6) / FPS for i in range(12)]
        if not os.path.exists(out):
            fa = _grab(fmap[id(A)], A["start"], A["dur"], times) if A else _grab(base, 0, TOTAL, [min(t, T - 1 / FPS) for t in times])
            fb = _grab(fmap[id(B)], B["start"], B["dur"], times) if B else _grab(base, 0, TOTAL, [max(t, T) for t in times])
            rng = np.random.default_rng(j)
            encp = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
                                     "-r", str(FPS), "-i", "-"] + enc(out), stdin=subprocess.PIPE)
            for i in range(12):
                encp.stdin.write(np.ascontiguousarray(TR.frame(kind, fa[i], fb[i], (i + 0.5) / 12, rng)).tobytes())
            encp.stdin.close(); encp.wait()
        ev.append({"start": T - 6 / FPS, "dur": 12 / FPS, "file": out, "kind": kind, "cut": T})
    return ev

def stage_compose():
    bev = broll_events()
    with ThreadPoolExecutor(4) as ex:
        files = list(ex.map(lambda ib: render_broll(*ib), enumerate(bev)))
    gev = gfx_events()
    cev = card_events()
    tev = render_transitions(bev, files)
    json.dump({"broll": bev, "gfx": gev, "cards": cev, "trans": tev}, open(os.path.join(R, "events.json"), "w"), indent=1)
    inputs = ["-i", os.path.join(R, "base.mp4")]
    fc, last, k = [], "[0:v]", 1
    # A-roll punch-ins on keywords and emphasis beats (quick ease in, hold, ease out)
    beats = [(g["start"], min(g["dur"], 2.2)) for g in gev if g["kind"] == "kw"]
    beats += [(fr(O(t0)), 1.6) for t0 in PUNCH_EXTRA]
    cuts = [t["cut"] for t in tev]
    beats = [(t0, d) for t0, d in beats if not any(t0 - 0.4 < c < t0 + d + 0.7 for c in cuts)]
    terms = [f"0.075*clip((it-{t0:.3f})/0.12,0,1)*clip(({t0 + d + 0.3:.3f}-it)/0.3,0,1)" for t0, d in beats]
    zexpr = "1+" + "+".join(terms)
    pre = [f"[0:v]setpts=PTS-STARTPTS,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS}"]
    fc.append(",".join(pre) + "[base]"); last = "[base]"
    for b, f in zip(bev, files):
        inputs += ["-i", f]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{b['start']:.4f}/TB[b{k}]")
        fc.append(f"{last}[b{k}]overlay=eof_action=pass:enable='between(t,{b['start']:.4f},{b['start'] + b['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    for tr in tev:
        inputs += ["-i", tr["file"]]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{tr['start']:.4f}/TB[t{k}]")
        fc.append(f"{last}[t{k}]overlay=eof_action=pass:enable='between(t,{tr['start']:.4f},{tr['start'] + tr['dur'] - 0.001:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    for g in gev:
        inputs += ["-i", g["mov"]]
        fc.append(f"[{k}:v]format=rgba,setpts=PTS-STARTPTS+{g['start']:.4f}/TB[g{k}]")
        fc.append(f"{last}[g{k}]overlay=eof_action=pass:format=auto:enable='between(t,{g['start']:.4f},{g['start'] + g['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    for c in cev:
        inputs += ["-i", c["file"]]
        fc.append(f"[{k}:v]format=rgba,setpts=PTS-STARTPTS+{c['start']:.4f}/TB[c{k}]")
        fc.append(f"{last}[c{k}]overlay=eof_action=pass:format=auto:enable='between(t,{c['start']:.4f},{c['start'] + c['dur']:.4f})'[v{k}]")
        last = f"[v{k}]"; k += 1
    fc.append(f"{last}noise=alls=5:allf=t,format=yuv420p[out]")
    script = os.path.join(R, "compose.txt"); open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", script, "-map", "[out]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-movflags", "+faststart", os.path.join(R, "video.mp4")])

# ---------------------------------------------------------------- 5. audio
SR = 48000
def load(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    assert w.getframerate() == SR; return a

def save(p, a):
    a = np.clip(a, -1, 1); w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()

def stage_audio():
    voice, inter = load(os.path.join(S, "work/voice48.wav")), load(os.path.join(S, "work/interview48.wav"))
    total_n = round(TOTAL * SR)
    v_track = np.zeros(total_n, np.float32); i_track = np.zeros(total_n, np.float32)
    fade = int(0.006 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)
    for it in timeline:
        if it["type"] not in ("aroll", "interview"): continue
        n = round(it["frames"] / FPS * SR); o = round(it["out"] * SR)
        srcarr = voice if it["type"] == "aroll" else inter
        s = round(it["src"][0] * SR); seg = srcarr[s:s + n].copy()
        seg[:fade] *= ramp; seg[-fade:] *= ramp[::-1]
        (v_track if it["type"] == "aroll" else i_track)[o:o + len(seg)] += seg
    # mute swear words (user request): silence each word with short fades
    fd = int(0.012 * SR); muted = 0
    for ws, we in SWEARS:
        o0, o1 = O(ws), O(we)
        if o1 <= o0 or o1 - o0 > 2: continue
        a, b = round((o0 - 0.04) * SR), round((o1 + 0.05) * SR)
        lo, hi = max(0, a - fd), min(len(v_track), b + fd)
        env = np.ones(hi - lo, np.float32)
        env[a - lo:b - lo] = 0
        env[:a - lo] = np.linspace(1, 0, a - lo); env[b - lo:] = np.linspace(0, 1, hi - b)
        v_track[lo:hi] *= env; muted += 1
    print("muted", muted, "swear words")
    save(os.path.join(R, "voice_raw.wav"), v_track); save(os.path.join(R, "interview_raw.wav"), i_track)

    title = next(it for it in timeline if it["type"] == "title")
    end = next(it for it in timeline if it["type"] == "end")
    t_title_end = title["out"] + title["frames"] / FPS
    bev = json.load(open(os.path.join(R, "events.json")))
    sfx = []  # (file, time, gain)
    sdir = os.path.join(R, "sfx"); os.makedirs(sdir, exist_ok=True)
    TR_GAIN = {"scan": 0.32, "zoom": 0.38, "grid": 0.30, "glitch": 0.30, "streak": 0.34, "pixel": 0.26}
    for j, tr in enumerate(bev["trans"]):
        fpath = os.path.join(sdir, f"tr_{j:03d}.wav"); sounds.trans_sound(tr["kind"], fpath, 1000 + j)
        sfx.append((fpath, max(0, tr["cut"] - 0.30), TR_GAIN[tr["kind"]]))
    for j, g in enumerate(bev["gfx"]):
        fpath = os.path.join(sdir, f"kw_{j:02d}.wav"); sounds.ui_sound("decode", fpath, 500 + j)
        sfx.append((fpath, g["start"], 0.22))
    sfx += [("hit", title["out"], 0.9), ("whoosh", title["out"] - 0.35, 0.4), ("hit", end["out"], 0.6)]
    for c in bev.get("cards", []):
        sfx += [("whoosh", max(0, c["start"] - 0.15), 0.3), ("pop", c["start"] + 0.32, 0.35),
                ("pop", c["start"] + 0.48, 0.25), ("whoosh", c["start"] + c["dur"] - 0.35, 0.18)]
        if c["stamp_t"] is not None: sfx.append(("hit", c["start"] + c["stamp_t"], 0.7))
    inter_item = next(it for it in timeline if it["type"] == "interview")
    sfx.append(("whoosh", inter_item["out"] - 0.3, 0.3))

    inputs = ["-i", os.path.join(R, "voice_raw.wav"), "-i", os.path.join(R, "interview_raw.wav"),
              "-stream_loop", "-1", "-i", os.path.join(A, "suspense.wav")]
    fc = [
        # voice cleanup: rumble cut, gentle denoise, presence, compression
        "[0:a]highpass=f=80,afftdn=nf=-28,equalizer=f=3500:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-2,"
        "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,aformat=sample_rates=48000:channel_layouts=stereo[vo]",
        "[1:a]highpass=f=100,afftdn=nf=-25,acompressor=threshold=-22dB:ratio=3:makeup=5,volume=1.6,"
        "aformat=sample_rates=48000:channel_layouts=stereo[io]",
        "[vo][io]amix=inputs=2:normalize=0,asplit=3[voice][sc][sc2]",
        # music: louder in cold open/title/end card, low bed elsewhere, ducked under voice
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},"
        f"volume='{MUSIC_GAIN}*if(lt(t,{t_title_end:.2f}),0.30,if(gt(t,{end['out']:.2f}),0.40,0.17))':eval=frame,"
        f"afade=t=out:st={TOTAL - 2.5:.2f}:d=2.5[mus]",
        "[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck]",
    ]
    k = 3; labels = []
    for name, t0, g in sfx:
        inputs += ["-i", name if os.path.isabs(name) else os.path.join(A, name + ".wav")]
        ms = int(t0 * 1000)
        fc.append(f"[{k}:a]volume={g},adelay={ms}|{ms}[s{k}]"); labels.append(f"[s{k}]"); k += 1
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0[sfx]")
    fc.append("[sc2]anullsink")
    fc.append(f"[voice][duck][sfx]amix=inputs=3:normalize=0,atrim=0:{TOTAL:.3f},"
              "loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[out]")
    script = os.path.join(R, "audio.txt"); open(script, "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", script, "-map", "[out]",
         "-c:a", "pcm_s16le", os.path.join(R, "mix.wav")])

def stage_mux():
    out = os.path.join(S, "output", "montverde_edit_v1.mp4"); os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(R, "video.mp4"), "-i", os.path.join(R, "mix.wav"),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
         "-movflags", "+faststart", out])
    print("wrote", out)

if __name__ == "__main__":
    stages = sys.argv[1:] or ["plan", "aroll", "compose", "audio", "mux"]
    for st in stages:
        print("==", st, flush=True); globals()["stage_" + st]()
