"""Michael Norman: clean the user's own read (Dropbox "Shell.m4a", 8:24).
Repeats: first takes removed, the clean restart kept. Long pauses: every silence over MIN_GAP s (between words,
mid-sentence, or inside a stretched word) shortened to 2*KEEP s, cut inside measured silence. No tempo change.
Output vo_clean.wav (-16 LUFS)."""
import json, os, subprocess, sys, numpy as np
P = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{P}/../../tools")
from safe_cuts import rms_db, noise_floor
SR = 48000; HOP = 0.01
S = "/tmp/claude-0/-home-user/9c604270-316e-5b2c-b8cd-3de373b077b3/scratchpad/norman/in"
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
def quiet(t, w=0.15):
    """Quietest 40 ms frame within +-w of t (cut point between two words that have no real gap)."""
    i0, i1 = int((t - w) / HOP), int((t + w) / HOP)
    seg = np.convolve(db[i0:i1], np.ones(4) / 4, mode="valid"); return round((i0 + int(np.argmin(seg)) + 2) * HOP, 3)
def after_gap(t0, t1, gap=0.15):
    """Onset of speech after the first run of >= gap s of quiet in [t0, t1]."""
    i, n, q = int(t0 / HOP), int(t1 / HOP), 0
    while i < n:
        q = q + 1 if not loud[i] else 0
        if q * HOP >= gap: break
        i += 1
    return onset(i * HOP, t1)
# first takes / misreads (raw seconds). Each cut runs from a measured quiet point to the onset of the kept words.
MIST = [
    (quiet(68.06), after_gap(73.0, 75.0) - 0.06),   # "and he ran seven races in like 20" (restarted: "...like seven races in 28 hours")
    (quiet(256.18), quiet(257.10)),                  # "eight tenths or" -> "only two tenths behind him"
    (quiet(269.02), onset(271.6, 272.5) - 0.06),     # "and he still barely got the job." (restarted with "...job done")
    (quiet(326.54, 0.08), quiet(326.86, 0.1)),       # "ass" (ad-friendly) -> "caught up with his."
    (quiet(429.94), quiet(430.68)),                  # "40 or" -> "a 400 meter runner"
    (quiet(450.22, 0.06), quiet(452.30)),            # "a way more or" -> "been in way better position"
]
start = onset(1.4, 2.0) - 0.12
end = min(offset(500.0, len(loud) * HOP) + 0.6, len(x) / SR)
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
