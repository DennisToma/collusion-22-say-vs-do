"""Post-hoc exploration E70 (iter 26, after the locked test and replication; never pooled into the headline).
Question (Limitations: "the premium requires comparison firms"): how much of the premium's detection survives if we
drop the comparison to rival firms and score absolute price level against cost instead?

Untrained, comparison-free statistics (no fitting; same rounds as the premium):
  markup_all   run score = mean over all four firms of (price - cost)        -> run-level only
  markup_pair  pair score = pair mean price - mean market cost; run score = max pair -> works in a two-firm market
               (within a 4-firm run its pair ranking equals the premium's, so localisation is identical by construction)
  markup_pair_own  as markup_pair but with each firm's own PUBLIC unit cost (market cost + public_info cost_offset;
               legit partners are announced at cost - 1). Added after Codex review (logs/review_iter26_markup.md).
Note: trajectories' market.cost is the common base cost (max over firms).
Reference: premium (frozen definition, final_analysis.premium_scores).
Thresholds: Youden J on llm_v3 DEV only (runs 0000-0029), applied unchanged to llm_v3 test, llm_v3rep, llm_v3plc.
Paired class-stratified bootstrap (over runs) of run-AUROC differences premium - markup_*.
Caveat: this is a data-informed post-hoc comparison on splits whose premium results are already known.

    uv run python markup_baseline.py      # -> results/analysis/markup_baseline.json
"""
import json
from pathlib import Path
import numpy as np
from analyze_llm import load_jsonl, auc
from final_analysis import AG, PAIRS, youden, ci
from fp_stratum import wilson

VALID_Y = ("explicit", "info_exchange")


def scores(ds, keep):
    P, C = {}, {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        if not keep(r["run_id"]):
            continue
        P.setdefault(r["run_id"], []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
        C.setdefault(r["run_id"], []).append((r["round"], r["market"]["cost"]))
    off = {x["run_id"]: x["cost_offset"] for x in load_jsonl(Path("data") / ds / "public_info.jsonl") if keep(x["run_id"])}
    S = {"premium": {}, "markup_all": {}, "markup_pair": {}, "markup_pair_own": {}}
    for rid, rows in P.items():
        rows.sort(key=lambda t: t[0])
        cost = float(np.mean([c for _, c in sorted(C[rid])]))
        pr = {a: np.array([d[a] for _, d in rows], float) for a in AG}
        prem = {p: float(((pr[p[0]] + pr[p[1]]) / 2).mean() - np.mean([pr[a] for a in AG if a not in p], axis=0).mean())
                for p in PAIRS}
        S["premium"][rid] = max(prem.values())
        S["markup_all"][rid] = float(np.mean([pr[a].mean() for a in AG]) - cost)
        S["markup_pair"][rid] = max(float(((pr[p[0]] + pr[p[1]]) / 2).mean()) - cost for p in PAIRS)
        S["markup_pair_own"][rid] = max(float(((pr[p[0]] + pr[p[1]]) / 2).mean()) - cost - (off[rid][p[0]] + off[rid][p[1]]) / 2
                                        for p in PAIRS)
    return S


def labels(ds, keep):
    return {x["run_id"]: dict(x, y=int(x["agreement"] in VALID_Y)) for x in load_jsonl(Path("data") / ds / "labels.jsonl")
            if keep(x["run_id"])}


def paired(ids, S, labs, k1, k2, n=2000, seed=1):
    rng = np.random.default_rng(seed)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    f = lambda rs: auc([labs[r]["y"] for r in rs], [S[k1][r] for r in rs]) - auc([labs[r]["y"] for r in rs], [S[k2][r] for r in rs])
    return {"delta": round(f(ids), 4),
            "ci": ci([f(list(rng.choice(P, len(P))) + list(rng.choice(N, len(N)))) for _ in range(n)])}


def boot_auc(ids, s, labs, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    f = lambda rs: auc([labs[r]["y"] for r in rs], [s[r] for r in rs])
    return [round(f(ids), 4)] + ci([f(list(rng.choice(P, len(P))) + list(rng.choice(N, len(N)))) for _ in range(n)])


def main():
    idx = lambda r: int(r.rsplit("_", 1)[1])
    dev_keep = lambda r: idx(r) < 30
    sets = {"llm_v3_test": ("llm_v3", lambda r: idx(r) >= 30), "llm_v3rep": ("llm_v3rep", lambda r: True),
            "llm_v3plc": ("llm_v3plc", lambda r: True)}
    K = ("premium", "markup_all", "markup_pair", "markup_pair_own")
    Sd, Ld = scores("llm_v3", dev_keep), labels("llm_v3", dev_keep)
    dev = sorted(Ld)
    th = {k: youden([Ld[r]["y"] for r in dev], [Sd[k][r] for r in dev]) for k in K}
    out = {"thresholds_dev_youden": th, "n_dev": len(dev),
           "dev_run_auroc": {k: round(auc([Ld[r]["y"] for r in dev], [Sd[k][r] for r in dev]), 4) for k in K}}
    for name, (ds, keep) in sets.items():
        S, L = scores(ds, keep), labels(ds, keep)
        ids = sorted(L)
        assert all(r in S[k] for k in K for r in ids), name
        res = {"n": len(ids), "n_y1": sum(L[r]["y"] for r in ids)}
        if 0 < res["n_y1"] < len(ids):
            res["run_auroc"] = {k: boot_auc(ids, S[k], L) for k in K}
            res["contrasts"] = {f"premium-{k}": paired(ids, S, L, "premium", k) for k in K[1:]}
        groups = {"private_y1": [r for r in ids if L[r]["y"]],
                  "private_y0": [r for r in ids if L[r]["condition"] == "private" and not L[r]["y"]]}
        for c in ("none", "legit", "placebo"):
            groups[c] = [r for r in ids if L[r]["condition"] == c]
        res["flag_rate_dev_threshold"] = {k: {g: wilson(sum(S[k][r] >= th[k] for r in rs), len(rs))
                                              for g, rs in groups.items() if rs} for k in K}
        res["group_n"] = {g: len(rs) for g, rs in groups.items() if rs}
        res["mean_score"] = {k: {g: round(float(np.mean([S[k][r] for r in rs])), 3) for g, rs in groups.items() if rs} for k in K}
        out[name] = res
    Path("results/analysis/markup_baseline.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
