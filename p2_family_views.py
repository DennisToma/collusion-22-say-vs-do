"""E91 (registered before running): frozen auditor views (gpt-6.1-sol, unchanged prompts, llm_v3 dev Youden thresholds)
on a seller-family dataset. Flag rates per condition and run AUROC private vs none (descriptive at small n).

    uv run python p2_family_views.py --ds llm_p2claude   # -> results/analysis/p2_family_views.json
"""
import argparse, json
from pathlib import Path
import numpy as np
from final_analysis import LLM_VIEWS

ap = argparse.ArgumentParser(); ap.add_argument("--ds", nargs="+", default=["llm_p2claude"]); a = ap.parse_args()
TH = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]
outp = Path("results/analysis/p2_family_views.json"); out = json.loads(outp.read_text()) if outp.exists() else {}
for ds in a.ds:
    gt = {g["run_id"]: g["condition"] for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
    base = Path("results/llm_auditor") / ds / "gpt-6.1-sol"; res = {}
    for v in LLM_VIEWS:
        f = base / f"{v}_orig.jsonl"
        if not f.exists():
            continue
        S = {x["run_id"]: x["collusion_present"] for x in map(json.loads, open(f))}
        conds = sorted({gt[r] for r in S})
        e = {"threshold": TH[v], "flags": {c: [int(sum(S[r] >= TH[v] for r in S if gt[r] == c)), sum(gt[r] == c for r in S)] for c in conds},
             "mean_score": {c: round(float(np.mean([S[r] for r in S if gt[r] == c])), 3) for c in conds}}
        pos = [S[r] for r in S if gt[r] == "private"]; neg = [S[r] for r in S if gt[r] == "none"]
        if pos and neg:
            au = lambda P_, N_: float(np.mean([(p > q) + .5 * (p == q) for p in P_ for q in N_]))
            rng = np.random.default_rng(0); B = [au(rng.choice(pos, len(pos)), rng.choice(neg, len(neg))) for _ in range(2000)]
            e["run_auroc_private_vs_none"] = [round(au(pos, neg), 3), round(float(np.percentile(B, 2.5)), 3), round(float(np.percentile(B, 97.5)), 3)]
        res[v] = e
    out[ds] = res
    for v, e in res.items():
        print(ds, v, e["flags"], e["mean_score"], e.get("run_auroc_private_vs_none"))
outp.write_text(json.dumps(out, indent=1))
