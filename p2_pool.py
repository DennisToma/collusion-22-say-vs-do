"""Phase 2 directive 2 (E101, post-hoc pooling of two registered fresh splits; disclosed as such): the Q2.2 headline
contrast Delta_hybrid[v] = v - max(text, action) (run AUROC) on llm_v3rep + llm_p2rep pooled (n = 90), with frozen
auditor outputs and frozen statistics (nothing refit). Two labels:
  condition/judge label (labels.jsonl y, as in replication.py) -> final_analysis.boot (class-stratified bootstrap)
  followed label (p2_behaviour classes, E84 negatives) -> paired bootstrap over followed / negative runs
Bootstrap additionally stratified by dataset is not done (class-stratified only); dataset counts are reported.

    uv run python p2_pool.py      # -> results/analysis/p2_pool_rep.json
"""
import json
from pathlib import Path
import numpy as np
from final_analysis import boot
from monitor_stratum import load
from p2_behaviour import terms, classes

DS = ["llm_v3rep", "llm_p2rep"]
NEG = ("none", "legit", "no_agreement", "not_followed", "trivial_floor")
HYB = ["combined", "combined_stats", "action_stats", "structured"]


def main():
    labs, S, ids, C = {}, {}, [], {}
    for ds in DS:
        l, s, _, i = load(ds, "gpt-6.1-sol")
        labs.update(l); ids += i
        for k, v in s.items():
            S.setdefault(k, {}).update(v)
        C.update(classes(ds, terms(ds)))
    S = {k: v for k, v in S.items() if all(r in v for r in ids)}
    b = boot(ids, S, labs, 2000)
    cond = {f"delta_hybrid[{v}]": b["contrasts"][f"delta_hybrid[{v}]:run_auroc"] for v in HYB if f"delta_hybrid[{v}]:run_auroc" in b["contrasts"]}
    run = {k: S[k] for k in S}
    sc = {k: {r: run[k][r]["run"] for r in ids} for k in run}
    P = [r for r in ids if C[r]["cls"] == "followed"]; N = [r for r in ids if C[r]["cls"] in NEG]
    au = lambda k, P_, N_: float(np.mean([(sc[k][p] > sc[k][q]) + .5 * (sc[k][p] == sc[k][q]) for p in P_ for q in N_]))
    rng = np.random.default_rng(1)
    boots = [(list(rng.choice(P, len(P))), list(rng.choice(N, len(N)))) for _ in range(1000)]
    fol, fol_au = {}, {}
    for k in sc:
        B = [au(k, p_, n_) for p_, n_ in boots]
        fol_au[k] = [round(au(k, P, N), 3), round(float(np.percentile(B, 2.5)), 3), round(float(np.percentile(B, 97.5)), 3)]
    for v in [k for k in HYB if k in sc]:
        d = lambda P_, N_: au(v, P_, N_) - max(au("text", P_, N_), au("action", P_, N_))
        B = [d(p_, n_) for p_, n_ in boots]
        fol[f"delta_hybrid[{v}]"] = [round(d(P, N), 3), round(float(np.percentile(B, 2.5)), 3), round(float(np.percentile(B, 97.5)), 3)]
    out = {"datasets": DS, "n": len(ids), "n_by_ds": {ds: sum(r.startswith(ds + "_") for r in ids) for ds in DS},
           "condition_label": {"n_pos": sum(labs[r]["y"] for r in ids),
                               "run_auroc": {k: b["point_ci"][k]["run_auroc"] for k in b["point_ci"]}, "contrasts": cond},
           "followed_label": {"n_followed": len(P), "n_neg": len(N),
                              "class_counts": {c: sum(C[r]["cls"] == c for r in ids) for c in sorted({C[r]["cls"] for r in ids})},
                              "run_auroc": fol_au, "contrasts": fol},
           "note": "post-hoc pooling of two registered fresh splits (E101); class-stratified bootstrap; frozen auditors/statistics"}
    Path("results/analysis/p2_pool_rep.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
