"""Rebuild a time-stretched voiceover from its natural-speed raw takes, keeping the same timeline.

Why: heavy rubberband slow-downs (0.78-0.92) made the cloned voice sound phasey/robotic.
How: split the raw takes into phrases at natural pauses, align their words to the word timestamps
of the voiceover the edit was cut to, and drop each phrase onto its original start time. Phrases get
only a mild WSOLA slow-down (atempo, default 0.95, never slower), so the extra time becomes pause
instead of stretched syllables. Every phrase still starts where the picture expects it.

Usage: python3 tools/rephrase_voiceover.py raw_words.json timeline_words.json OUT.wav [--tempo 0.95] [--total SECONDS]
  raw_words.json: [{"file": raw.mp3, "dur": s, "words": [{w,s,e}...]}, ...] (faster-whisper on each raw take)
  timeline_words.json: [{"words": [{w,s,e}...]}, ...] (faster-whisper on the voiceover the edit was cut to)
"""
import argparse, difflib, json, re, subprocess, tempfile, os
import numpy as np

SR = 48000

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)

def atempo(x, tempo):
    if abs(tempo - 1) < 1e-3: return x
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.4f}",
                        "-f", "f32le", "-"], input=x.tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw"); ap.add_argument("timeline"); ap.add_argument("out")
    ap.add_argument("--tempo", type=float, default=0.95)
    ap.add_argument("--gap", type=float, default=0.2, help="pause (s) that splits phrases")
    ap.add_argument("--total", type=float, default=0)
    a = ap.parse_args()
    raw = json.load(open(a.raw)); tl = json.load(open(a.timeline))
    tlw = [x for seg in tl for x in seg["words"]]
    rw = [dict(sec=si, k=k, **x) for si, sec in enumerate(raw) for k, x in enumerate(sec["words"])]
    sm = difflib.SequenceMatcher(None, [norm(x["w"]) for x in rw], [norm(x["w"]) for x in tlw], autojunk=False)
    m = {}
    for i, j, n in sm.get_matching_blocks():
        for d in range(n): m[i + d] = j + d
    print(f"matched {len(m)}/{len(rw)} raw words to {len(tlw)} timeline words")
    # phrases
    chunks = []
    for si, sec in enumerate(raw):
        idx = [i for i, x in enumerate(rw) if x["sec"] == si]
        cur = [idx[0]]
        for p, q in zip(idx, idx[1:]):
            if rw[q]["s"] - rw[p]["e"] >= a.gap: chunks.append(cur); cur = [q]
            else: cur.append(q)
        chunks.append(cur)
    audio = {si: load(sec["file"]) for si, sec in enumerate(raw)}
    plan = []
    for c in chunks:
        anchors = [i for i in c if i in m]
        si = rw[c[0]]["sec"]; words = raw[si]["words"]; k0, k1 = rw[c[0]]["k"], rw[c[-1]]["k"]
        tlw_override = None
        if not anchors:  # e.g. whisper heard it differently in the two takes: interpolate from neighbours
            secm = sorted(i for i in m if rw[i]["sec"] == si)
            before = [i for i in secm if i < c[0]]; after = [i for i in secm if i > c[-1]]
            if not after: print("unanchored phrase skipped:", " ".join(rw[i]["w"] for i in c)); continue
            f2 = min(after); ra, ta = rw[f2]["s"], tlw[m[f2]]["s"]
            if before:
                b = max(before); rb, tb = rw[b]["s"], tlw[m[b]]["s"]
                tlw_override = tb + (rw[c[0]]["s"] - rb) * (ta - tb) / max(1e-3, ra - rb)
            else:  # first phrase of a section: use the section's overall stretch ratio
                ratio = (tlw[m[secm[-1]]]["s"] - tlw[m[secm[0]]]["s"]) / max(1e-3, rw[secm[-1]]["s"] - rw[secm[0]]["s"])
                tlw_override = ta - (ra - rw[c[0]]["s"]) * ratio
            anchors = [c[0]]
        prev_e = words[k0 - 1]["e"] if k0 > 0 else 0.0
        next_s = words[k1 + 1]["s"] if k1 + 1 < len(words) else raw[si]["dur"]
        cs = max(words[k0]["s"] - 0.10, (prev_e + words[k0]["s"]) / 2, 0)
        ce = min(words[k1]["e"] + 0.22, (words[k1]["e"] + next_s) / 2 if k1 + 1 < len(words) else raw[si]["dur"])
        am = anchors[0]
        t_anchor = tlw_override if tlw_override is not None else tlw[m[am]]["s"]
        plan.append(dict(si=si, cs=cs, ce=ce, r_anchor=rw[am]["s"], t_anchor=t_anchor, text=" ".join(rw[i]["w"].strip() for i in c)))
    plan.sort(key=lambda p: p["t_anchor"])
    total = a.total or (max(p["t_anchor"] for p in plan) + 15)
    buf = np.zeros(int(total * SR) + SR, np.float32)
    fast = 0; tight = 0
    for n, p in enumerate(plan):
        nxt = plan[n + 1] if n + 1 < len(plan) else None
        seg = audio[p["si"]][int(p["cs"] * SR):int(p["ce"] * SR)].copy()
        tempo = a.tempo
        start = p["t_anchor"] - (p["r_anchor"] - p["cs"]) / tempo
        nstart = None
        if nxt:
            nstart = nxt["t_anchor"] - (nxt["r_anchor"] - nxt["cs"]) / a.tempo
            room = nstart - start
            need = len(seg) / SR / tempo
            if need > room:
                tempo = min(1.0, len(seg) / SR / max(room, 0.05)); fast += 1
                start = p["t_anchor"] - (p["r_anchor"] - p["cs"]) / tempo
                over = len(seg) / SR / tempo - (nstart - start)
                if over > 0.01: tight += 1; print(f"  overlap {over:.2f}s at {start:.1f}s: {p['text'][:60]}")
        y = atempo(seg, tempo)
        if nxt:  # never run into the next phrase: trim the (silent) tail instead
            lim = int((nstart - start) * SR)
            if 0 < lim < len(y): y = y[:lim]
        f = int(0.012 * SR)
        if len(y) > 2 * f:
            y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        i0 = max(0, int(start * SR)); buf[i0:i0 + len(y)] += y[:len(buf) - i0]
    print(f"{len(plan)} phrases placed; {fast} sped up toward 1.0 to fit; {tight} still overlap slightly")
    buf = buf[:int(total * SR)]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", a.out],
                   input=np.clip(buf, -1, 1).tobytes(), check=True)

if __name__ == "__main__":
    main()
