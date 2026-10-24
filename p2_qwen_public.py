"""C3 (E100, post hoc descriptive): public-invitation regex (frozen, = p2_family3way.RX) on qwen base/abliterated markets.
uv run python p2_qwen_public.py -> results/analysis/p2_qwen_public.json"""
import json
from p2_family3way import RX

out = {}
for ds in ["llm_p2qwenb", "llm_p2qwena"]:
    cond = {}
    for l in open(f"data/{ds}/ground_truth.jsonl"):
        r = json.loads(l); cond[r["run_id"]] = r["condition"]
    agg = {}
    for l in open(f"data/{ds}/trajectories.jsonl"):
        t = json.loads(l); c = cond[t["run_id"]]
        a = agg.setdefault(c, {"msgs": 0, "hits": 0, "markets_hit": set(), "markets": set()})
        a["markets"].add(t["run_id"])
        for ag in t["agents"]:
            m = ag.get("public_message") or ""
            if m.strip():
                a["msgs"] += 1
                if RX.search(m):
                    a["hits"] += 1; a["markets_hit"].add(t["run_id"])
    out[ds] = {c: {"public_msgs": a["msgs"], "regex_hits": a["hits"], "markets_with_hit": len(a["markets_hit"]),
                   "markets": len(a["markets"])} for c, a in agg.items()}
json.dump(out, open("results/analysis/p2_qwen_public.json", "w"), indent=1)
print(json.dumps(out, indent=1))
