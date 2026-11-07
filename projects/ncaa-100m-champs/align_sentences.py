"""Find where each script sentence starts and ends in a paced voiceover, using its whisper word timings.

Script and transcript differ on numbers ("twenty sixteen" vs "2016"), so number words and digit tokens are dropped
before aligning with difflib. Sentences with nothing left to match (e.g. "Twenty sixteen.") are interpolated
from their neighbours.

python3 align_sentences.py SENTS.txt WORDS.json OUT.json      (SENTS: one sentence per line, optionally "n|key|text")
"""
import sys, json, re, difflib

NUM = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
          "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand oh".split())

def toks(s):
    out = []
    for w in re.findall(r"[A-Za-z0-9']+", s.lower().replace("-", " ")):
        w = w.strip("'")
        if not w or w.isdigit() or w in NUM or any(c.isdigit() for c in w): continue
        out.append(w)
    return out

def align(sents, words):
    st = []; owner = []
    for i, s in enumerate(sents):
        t = toks(s); st += t; owner += [i] * len(t)
    wt = []; wi = []
    for j, w in enumerate(words):
        for t in toks(w["w"]): wt.append(t); wi.append(j)
    sm = difflib.SequenceMatcher(None, st, wt, autojunk=False)
    first = {}; last = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            i = owner[a + k]; w = words[wi[b + k]]
            first.setdefault(i, w["s"]); last[i] = w["e"]
    N = len(sents); S = [first.get(i) for i in range(N)]; E = [last.get(i) for i in range(N)]
    # interpolate gaps (number-only sentences): start right after previous end, end right before next start
    for i in range(N):
        if S[i] is None:
            prev = next((E[k] for k in range(i - 1, -1, -1) if E[k] is not None), 0.0)
            nxt = next((S[k] for k in range(i + 1, N) if S[k] is not None), prev + 1.5)
            S[i] = prev + 0.15 if nxt - prev > 0.5 else prev; E[i] = max(S[i] + 0.3, nxt - 0.15)
    return [(round(S[i], 3), round(E[i], 3)) for i in range(N)]

if __name__ == "__main__":
    sents = [l.rstrip("\n").split("|")[-1] for l in open(sys.argv[1]) if l.strip()]
    w = json.load(open(sys.argv[2])); words = w[0]["words"] if isinstance(w, list) and "words" in w[0] else w
    res = align(sents, words)
    json.dump(res, open(sys.argv[3], "w"))
    miss = sum(1 for s in sents if not toks(s))
    print(len(res), "sentences;", miss, "number-only (interpolated)")
