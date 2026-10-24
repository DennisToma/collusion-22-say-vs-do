"""Post-lock DESCRIPTIVE exploration (iter 13): how many rounds does the untrained pair-premium statistic need?
Architecture question behind the "stats always-on -> LLM audit" takeaway: if the premium separates colluding
markets after a few rounds, an always-on monitor can trigger audits early. Premium over rounds 1..k (prefix; k = 1..12)
and, as a check on the "opening round" effect, rounds 2..k. No fitting, no thresholds. Run AUROC (run score = max pair
premium) and within-market localisation AUROC (positive runs), 95% class-stratified run-bootstrap CIs (1000).
Uses the same label file / metrics as final_analysis.py. Not a pre-registered analysis; test runs were already
unlocked (headline done 00:03), so this does not touch the headline.

    uv run python early_detection.py --ds llm_v3            # all 125 runs (+ dev/test split rows)
    uv run python early_detection.py --ds llm_v3rep          # exploratory, after replication.py has run
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import PAIRS, load_jsonl
from final_analysis import AG, metrics, ci, idx


def prefix_premium(ds, k, start=0):
    P = {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        P.setdefault(r["run_id"], []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
    out = {}
    for rid, rows in P.items():
        rows.sort(key=lambda t: t[0])
        pr = {a: np.array([d[a] for _, d in rows[start:k]], float) for a in AG}
        sc = {}
        for p in PAIRS:
            o = [a for a in AG if a not in p]
            sc[p] = float(((pr[p[0]] + pr[p[1]]) / 2).mean() - np.mean([pr[a] for a in o], axis=0).mean())
        out[rid] = {"scores": sc, "run": max(sc.values())}
    return out


def evaluate(ids, S, labs, nb=1000, seed=0):
    rng = np.random.default_rng(seed)
    pt = metrics(ids, S, labs)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    bs = [metrics(list(rng.choice(P, len(P))) + list(rng.choice(N, len(N))), S, labs) for _ in range(nb)]
    return {k: {m: [round(pt[k][m], 4)] + ci([b[k][m] for b in bs]) for m in ("run_auroc", "within_market_auroc")}
            for k in pt}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--nboot", type=int, default=1000)
    a = ap.parse_args()
    labs = {r["run_id"]: dict(r, y=int(r["agreement"] in ("explicit", "info_exchange")))  # same y as final_analysis
            for r in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    T = max(r["round"] for r in load_jsonl(Path("data") / a.ds / "trajectories.jsonl")) + 1
    S = {}
    for k in range(1, T + 1):
        S[f"r1-{k}"] = prefix_premium(a.ds, k)
        if k >= 2:
            S[f"r2-{k}"] = prefix_premium(a.ds, k, start=1)
    ids = sorted(r for r in labs if all(r in s for s in S.values()))
    splits = {"all": ids}
    if a.ds == "llm_v3":
        splits["dev"] = [r for r in ids if idx(r) < 30]
        splits["test"] = [r for r in ids if idx(r) >= 30]
    out = {"ds": a.ds, "rounds": T, "n": {s: len(v) for s, v in splits.items()},
           "n_pos": {s: sum(labs[r]["y"] for r in v) for s, v in splits.items()},
           "results": {s: evaluate(v, S, labs, a.nboot) for s, v in splits.items()}}
    dst = Path("results/analysis") / f"early_detection_{a.ds}.json"
    dst.write_text(json.dumps(out, indent=1))
    print("wrote", dst, out["n"], out["n_pos"])
    for s, R in out["results"].items():
        print(f"== {s}")
        for k, v in R.items():
            print(f"  {k:6s} run {v['run_auroc'][0]:.2f} [{v['run_auroc'][1]:.2f},{v['run_auroc'][2]:.2f}]"
                  f"  within {v['within_market_auroc'][0]:.2f} [{v['within_market_auroc'][1]:.2f},{v['within_market_auroc'][2]:.2f}]")


if __name__ == "__main__":
    main()
