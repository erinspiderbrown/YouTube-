"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/ncaa-xc-nationals-2026/nats_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bHend[a-z]*gr[ae]n[a-z]*\b|\bHen+[a-z]*gren\b|\bHedgren\b", "Hedengren"), (r"\bHannah (Grapes|Gates|Gaps)\b", "Hannah Gapes"),
       (r"\b(Grapes|Gates)\b", "Gapes"), (r"\bKaitlyn Toohey\b|\bKatelyn Toohey\b|\bToohey\b", "Katelyn Tuohy"), (r"\bOrdon\b|\bOrden\b", "Orton"),
       (r"\bWhitney Orton\b", "Whittni Orton"), (r"\b(Lemon-?Golay|Levin Golay|Lemngoli)\b", "Lemngole"), (r"\b(Kausgeye|Cosgai|Kostai|Kosgey)\b", "Kosgei"),
       (r"\b(Jepkirwi|Jepkiroi|Jepkurui)\b", "Jepkirui"), (r"\bchorus\b", "course"), (r"\bnc double a\b", "NCAA"), (r"\bI'm gonna\b", "I'ma"),
       (r"\bValbee\b|\bVolby\b", "Valby"), (r"\bass\b", "a**"), (r"\bHanson\b", "Hansen"), (r"\bKiprut?ho\b", "Kipruto"), (r"\bHa(p|m)ton Samuel\b", "Habtom Samuel"), (r"\bBilla\b", "Billah"), (r"\bKatie Zhang\b", "Katy Zang"), (r"\bDanny Jones\b", "Dani Jones"), (r"\bLet'?s Run\b", "LetsRun"), (r"\bTaylor Lavelle\b", "Taylor Lovell"), (r"\bmeat history\b", "meet history"), (r"\btold the line\b", "toed the line"), (r"\bElsingy\b", "Elsingi"), (r"\bHeddingren\b", "Hedengren"), (r"\bStenoff\b|\bStenuff\b", "Stenuf")]
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
open("/home/user/YouTube-/projects/ncaa-xc-nationals-2026/captions.srt", "w").write("\n".join(out)); print(len(out), "cues")
