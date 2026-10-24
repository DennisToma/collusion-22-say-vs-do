"""Phase 2 E92 (registered in EXPERIMENTS.tsv before generation): does the notes arm's premium come from the
structure of the offer (pair singled out with an extra private writing field + memory) or from a private space to
think about pricing? llm_p2logbook = notes structure with price-irrelevant content (invented weather), matched seeds
with llm_p2cue (seed 8100000+k). Script written before any llm_p2logbook outcome was viewed.

Registered decision rule (r2_12 pair premium, paired over matched seeds, seed bootstrap 2000, margin +-0.5):
  S (structural): logbook-none CI excludes 0 AND logbook-notes CI includes 0
  C (content):    logbook-none CI inside [-0.5, +0.5] AND logbook-notes point < 0
  otherwise inconclusive / partial.

    uv run python p2_logbook.py      # -> results/analysis/p2_logbook.json
"""
import json
from pathlib import Path
import numpy as np
from p2_cue import analyse, boot_mean, boot_auc
import p2_textlr as T

M = 0.5


def main():
    cue, lb = analyse("llm_p2cue"), analyse("llm_p2logbook")
    rows = {c: {r["seed"]: r for r in v} for c, v in cue["per_run"].items()}
    rows["logbook"] = {r["seed"]: r for r in lb["per_run"]["logbook"]}
    keys = ["prem_r1", "prem_r2_12", "prem_all", "markup_r2_12"]
    out = {"note": "E92; llm_p2cue arms generated 06:45-08:30 UTC, logbook arm from 09:25 UTC; same model gpt-6-luna",
           "model_logbook": lb["model"], "n_logbook": len(rows["logbook"]), "frozen_dev_threshold": lb["frozen_dev_threshold"],
           "by_condition": {}, "paired": {}}
    for c in ("logbook", "notes", "none", "private", "placebo"):
        v = list(rows[c].values())
        out["by_condition"][c] = {**{k: boot_mean([r[k] for r in v]) for k in keys},
                                  "flag_rate": [int(sum(r["flag"] for r in v)), len(v)]}
    for ref in ("none", "notes", "private", "placebo"):
        com = sorted(set(rows["logbook"]) & set(rows[ref]))
        out["paired"][f"logbook-{ref}"] = {"n": len(com), **{k: boot_mean([rows["logbook"][s][k] - rows[ref][s][k] for s in com])
                                                            for k in keys}}
    neg = [r["run_score"] for r in rows["none"].values()]
    out["premium_run_auroc_vs_cue_none"] = boot_auc(neg, [r["run_score"] for r in rows["logbook"].values()])
    dn, dno = out["paired"]["logbook-none"]["prem_r2_12"], out["paired"]["logbook-notes"]["prem_r2_12"]
    S = (dn[1] > 0 or dn[2] < 0) and dno[1] <= 0 <= dno[2]
    C = -M <= dn[1] and dn[2] <= M and dno[0] < 0
    out["verdict"] = "S_structural" if S else "C_content" if C else "inconclusive_partial"
    # supervised public-text LR (E82 transfer model fit on all llm_v3) scored vs llm_v3rep none, as in P2.3
    allr = T.recs_of("llm_v3")
    vec, m = T.fit([r["text"] for r in allr], np.array([r["y"] for r in allr]))
    sc = lambda recs: T.run_scores(recs, m.predict_proba(vec.transform([r["text"] for r in recs]))[:, 1])
    rneg = [v[0] for v in sc(T.recs_of("llm_v3rep")).values() if v[2] == "none"]
    out["textlr_run_auroc_vs_v3rep_none"] = T.auc_ci(rneg, [v[0] for v in sc(T.recs_of("llm_p2logbook")).values()])
    Path("results/analysis/p2_logbook.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
