"""Tag the 9 script parts in vo_words.json (after check_vo.py re-transcribes the cleaned voiceover)."""
import json, re, os
P = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{P}/men_vo_words.json"))
if W and "words" in W[0]: W = W[0]["words"]
tok = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
T = [tok(w["w"]) for w in W]
starts = [["so", "the", "ncaa"], ["now", "a", "lot", "of", "people"], ["and", "the", "guy", "everybodys"], ["but", "heres", "what", "got"],
          ["you", "got"], ["so", "for", "me"]]
idx, cur = [], 0
for p in starts:
    for i in range(cur, len(T)):
        if T[i:i + len(p)] == p: idx.append(i); cur = i + 1; break
    else: raise SystemExit(f"MISS {p}")
for k in range(6):
    for w in W[idx[k]:(idx[k + 1] if k < 5 else len(W))]: w["part"] = k + 1
json.dump([{"words": W}], open(f"{P}/men_vo_words.json", "w"))
print({k + 1: (round(W[i]["s"], 1), " ".join(T[i:i+5])) for k, i in enumerate(idx)})
