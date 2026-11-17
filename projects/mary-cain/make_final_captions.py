"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/mary-cain/mary_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bMary (Kane|Kay|Key)\b", "Mary Cain"), (r"\bKane\b", "Cain"), (r"\bAtlanta NYC\b", "Atalanta NYC"), (r"\bMofera\b|\bMo Fara\b", "Mo Farah"),
       (r"\breds\b|\bReds\b|\bR\.E\.D\.S\b", "RED-S"), (r"\bSafe Support\b|\bSafe Sport\b", "SafeSport"), (r"\bAlberta\b", "Alberto"),
       (r"\b417\b", "4:17"), (r"\b404 -62\b|\b404-62\b", "4:04.62"), (r"\b159 \.51\b", "1:59.51"), (r"\bUSA's\b", "USAs"),
       (r"\bsports like that\b", "sports psychologist"), (r"\bdeferser\b", "get first"), (r"\bMr\. Caldwell\b", "Mary Cain"),
       (r"\bweighted\b", "weighed"), (r"\bOregon projects\b", "Oregon Project")]
words = []
for w in WORDS:
    words.append((FT(w["s"]), FT(w["e"]), w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    segs = json.load(open(f"{CS_}/tx_{src_}.json"))
    for s in segs:
        for w in s.get("words", s.get("w", [])):
            if ss - 0.05 <= w["s"] and w["e"] <= ss + dur + 0.05:
                words.append((t0 + w["s"] - ss, t0 + w["e"] - ss, w["w"], src_ + str(round(t0))))
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
    for a_, b_ in FIX: t = re.sub(a_, b_, t, flags=0)
    end = min(c[-1][1] + 0.3, cues[k + 1][0][0] - 0.02) if k + 1 < len(cues) else c[-1][1] + 0.5
    out.append(f"{k + 1}\n{ts(c[0][0])} --> {ts(end)}\n{t}\n")
open(f"{P}/captions_en.srt", "w").write("\n".join(out)); print(len(out), "cues")
