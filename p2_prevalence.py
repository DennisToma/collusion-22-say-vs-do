"""Phase 2 (shared gap): precision at realistic collusion prevalence, at the FROZEN llm_v3 dev thresholds.
Post-hoc re-expression of saved scores only (no audit, no threshold refit). For each detector, TPR on y=1 and FPR on
y=0 at the dev Youden threshold; precision(pi) = TPR*pi / (TPR*pi + FPR*(1-pi)) and alarms per 1000 audited markets,
for pi in {1%, 5%, 20%}. CIs: class-stratified bootstrap over runs (2000), TPR and FPR resampled jointly.
Fusion uses the dev-chosen text weight (final_llm_v3_*_dev.json).

    uv run python p2_prevalence.py     # -> results/analysis/p2_prevalence.json
"""
import json
from pathlib import Path
import numpy as np
from final_analysis import LLM_VIEWS, DEV_MAX, idx, premium_scores

PI = [0.01, 0.05, 0.2]
DEV = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))
TH, W = DEV["thresholds_dev_youden"], DEV["fusion_w_text"]


def load(ds, ids_filter):
    labs = {x["run_id"]: int(x["agreement"] in ("explicit", "info_exchange"))
            for x in map(json.loads, open(Path("data") / ds / "labels.jsonl"))}
    S = {}
    for v in LLM_VIEWS:
        S[v] = {x["run_id"]: x["collusion_present"]
                for x in map(json.loads, open(Path("results/llm_auditor") / ds / "gpt-6.1-sol" / f"{v}_orig.jsonl"))}
    S["fusion"] = {r: W * S["text"][r] + (1 - W) * S["action"][r] for r in S["text"] if r in S["action"]}
    S["premium"] = {r: v["run"] for r, v in premium_scores(ds)[0].items()}
    ids = sorted(r for r in labs if ids_filter(r) and all(r in S[k] for k in S))
    return ids, labs, S


def wilson(k, n, z=1.96):
    c, h = (k + z * z / 2) / (n + z * z), z * np.sqrt(k * (n - k) / n + z * z / 4) / (n + z * z)
    return c - h, c + h


def stats(tp, fp, npos, nneg):
    tpr, fpr = tp / npos, fp / nneg
    o = {"tpr": tpr, "fpr": fpr}
    for pi in PI:
        den = tpr * pi + fpr * (1 - pi)
        o[f"precision@{pi}"] = tpr * pi / den if den > 0 else np.nan
        o[f"alarms_per_1000@{pi}"] = 1000 * den
        o[f"false_alarms_per_1000@{pi}"] = 1000 * fpr * (1 - pi)
    return o


def main():
    out = {"thresholds_dev_youden": TH, "fusion_w_text": W, "prevalences": PI,
           "note": "precision computed from split TPR/FPR at frozen dev thresholds; prevalence is hypothetical"}
    rng = np.random.default_rng(0)
    for name, ds, f in (("llm_v3_test", "llm_v3", lambda r: idx(r) >= DEV_MAX), ("llm_v3rep", "llm_v3rep", lambda r: True)):
        ids, labs, S = load(ds, f)
        pos = [r for r in ids if labs[r]]; neg = [r for r in ids if not labs[r]]
        res = {"n_pos": len(pos), "n_neg": len(neg), "detectors": {}}
        for k in ["premium"] + LLM_VIEWS + ["fusion"]:
            tpf = np.array([S[k][r] >= TH[k] for r in pos]); fpf = np.array([S[k][r] >= TH[k] for r in neg])
            pt = stats(tpf.sum(), fpf.sum(), len(pos), len(neg))
            B = [stats(rng.choice(tpf, len(pos)).sum(), rng.choice(fpf, len(neg)).sum(), len(pos), len(neg))
                 for _ in range(2000)]
            res["detectors"][k] = {m: [round(float(pt[m]), 3), round(float(np.nanpercentile([b[m] for b in B], 2.5)), 3),
                                       round(float(np.nanpercentile([b[m] for b in B], 97.5)), 3)] for m in pt}
            res["detectors"][k]["counts"] = {"tp": int(tpf.sum()), "fp": int(fpf.sum())}
            # conservative: Wilson lower TPR bound with Wilson upper FPR bound (bootstrap CI degenerates when FP = 0)
            tl, fu = wilson(tpf.sum(), len(pos))[0], wilson(fpf.sum(), len(neg))[1]
            res["detectors"][k]["precision_conservative_wilson"] = {
                str(pi): round(float(tl * pi / (tl * pi + fu * (1 - pi))), 3) for pi in PI}
        out[name] = res
    Path("results/analysis/p2_prevalence.json").write_text(json.dumps(out, indent=1))
    for name in ("llm_v3_test", "llm_v3rep"):
        print(name, out[name]["n_pos"], out[name]["n_neg"])
        for k, d in out[name]["detectors"].items():
            print(f"  {k:15s} TPR {d['tpr']} FPR {d['fpr']} prec@1% {d['precision@0.01']} @5% {d['precision@0.05']} @20% {d['precision@0.2']} cons {d['precision_conservative_wilson']}")


if __name__ == "__main__":
    main()
