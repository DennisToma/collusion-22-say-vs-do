"""Post-lock EXPLORATION (E71, iter 27): is the stats-table gain carried by its LEVEL columns? View
`action_stats_nolevel` = action_stats with the pair table reduced to co-movement columns (rounds within 1, corr of
price changes); pair mean, other-two mean and premium are removed. Same task text as action_stats, one prompt, no
tuning. Compared on identical runs with action and action_stats (paired, class-stratified bootstrap over runs;
final_analysis.metrics/_pd). Hypothesis registered in EXPERIMENTS.tsv before any audit was run.
Exploratory: test and llm_v3rep were already used for the locked/registered analyses; nothing here changes them.

    uv run python nolevel_view.py   # -> results/analysis/nolevel_view.json
"""
import json
from pathlib import Path
from analyze_llm import load_jsonl
from final_analysis import metrics, _pd, idx, DEV_MAX, premium_scores

M = ("run_auroc", "within_market_auroc", "pair_id_acc")
V = ("action", "action_stats", "action_stats_nolevel")


def load(ds, v):
    rows = load_jsonl(Path("results/llm_auditor") / ds / "gpt-6.1-sol" / f"{v}_orig.jsonl")
    return {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in rows}


def main(nb=2000):
    out = {}
    for ds, split in (("llm_v3", "dev"), ("llm_v3", "test"), ("llm_v3rep", "all")):
        labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
                for x in load_jsonl(Path("data") / ds / "labels.jsonl")}
        S = {v: load(ds, v) for v in V}
        S["premium"], _ = premium_scores(ds)
        ids = sorted(r for r in set(labs).intersection(*map(set, S.values()))
                     if split == "all" or (idx(r) < DEV_MAX) == (split == "dev"))
        pt = metrics(ids, S, labs)
        res = {"n_runs": len(ids), "n_pos": sum(labs[r]["y"] for r in ids),
               "point": {k: {m: round(pt[k][m], 4) for m in M} for k in pt}, "contrasts": {}}
        for k1, k2 in (("action_stats", "action_stats_nolevel"), ("action_stats_nolevel", "action")):
            for m in ("run_auroc", "within_market_auroc"):
                res["contrasts"][f"{k1}-{k2}:{m}"] = _pd(ids, S, labs, k1, k2, m, nb)
        out[f"{ds}_{split}"] = res
    Path("results/analysis/nolevel_view.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
