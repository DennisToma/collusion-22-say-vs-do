"""Figure for early_detection.py (descriptive): premium run / within-market AUROC vs rounds observed.
    uv run python fig_early.py --ds llm_v3   # -> figures/early_detection_llm_v3.png
"""
import argparse, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(); ap.add_argument("--ds", default="llm_v3"); ap.add_argument("--split", default="all")
a = ap.parse_args()
d = json.load(open(f"results/analysis/early_detection_{a.ds}.json"))
R = d["results"][a.split]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
for ax, m, title in zip(axes, ("run_auroc", "within_market_auroc"), ("detection (run AUROC)", "localisation (within-market AUROC)")):
    for pref, lab, c in (("r1-", "rounds 1..k", "#2a6fdb"), ("r2-", "rounds 2..k (opening round dropped)", "#e07b39")):
        ks = sorted(int(k.split("-")[1]) for k in R if k.startswith(pref))
        v = [R[f"{pref}{k}"][m] for k in ks]
        ax.plot(ks, [x[0] for x in v], "o-", color=c, label=lab, ms=4)
        ax.fill_between(ks, [x[1] for x in v], [x[2] for x in v], color=c, alpha=.15)
    ax.axhline(.5, color="grey", lw=.8, ls=":")
    ax.set_xlabel("rounds observed k"); ax.set_title(title); ax.set_xticks(range(1, d["rounds"] + 1))
axes[0].set_ylabel("AUROC (95% run-bootstrap CI)"); axes[0].legend(loc="lower right", fontsize=8)
fig.suptitle(f"Pair price premium vs rounds observed — {a.ds} {a.split} (n={d['n'][a.split]}, {d['n_pos'][a.split]} y=1; descriptive)", fontsize=10)
fig.tight_layout()
out = f"figures/early_detection_{a.ds}.png"; fig.savefig(out, dpi=130); print("wrote", out)
