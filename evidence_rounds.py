"""Post-lock DESCRIPTIVE (iter 14): do the LLM auditors look where the signal is? The pair premium is largest in round 1
(set before any private message is read; round1_effect.py). Per view: share of cited evidence items in round 1 (uniform
chance = 1/12), share of audits of y=1 runs that cite round 1 at all, mean cited round, and the Spearman correlation of
the auditor's run score (collusion_present, as in the headline) with the round-1 premium vs the rounds-2..12 premium (max over the 6 pairs,
as in the premium run score). Bootstrap CI over runs.

    uv run python evidence_rounds.py --ds llm_v3 --split test   # -> results/analysis/evidence_rounds_<ds>_<split>.json
"""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from analyze_llm import load_jsonl
from final_analysis import LLM_VIEWS, idx, DEV_MAX, premium_scores


def bci(f, n_runs, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    b = [f(rng.integers(0, n_runs, n_runs)) for _ in range(n)]
    b = [x for x in b if x == x]
    return [round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3"); ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--split", default="test", choices=["dev", "test", "all"])
    a = ap.parse_args()
    labs = {x["run_id"]: int(x["agreement"] in ("explicit", "info_exchange"))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    keep = lambda r: a.split == "all" or (idx(r) < DEV_MAX) == (a.split == "dev")
    p1, _ = premium_scores_window(a.ds, 0, 1)
    p2, _ = premium_scores_window(a.ds, 1, None)
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    out = {"ds": a.ds, "split": a.split, "auditor": a.auditor, "chance_round1_share": round(1 / 12, 3), "views": {}}
    for v in LLM_VIEWS:
        rows = [x for x in load_jsonl(d / f"{v}_orig.jsonl") if x["run_id"] in labs and keep(x["run_id"])]
        if not rows:
            continue
        rounds = [[int(e["round"]) for e in (x.get("evidence") or []) if str(e.get("round", "")).lstrip("-").isdigit()]
                  for x in rows]
        y = np.array([labs[x["run_id"]] for x in rows])
        s = np.array([x["collusion_present"] for x in rows], float)  # headline run score (final_analysis.py)
        r1 = np.array([p1[x["run_id"]]["run"] for x in rows]); r2 = np.array([p2[x["run_id"]]["run"] for x in rows])
        n = len(rows)
        share1 = lambda I: (sum(sum(t == 1 for t in rounds[i]) for i in I) / max(1, sum(len(rounds[i]) for i in I)))
        pos = [i for i in range(n) if y[i] == 1]
        any1 = lambda I: float(np.mean([1 in rounds[i] for i in I])) if len(I) else float("nan")
        sp = lambda I, z: spearmanr(s[I], z[I])[0] if len(set(s[I])) > 1 else float("nan")
        allI = np.arange(n)
        out["views"][v] = {
            "n_runs": n, "n_items": int(sum(map(len, rounds))),
            "round1_item_share": [round(share1(allI), 3), *bci(share1, n)],
            "round1_item_share_y1": round(share1(pos), 3),
            "audits_citing_round1_y1": round(any1(pos), 3),
            "audits_citing_round1_y0": round(any1([i for i in range(n) if y[i] == 0]), 3),
            "mean_cited_round": round(float(np.mean([t for R in rounds for t in R])), 2),
            "spearman_score_vs_round1_premium": [round(float(sp(allI, r1)), 3), *bci(lambda I: sp(I, r1), n)],
            "spearman_score_vs_rounds2_12_premium": [round(float(sp(allI, r2)), 3), *bci(lambda I: sp(I, r2), n)],
        }
    Path(f"results/analysis/evidence_rounds_{a.ds}_{a.split}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


def premium_scores_window(ds, start, stop):
    """premium_scores restricted to rounds[start:stop] (0-based)."""
    import final_analysis as F
    P = {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        P.setdefault(r["run_id"], []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
    out = {}
    for rid, rows in P.items():
        rows.sort(key=lambda t: t[0])
        pr = {g: np.array([d[g] for _, d in rows[start:stop]], float) for g in F.AG}
        sc = {p: float(((pr[p[0]] + pr[p[1]]) / 2).mean() - np.mean([pr[g] for g in F.AG if g not in p], axis=0).mean())
              for p in F.PAIRS}
        out[rid] = {"scores": sc, "run": max(sc.values())}
    return out, None


if __name__ == "__main__":
    main()
