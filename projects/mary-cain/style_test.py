"""Mary Cain: ~40 s style test of the new modern look (user, 17 Nov 2026), built from real footage only.
Clean grade (no grain), slow push-ins, speed ramp, xfade transitions, modern.py graphics, a dark bed ducked under
her real voice (NYT Opinion 2019). No voiceover yet: the user records theirs from the teleprompter.
Run: python3 projects/mary-cain/style_test.py"""
import os, sys, subprocess, json
ROOT = "/home/user/YouTube-"; sys.path.insert(0, f"{ROOT}/tools")
import modern as M
SCR = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/mary"; C = f"{SCR}/clips"; R = f"{SCR}/test"
os.makedirs(R, exist_ok=True)
W, H, FPS = 1920, 1080, 24
GRADE = "eq=contrast=1.06:saturation=1.07:gamma=0.99,unsharp=5:5:0.6"

# (video src, video ss, dur, audio src or None, audio ss, opts)
SEGS = [
    dict(v="m_nyt", ss=61.0, d=3.6, push=0.05, crop=1.06, gfx=("date", "November 7, 2019", "New York Times Opinion")),
    dict(v="m_nyt", ss=254.0, d=2.9, a="m_nyt", ass=4.35, crop=1.06, src="New York Times Opinion · 2019"),
    dict(v="m_millrose2013", ss=160.0, d=5.2, slow=0.55, gfx=("name", "Mary Cain", "Age 16 · Millrose Games 2013"), src="Fan video · John Kuehn"),
    dict(v="m_nyt", ss=184.0, d=3.4, slow=0.7, crop=1.06, gfx=("number", "4:04.62", "American junior record", "1500m · May 2013")),
    dict(v="m_salazar2013", ss=2.0, d=4.0, a="m_nyt", ass=19.15, gfx=("name", "Alberto Salazar", "Head coach · Nike Oregon Project"), src="LetsRun · 2013"),
    dict(v="m_nyt", ss=96.0, d=4.9, a="m_nyt", ass=23.15, crop=1.06),
    dict(v="m_millrose2013", ss=101.0, d=2.8, push=0.06, slow=0.6, gfx=("chapter", "02", "The Deal"), xin="zoomin"),
    dict(v="m_nyt", ss=271.0, d=6.6, a="m_nyt", ass=101.4, crop=1.06, push=0.05),
    dict(v="m_nyt", ss=359.0, d=8.4, a="m_nyt", ass=108.0, crop=1.06, gfx=("number", "114", "Pounds", "The number Salazar set for her"), gfx_at=0.2, gfx_d=3.6),
    dict(v="m_nyt", ss=61.0, d=4.6, push=0.04, crop=1.06, gfx=("quote", "They wanted me thinner, and thinner, and thinner.", "Mary Cain, 2019")),
]
XF = 0.5   # crossfade length


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:800]); print(r.stderr[-1500:]); raise SystemExit(1)


def seg(i, s):
    out = f"{R}/s{i:02d}.mp4"; d = s["d"] + XF; slow = s.get("slow", 1.0); crop = s.get("crop", 1.0); push = s.get("push", 0.03)
    z = f"{crop}*(1+{push}*t/{d:.3f})"
    dl = "delogo=x=36:y=46:w=286:h=72," if s["v"] == "m_nyt" else ""   # NYT Opinion corner logo
    vf = (f"[0:v]setpts={1/slow:.4f}*(PTS-STARTPTS),{dl}scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,"
          f"scale='trunc(1920*{z}/2)*2':-2:eval=frame:flags=lanczos,crop=1920:1080,setsar=1,{GRADE},fps={FPS},format=yuva420p[b0]")
    ins = ["-ss", f"{s['ss']}", "-t", f"{d * slow + 0.3}", "-i", f"{C}/{s['v']}.mp4"]; k = 0; fl = [vf]
    if s.get("gfx"):
        gd = s.get("gfx_d", d - 0.2); mov = f"{R}/g{i:02d}.mov"; M.render(s["gfx"], gd, mov); k += 1
        ins += ["-i", mov]; ga = s.get("gfx_at", 0.1)
        fl.append(f"[{k}:v]setpts=PTS-STARTPTS+{ga}/TB,format=rgba[o{k}];[b{k-1}][o{k}]overlay=0:0:eof_action=pass[b{k}]")
    if s.get("src"):
        mov = f"{R}/c{i:02d}.mov"; M.render(("source", s["src"]), min(3.5, d), mov); k += 1
        ins += ["-i", mov]; fl.append(f"[{k}:v]setpts=PTS-STARTPTS,format=rgba[o{k}];[b{k-1}][o{k}]overlay=0:0:eof_action=pass[b{k}]")
    fl.append(f"[b{k}]format=yuv420p[v]")
    if s.get("a"):
        ins += ["-ss", f"{s['ass']}", "-t", f"{d}", "-i", f"{C}/{s['a']}.mp4"]; k += 1
        fl.append(f"[{k}:a]aresample=48000,loudnorm=I=-17:TP=-2:LRA=11,afade=t=in:d=0.08,apad=whole_dur={d:.3f}[a]")
    else:
        ins += ["-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=48000:cl=stereo"]; k += 1; fl.append(f"[{k}:a]anull[a]")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[v]", "-map", "[a]", "-t", f"{d:.3f}", "-r", str(FPS),
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-ar", "48000", "-ac", "2", out])
    return out


