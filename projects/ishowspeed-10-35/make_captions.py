"""Captions for the final cut: the user's VO words (mapped with FT) + every soundbite's own words, names fixed."""
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/ishowspeed-10-35/speed_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bI show speed\b|\bIshowspeed\b|\biShowSpeed\b", "IShowSpeed"), (r"\bI don't boat and\b|\bOtto Bolton\b|\bAto Bolton\b", "Ato Boldon"),
       (r"\byou saying boat\b|\byou saying both\b|\bUsain boat\b", "Usain Bolt"), (r"\bBoth said\b", "Bolt said"), (r"\bboth straight up\b", "Bolt straight up"),
       (r"\bSpeed as Usain Bolt\b", "Speed asked Usain Bolt"), (r"\bno allows\b|\bNoah Laws\b|\bNoah Allows\b", "Noah Lyles"), (r"\braised Noah\b", "raced Noah"),
       (r"\bGout gout\b|\bGod, God\b", "Gout Gout"), (r"\bGalt\b", "Gatlin"), (r"\bspeed goes pro\b", "Speed Goes Pro"), (r"\btime against\b", "timing gates"),
       (r"\bfat meets\b", "FAT meets"), (r"\blegal win\b", "legal wind"), (r"\bmeats\b", "meets"), (r"\bthey put that at work\b", "their pathetic sport"),
       (r"\bmodule\b", "y'all"), (r"\bran illegally\b", "ran it legally"), (r"\bShakira Richardson\b", "Sha'Carri Richardson"),
       (r"\b10 ?-?\.?35\b|\b1035\b", "10.35"), (r"\b10 ?-?\.?5\b", "10.5"), (r"\b10 3\b", "10.3"), (r"\b10 2\b", "10.2"), (r"\b10 6\b", "10.6"),
       (r"\b10 7\b", "10.7"), (r"\b10 8\b", "10.8"), (r"\b1967\b", "19.67"), (r"\b20 \.6\b", "20.6"), (r"\bten three\b", "10.3"), (r"\bnine seven\b", "9.7"),
       (r"\ba hundred and eighty six million\b", "186 million"), (r"\by 'all\b", "y'all"), (r"\*\*\*\*", "[bleep]"), (r"\bran 10.35 and 100\b", "ran 10.35 in the 100"), (r"\bhis fate\. It's not real\b", "it's fake. It ain't real"),
       (r"\bboat\b", "Bolt"), (r"\bthey mean watch it\b", "they ain't even watched it"), (r"\bspeed ran 10.5\b", "Speed ran 10.5"), (r"\b10\.3\.5\b", "10.35"),
       (r"\b70 %", "70%"), (r"\bran illegally\b", "ran it legally"), (r"\bwouldn't break you living in a hundred\b", "wouldn't break 11 in the 100"),
       (r"\bten for 10.3 hundred\b", "10.4, 10.3 in the 100"), (r"\bran ten three\b", "ran 10.3"), (r"\bfat meets\b", "FAT meets"),
       (r"\bin a life\b", "in their life"), (r"\bNo things\b", "know things"), (r"\bit's speed 10.35\b", "is Speed's 10.35"), (r"\bnobody knew get\b", "nobody new get")]
words = []
from safe_cuts import rms_db
_DB = rms_db(np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32), 16000)
for w in WORDS:   # place each word by its midpoint, so a word whisper starts a hair before a soundbite split lands after the bite
    m = (w["s"] + w["e"]) / 2
    for sb_ in SOUNDBITES:   # a word whisper puts across a split goes to the side where its audio actually is
        if w["s"] < sb_["t"] < w["e"]:
            i0, i1, it = int(w["s"] / 0.01), int(w["e"] / 0.01), int(sb_["t"] / 0.01)
            m = sb_["t"] + 0.01 if _DB[it:i1 + 1].max() >= _DB[max(i0, it - 60):it].max() else sb_["t"] - 0.01
    sh = FT(m) - m
    words.append((w["s"] + sh, w["e"] + sh, w["w"], "vo"))
def sbw(src_, ss, dur, t0):
    try: segs = json.load(open(f"{CS_}/tx/{src_}.json"))
    except FileNotFoundError: return
    if isinstance(segs, dict): segs = segs.get("segments", [])
    for s in segs:
        for w in s.get("words", s.get("w", [])):
            if isinstance(w, list): w = {"w": w[0], "s": w[1], "e": w[2]}
            if ss + PAD - 0.12 <= (w["s"] + w["e"]) / 2 <= ss + dur:   # words whose middle falls in the bite (not a faded pad)
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
open("/home/user/YouTube-/projects/ishowspeed-10-35/captions.srt", "w").write("\n".join(out)); print(len(out), "cues")
