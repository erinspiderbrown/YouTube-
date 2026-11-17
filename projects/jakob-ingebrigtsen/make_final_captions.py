"""Jakob Ingebrigtsen: child prodigy. Boling v2 style. No Olympic, NCAA, Worlds or FloTrack footage.
import sys, json, re
sys.argv = ["x"]
src = open("/home/user/YouTube-/projects/jakob-ingebrigtsen/jakob_build.py").read().split("if __name__")[0]
exec(src)
TL()
CS_ = CS
FIX = [(r"\bHend[a-z]*gr[ae]n[a-z]*\b|\bHen+[a-z]*gren\b|\bHennigran\b|\bHedinger\b|\bHendringen\b|\bHettingrand\b|\bHedgren\b|\bHead and grin\b|\bhead and grin\b|\bHendergram\b|\bAhedegren\b|\bDeHeadengrin\b|\bHendegrenz\b", "Hedengren"),
       (r"\bKaitlyn Toohey\b|\bKaitlin Toohey\b|\bCaitlin Tuey\b|\bCaitlyn to me\b|\bKatelyn Chuey\b|\bkalen tui\b", "Katelyn Tuohy"),
       (r"\bToohey\b|\bTui\b|\btui\b|\bTuey\b", "Tuohy"), (r"\bKaitlyn\b|\bKalen\b|\bCaitlin\b|\bKaitlin\b", "Katelyn"),
       (r"\b10th View\b|\bTimfield\b|\bTimview\b", "Timpview"), (r"\bDejeet Taylor\b|\bDlG Taylor\b|\bDel G Taylor\b", "Diljeet Taylor"),
       (r"\bMary Kane\b|\bMary Key\b", "Mary Cain"), (r"\bAlberta\b", "Alberto"), (r"\bmilrose game\b|\bMiro's game\b", "Millrose Games"),
       (r"\bchorus records\b", "course records"), (r"\bfastest school girl\b", "fastest high school girl"),
       (r"\b15 -13\b|\b1513\b", "15:13"), (r"\b426\b", "4:26"), (r"\b14 57\b|\b1457\b", "14:57"), (r"\b423 \.50\b", "4:23.50"),
       (r"\b4 \.33\b", "4:33"), (r"\b9 \.17\b", "9:17"), (r"\b8 \.40\b", "8:40"), (r"\b14 44\b", "14:44"), (r"\b8 34 \.98\b", "8:34.98"),
       (r"\b1439\b", "14:39"), (r"\b30 usas\b|\b30 USA's\b", "3rd at USAs"), (r"\b16 c -double -a titles\b", "6 NCAA titles"),
       (r"\b6th in October\b", "sick in October"), (r"\bnc double a\b|\bNC double A\b", "NCAA"), (r"\bLemon-Golay\b|\bLevin Golay\b", "Lemngole"),
       (r"\bKausgeye\b|\bCosgai\b|\bKostai\b|\bcos-guy\b", "Kosgei"), (r"\bI'm gonna\b", "I'ma"), (r"\bAaron Brown\b", "Erin Brown"),
       (r"\bRojo\b|\brojo\b", "Rojo"), (r"\bGlendaver\b", "Glendoveer"), (r"\bshit\b", "s***")]
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
