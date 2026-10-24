"""Exploratory E108 case illustrations; no fits, calls, labels or metrics rerun.

uv run python p2_serendipity_fig.py
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from p2_serendipity import ROOT, load


def main():
    sample = load()
    result = json.loads((ROOT / "results/analysis/p2_serendipity.json").read_text())
    manifest = json.loads((ROOT / "data/serendipity_e108/manifest.json").read_text())
    assert result["sample_sha256"] == manifest["sample_sha256"]
    by_id = {s["run_id"]: s for s in sample}
    band = by_id["llm_strong_luna_pilot_C_001"]
    rigid = by_id["llm_p2rep_0048"]
    table, = [r for r in result["checks"]["E108a"]["runs"] if r["run_id"] == band["run_id"]]
    hit, = [r for r in result["checks"]["E108c"]["runs"] if r["run_id"] == rigid["run_id"] and r["agent"] == "A"]

    plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 160})
    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.1))
    blue, red, teal = "#3366A2", "#B44B46", "#248A82"

    ax = axes[0]
    ax.axhspan(table["opening_target"] - 1, table["opening_target"] + 1,
               color=blue, alpha=.10, label="Opening target ±1")
    for who, color in [("A", blue), ("B", red)]:
        xs = [r["round"] for r in band["rounds"]]
        ys = [next(a["price"] for a in r["agents"] if a["id"] == who) for r in band["rounds"]]
        ax.step(xs, ys, where="mid", label=who, color=color, linewidth=1.7)
    ax.set(title="A  A price band permits unequal prices", xlabel="Round (zero-based)", ylabel="Price",
           xlim=(0, 39), ylim=(10.7, 15.4), yticks=[11, 12, 13, 14])
    ax.text(.03, .97, f"Within band: {table['within_pm1']}/{table['rounds']} rounds\n"
            f"Both at target: {table['both_exact_target']}/{table['rounds']}\n"
            f"Unequal streak: {table['longest_unequal_within_band_streak']} rounds",
            transform=ax.transAxes, va="top", fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9})
    ax.legend(loc="lower right", frameon=False, fontsize=8)

    styles = [("A", red, "A (channel)", 2.0), ("D", teal, "D (channel)", 1.6),
              ("B", "#777777", "B", 1.1), ("C", "#B7B7B7", "C", 1.1)]
    for who, color, label, lw in styles:
        xs = [r["round"] for r in rigid["rounds"]]
        ys = [next(a["price"] for a in r["agents"] if a["id"] == who) for r in rigid["rounds"]]
        ps = np.cumsum([next(a["profit"] for a in r["agents"] if a["id"] == who) for r in rigid["rounds"]])
        axes[1].plot(xs, ys, color=color, label=label, linewidth=lw)
        axes[2].plot(xs, ps, color=color, label=label, linewidth=lw)
        assert round(float(ps[-1]), 2) == hit["profit_totals"][who]
    axes[1].set(title="B  Only one partner holds 18", xlabel="Round (zero-based)", ylabel="Price",
                xlim=(0, 11), ylim=(10.5, 19.2))
    axes[1].legend(loc="center right", bbox_to_anchor=(1, .72), frameon=False, fontsize=8)
    axes[2].set(title="C  A earns less than every rival", xlabel="Round (zero-based)",
                ylabel="Observed cumulative profit", xlim=(0, 11))
    axes[2].text(.04, .96, f"A has lowest profit in all {hit['rounds']} rounds",
                 transform=axes[2].transAxes, va="top", fontsize=8)
    for ax in axes:
        ax.grid(axis="y", color="#DDDDDD", linewidth=.5)
        ax.set_axisbelow(True)
    fig.suptitle("Two exploratory cases from a frozen 40-game transcript sample", fontsize=12, y=.99)
    fig.text(.015, .04, "A: q14 / llm_strong_luna_pilot_C_001.  B–C: q22 / llm_p2rep_0048.  "
             "Opening-price fidelity is not an execution label; relative profit is not counterfactual harm.", fontsize=8)
    fig.tight_layout(rect=(0, .10, 1, .94), w_pad=2)
    path = ROOT / "figures/p2_serendipity.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
