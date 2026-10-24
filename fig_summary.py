"""Abstract-level summary figure, built only from existing results JSON (no LLM calls, no refitting).

Left: run AUROC [95% bootstrap CI] per scorer on the locked test split (n=95) and the fresh replication
(llm_v3rep, n=30). Right: flag rate at frozen dev thresholds in the placebo-channel stratum (exploration).

uv run python fig_summary.py  ->  figures/summary.png
"""
import json
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = "results/analysis/"
test = json.load(open(A + "final_llm_v3_gpt-6.1-sol_test.json"))["point_ci"]
rep = json.load(open(A + "replication_llm_v3rep.json"))["point_ci"]
ed_test = json.load(open(A + "early_detection_llm_v3.json"))["results"]["test"]["r1-1"]["run_auroc"]
ed_rep = json.load(open(A + "early_detection_llm_v3rep.json"))["results"]["all"]["r1-1"]["run_auroc"]
plc = json.load(open(A + "placebo_llm_v3plc.json"))

# (label, test [pt, lo, hi], rep [pt, lo, hi], kind)
rows = [
    ("text (LLM)", test["text"]["run_auroc"], rep["text"]["run_auroc"], "say"),
    ("action (LLM)", test["action"]["run_auroc"], rep["action"]["run_auroc"], "do"),
    ("combined (LLM)", test["combined"]["run_auroc"], rep["combined"]["run_auroc"], "both"),
    ("structured (LLM)", test["structured"]["run_auroc"], rep["structured"]["run_auroc"], "both"),
    ("combined_stats (LLM)", test["combined_stats"]["run_auroc"], rep["combined_stats"]["run_auroc"], "both"),
    ("action_stats (LLM)", test["action_stats"]["run_auroc"], rep["action_stats"]["run_auroc"], "do"),
    ("premium, round 1 only", ed_test, ed_rep, "stat"),
    ("premium, all rounds", test["premium"]["run_auroc"], rep["premium"]["run_auroc"], "stat"),
]
color = {"say": "#c0392b", "do": "#2471a3", "both": "#7d3c98", "stat": "#1e8449"}

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1.25, 1]})
for i, (lab, t, r, k) in enumerate(rows):
    y = len(rows) - 1 - i
    ax.errorbar(t[0], y + 0.15, xerr=[[t[0] - t[1]], [t[2] - t[0]]], fmt="o", color=color[k], capsize=3)
    ax.errorbar(r[0], y - 0.15, xerr=[[r[0] - r[1]], [r[2] - r[0]]], fmt="o", mfc="white", color=color[k],
                capsize=3, alpha=0.8)
    ax.text(1.005, y + 0.15, f"{t[0]:.2f}", va="center", fontsize=8)
    ax.text(1.005, y - 0.15, f"{r[0]:.2f}", va="center", fontsize=8, color="grey")
ax.axvline(0.5, color="grey", ls=":", lw=1)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1])
ax.set_xlim(0.3, 1.0)
ax.set_xlabel("run AUROC (private-channel coordination vs not), 95% bootstrap CI")
ax.plot([], [], "o", color="k", label="locked test (n=95, run once)")
ax.plot([], [], "o", color="k", mfc="white", label="fresh replication (n=30)")
ax.legend(loc="lower left", fontsize=8)
ax.set_title("(a) Reading what sellers say adds no resolved gain;\na one-line price statistic ranks highest", fontsize=10)


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)


scorers = [("text", plc["auditors"]["text"]["flag_rate"]), ("action", plc["auditors"]["action"]["flag_rate"]),
           ("combined", plc["auditors"]["combined"]["flag_rate"]),
           ("action_stats", plc["auditors"]["action_stats"]["flag_rate"]),
           ("premium", plc["premium_scorer"]["flag_rate"])]
arms = [("private (delivered)", "private", "#2471a3"), ("placebo (offered, not delivered)", "placebo", "#e67e22"),
        ("none (no channel)", "none", "#7f8c8d")]
w = 0.26
for j, (alab, akey, c) in enumerate(arms):
    xs, ps, lo, hi = [], [], [], []
    for i, (_, fr) in enumerate(scorers):
        k, n = fr[akey]
        p, l, h = wilson(k, n)
        xs.append(i + (j - 1) * w)
        ps.append(p)
        lo.append(p - l)
        hi.append(h - p)
    bx.bar(xs, ps, w, color=c, label=alab, yerr=[lo, hi], capsize=2, error_kw={"lw": 0.8})
bx.set_xticks(range(len(scorers)))
bx.set_xticklabels([s for s, _ in scorers], fontsize=9)
bx.set_ylim(0, 1.05)
bx.set_ylabel("flag rate at frozen dev threshold (Wilson 95% CI)")
bx.legend(fontsize=8, loc="upper left")
bx.set_title("(b) Placebo stratum (exploration, 15 matched seeds; 10 none):\nflags fire on the channel offer, not only delivery",
             fontsize=10)
fig.tight_layout()
fig.savefig("figures/summary.png", dpi=140)
print("wrote figures/summary.png")
