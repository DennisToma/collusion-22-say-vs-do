"""Post-headline descriptive figure (after HEADLINE_DONE): test-split run-level ROC curves of the premium and the LLM
views, with each scorer's dev-chosen (Youden) operating point marked, and legit-run flags shown separately.
Reads the frozen thresholds from the locked final json; recomputes nothing that is reported as a metric.
    uv run python fig_roc.py  -> figures/roc_test.png
"""
import json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from analyze_llm import load_jsonl
from final_analysis import premium_scores, idx

F = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_test.json"))
th = F["thresholds_dev_youden"]
gt = {x["run_id"]: x for x in load_jsonl(Path("data/llm_v3/ground_truth.jsonl"))}
labs = {x["run_id"]: int(x["agreement"] in ("explicit", "info_exchange")) for x in load_jsonl(Path("data/llm_v3/labels.jsonl"))}
ids = sorted(r for r in labs if idx(r) >= 30)
assert len(ids) == F["n_runs"]
S = {}
for v in ["text", "combined", "action_stats", "structured"]:
    S[v] = {x["run_id"]: x["collusion_present"] for x in load_jsonl(Path(f"results/llm_auditor/llm_v3/gpt-6.1-sol/{v}_orig.jsonl"))}
P, _ = premium_scores("llm_v3"); S["premium"] = {r: P[r]["run"] for r in P}
cols = {"premium": "#222222", "action_stats": "#1f77b4", "structured": "#2ca02c", "combined": "#ff7f0e", "text": "#9467bd"}
y = np.array([labs[r] for r in ids]); neg = [r for r in ids if not labs[r]]
fig, ax = plt.subplots(figsize=(6.2, 5.4))
for v, c in cols.items():
    s = np.array([S[v][r] for r in ids]); fpr, tpr, _ = roc_curve(y, s)
    ax.plot(fpr, tpr, color=c, lw=1.8, label=f"{v} (AUROC {F['point_ci'][v]['run_auroc'][0]:.2f})")
    t = th[v]; op = ((s[y == 0] >= t).mean(), (s[y == 1] >= t).mean())
    nl = sum(S[v][r] >= t for r in neg if gt[r]["condition"] == "legit"); nlt = sum(gt[r]["condition"] == "legit" for r in neg)
    ax.scatter(*op, color=c, s=60, edgecolor="white", zorder=5)
    ax.annotate(f"legit {nl}/{nlt}", op, textcoords="offset points", xytext=(6, -12), fontsize=7.5, color=c)
ax.plot([0, 1], [0, 1], ":", color="grey", lw=1)
ax.set_xlabel("false-positive rate (45 test negatives: 30 none + 15 legit)"); ax.set_ylabel("true-positive rate (50 y=1)")
ax.set_title("Test split: run-level detection; dots = dev-chosen thresholds", fontsize=10)
ax.legend(loc="lower right", fontsize=8, frameon=False)
fig.tight_layout(); Path("figures").mkdir(exist_ok=True); fig.savefig("figures/roc_test.png", dpi=150)
print("wrote figures/roc_test.png")
