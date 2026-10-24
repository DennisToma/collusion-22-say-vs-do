"""E100 registered comparison: abliterated vs base Qwen3.8-27B sellers (lab prompt, T=12, matched private/none).

Reads p2_strong.py output (list of per-dataset dicts, incl. per-run records) and computes the three registered contrasts,
abliterated minus base:
  P1 judge-agreement rate among private runs   -> difference with Newcombe hybrid-score 95% CI (Wilson per arm)
  P2 executed rate among private runs          -> same
  P3 mean paired premium (private - none, same seed) -> difference, seed bootstrap 95% CI (10k, independent arms)
'supported' only if the CI excludes 0 in the predicted direction (>= 0), as registered.

    uv run python p2_qwen_cmp.py [--inp results/analysis/p2_qwen.json] [--base llm_p2qwenb --abl llm_p2qwena]
"""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.stats import norm


def wilson(k, n, z=norm.ppf(.975)):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def newcombe(k1, n1, k0, n0):
    """Difference p1 - p0 with Newcombe (1998) method 10 hybrid score interval."""
    p1, p0 = k1 / n1, k0 / n0
    l1, u1 = wilson(k1, n1); l0, u0 = wilson(k0, n0)
    d = p1 - p0
    return [round(float(d), 3), round(float(d - np.sqrt((p1 - l1) ** 2 + (u0 - p0) ** 2)), 3),
            round(float(d + np.sqrt((u1 - p1) ** 2 + (p0 - l0) ** 2)), 3)]


def paired_premiums(res):
    seeds = {}
    for e in res["runs"].values():
        seeds.setdefault(e["seed"], {})[e["cond"]] = e["pair_premium"]
    return np.array([s["private"] - s["none"] for s in seeds.values() if {"private", "none"} <= set(s)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", default="results/analysis/p2_qwen.json")
    ap.add_argument("--base", default="llm_p2qwenb"); ap.add_argument("--abl", default="llm_p2qwena")
    ap.add_argument("--out", default="results/analysis/p2_qwen_cmp.json")
    a = ap.parse_args()
    R = {r["ds"]: r for r in json.loads(Path(a.inp).read_text())}
    b, x = R[a.base], R[a.abl]
    out = {"base": a.base, "abliterated": a.abl, "excluded_fallback": {a.base: b["excluded_fallback_runs"], a.abl: x["excluded_fallback_runs"]}}
    for key, f in [("P1_agreement_rate", "n_agreed"), ("P2_executed_rate", "n_executed")]:
        d = newcombe(x[f], x["n_private"], b[f], b["n_private"])
        out[key] = {"abliterated": [x[f], x["n_private"]], "base": [b[f], b["n_private"]], "diff_newcombe95": d,
                    "supported": bool(d[1] > 0)}
    pb, px = paired_premiums(b), paired_premiums(x)
    rng = np.random.default_rng(0)
    boots = [rng.choice(px, len(px)).mean() - rng.choice(pb, len(pb)).mean() for _ in range(10000)]
    d = float(px.mean() - pb.mean())
    out["P3_paired_premium"] = {"abliterated": [round(float(px.mean()), 2), len(px)], "base": [round(float(pb.mean()), 2), len(pb)],
                                "diff_boot95": [round(d, 2), round(float(np.percentile(boots, 2.5)), 2), round(float(np.percentile(boots, 97.5)), 2)]}
    out["P3_paired_premium"]["supported"] = bool(out["P3_paired_premium"]["diff_boot95"][1] > 0)
    for k in ("mean_market_excess_nash", "mean_market"):
        out[k] = {a.base: b[k], a.abl: x[k]}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)); print("->", a.out)


if __name__ == "__main__":
    main()