files = [seg(i, s) for i, s in enumerate(SEGS)]
# chain with xfade (video) + acrossfade (audio)
ins = sum((["-i", f] for f in files), []); fl = []; off = 0.0; vl, al = "[0:v]", "[0:a]"
for i in range(1, len(files)):
    off += SEGS[i - 1]["d"]; tr = SEGS[i].get("xin", "fade")
    fl.append(f"{vl}[{i}:v]xfade=transition={tr}:duration={XF}:offset={off - XF * (i - 1) if False else off:.3f}[v{i}]")
    fl.append(f"{al}[{i}:a]acrossfade=d={XF}[a{i}]"); vl, al = f"[v{i}]", f"[a{i}]"
    off -= XF * 0  # offsets are on the growing output timeline
# xfade offsets: each new segment starts XF before the end of the accumulated output
fl = []; vl, al = "[0:v]", "[0:a]"; acc = SEGS[0]["d"] + XF
for i in range(1, len(files)):
    tr = SEGS[i].get("xin", "fade"); offs = acc - XF
    fl.append(f"{vl}[{i}:v]xfade=transition={tr}:duration={XF}:offset={offs:.3f}[v{i}]")
    fl.append(f"{al}[{i}:a]acrossfade=d={XF}[a{i}]"); vl, al = f"[v{i}]", f"[a{i}]"
    acc = offs + SEGS[i]["d"] + XF
total = acc
bed = f"{ROOT}/projects/jon-drummond/music/M1_cold-open-background.mp3"
hits = [(0.15, "zoom"), (sum(s["d"] for s in SEGS[:6]) + 0.1, "zoom"), (sum(s["d"] for s in SEGS[:8]) + 0.3, "scan")]
import sounds
hp = []
for j, (t, kind) in enumerate(hits):
    p = f"{R}/hit{j}.wav"
    if not os.path.exists(p): sounds.trans_sound(kind, p, 50 + j * 7)
    hp.append((t, p))
ins += ["-stream_loop", "-1", "-i", bed] + sum((["-i", p] for _, p in hp), [])
nb = len(files)
fl.append(f"[{nb}:a]atrim=0:{total:.2f},volume=0.55,afade=t=in:d=1.5,afade=t=out:st={total - 2.5:.2f}:d=2.5[bed]")
fl.append(f"{al}asplit=2[vo][key]")
fl.append("[bed][key]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=500[duck]")
mix = "[vo][duck]"
for j, (t, _) in enumerate(hp):
    fl.append(f"[{nb + 1 + j}:a]volume=0.35,adelay={int(t * 1000)}|{int(t * 1000)}[h{j}]"); mix += f"[h{j}]"
fl.append(f"{mix}amix=inputs={2 + len(hp)}:normalize=0:duration=first,alimiter=limit=0.95[aout]")
out = f"{SCR}/Mary_Cain_style_test.mp4"
run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", vl, "-map", "[aout]", "-c:v", "libx264", "-preset", "medium",
     "-crf", "17", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
print("wrote", out, round(total, 1))
