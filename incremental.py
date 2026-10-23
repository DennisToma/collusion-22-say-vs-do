"""Does an LLM auditor view add information BEYOND the always-on pair premium? (iter 7, pre-registered before any
test look; DIRECTION directive 4 'architecture takeaway'.)

Combination is UNTRAINED and label-free: within the evaluated split, each scorer's pair scores and run scores are
turned into percentile ranks (pooled over the split's runs, no labels); combo[v] = (rank(premium) + rank(v)) / 2.
Compared with premium alone on identical runs: run AUROC, within-market AUROC, pair-ID; paired class-stratified
bootstrap over runs (n = runs). Plus complementarity counts on y=1 runs: premium's top pair wrong but view's right,
and vice versa (tie-aware).

    uv run python incremental.py --split dev
    uv run python incremental.py --split test     # once, in finalize_test.sh
"""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.stats import rankdata
from analyze_llm import PAIRS, load_jsonl
from final_analysis import LLM_VIEWS, DEV_MAX, idx, premium_scores, metrics, ci


def pct_rank(R, ids):
    """label-free percentile ranks of pair scores (pooled over ids x pairs) and of run scores (over ids)"""
    ps = rankdata([R[r]["scores"][p] for r in ids for p in PAIRS]) / (6 * len(ids))
    rs = rankdata([R[r]["run"] for r in ids]) / len(ids)
    return {r: {"scores": {p: float(ps[6 * i + j]) for j, p in enumerate(PAIRS)}, "run": float(rs[i])}
            for i, r in enumerate(ids)}


def top_ok(sc, ap):
    top = [p for p in PAIRS if sc[p] == max(sc.values())]
    return (ap in top) / len(top)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--split", required=True, choices=["dev", "test"])
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--allow-partial", action="store_true")
    a = ap.parse_args()
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    S = {v: {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in load_jsonl(d / f"{v}_orig.jsonl")}
         for v in LLM_VIEWS}
    S["premium"], _ = premium_scores(a.ds)
    want = [r for r in sorted(labs) if (idx(r) < DEV_MAX) == (a.split == "dev")]
    ids = [r for r in want if all(r in R for R in S.values())]
    if not a.allow_partial:
        assert len(ids) == len(want), f"incomplete: {len(ids)}/{len(want)} runs have all views"
    rk = {k: pct_rank(R, ids) for k, R in S.items()}
    C = {"premium": rk["premium"]}
    for v in LLM_VIEWS:
        C[f"combo[{v}]"] = {r: {"scores": {p: (rk["premium"][r]["scores"][p] + rk[v][r]["scores"][p]) / 2 for p in PAIRS},
                                "run": (rk["premium"][r]["run"] + rk[v][r]["run"]) / 2} for r in ids}
    pt = metrics(ids, C, labs)
    rng = np.random.default_rng(0)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    bs = [metrics(list(rng.choice(P, len(P))) + list(rng.choice(N, len(N))), C, labs) for _ in range(a.boot)]
    M = ("run_auroc", "within_market_auroc", "pair_id_acc")
    out = {"dataset": a.ds, "auditor": a.auditor, "split": a.split, "n_runs": len(ids), "n_pos": len(P),
           "method": "untrained label-free percentile-rank average of premium and each LLM view; paired class-stratified "
                     "run bootstrap vs premium alone",
           "point_ci": {k: {m: [round(pt[k][m], 4)] + ci([b[k][m] for b in bs]) for m in M} for k in C},
           "combo_minus_premium": {v: {m: {"delta": round(pt[f"combo[{v}]"][m] - pt["premium"][m], 4),
                                           "ci": ci([b[f"combo[{v}]"][m] - b["premium"][m] for b in bs])} for m in M}
                                   for v in LLM_VIEWS}}
    comp = {}
    for v in LLM_VIEWS:
        a_only = b_only = both_wrong = 0.0
        for r in P:
            apr = "".join(labs[r]["assigned_pair"])
            pp, vv = top_ok(S["premium"][r]["scores"], apr), top_ok(S[v][r]["scores"], apr)
            a_only += pp * (1 - vv); b_only += vv * (1 - pp); both_wrong += (1 - pp) * (1 - vv)
        comp[v] = {"premium_right_view_wrong": round(a_only, 2), "view_right_premium_wrong": round(b_only, 2),
                   "both_wrong": round(both_wrong, 2), "n_y1": len(P)}
    out["pair_id_complementarity_y1"] = comp
    o = Path("results/analysis") / f"incremental_{a.ds}_{a.auditor}_{a.split}.json"
    o.write_text(json.dumps(out, indent=1))
    print(f"{a.split}: n={len(ids)} ({len(P)} y=1)")
    for k in C:
        print(f"  {k:22s} " + "  ".join(f"{m[:6]} {pt[k][m]:.3f}" for m in M))
    for v in LLM_VIEWS:
        print(f"  combo[{v}]-premium: " + "  ".join(f"{m[:6]} {out['combo_minus_premium'][v][m]['delta']:+.3f} "
                                                     f"{out['combo_minus_premium'][v][m]['ci']}" for m in M)
              + f"  | pair-ID view-only-right {comp[v]['view_right_premium_wrong']}, premium-only-right {comp[v]['premium_right_view_wrong']}")
    print("->", o)


if __name__ == "__main__":
    main()
