"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/shelby-houlihan/shelby_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bHolohan\b|\bHoulahan\b|\bHoolihan\b", "Houlihan"), (r"\bSchumaker\b|\bShoemaker\b", "Schumacher"),
       (r"\bnandrolon\b|\bnandoline\b|\bnandrolin\b", "nandrolone"), (r"\bGabriella DeBue Stafford\b|\bDeBue Stafford\b|\bDebues Stafford\b", "DeBues-Stafford"),
       (r"\bGabriella\b", "Gabriela"), (r"\bBeverton\b", "Beaverton"), (r"\bBowman\b", "Bowerman"), (r"\bPolycraft\b", "polygraph"),
       (r"\bWhat I agreed\b", "WADA agreed"), (r"\bAIU in WADA\b", "AIU and WADA"), (r"\bcourt of arbitration for sport\b", "Court of Arbitration for Sport"),
       (r"\bmeddled\b", "medaled"), (r"\bvillain arrow\b", "villain era"), (r"\bnc double a\b", "NCAA"), (r"\bI'm gonna\b", "I'ma"), (r"\bass\b", "a**"),
       (r"\b354 ?\.99\b", "3:54.99"), (r"\b1423 ?\.92\b", "14:23.92"), (r"\b8 ?\.31 ?\.56\b", "8:31.56"), (r"\b30 ?\.50\b", "30:50"),
       (r"\b10 ?,000\b", "10,000"), (r"\by 'all\b", "y'all"), (r"\bUSA's\b", "USAs")]
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
open("/home/user/YouTube-/projects/shelby-houlihan/captions.srt", "w").write("\n".join(out)); print(len(out), "cues")
