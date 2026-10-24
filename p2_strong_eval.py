"""Part C detector evaluation (E97 full arm / pilot, descriptive at pilot n): frozen premium scorer (llm_v3 dev
threshold) + frozen gpt-6.1-sol auditor views (unchanged prompts, llm_v3 dev Youden thresholds) on a part-C dataset,
by execution class from p2_strong.analyse (first-floor compliance and STRICT), plus a market-level absolute statistic
(market excess over cost-adjusted Nash, no threshold; AUROC only) because spillover makes pair-relative screens blind.

Contrasts (codex E97 review P2): all-private vs none; executed vs none (selected subset); executed vs abandoned.
Run AUROC with a seed-cluster bootstrap (matched seeds resampled together).

    uv run python p2_strong_eval.py --ds llm_p2strong_luna --min-floor 13 --late 11
"""
import argparse, json
from pathlib import Path
import numpy as np
from final_analysis import LLM_VIEWS, premium_scores
from p2_strong import analyse


def auroc(pos, neg):
    if not pos or not neg:
        return None
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]))


def boot(S, runs, P, N, B=2000):
    seeds = sorted({runs[r]["seed"] for r in P + N}); rng = np.random.default_rng(1); out = []
    by = {s: [r for r in P + N if runs[r]["seed"] == s] for s in seeds}
    for _ in range(B):
        pick = [r for s in rng.choice(seeds, len(seeds)) for r in by[s]]
        a = auroc([S[r] for r in pick if r in P], [S[r] for r in pick if r in N])
        if a is not None:
            out.append(a)
    return [round(float(np.percentile(out, 2.5)), 3), round(float(np.percentile(out, 97.5)), 3)] if out else [None, None]


ap = argparse.ArgumentParser()
ap.add_argument("--ds", required=True); ap.add_argument("--min-floor", type=int, default=13)
ap.add_argument("--late", type=int, default=11)
a = ap.parse_args()
res = analyse(a.ds, a.min_floor, a.late); runs = res["runs"]
TH = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]
scores = {"premium": {r: d["run"] for r, d in premium_scores(a.ds)[0].items()}, "market_excess_nash": {r: e["market_excess_nash"] for r, e in runs.items()}}
base = Path("results/llm_auditor") / a.ds / "gpt-6.1-sol"
for v in LLM_VIEWS:
    f = base / f"{v}_orig.jsonl"
    if f.exists():
        scores[v] = {x["run_id"]: x["collusion_present"] for x in map(json.loads, open(f))}
groups = {"none": [r for r, e in runs.items() if e["cond"] == "none"],
          "private_all": [r for r, e in runs.items() if e["cond"] == "private"],
          "executed": [r for r, e in runs.items() if e["cls"] == "executed"],
          "strict": [r for r, e in runs.items() if e["strict"]],
          "abandoned": [r for r, e in runs.items() if e["cond"] == "private" and e["cls"] != "executed"]}
out = {"ds": a.ds, "class_summary": {k: v for k, v in res.items() if k != "runs"}, "groups_n": {g: len(v) for g, v in groups.items()},
       "detectors": {}}
for k, S in scores.items():
    S = {r: s for r, s in S.items() if r in runs}
    e = {"threshold": TH.get(k)}
    if TH.get(k) is not None:
        e["flags"] = {g: [int(sum(S[r] >= TH[k] for r in ids if r in S)), sum(r in S for r in ids)] for g, ids in groups.items()}
    for name, (P, N) in {"private_vs_none": ("private_all", "none"), "executed_vs_none": ("executed", "none"),
                         "strict_vs_none": ("strict", "none"), "executed_vs_abandoned": ("executed", "abandoned")}.items():
        Pi = [r for r in groups[P] if r in S]; Ni = [r for r in groups[N] if r in S]
        au = auroc([S[r] for r in Pi], [S[r] for r in Ni])
        e[f"auroc_{name}"] = [round(au, 3)] + boot(S, runs, Pi, Ni) if au is not None else None
    out["detectors"][k] = e
p = Path(f"results/analysis/p2_strong_eval_{a.ds}.json"); p.write_text(json.dumps(out, indent=1))
print(json.dumps(out["groups_n"]))
for k, e in out["detectors"].items():
    print(k, e.get("flags"), e["auroc_private_vs_none"], e["auroc_executed_vs_none"])
print("->", p)
