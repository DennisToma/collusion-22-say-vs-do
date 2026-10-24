"""Registered replication on a fresh split (iter 12, data/SPLITS.md §llm_v3rep). Registration followed the start
of generation; no replication metrics existed, but partial raw outputs did. See SPLITS.md for full chronology.
Same generator/framing as llm_v3 (lab, sim llm-0.3), seed 9000, private:15 none:10 legit:5.
Nothing is fitted: thresholds and the fusion weight are the FROZEN llm_v3 dev values; "best LLM view" is fixed from
the llm_v3 TEST json (highest test run AUROC). Run ONCE on the complete set.

    uv run python replication.py            # -> results/analysis/replication_llm_v3rep.json
"""
import argparse, hashlib, json, os
from pathlib import Path
import numpy as np
from final_analysis import LLM_VIEWS, PAIRS, boot, _pd
from monitor_stratum import load
from fp_stratum import wilson

PREDICTIONS = {"P1": "premium run AUROC >= 0.85", "P2": "text run AUROC CI includes 0.5",
               "P3": "premium - best view (run AUROC) >= 0 (point)", "P4": "combined - action (run AUROC) CI includes 0"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3rep")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--allow-partial", action="store_true", help="smoke test only")
    ap.add_argument("--max-idx", type=int, default=None, help="smoke test only (e.g. --ds llm_v3 --max-idx 30 = dev)")
    a = ap.parse_args()
    smoke = a.allow_partial or a.max_idx is not None or a.ds != "llm_v3rep"
    if a.ds == "llm_v3rep":
        from evaluation_guard import refuse_completed
        refuse_completed("replication")
    if a.ds == "llm_v3" and (a.max_idx is None or a.max_idx > 30):
        from evaluation_guard import refuse_completed
        refuse_completed("headline")
    frozen = {f: hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16] for f in
              ("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json", "results/analysis/final_llm_v3_gpt-6.1-sol_test.json")}
    if not smoke:  # run-once lock (codex review_iter12 P2)
        os.makedirs("logs/final", exist_ok=True)
        os.mkdir("logs/final/REPLICATION_ONCE.lock")  # raises if it already ran; a rerun must be disclosed in SPLITS.md
    dev = json.loads(Path("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json").read_text())
    test = json.loads(Path("results/analysis/final_llm_v3_gpt-6.1-sol_test.json").read_text())
    th, w = dev["thresholds_dev_youden"], dev["fusion_w_text"]
    best = max(LLM_VIEWS, key=lambda v: test["point_ci"][v]["run_auroc"][0])
    labs, S, markup, ids = load(a.ds, a.auditor, a.max_idx)
    if not smoke:  # exact registered cohort (codex review_iter12 P3)
        want = {f"llm_v3rep_{i:04d}" for i in range(30)}
        assert set(ids) == set(labs) == want, f"cohort mismatch: {len(ids)} audited / {len(labs)} labelled"
        cnt = {c: sum(labs[r]["condition"] == c for r in ids) for c in ("private", "none", "legit")}
        assert cnt == {"private": 15, "none": 10, "legit": 5}, cnt
        for k in S:
            assert all(np.isfinite(S[k][r]["run"]) and all(np.isfinite(v) for v in S[k][r]["scores"].values()) for r in ids), k
    S["fusion"] = {r: {"scores": {p: w * S["text"][r]["scores"][p] + (1 - w) * S["action"][r]["scores"][p] for p in PAIRS},
                       "run": w * S["text"][r]["run"] + (1 - w) * S["action"][r]["run"]} for r in ids}
    b = boot(ids, S, labs, a.n_boot)
    con = b["contrasts"]
    con[f"premium-best[{best}]:run_auroc"] = _pd(ids, S, labs, "premium", best, "run_auroc", a.n_boot)
    con[f"premium-best[{best}]:within_market_auroc"] = _pd(ids, S, labs, "premium", best, "within_market_auroc", a.n_boot)
    groups = {"private_y1": [r for r in ids if labs[r]["y"]],
              "private_y0": [r for r in ids if labs[r]["condition"] == "private" and not labs[r]["y"]],
              "none": [r for r in ids if labs[r]["condition"] == "none"],
              "legit": [r for r in ids if labs[r]["condition"] == "legit"]}
    flag = {k: {g: wilson(sum(S[k][r]["run"] >= th[k] for r in rs), len(rs)) if rs and th.get(k) is not None else None
                for g, rs in groups.items()} for k in S}
    con["combined-action:run_auroc"] = _pd(ids, S, labs, "combined", "action", "run_auroc", a.n_boot)
    con["combined-action:within_market_auroc"] = _pd(ids, S, labs, "combined", "action", "within_market_auroc", a.n_boot)
    pc = b["point_ci"]
    pv = {"P1": pc["premium"]["run_auroc"][0] >= 0.85,
          "P2": pc["text"]["run_auroc"][1] is not None and pc["text"]["run_auroc"][1] <= 0.5 <= pc["text"]["run_auroc"][2],
          "P3": con[f"premium-best[{best}]:run_auroc"]["delta"] >= 0,
          "P4": (lambda c: c[0] is not None and c[0] <= 0 <= c[1])(con["combined-action:run_auroc"]["ci"])}
    out = {"dataset": a.ds, "auditor": a.auditor, "n_runs": len(ids), "group_n": {g: len(v) for g, v in groups.items()},
           "agreement_counts": {k: sum(labs[r]["agreement"] == k for r in labs) for k in sorted({labs[r]["agreement"] for r in labs})},
           "smoke": smoke, "frozen_input_sha256_16": frozen,
           "registered_contrasts": [f"premium-best[{best}]", "action_stats-action", "combined-action"],
           "note": "all other contrasts are exploratory (not pre-registered); P2/P4 = CI inclusion, not equivalence",
           "best_view_fixed_from_llm_v3_test": best, "fusion_w_text_dev": w,
           "point_ci": pc, "contrasts": con, "flag_rate_frozen_dev_thresholds": flag,
           "predictions": PREDICTIONS, "prediction_held": pv,
           "mean_markup": {g: round(float(np.mean([markup[r] for r in rs])), 2) if rs else None for g, rs in groups.items()}}
    Path("results/analysis").mkdir(parents=True, exist_ok=True)
    (Path("results/analysis") / (f"replication_{a.ds}" + ("_SMOKE" if smoke else "") + ".json")).write_text(json.dumps(out, indent=1))
    print(f"{a.ds}: n={len(ids)} groups {out['group_n']} agreement {out['agreement_counts']} best={best}")
    for k in S:
        print(f"{k:15s} run {pc[k]['run_auroc']} within {pc[k]['within_market_auroc']}  flag {flag[k]}")
    for c in sorted(con):
        if "run_auroc" in c or "within" in c:
            print(f"  {c:45s} {con[c]['delta']:+.3f} {con[c]['ci']}")
    print("predictions held:", pv)


if __name__ == "__main__":
    main()
