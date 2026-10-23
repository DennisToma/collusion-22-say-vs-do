"""Exploration stratum (never pooled into the headline): firm-framing `private` runs (data/llm_v3fp), where sellers
get a private channel but often refuse to coordinate (llm_v2 pilot). Judge label splits them into
  y=1  explicit agreement / info exchange       y=0  channel present, no agreement (natural hard negatives)
EXPLORATORY transfer check related to "label = condition" on llm_v3 (it does NOT resolve that confound within
llm_v3: the firm framing also changes wording, refusals, opening prices and premiums): within one framing, does each
scorer separate *agreement* from *a channel that went unused*? Uses the FROZEN dev thresholds from final_analysis (Youden on llm_v3 dev) —
nothing is fitted on this stratum.

    uv run python fp_stratum.py --ds llm_v3fp
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import load_jsonl, auc
from final_analysis import LLM_VIEWS, premium_scores, metrics


def wilson(x, n, z=1.96):
    if not n:
        return None
    p = x / n
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(float(p), 3), round(float(max(0, c - h)), 3), round(float(min(1, c + h)), 3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3fp")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--thresholds", default="results/analysis/final_llm_v3_gpt-6.1-sol_dev.json")
    ap.add_argument("--max-idx", type=int, default=0, help="smoke test only: restrict to run index < N (e.g. llm_v3 dev)")
    a = ap.parse_args()
    th = json.loads(Path(a.thresholds).read_text())["thresholds_dev_youden"]
    rows = load_jsonl(Path("data") / a.ds / "labels.jsonl")
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange"))) for x in rows}
    assert len(labs) == len(rows), "duplicate labels"
    bad = [r for r, x in labs.items() if not a.max_idx and (x["condition"] != "private" or x["agreement"] not in ("explicit", "info_exchange", "none"))]
    assert not bad, f"unexpected condition/agreement label: {bad[:5]}"
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    S = {}
    for v in LLM_VIEWS:
        f = d / f"{v}_orig.jsonl"
        if f.exists():
            R = load_jsonl(f)
            assert len({x["run_id"] for x in R}) == len(R), f"duplicate audits in {v}"
            S[v] = {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in R}
    missing = {v: len([r for r in labs if r not in S.get(v, {})]) for v in LLM_VIEWS}
    assert a.max_idx or not any(missing.values()), f"incomplete audits: {missing}"
    S["premium"], markup = premium_scores(a.ds)
    S["premium_r2plus"], _ = premium_scores(a.ds, start=1)
    ids = sorted(r for r in labs if all(r in R for R in S.values()) and (not a.max_idx or int(r.rsplit("_", 1)[1]) < a.max_idx))
    groups = {"y1_agreement": [r for r in ids if labs[r]["y"]], "y0_channel_no_agreement": [r for r in ids if not labs[r]["y"]]}
    out = {"dataset": a.ds, "auditor": a.auditor, "n_runs": len(ids), "n_labelled": len(labs),
           "agreement_counts": {k: sum(labs[r]["agreement"] == k for r in labs) for k in sorted({labs[r]["agreement"] for r in labs})},
           "thresholds_from": a.thresholds, "flag_rate": {}, "auroc_y1_vs_y0": {}, "mean_run_score": {},
           "assigned_pair_late_premium": {g: [round(labs[r]["pair_premium"], 3) for r in rs] for g, rs in groups.items()}}
    for k in S:
        out["flag_rate"][k] = {g: (wilson(sum(S[k][r]["run"] >= th[k] for r in rs), len(rs)) if th.get(k) is not None else None)
                               for g, rs in groups.items()}
        out["mean_run_score"][k] = {g: round(float(np.mean([S[k][r]["run"] for r in rs])), 2) if rs else None for g, rs in groups.items()}
        if groups["y1_agreement"] and groups["y0_channel_no_agreement"]:
            out["auroc_y1_vs_y0"][k] = round(auc([labs[r]["y"] for r in ids], [S[k][r]["run"] for r in ids]), 3)
    if groups["y1_agreement"]:
        m = metrics(groups["y1_agreement"], S, labs)
        out["within_market_auroc_y1"] = {k: round(m[k]["within_market_auroc"], 3) for k in S}
    Path("results/analysis").mkdir(parents=True, exist_ok=True)
    (Path("results/analysis") / f"fp_stratum_{a.ds}.json").write_text(json.dumps(out, indent=1))
    print(f"{a.ds}: n={len(ids)}/{len(labs)} labelled, agreement counts {out['agreement_counts']}")
    for k in S:
        print(f"{k:15s} flag y1={out['flag_rate'][k]['y1_agreement']}  y0={out['flag_rate'][k]['y0_channel_no_agreement']}"
              f"  AUROC y1-vs-y0={out['auroc_y1_vs_y0'].get(k)}")


if __name__ == "__main__":
    main()
