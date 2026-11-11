"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/candace-hill/candace_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bAsics\b|\bA6\b|\ba6\b|\b86\b(?=\??$)", "ASICS"), (r"\bHeal\b|\bheel\b", "Hill"), (r"\bRoxdale\b", "Rockdale"),
       (r"\bSlick\b|\bSlitt\b|\bLipp\b", "Split"), (r"\bMiles Split\b", "MileSplit"), (r"\bShavers\b", "Shaver"), (r"\bAliyah\b", "Aleia"),
       (r"\bCandice\b", "Candace"), (r"\bAaron\b", "Erin"), (r"\bWhen dated\b", "Wind-aided"), (r"\bthe win\b", "the wind"),
       (r"\b10 ?\.98\b|\b1098\b|\b10-9\b|\b10\.9\b(?! ?8)", "10.98"), (r"\b1107\b", "11.07"), (r"\b2243\b", "22.43"), (r"\b10 ?\.99\b", "10.99"),
       (r"\b2 ?\.5\b", "2.5"), (r"\b2 ?\.0\b", "2.0"), (r"\bfor Ness\b", "finesse"), (r"\bcandidates Hill\b", "Candace Hill"),
       (r"\bThe Candace Hill finesse\b", "Did Candace Hill finesse"), (r"\b100th\b", "100"), (r"\bColumbia\b", "Colombia"), (r"\bFinesse 86\b", "finesse ASICS"), (r"\bfor Boda\b|\bSo a Boda\b|\bSwoboda\b", "Swoboda"), (r"\bHill Star\b", "Hill's star"), (r"\bwhat call\b", "what you call"),
       (r"\bThere is calling\b", "They was calling"), (r"\bWorld Athletics\b|\bworld athletics\b", "World Athletics"), (r"\bUSAs\b", "USAs")]
words = []
for w in WORDS:
    words.append((FT(w["s"]), FT(w["e"]), w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    segs = json.load(open(f"{CS_}/tx/{src_}.json"))
    for s in segs:
        for w in s["w"]:
            if ss - 0.05 <= w["s"] and w["e"] <= ss + dur + 0.05:
                words.append((t0 + w["s"] - ss, t0 + w["e"] - ss, w["w"], src_ + str(round(t0))))
pre_ss = PRE_SB[1] - PAD; sbw(PRE_SB[0], pre_ss, PRE, 0.0)
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
    for a_, b_ in FIX: t = re.sub(a_, b_, t, flags=re.I if "Boda" in a_ else 0)
    end = min(c[-1][1] + 0.3, cues[k + 1][0][0] - 0.02) if k + 1 < len(cues) else c[-1][1] + 0.5
    out.append(f"{k + 1}\n{ts(c[0][0])} --> {ts(end)}\n{t}\n")
open(f"{P}/captions_en.srt", "w").write("\n".join(out)); print(len(out), "cues")
