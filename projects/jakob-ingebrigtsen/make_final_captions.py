"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/jakob-ingebrigtsen/jakob_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bIngeb[a-z]*s[eo]n\b|\bIngenreichsen\b|\bIncombrison\b|\bIngebretsen\b", "Ingebrigtsen"),
       (r"\bJacob\b|\bYacob\b|\bYaakob\b|\bYaakov\b|\bJakub\b|\bJaco\b", "Jakob"), (r"\bHerrick\b|\bHerek\b|\bHenneke\b", "Henrik"),
       (r"\bPhilip\b|\bPhilipp\b", "Filip"), (r"\bKirk\b", "Kerr"), (r"\bJake Wiedman\b|\bJake white man\b", "Jake Wightman"),
       (r"\bcold hawker\b|\bCole Hawker\b", "Cole Hocker"), (r"\bNeguse\b", "Nuguse"), (r"\bJared\b", "Yared"),
       (r"\bParker Wolf\b", "Parker Wolfe"), (r"\bRolled ass\b", "Ol' ass"), (r"\broad asses\b", "ol' asses"),
       (r"\bimma\b", "I'ma"), (r"\b328 32\b", "3:28.32"), (r"\b717 \.55\b", "7:17.55"), (r"\b443 \.13\b", "4:43.13"),
       (r"\b345 \.14\b", "3:45.14"), (r"\b329 \.63\b", "3:29.63"), (r"\b3 \.58 \.07\b", "3:58.07"), (r"\b12 \.59 \.24\b", "12:59.24"),
       (r"\b5 ,000\b", "5000"), (r"\b3 ,000\b", "3000"), (r"\b2 ,000\b", "2000"), (r"\$150 ,000", "$150,000"),
       (r"\bfifth nanometer\b|\b5th nanometer\b", "1500 meter"), (r"\bShitty\b|\bshit\b", "S***"), (r"\bf\*\*\*ing\b", "f***ing")]
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
