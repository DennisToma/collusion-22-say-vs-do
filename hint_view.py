"""Post-lock EXPLORATION (E56, iter 15): does telling the LLM auditor where the signal is close the gap to the
untrained premium? View `action_stats_hint` = action_stats + one fixed sentence pointing at the pair premium and
round-1 prices (auditors.py WHAT). One prompt, written once, no tuning on any split. Compared on identical runs with
action_stats and premium (paired, class-stratified bootstrap over runs; final_analysis.metrics/_pd).
Exploratory: test and llm_v3rep were already used for the locked/registered analyses; nothing here changes them.

    uv run python hint_view.py   # -> results/analysis/hint_view.json
"""
import json
from scipy.stats import spearmanr
from pathlib import Path
from analyze_llm import load_jsonl
from final_analysis import metrics, _pd, idx, DEV_MAX, premium_scores

M = ("run_auroc", "within_market_auroc", "pair_id_acc")


def load(ds, v):
    rows = load_jsonl(Path("results/llm_auditor") / ds / "gpt-6.1-sol" / f"{v}_orig.jsonl")
    return {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in rows}


def main(nb=2000):
    out = {}
    for ds, split in (("llm_v3", "dev"), ("llm_v3", "test"), ("llm_v3rep", "all")):
        labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
                for x in load_jsonl(Path("data") / ds / "labels.jsonl")}
        S = {v: load(ds, v) for v in ("action", "action_stats", "action_stats_hint")}
        S["premium"], _ = premium_scores(ds)
        ids = sorted(r for r in set(labs).intersection(*map(set, S.values()))
                     if split == "all" or (idx(r) < DEV_MAX) == (split == "dev"))
        pt = metrics(ids, S, labs)
        res = {"n_runs": len(ids), "n_pos": sum(labs[r]["y"] for r in ids),
               "point": {k: {m: round(pt[k][m], 4) for m in M} for k in pt}, "contrasts": {}}
        for k1, k2 in (("action_stats_hint", "action_stats"), ("premium", "action_stats_hint")):
            for m in ("run_auroc", "within_market_auroc"):
                res["contrasts"][f"{k1}-{k2}:{m}"] = _pd(ids, S, labs, k1, k2, m, nb)
        res["spearman_run_score_vs_premium"] = {
            v: round(float(spearmanr([S[v][r]["run"] for r in ids], [S["premium"][r]["run"] for r in ids])[0]), 3)
            for v in ("action", "action_stats", "action_stats_hint")}
        out[f"{ds}_{split}"] = res
    Path("results/analysis/hint_view.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
