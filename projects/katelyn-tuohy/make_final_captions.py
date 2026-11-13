"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/katelyn-tuohy/tuohy_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\b[KC]a[iy]?t?lyn T[ou]{1,2}e?h?e?y\b|\bCaitlin T\w+\b|\bKaitlyn T\w+\b|\bCaitlin Tui\b|\bTui\b|\bTooey\b|\bChuey\b", "Katelyn Tuohy"),
       (r"\b[KC]aitlyn\b|\bCaitlin\b|\bKaylin\b", "Katelyn"), (r"\bToohey\b|\bTuey\b|\bTooey\b", "Tuohy"),
       (r"\bLori Hens\b|\bco-?tennis\b|\bCoach Henness\b|\bHennis\b|\bHenness\b", "Coach Henes"), (r"\bNo pairs\b", "No Paris"),
       (r"\b1537\b", "15:37"), (r"\b4 ?\.33 ?\.87\b", "4:33.87"), (r"\b4 ?[.-]24\b", "4:24"), (r"\b425\b", "4:25"), (r"\b15-53\b", "15:53"),
       (r"\brolled 5K\b|\bRoll 5K\b", "road 5K"), (r"\bwinner went\b", "winter went"), (r"\btheme that\b", "thing that"),
       (r"\bran to 5k\b", "ran the 5K"), (r"\bimma\b", "I'ma"), (r"\bIndia\b", "Indy"), (r"\bCampbell City\b", "Camel City"),
       (r"\bNew York road runners\b", "New York Road Runners"), (r"\bAdidas\b", "adidas"), (r"\bU \.S\.\b", "US"), (r"\bMC State\b", "NC State"), (r"\bCoach Coach\b", "Coach"), (r"\bValve\b|\bVolby\b|\bVal by\b", "Valby")]
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
