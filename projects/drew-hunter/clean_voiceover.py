"""Drew Hunter: clean the user's own read (Dropbox '2220 W Mission Ln 7.m4a', 6:48).
Repeats: first takes removed, the clean restart kept. Long pauses: every silence over MIN_GAP s (between words,
mid-sentence, or inside a stretched word) shortened to 2*KEEP s, cut inside measured silence. No tempo change.
Output vo_clean.wav (-16 LUFS)."""
import json, os, subprocess, sys, numpy as np
P = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{P}/../../tools")
from safe_cuts import rms_db, noise_floor
SR = 48000; HOP = 0.01
S = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/hunter/in"
RAW = f"{S}/raw.m4a"
MIN_GAP, KEEP = 0.75, 0.3
CHAIN = ("highpass=f=75,afftdn=nr=10:nf=-50:tn=1,deesser=i=0.4,"
         "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
         "equalizer=f=180:t=q:w=1.2:g=-1.5,equalizer=f=3500:t=q:w=1.5:g=1.5")
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", RAW, "-af", CHAIN, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).copy()
db = rms_db(x, SR); thr = noise_floor(db) + 12
loud = db > thr
def onset(t0, t1):
    for i in range(int(t0 / HOP), int(t1 / HOP)):
        if loud[i]: return i * HOP
    return t1
def offset(t0, t1):
    last = t0
    for i in range(int(t0 / HOP), int(t1 / HOP)):
        if loud[i]: last = (i + 1) * HOP
    return last
# first takes the user repeated (raw seconds): cut from the end of the line before to the onset of the restart
MIST = [
    (offset(80.0, 80.9) + 0.25, onset(85.5, 86.9) - 0.06),    # "when Allen Webb was a freshman in high school" (1st try)
    (offset(242.9, 243.9) + 0.25, onset(246.6, 247.4) - 0.06), # "He had to pull off the world championships." (1st try, 2nd adds "in 2019")
]
start = onset(3.3, 3.9) - 0.12            # drop the "Mmm." before the first line
end = min(offset(406.0, len(loud) * HOP) + 0.6, len(x) / SR)
# silences: runs of quiet longer than MIN_GAP anywhere
cuts = []; i = int(start / HOP); n = min(int(end / HOP), len(loud))
while i < n:
    if not loud[i]:
        j = i
        while j < n and not loud[j]: j += 1
        if (j - i) * HOP > MIN_GAP:
            a, b = i * HOP + KEEP, j * HOP - KEEP
            if b - a > 0.1: cuts.append((round(a, 3), round(b, 3)))
        i = j
    else: i += 1
cuts = sorted([c for c in cuts if all(c[1] <= a or c[0] >= b for a, b in MIST)] + MIST)
segs = []; s0 = start
for c0, c1 in cuts:
    if c0 > s0: segs.append((s0, c0))
    s0 = max(s0, c1)
segs.append((s0, end))
y = []
for u, v in segs:
    seg = x[int(u * SR):int(v * SR)].copy(); k = int(0.012 * SR)
    if len(seg) > 2 * k: seg[:k] *= np.linspace(0, 1, k); seg[-k:] *= np.linspace(1, 0, k)
    y.append(seg)
y = np.concatenate(y)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=9,alimiter=limit=0.89", "-ar", str(SR), "-c:a", "pcm_s16le", f"{P}/vo_clean.wav"],
               input=y.tobytes(), check=True)
json.dump({"mist": MIST, "cuts": cuts, "start": start, "end": end, "segs": segs}, open(f"{P}/vo_cuts.json", "w"))
print("mist", [(round(a, 2), round(b, 2)) for a, b in MIST], "cuts", len(cuts), "raw", round(len(x) / SR, 1), "->", round(len(y) / SR, 1), "s")
