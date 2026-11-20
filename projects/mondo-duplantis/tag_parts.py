"""Tag the 9 script parts in vo_words.json (after check_vo.py re-transcribes the cleaned voiceover)."""
import json, re, os
P = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{P}/vo_words.json"))
if W and "words" in W[0]: W = W[0]["words"]
tok = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
T = [tok(w["w"]) for w in W]
starts = [["june"], ["to", "understand", "why"], ["now", "look", "at"], ["and", "heres", "the", "part"], ["july"],
          ["his", "name", "is"], ["then", "something", "changes"], ["now", "lets", "keep"], ["one", "more", "thing"]]
idx, cur = [], 0
for p in starts:
    for i in range(cur, len(T)):
        if T[i:i + len(p)] == p: idx.append(i); cur = i + 1; break
    else: raise SystemExit(f"MISS {p}")
if T[idx[8] - 1] in ("theres", "is"): idx[8] -= 1
if T[idx[8] - 1] in ("there",): idx[8] -= 1
if T[idx[8] - 1] == "and": idx[8] -= 1
for k in range(9):
    for w in W[idx[k]:(idx[k + 1] if k < 8 else len(W))]: w["part"] = k + 1
json.dump([{"words": W}], open(f"{P}/vo_words.json", "w"))
print({k + 1: (round(W[i]["s"], 1), " ".join(T[i:i+5])) for k, i in enumerate(idx)})
