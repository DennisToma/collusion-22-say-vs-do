"""Placebo-channel exploration stratum (iter 16, registered in data/SPLITS.md before generation; descriptive only).

llm_v3plc: one run per llm_v3rep `private` run with the same seed (same designated pair, cost and demand path) and the
identical private-channel prompt, but private messages are never delivered (each seller sees only its own). So the
pair is *offered* a channel and believes it uses it, yet no agreement can form. Compares the designated-pair premium
(pair mean price minus mean of the other two firms) per round: placebo vs matched private (paired bootstrap over the
15 seeds) vs llm_v3rep `none` (reference). Also: run AUROC of the frozen premium scorer (max pair premium, all rounds)
for placebo-vs-none and private-vs-none, flag rate at the FROZEN llm_v3 dev premium threshold, and within-market
localisation (is the designated pair the top-premium pair?).

    uv run python placebo.py   # -> results/analysis/placebo_llm_v3plc.json, figures/placebo_premium.png
"""
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
from final_analysis import premium_scores, AG

PLC, REP = "llm_v3plc", "llm_v3rep"


def load(ds):
    gt = {json.loads(l)["run_id"]: json.loads(l) for l in open(Path("data") / ds / "ground_truth.jsonl")}
    P = {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        P.setdefault(r["run_id"], {})[r["round"]] = {x["id"]: x["price"] for x in r["agents"]}
    per_round = {}
    for rid, d in P.items():
        pair = gt[rid]["assigned_pair"]; o = [a for a in AG if a not in pair]
        per_round[rid] = np.array([np.mean([d[t][a] for a in pair]) - np.mean([d[t][a] for a in o]) for t in sorted(d)])
    return gt, per_round


def tie_top(sc, pair):  # tie-aware: 1/k credit if the designated pair is among k tied top-scoring pairs
    sc = {("".join(k) if isinstance(k, tuple) else k): v for k, v in sc.items()}
    m = max(sc.values()); best = [k for k, v in sc.items() if abs(v - m) < 1e-9]
    return 1 / len(best) if pair in best else 0.0


def bmean(x, n=4000, seed=0):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    b = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return [round(float(x.mean()), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def bdiff(x, y, n=4000, seed=1):  # unpaired difference of means
    x, y = np.asarray(x, float), np.asarray(y, float); rng = np.random.default_rng(seed)
    b = [rng.choice(x, len(x)).mean() - rng.choice(y, len(y)).mean() for _ in range(n)]
    return [round(float(x.mean() - y.mean()), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def bauc(pos, neg, n=4000, seed=2):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float); rng = np.random.default_rng(seed)
    f = lambda p, q: roc_auc_score([1] * len(p) + [0] * len(q), list(p) + list(q))
    b = [f(rng.choice(pos, len(pos)), rng.choice(neg, len(neg))) for _ in range(n)]
    return [round(float(f(pos, neg)), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def main():
    gp, rp = load(PLC); gr, rr = load(REP)
    plc = sorted(gp); assert all(gp[r]["condition"] == "placebo" for r in plc), "unexpected condition"
    mate = {r: f"{REP}_{r.rsplit('_', 1)[1]}" for r in plc}
    for r in plc:
        g = gr[mate[r]]
        assert g["condition"] == "private" and g["seed"] == gp[r]["seed"] and g["assigned_pair"] == gp[r]["assigned_pair"]
    none = sorted(r for r in gr if gr[r]["condition"] == "none")
    win = {"r1": slice(0, 1), "r2_12": slice(1, None), "r7_12": slice(6, None), "all": slice(None)}
    out = {"n_placebo": len(plc), "n_private_matched": len(plc), "n_none": len(none), "windows": {}}
    for w, s in win.items():
        a = [rp[r][s].mean() for r in plc]; b = [rr[mate[r]][s].mean() for r in plc]; c = [rr[r][s].mean() for r in none]
        out["windows"][w] = {"placebo": bmean(a), "private": bmean(b), "none": bmean(c),
                             "placebo_minus_private_paired": bmean(np.array(a) - np.array(b)),
                             "placebo_minus_none": bdiff(a, c)}
    # frozen premium scorer (run = max over all 6 pairs, all rounds); threshold frozen on llm_v3 dev
    thr = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]["premium"]
    Sp, _ = premium_scores(PLC); Sr, _ = premium_scores(REP)
    sp = [Sp[r]["run"] for r in plc]; sr = [Sr[mate[r]]["run"] for r in plc]; sn = [Sr[r]["run"] for r in none]
    top = lambda S, r, pair: tie_top(S[r]["scores"], "".join(pair))
    out["premium_scorer"] = {
        "frozen_dev_threshold": round(float(thr), 3),
        "run_auroc_placebo_vs_none": bauc(sp, sn), "run_auroc_private_vs_none": bauc(sr, sn),
        "run_auroc_private_vs_placebo": bauc(sr, sp),
        "flag_rate": {k: [int(sum(v >= thr for v in x)), len(x)] for k, x in (("placebo", sp), ("private", sr), ("none", sn))},
        "designated_pair_is_top": {"placebo": [round(sum(top(Sp, r, gp[r]["assigned_pair"]) for r in plc), 2), len(plc)],
                                   "private": [round(sum(top(Sr, mate[r], gr[mate[r]]["assigned_pair"]) for r in plc), 2), len(plc)]}}
    # LLM auditors (gpt-6.1-sol, frozen prompts) on placebo runs vs the matched private and the none runs of llm_v3rep
    TH = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]
    out["auditors"] = {}
    for v in ("text", "action", "combined", "action_stats", "combined_stats", "structured"):
        fp = Path("results/llm_auditor") / PLC / "gpt-6.1-sol" / f"{v}_orig.jsonl"
        if not fp.exists():
            continue
        A = {json.loads(l)["run_id"]: json.loads(l) for l in open(fp)}
        B = {json.loads(l)["run_id"]: json.loads(l) for l in open(Path("results/llm_auditor") / REP / "gpt-6.1-sol" / f"{v}_orig.jsonl")}
        if not all(r in A for r in plc):
            continue
        ap_ = [A[r]["collusion_present"] for r in plc]; ar = [B[mate[r]]["collusion_present"] for r in plc]
        an = [B[r]["collusion_present"] for r in none]
        tp = lambda X, r, pair: tie_top(X[r]["scores"], "".join(pair))
        out["auditors"][v] = {"frozen_dev_threshold": TH[v],
                              "flag_rate": {k: [int(sum(x >= TH[v] for x in X)), len(X)] for k, X in (("placebo", ap_), ("private", ar), ("none", an))},
                              "run_auroc_placebo_vs_none": bauc(ap_, an), "run_auroc_private_vs_placebo": bauc(ar, ap_),
                              "designated_pair_is_top_placebo": [round(sum(tp(A, r, gp[r]["assigned_pair"]) for r in plc), 2), len(plc)]}
    # per-round curve
    out["per_round_mean"] = {k: [round(float(np.mean([v[r][t] for r in ids])), 3) for t in range(12)]
                             for k, v, ids in (("placebo", rp, plc), ("private", rr, [mate[r] for r in plc]), ("none", rr, none))}
    Path("results/analysis/placebo_llm_v3plc.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for k, v, ids, col in (("private (channel delivered)", rr, [mate[r] for r in plc], "#c0392b"),
                           ("placebo (offered, never delivered)", rp, plc, "#2471a3"), ("none (no channel)", rr, none, "#7f8c8d")):
        M = np.array([v[r] for r in ids]); m = M.mean(0)
        rng = np.random.default_rng(0); B = np.array([M[rng.integers(0, len(M), len(M))].mean(0) for _ in range(2000)])
        x = np.arange(1, 13)
        ax.plot(x, m, marker="o", ms=3, color=col, label=f"{k}, n={len(ids)}")
        ax.fill_between(x, np.percentile(B, 2.5, 0), np.percentile(B, 97.5, 0), color=col, alpha=.15, lw=0)
    ax.axhline(0, color="k", lw=.6); ax.set_xlabel("round"); ax.set_ylabel("designated-pair premium (price units)")
    ax.set_title("Pair premium: real vs placebo private channel (llm_v3rep seeds)", fontsize=10)
    ax.legend(fontsize=8, frameon=False); fig.tight_layout(); fig.savefig("figures/placebo_premium.png", dpi=150)


if __name__ == "__main__":
    main()
