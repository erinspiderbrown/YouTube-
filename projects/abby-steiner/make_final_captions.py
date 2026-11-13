"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/abby-steiner/abby_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\b[Hh]oglins\b|\b[Hh]oggins\b|\b[Hh]aggling\b", "Haglund's"), (r"\bIt's printing!", "In sprinting,"), (r"\bstore\b", "story"),
       (r"\bNo meat\b", "No meets"), (r"\bNo pairs\b", "No Paris"), (r"\bSearch me\b", "Surgery"), (r"four ball one", "4x100"),
       (r"\b4x4\b", "4x400"), (r"\b2180\b", "21.80"), (r"\b2177\b", "21.77"), (r"\b21 ?-7\b", "21.77"), (r"\bSpritters\b", "Sprinters"),
       (r"\b2627\b", "26, 27"), (r"\bprom\b", "prime"), (r"\bIt whirls!", "At Worlds,"), (r"soccer star's window", "soccer star too"),
       (r"\bAny college\?", "And in college,"), (r"\bDid August", "Then August"), (r"\bmeeting\b", "meet"), (r"U \.S \.A\.", "USA"),
       (r"U \.S\.", "US"), (r"\badd each\b", "Adaeze"), (r"\bOpheli\b|\bO'Feely\b", "Ofili"), (r"\bSteiner\b", "Steiner"),
       (r"\bhoglands\b|\bHaglands\b", "Haglund's"), (r"\bStedman Clinic\b", "Steadman Clinic"), (r"\bAchilles Tinnitus\b", "Achilles tendinitis")]
words = []
for w in WORDS:
    words.append((FT(w["s"]), FT(w["e"]), w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    segs = json.load(open(f"{CS_}/tx_{src_}.json"))
    for s in segs:
        for w in s["w"]:
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
