"""Cut points for voiceover cleanup that never clip a word.

Whisper's word END times run early on long words and numbers ("2024" ends
after "twenty twenty"), so cutting at whisper_end + pad chopped the "four".
These helpers place every cut inside measured silence instead.

    from safe_cuts import pause_cuts, safe_point
    cuts = pause_cuts(x, sr, words, min_gap=1.0, keep=0.35)

x: mono float32 audio, words: [{"s":..,"e":..}] from whisper.
"""
import numpy as np

HOP = 0.01


def rms_db(x, sr, hop=HOP, win=0.03):
    h, w = int(hop * sr), int(win * sr)
    n = max(1, (len(x) - w) // h + 1)
    out = np.empty(n)
    for i in range(n):
        seg = x[i * h:i * h + w]
        out[i] = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    return out


def noise_floor(db):
    return float(np.percentile(db, 10))


def speech_end(db, t0, t1, thr, hold=0.12):
    """Last time in [t0,t1] where speech energy is above thr, then held silence."""
    i0, i1 = int(t0 / HOP), min(len(db), int(t1 / HOP))
    last = t0
    for i in range(i0, i1):
        if db[i] > thr:
            last = (i + 1) * HOP
    return last


def speech_start(db, t0, t1, thr):
    i0, i1 = int(t0 / HOP), min(len(db), int(t1 / HOP))
    for i in range(i0, i1):
        if db[i] > thr:
            return i * HOP
    return t1


def pause_cuts(x, sr, words, min_gap=1.0, keep=0.35, margin=12.0):
    """Shorten long pauses. Each cut lies inside real silence, with `keep`
    seconds of silence left after the last sound and before the next one."""
    db = rms_db(x, sr)
    thr = noise_floor(db) + margin
    cuts = []
    for p, q in zip(words, words[1:]):
        if q["s"] - p["e"] <= min_gap:
            continue
        # look for the true end of p from its whisper end up to the next word
        end = _true_end(db, p["e"], q["s"], thr)
        start = speech_start(db, end, q["s"] + 0.2, thr)
        a, b = end + keep, start - keep
        if b - a > 0.15:
            cuts.append((round(a, 3), round(b, 3)))
    return cuts


def _true_end(db, e, nxt, thr, hold=0.15):
    """From whisper end e, walk forward while sound continues; stop at the
    first run of `hold` seconds below thr."""
    i, n = int(e / HOP), min(len(db), int(nxt / HOP))
    quiet = 0
    last = e
    while i < n:
        if db[i] > thr:
            last = (i + 1) * HOP
            quiet = 0
        else:
            quiet += 1
            if quiet * HOP >= hold:
                break
        i += 1
    return last


def safe_point(x, sr, t, search=0.4, margin=12.0):
    """Move a cut time t to the quietest spot within +-search seconds."""
    db = rms_db(x, sr)
    i0, i1 = max(0, int((t - search) / HOP)), min(len(db), int((t + search) / HOP))
    j = i0 + int(np.argmin(db[i0:i1]))
    return j * HOP


def check_numbers(script_text, transcript_words):
    """Every number in the script must appear in the cleaned VO's transcript.
    Returns numbers that are missing or changed (e.g. 2024 heard as 2020)."""
    import re
    want = re.findall(r"\d[\d.,x]*", script_text)
    got = " ".join(w["w"] if isinstance(w, dict) else str(w) for w in transcript_words)
    got_nums = re.findall(r"\d[\d.,x]*", got)
    missing = []
    pool = list(got_nums)
    for n in want:
        n0 = n.rstrip(".,")
        hit = next((g for g in pool if g.rstrip(".,") == n0), None)
        if hit:
            pool.remove(hit)
        else:
            missing.append(n0)
    return missing
