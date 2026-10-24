"""Part C figure (P2.7): market-mean price minus Nash per round, by E99-amend behaviour class.
Reads data/<ds>/trajectories.jsonl + results/analysis/p2_strong_classes_<ds>.json (written by p2_strong_eval.py; no LLM calls).
Left: every run (thin). Right: class mean with 95% bootstrap band over runs. Nash = cost + 5 per round (as p2_strong.py).
Usage: uv run python p2_strongF_fig.py --ds llm_p2strongF  ->  figures/p2_strong_<ds>.png"""
import argparse, json
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(); ap.add_argument("--ds", default="llm_p2strongF"); a = ap.parse_args()
C = json.load(open(f"results/analysis/p2_strong_classes_{a.ds}.json"))["runs"]
X = defaultdict(dict)  # run -> round -> market mean excess over Nash
for r in map(json.loads, open(f"data/{a.ds}/trajectories.jsonl")):
    if r["run_id"] in C:
        X[r["run_id"]][r["round"]] = np.mean([g["price"] for g in r["agents"]]) - (r["market"]["cost"] + 5)
# categorical slots 1-4 (validated light palette); line style = secondary encoding (contrast WARN on aqua/yellow)
STY = {"executed": ("#2a78d6", "-", "executed (private, strict)"), "nonexec_private": ("#eb6834", "--", "private, not executed"),
       "tacit_high": ("#1baf7a", "-.", "tacit-high (no channel)"), "competitive": ("#eda100", ":", "competitive (no channel)")}
rng = np.random.default_rng(0)
fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for cls, (col, ls, lab) in STY.items():
    rs = [r for r, e in C.items() if e["class"] == cls and r in X]
    if not rs:
        continue
    T = min(len(X[r]) for r in rs)
    M = np.array([[X[r][t] for t in range(T)] for r in rs])
    for row in M:
        ax[0].plot(range(1, T + 1), row, color=col, ls=ls, lw=0.8, alpha=0.6)
    mu = M.mean(0)
    boot = np.array([M[rng.integers(0, len(M), len(M))].mean(0) for _ in range(2000)])
    lo, hi = np.percentile(boot, [2.5, 97.5], axis=0)
    ax[1].fill_between(range(1, T + 1), lo, hi, color=col, alpha=0.15, lw=0)
    ax[1].plot(range(1, T + 1), mu, color=col, ls=ls, lw=2, label=f"{lab}, n = {len(rs)}")
    ax[1].annotate(f"{cls.replace('_', ' ')} ({len(rs)})", (T, mu[-1]), xytext=(4, 0), textcoords="offset points",
                   va="center", fontsize=8, color="#333333")
for k, t in enumerate(["every run", "class mean, 95% bootstrap band over runs"]):
    ax[k].axhline(0, color="#888888", lw=0.8); ax[k].axhline(2, color="#888888", lw=0.8, ls="--")
    ax[k].set_title(t, fontsize=10, color="#333333"); ax[k].set_xlabel("round")
    for s in ("top", "right"):
        ax[k].spines[s].set_visible(False)
    ax[k].grid(axis="y", color="#eeeeee", lw=0.6)
ax[0].set_ylabel("market-mean price − Nash")
ax[0].text(1, 2.1, "Nash + 2 (tacit-high threshold: market mean, 2nd half)", fontsize=7, color="#666666", va="bottom")
h, l = ax[1].get_legend_handles_labels()
fig.legend(h, l, fontsize=8, frameon=False, loc="lower center", ncol=4)
ax[1].set_xlim(right=ax[1].get_xlim()[1] * 1.18)
fig.suptitle(f"Strong framing ({a.ds}): price paths by behaviour class", fontsize=11)
fig.tight_layout(rect=(0, 0.07, 1, 1))
out = Path(f"figures/p2_strong_{a.ds}.png"); fig.savefig(out, dpi=130); print("wrote", out)
