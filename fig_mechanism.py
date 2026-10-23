"""Descriptive figure (no metric, no labels beyond condition): mean price per round of the assigned pair vs the other
two firms, by condition. Shows WHY the untrained pair premium works on llm_v3 (round-1 joint high opening, quickly
undercut). Default = dev runs only (0000-0029) so it can be made before the locked test analysis; `--split all` after.
    uv run python fig_mechanism.py --split dev   -> figures/mechanism_dev.png
"""
import argparse, json, collections
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument("--ds", default="llm_v3"); ap.add_argument("--split", default="dev",
                                                                                         choices=["dev", "test", "all"])
a = ap.parse_args()
if a.split != "dev":  # condition-linked price summaries of test runs = a test look: only after the locked headline
    import pathlib; st = pathlib.Path("logs/final/RUN_ONCE.stamp")
    assert st.exists() and "HEADLINE_DONE" in st.read_text(), "--split test/all only after finalize_test.sh HEADLINE_DONE"
def in_split(rid):
    i = int(rid.rsplit("_", 1)[1]); return a.split == "all" or (a.split == "dev") == (i < 30)
gt = {r["run_id"]: r for r in map(json.loads, open(f"data/{a.ds}/ground_truth.jsonl")) if in_split(r["run_id"])}
series = collections.defaultdict(list)   # cond -> list of (pair[T], others[T])
by_run = collections.defaultdict(dict)
for r in map(json.loads, open(f"data/{a.ds}/trajectories.jsonl")):
    if r["run_id"] in gt:
        assert r["round"] not in by_run[r["run_id"]], f"duplicate round {r['run_id']} {r['round']}"
        by_run[r["run_id"]][r["round"]] = {x["id"]: x["price"] for x in r["agents"]}
assert set(by_run) == set(gt), "trajectories missing for some runs"
for rid, rounds in by_run.items():
    g = gt[rid]; pair = set(g["assigned_pair"]); T = sorted(rounds)
    assert T == list(range(g["rounds"])), f"{rid}: rounds {T}"
    p = [np.mean([rounds[t][f] for f in pair]) for t in T]; o = [np.mean([v for f, v in rounds[t].items() if f not in pair]) for t in T]
    series[g["condition"]].append((p, o))
conds = [c for c in ["private", "none", "legit"] if c in series]
fig, axs = plt.subplots(1, len(conds), figsize=(4.2 * len(conds), 3.4), sharey=True)
for ax, c in zip(np.atleast_1d(axs), conds):
    P = np.array([s[0] for s in series[c]]); O = np.array([s[1] for s in series[c]]); x = np.arange(1, P.shape[1] + 1)
    for M, lab_, col in [(P, "assigned pair", "#c0392b"), (O, "other two firms", "#7f8c8d")]:
        m = M.mean(0); se = M.std(0, ddof=1) / np.sqrt(len(M)) if len(M) > 1 else 0 * m
        ax.plot(x, m, color=col, label=lab_, lw=2); ax.fill_between(x, m - 1.96 * se, m + 1.96 * se, color=col, alpha=.18)
    ax.axhline(11, ls=":", c="k", lw=.8); ax.axhline(19, ls="--", c="k", lw=.8)
    ax.set_title(f"{c} (n={len(P)} runs)", fontsize=10); ax.set_xlabel("round"); ax.grid(alpha=.3); ax.set_xticks(x[::2] if len(x) > 8 else x)
np.atleast_1d(axs)[0].set_ylabel("mean price (±95% CI)"); np.atleast_1d(axs)[0].legend(frameon=False, fontsize=8)
fig.text(.01, -.06, "dotted: static Nash ≈ 11; dashed: joint monopoly ≈ 19 (cost 6, normal demand)", fontsize=8)
fig.suptitle(f"{a.ds} {a.split.upper()} split: assigned pair vs rivals", fontsize=10, y=1.03)
out = f"figures/mechanism_{a.split}.png"; fig.savefig(out, dpi=160, bbox_inches="tight"); print("wrote", out)
# descriptive numbers quoted in REPORT: late-window (rounds 9-12 = round ids 8..11; every run has ids 0..11, asserted)
for c in conds:
    v = np.array([np.mean(np.array(p[8:12]) - np.array(o[8:12])) for p, o in series[c]])
    print(f"{c}: n={len(v)} late(r9-12) premium mean {v.mean():+.2f}, fraction of runs > 0: {(v > 0).mean():.2f}")
