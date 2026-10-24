"""E99 descriptive (post hoc, iter 20): how often do public-board messages announce holding/maintaining a price, by arm
and behaviour class? Crude keyword rule (hold/keep/maintain/stay/stable/match + a price 10-19 in the same message);
explains why public-text auditors score tacit-high no-channel markets ABOVE executed private ones (E99-x).
    uv run python p2_strongF_public.py   # -> results/analysis/p2_strongF_public.json
"""
import json, re
from collections import defaultdict
from pathlib import Path
ds = "llm_p2strongF"
RX = re.compile(r"\b(hold|keep|maintain|stay|stable|match)\w*\b.*\b1\d\b|\b1\d\b.*\b(hold|keep|maintain|stable)")
gt = {g["run_id"]: g for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
C = json.load(open(f"results/analysis/p2_strong_classes_{ds}.json"))["runs"]
cls = {r["run_id"]: r.get("class") for r in C} if isinstance(C, list) else {k: v.get("class") for k, v in C.items()}
per = defaultdict(lambda: [0, 0])
for r in map(json.loads, open(f"data/{ds}/trajectories.jsonl")):
    for a in r["agents"]:
        per[r["run_id"]][1] += 1
        per[r["run_id"]][0] += bool(RX.search(a["public_message"].lower()))
out = {"rule": RX.pattern, "by_condition": {}, "by_class": {}}
for key, f in (("by_condition", lambda rid: gt[rid]["condition"]), ("by_class", lambda rid: cls.get(rid))):
    agg = defaultdict(lambda: [0, 0, 0])
    for rid, (k, n) in per.items():
        g = agg[str(f(rid))]; g[0] += k; g[1] += n; g[2] += 1
    out[key] = {c: {"hold_msgs": k, "msgs": n, "share": round(k / n, 3), "runs": m} for c, (k, n, m) in agg.items()}
Path("results/analysis/p2_strongF_public.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
