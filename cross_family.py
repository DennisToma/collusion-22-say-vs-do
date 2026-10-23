"""Cross-family auditor check (PLAN validity req. 4): GPT (gpt-6.1-sol) vs Claude auditor on the same runs/views.

Per view, on runs scored by both: pair-AUROC of each auditor, Spearman rho of the 6 pair scores pooled over runs,
top-pair agreement, and Δ_hybrid(pair) for each auditor (so we can say whether the *ranking of views* replicates).

    uv run python cross_family.py --ds llm_v3 --other claude-sonnet-5-5
"""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from analyze_llm import PAIRS, VIEWS, load_jsonl, auc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--base", default="gpt-6.1-sol")
    ap.add_argument("--other", default="claude-sonnet-5-5")
    ap.add_argument("--boot", type=int, default=1000)
    a = ap.parse_args()
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    R = {}
    for m in (a.base, a.other):
        for v in VIEWS:
            rows = load_jsonl(Path("results/llm_auditor") / a.ds / m / f"{v}_orig.jsonl")
            if rows:
                R[(m, v)] = {x["run_id"]: x for x in rows}
    views = [v for v in VIEWS if (a.base, v) in R and (a.other, v) in R]
    common = sorted(set(labs).intersection(*[set(R[(m, v)]) for v in views for m in (a.base, a.other)]))

    def pair_auc(m, v, ids):
        y = [int(labs[r]["y"] and p == "".join(labs[r]["assigned_pair"])) for r in ids for p in PAIRS]
        return auc(y, [R[(m, v)][r]["scores"][p] for r in ids for p in PAIRS])

    rng = np.random.default_rng(0)
    boots = [list(rng.choice(common, len(common))) for _ in range(a.boot)]
    out = {"dataset": a.ds, "base": a.base, "other": a.other, "n_runs": len(common),
           "n_pos": int(sum(labs[r]["y"] for r in common)), "views": {}}
    for v in views:
        sb = [R[(a.base, v)][r]["scores"][p] for r in common for p in PAIRS]
        so = [R[(a.other, v)][r]["scores"][p] for r in common for p in PAIRS]
        def tops(m, r):  # tie-aware top set
            sc = R[(m, v)][r]["scores"]; return {p for p in PAIRS if sc[p] == max(sc.values())}
        # expected agreement when each auditor breaks its own ties uniformly at random
        top = np.mean([len(tops(a.base, r) & tops(a.other, r)) / (len(tops(a.base, r)) * len(tops(a.other, r))) for r in common])
        out["views"][v] = {"pair_auroc_" + m: round(pair_auc(m, v, common), 4) for m in (a.base, a.other)}
        out["views"][v].update(spearman_pair_scores=round(float(spearmanr(sb, so)[0]), 3), top_pair_agree=round(float(top), 3))
    for m in (a.base, a.other):
        for h in ("combined", "structured", "action_stats"):
            if h in views and {"text", "action"} <= set(views):
                f = lambda ids: pair_auc(m, h, ids) - max(pair_auc(m, "text", ids), pair_auc(m, "action", ids))
                db = np.array([f(b) for b in boots])
                out.setdefault("delta_pair", {})[f"{m}:{h}"] = {"delta": round(f(common), 4),
                    "ci": [round(float(np.nanpercentile(db, 2.5)), 4), round(float(np.nanpercentile(db, 97.5)), 4)]}
    fn = Path("results/analysis") / f"{a.ds}_crossfamily_{a.other}.json"
    fn.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
