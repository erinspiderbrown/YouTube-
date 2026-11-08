"""Make an .srt caption file from the exact script text, timed to the paced voiceover's whisper word timings.

The script is authoritative for the words (names spelled right); whisper only supplies timing. Number words and digits are
left out of the alignment (script says "nine ninety-six", whisper writes "996"), and unmatched words are interpolated.

python3 tools/make_captions.py SCRIPT.md WORDS.json OUT.srt [--replace "Let-see-lay=Letsile" ...]
SCRIPT.md: text after the first '---'; '#' lines and [tags] are dropped.
"""
import sys, json, re, difflib, argparse
import numpy as np

NUM = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
          "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand oh".split())

def key(t):
    n = re.sub(r"[^a-z0-9']", "", t.lower().replace("-", "")).strip("'")
    parts = re.split(r"[- ]", t.lower().strip('.,?!"\''))
    if not n or any(c.isdigit() for c in n) or any(p in NUM for p in parts): return None
    return n

def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("words"); ap.add_argument("out")
    ap.add_argument("--replace", action="append", default=[]); ap.add_argument("--maxlen", type=int, default=38)
    a = ap.parse_args()
    W = json.load(open(a.words))[0]["words"]
    body = open(a.script).read().split("---", 1)[-1]
    lines = [re.sub(r"\[[^\]]*\]", "", l).strip() for l in body.split("\n") if l.strip() and not l.strip().startswith("#")]
    text = " ".join(l for l in lines if l)
    for r in a.replace:
        k, v = r.split("=", 1); text = text.replace(k, v)
    sw = text.split()
    sk = [(i, key(t)) for i, t in enumerate(sw)]; sk = [(i, k) for i, k in sk if k]
    wk = [(j, key(x["w"])) for j, x in enumerate(W)]; wk = [(j, k) for j, k in wk if k]
    sm = difflib.SequenceMatcher(None, [k for _, k in sk], [k for _, k in wk], autojunk=False)
    anch = {}
    for b in sm.get_matching_blocks():
        for n in range(b.size): anch[sk[b.a + n][0]] = (W[wk[b.b + n][0]]["s"], W[wk[b.b + n][0]]["e"])
    good, last = {}, -1
    for i in sorted(anch):
        if anch[i][0] > last: good[i] = anch[i]; last = anch[i][0]
    xi = np.array(sorted(good)); st = np.interp(range(len(sw)), xi, [good[i][0] for i in xi]); en = np.interp(range(len(sw)), xi, [good[i][1] for i in xi])
    cues, cur = [], []
    for i, t in enumerate(sw):
        cur.append(i); txt = " ".join(sw[k] for k in cur); core = t.rstrip('"\'')
        if core[-1:] in ".?!" or (core[-1:] in ",:" and len(txt) > 28) or len(txt) > a.maxlen: cues.append(cur); cur = []
    if cur: cues.append(cur)
    out = []
    for n, c in enumerate(cues):
        s0 = st[c[0]]; e0 = max(en[c[-1]], s0 + 0.6)
        if n + 1 < len(cues): e0 = min(e0 + 0.25, st[cues[n + 1][0]] - 0.02)
        out.append(f"{n + 1}\n{ts(s0)} --> {ts(e0)}\n{' '.join(sw[k] for k in c)}\n")
    open(a.out, "w").write("\n".join(out))
    print(f"{len(sw)} words, {len(good)} anchors, {len(cues)} cues -> {a.out}")

if __name__ == "__main__":
    main()
