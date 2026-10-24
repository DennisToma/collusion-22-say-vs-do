"""Phase 2 gap 1: registered E77 + amendment verdicts and Figure P2.5, from results/analysis/p2_cue_<ds>.json
(written by p2_cue.py) plus trajectories. Written before any llm_p2cue outcome was viewed. Nothing is fitted.

Equivalence: a paired difference is "equivalent to 0" if its 95% CI lies inside [-0.5, +0.5] price units (amendment);
"positive" if the CI lower bound > 0; else "inconclusive".

    uv run python p2_cue_verdict.py --ds llm_p2cue   # -> results/analysis/p2_cue_verdict_<ds>.json, figures/p2_cue_rounds.png
"""
import argparse, json
from pathlib import Path
import numpy as np

EQ = 0.5
CONTRASTS = [  # (key in p2_cue.json "paired", statistic) -- the registered pattern, primary window r2_12
    ("private-none", "prem_r2_12"), ("neutral-none", "prem_r2_12"), ("notes-none", "prem_r2_12"),
    ("placebo-none", "prem_r2_12"), ("private-notes", "prem_r2_12"), ("neutral-private", "prem_r2_12"),
    ("placebo-notes", "prem_r2_12"), ("placebo-private", "prem_r2_12"),
    ("private-placebo", "did_r2_12_minus_r1"), ("private-notes", "did_r2_12_minus_r1"),
    ("private-none", "prem_r1"), ("notes-none", "prem_r1"), ("placebo-none", "prem_r1"), ("neutral-none", "prem_r1"),
]
ARMS = ["private", "neutral", "notes", "randpartner", "placebo", "none"]


def verdict(ci):
    m, lo, hi = ci
    if lo > 0:
        return "positive"
    if hi < 0:
        return "negative"
    if -EQ <= lo and hi <= EQ:
        return "equivalent_to_0"
    return "inconclusive"


def get(paired, key, stat):
    if key in paired:
        return paired[key][stat]
    a, b = key.split("-")  # stored only one direction: flip sign
    m, lo, hi = paired[f"{b}-{a}"][stat]
    return [round(-m, 3), round(-hi, 3), round(-lo, 3)]


def per_round(ds):
    D = Path("data") / ds
    gt = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))}
    P = {}
    for r in map(json.loads, open(D / "trajectories.jsonl")):
        P.setdefault(r["run_id"], {})[r["round"]] = {x["id"]: x["price"] for x in r["agents"]}
    out = {}
    for rid, g in gt.items():
        pair = g["assigned_pair"]; oth = [a for a in "ABCD" if a not in pair]
        R = sorted(P[rid])
        out.setdefault(g["condition"], []).append([np.mean([P[rid][t][a] for a in pair]) - np.mean([P[rid][t][a] for a in oth]) for t in R])
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ds", default="llm_p2cue"); a = ap.parse_args()
    J = json.load(open(f"results/analysis/p2_cue_{a.ds}.json"))
    res = {"ds": a.ds, "equivalence_margin": EQ, "n": J["n"], "contrasts": {}}
    for key, stat in CONTRASTS:
        try:
            ci = get(J["paired"], key, stat)
        except KeyError:
            continue
        res["contrasts"][f"{key}:{stat}"] = {"ci": ci, "verdict": verdict(ci)}
    pn = J["paired"]["private-none"]["prem_r2_12"][0]
    nn = J["paired"]["notes-none"]["prem_r2_12"]
    res["H3_amended"] = {"rule": "notes-none r2_12 upper CI < 0.5 * private-none point", "notes_none": nn,
                         "half_private_none": round(pn / 2, 3), "held": nn[2] < pn / 2}
    bc = J["by_condition"]
    res["per_arm"] = {c: {k: bc[c].get(k) for k in ("prem_r1", "prem_r2_12", "markup_r2_12", "flag_rate", "agreement_counts",
                                                    "unilateral_proposals_per_run", "partner_gap_next_minus_same")}
                      for c in ARMS if c in bc}
    res["run_auroc_vs_none"] = J["run_auroc_vs_none"]
    Path(f"results/analysis/p2_cue_verdict_{a.ds}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    PR = per_round(a.ds)
    fig, ax = plt.subplots(figsize=(7, 4))
    for c in ARMS:
        if c not in PR or c == "randpartner":
            continue
        X = np.array(PR[c]); t = np.arange(1, X.shape[1] + 1)
        B = np.random.default_rng(0).choice(len(X), (2000, len(X)))
        lo, hi = np.percentile(X[B].mean(1), [2.5, 97.5], axis=0)
        ax.plot(t, X.mean(0), marker="o", ms=3, label=f"{c} (n={len(X)})"); ax.fill_between(t, lo, hi, alpha=.12)
    ax.axhline(0, color="grey", lw=.8); ax.set_xlabel("round"); ax.set_ylabel("assigned-pair premium (price units)")
    ax.set_title(f"{a.ds}: pair premium by arm (95% seed-bootstrap band)", fontsize=10)
    ax.legend(fontsize=8, ncol=2); fig.tight_layout()
    Path("figures").mkdir(exist_ok=True); fig.savefig("figures/p2_cue_rounds.png", dpi=150)


if __name__ == "__main__":
    main()
