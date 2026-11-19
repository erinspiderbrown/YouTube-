"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/athing-mu/athing_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\b(E?A? ?[Tt]hing ?[Mm]o|Athene M[oo]e?|Athene Mo|a thing mo|Thingmo|A Thingmo)\b", "Athing Mu"), (r"\bMoe goes\b|\bMo goes\b", "Mu goes"),
       (r"\bRaven Rogers\b", "Raevyn Rogers"), (r"\bKe[e]?ley Hodg(e)?son\b|\bKeely Hodgeson\b|\bKeeley\b", "Keely Hodgkinson"),
       (r"\bBobby Kersey\b", "Bobby Kersee"), (r"\bEugene,? Orton\b", "Eugene, Oregon"), (r"\b123 ?\.57\b", "1:23.57"),
       (r"\b49 ?-57\b", "49.57"), (r"\b156 ?-07\b", "1:56.07"), (r"\b155 ?(point|\.) ?21\b", "1:55.21"), (r"\b154 ?\.97\b", "1:54.97"),
       (r"\b2 ?-19 ?-69\b", "2:19.69"), (r"\b203 ?\.44\b", "2:03.44"), (r"\b159 ?\.79\b", "1:59.79"), (r"\bno racist\b", "no races"),
       (r"\bfalls a protest\b", "files a protest"), (r"\bpre ?-fontaine\b", "Prefontaine"), (r"\bchill call\b", "chill pill"), (r"\b1 ?-800\b", "one 800")]
words = []
for w in WORDS:
    words.append((FT(w["s"]), FT(w["e"]), w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    try: segs = json.load(open(f"{CS_}/tx/{src_}.json"))
    except FileNotFoundError: return
    for s in segs:
        for w in s.get("words", s.get("w", [])):
            if isinstance(w, list): w = {"w": w[0], "s": w[1], "e": w[2]}
            if ss - 0.05 <= w["s"] and w["e"] <= ss + dur + 0.05:
                words.append((t0 + w["s"] - ss, t0 + w["e"] - ss, w["w"].strip(), src_ + str(round(t0))))
pre_ss = PRE_SB[1] - PAD; sbw(PRE_SB[0], pre_ss, PRE - 0.6, 0.0)
for s in SOUNDBITES: sbw(s["src"], s["ss"] - PAD, s["dur"] + 2 * PAD, SB_START(s))
words.sort()
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
open(f"{P}/captions_en.srt", "w").write("\n".join(out)); print(len(out), "cues")
