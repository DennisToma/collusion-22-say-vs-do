"""Descriptive (iter 17): mean market price in round 1 and round 12 for the firm-framing stratum (llm_v3fp) vs the
lab-framing `none` test runs (llm_v3_0030-0124). Regenerates the 13.2/12.5 vs 12.9/12.0 numbers quoted in REPORT
Appendix D (previously computed ad hoc; flagged by logs/review_iter17_final.md).

    uv run python fp_prices.py   # -> results/analysis/fp_prices.json
"""
import json
from pathlib import Path
import numpy as np


def mean_prices(ds, keep):
    gt = {json.loads(l)["run_id"]: json.loads(l) for l in open(Path("data") / ds / "ground_truth.jsonl")}
    by = {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        if keep(r["run_id"], gt[r["run_id"]]):
            by.setdefault(r["round"], []).extend(x["price"] for x in r["agents"])
    last = max(by)
    return {"n_runs": len({k for k, g in gt.items() if keep(k, g)}), "round1": round(float(np.mean(by[0])), 3),
            f"round{last + 1}": round(float(np.mean(by[last])), 3)}


def is_test_none(rid, g):
    return g["condition"] == "none" and 30 <= int(rid.rsplit("_", 1)[-1]) <= 124


out = {"llm_v3fp": mean_prices("llm_v3fp", lambda r, g: True), "llm_v3_test_none": mean_prices("llm_v3", is_test_none)}
Path("results/analysis/fp_prices.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
