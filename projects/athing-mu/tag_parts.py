"""Tag the 11 script parts in vo_words.json (after check_vo.py re-transcribes the cleaned voiceover)."""
import json, re, os
P = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{P}/vo_words.json"))
if W and "words" in W[0]: W = W[0]["words"]
tok = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
T = [tok(w["w"]) for w in W]
starts = [["june", "24th"], ["grew", "up", "in"], ["february", "24th"], ["2021"], ["2022", "world"], ["march", "2023"], ["2024", "weeks"],
          ["march", "2025"], ["september"], ["october", "15th"], ["so", "what", "really"]]
idx, cur = [], 0
for p in starts:
    for i in range(cur, len(T)):
        if T[i:i + len(p)] == p: idx.append(i); cur = i + 1; break
    else: raise SystemExit(f"MISS {p}")
j = idx[1]
while j > 0 and T[j - 1] in ("a", "athing", "thing", "mu", "mo", "thingmo", "athingmu"): j -= 1
idx[1] = j
for k in range(11):
    for w in W[idx[k]:(idx[k + 1] if k < 10 else len(W))]: w["part"] = k + 1
json.dump([{"words": W}], open(f"{P}/vo_words.json", "w"))
print({k + 1: round(W[i]["s"], 1) for k, i in enumerate(idx)})
