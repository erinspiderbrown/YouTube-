"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/young-twins/twins_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bNewberry\b", "Newbury"), (r"\bBrosnan\b|\bBrosnin\b|\bBrosman\b", "Brosnan"), (r"\b(Solman|Salman|Saltman)\b", "Sahlman"),
       (r"\bAlex Young\b", "Lex Young"), (r"\bNiko'?s?\b", "Nico"), (r"\bNikos\b", "Nicos"), (r"\bRunning Lane\b", "RunningLane"),
       (r"\bnc double a\b", "NCAA"), (r"\bI'm gonna\b", "I'ma"), (r"\bass\b", "a**"), (r"\bbut\.\.\.$", ""),
       (r"\bthe 1338\b", "the 13:38"), (r"\b1338\b", "13:38"), (r"\b1405\b", "14:05"), (r"\b1334 ?\.96\b", "13:34.96"), (r"\b1335 ?\.52\b", "13:35.52"),
       (r"\b1325 ?\.86\b", "13:25.86"), (r"\b339\b", "3:39"), (r"\b356\b", "3:56"), (r"\b335 ?\.96\b", "3:35.96"), (r"\b2748\b", "27:48"),
       (r"\b0 ?\.26\b", "0.26"), (r"\b5 ?,000\b", "5,000"), (r"\b100 ?,000\b", "100,000"), (r"\bPac ?-12\b", "Pac-12"), (r"\bAll ?-American", "All-American"),
       (r"\bsemi ?-final\b", "semifinal"), (r"\by 'all\b", "y'all")]
words = []
for w in WORDS:
    words.append((FT(w["s"]), FT(w["e"]), w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    try: segs = json.load(open(f"{CS_}/tx/{src_}.json"))
    except FileNotFoundError: return
    if isinstance(segs, dict): segs = segs.get("segments", [])
    for s in segs:
        for w in s.get("words", s.get("w", [])):
            if isinstance(w, list): w = {"w": w[0], "s": w[1], "e": w[2]}
            if ss - 0.05 <= w["s"] and w["e"] <= ss + dur + 0.05:
                words.append((t0 + w["s"] - ss, t0 + w["e"] - ss, w["w"].strip(), src_ + str(round(t0))))
pre_ss = PRE_SB[1] - PAD; sbw(PRE_SB[0], pre_ss, PRE - 0.6, 0.0)
for s in SOUNDBITES: sbw(s["src"], s["ss"] - PAD, s["dur"] + 2 * PAD, SB_START(s))
words.sort()
import re as _re
_m = []
for a_, b_, w_, sr_ in words:
    w_ = w_.replace('"', '')
    if _m and _re.match(r"^[-'.]\d", w_) and _re.search(r"\d$", _m[-1][2]) and _m[-1][3] == sr_:
        pa, pb, pw, ps = _m[-1]; _m[-1] = (pa, b_, pw + "." + w_[1:], ps)
    else: _m.append((a_, b_, w_, sr_))
words = _m
cues, cur = [], []
for i, (a, b, w, sr) in enumerate(words):
    if cur and (sr != cur[-1][3] or len(" ".join(x[2] for x in cur)) + len(w) > 40 or a - cur[-1][1] > 0.7 or b - cur[0][0] > 4.5):
        cues.append(cur); cur = []
    cur.append((a, b, w, sr))
    if w.endswith((".", "?", "!")) and len(" ".join(x[2] for x in cur)) > 18: cues.append(cur); cur = []
if cur: cues.append(cur)
def ts(x):
    ms = int(round(max(0, x) * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
out = []
for k, c in enumerate(cues):
    t = " ".join(x[2] for x in c).replace(" -", "-").replace(" '", "'").replace(" .", ".")
    for a_, b_ in FIX: t = re.sub(a_, b_, t, flags=re.I)
    end = min(c[-1][1] + 0.3, cues[k + 1][0][0] - 0.02) if k + 1 < len(cues) else c[-1][1] + 0.5
    out.append(f"{k + 1}\n{ts(c[0][0])} --> {ts(end)}\n{t}\n")
open("/home/user/YouTube-/projects/young-twins/captions.srt", "w").write("\n".join(out)); print(len(out), "cues")
