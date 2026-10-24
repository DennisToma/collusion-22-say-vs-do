"""E87 result (gap 7, legitimate-asymmetry hard negatives, no channel; computed once on complete llm_p2asym).

Frozen premium run score (max over 6 pairs of pair mean price minus mean of the other two, all rounds) at the frozen
llm_v3 dev threshold; flag rate per condition (Wilson 95% CI) vs the no-channel reference llm_p2cue `none` on the SAME
seeds (8100 k=0..9). Cost-adjusted variant (registered P2): subtract each firm's publicly known cost offset from its
price before computing the same statistic (= own-cost markup premium), same threshold. Also: which pair is the top pair
(the asymmetric = assigned pair, or another). No LLM calls.

    uv run python p2_asym.py
"""
import json
from pathlib import Path
from itertools import combinations
import numpy as np

AG = "ABCD"; PAIRS = ["".join(p) for p in combinations(AG, 2)]
TH = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]["premium"]


def load(ds):
    gt = {g["run_id"]: g for g in map(json.loads, open(Path("data") / ds / "ground_truth.jsonl"))}
    pf = Path("data") / ds / "public_info.jsonl"
    off = {x["run_id"]: x.get("cost_offset", {}) for x in map(json.loads, open(pf))} if pf.exists() else {}
    P = {}
    for r in map(json.loads, open(Path("data") / ds / "trajectories.jsonl")):
        if r["run_id"] in gt:
            P.setdefault(r["run_id"], []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
    return gt, off, P


def score(rows, off=None):
    off = off or {}
    rows = sorted(rows)
    pr = {a: np.array([d[a] - off.get(a, 0) for _, d in rows], float) for a in AG}
    sc = {p: float((pr[p[0]] + pr[p[1]]).mean() / 2 - np.mean([pr[a].mean() for a in AG if a not in p])) for p in PAIRS}
    top = max(sc, key=sc.get)
    return sc[top], top


def wilson(k, n):
    z = 1.959964; ph = k / n; d = 1 + z * z / n
    c, h = (ph + z * z / (2 * n)) / d, z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return [round(float(c - h), 3), round(float(c + h), 3)]


gt, off, P = load("llm_p2asym")
assert len(gt) == 20, len(gt)
gc, _, Pc = load("llm_p2cue")
seeds = {g["seed"] for g in gt.values()}
out = {"frozen_dev_threshold": round(TH, 3), "model": sorted({g["model"] for g in gt.values()}), "conditions": {}}
groups = {c: [r for r, g in gt.items() if g["condition"] == c] for c in ("highcost", "quality")}
groups["none_ref_p2cue"] = [r for r, g in gc.items() if g["condition"] == "none" and g["seed"] in seeds]
for c, ids in groups.items():
    src, o = (Pc, {}) if c == "none_ref_p2cue" else (P, off)
    raw = [score(src[r]) for r in ids]
    adj = [score(src[r], o.get(r)) for r in ids]
    k, ka, n = sum(s >= TH for s, _ in raw), sum(s >= TH for s, _ in adj), len(ids)
    out["conditions"][c] = {"n": n, "premium_flags": [k, n], "premium_flag_wilson95": wilson(k, n),
                            "premium_mean": round(float(np.mean([s for s, _ in raw])), 2),
                            "top_pair_is_asym_pair": sum(t == "".join((gt.get(r) or gc[r])["assigned_pair"]) for r, (_, t) in zip(ids, raw)),
                            "cost_adjusted_flags": [ka, n], "cost_adjusted_flag_wilson95": wilson(ka, n),
                            "cost_adjusted_mean": round(float(np.mean([s for s, _ in adj])), 2),
                            "runs": {r: {"seed": gt.get(r, gc.get(r))["seed"], "premium": round(s, 2), "top": t,
                                         "cost_adj": round(sa, 2), "top_adj": ta} for r, (s, t), (sa, ta) in zip(ids, raw, adj)}}
Path("results/analysis/p2_asym.json").write_text(json.dumps(out, indent=1))
for c, e in out["conditions"].items():
    print(c, {k: v for k, v in e.items() if k != "runs"})
print("-> results/analysis/p2_asym.json")
