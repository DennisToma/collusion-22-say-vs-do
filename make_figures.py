"""Figures for the say-vs-do report. Usage: uv run python make_figures.py --split dev"""
import argparse, json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = "results/analysis"
TAG = "llm_v3_gpt-6.1-sol"
C1, C2, INK, MUTED = "#0072B2", "#D55E00", "#222222", "#888888"
ORDER = ["text", "action", "combined", "fusion", "combined_stats", "action_stats", "structured", "premium"]
LABEL = {"premium": "pair premium (untrained)"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

def lab(s): return LABEL.get(s, s)
def load(p):
    return json.load(open(p)) if os.path.exists(p) else None
def save(fig, name, split):
    os.makedirs("figures", exist_ok=True)
    out = f"figures/{name}_{split}.png" if split else f"figures/{name}.png"
    fig.savefig(out, dpi=160, bbox_inches="tight"); plt.close(fig); print("wrote", out)

def auroc(d, title, split):
    pc = d["point_ci"]; sc = [s for s in ORDER if s in pc]
    fig, ax = plt.subplots(figsize=(7.5, 0.55 * len(sc) + 1.8))
    for k, (m, c, mk, off, nm) in enumerate([("run_auroc", C1, "o", -0.15, "run AUROC"),
                                              ("within_market_auroc", C2, "s", 0.15, "within-market AUROC")]):
        ys = [i + off for i in range(len(sc))]
        pt = [pc[s][m][0] for s in sc]
        for y, s in zip(ys, sc):  # CI drawn independently of the point (percentile CIs need not contain it)
            if pc[s][m][1] is not None and pc[s][m][2] is not None:
                ax.plot([pc[s][m][1], pc[s][m][2]], [y, y], color=c, lw=1.5)
        ax.plot(pt, ys, mk, color=c, ms=6, mec="white", label=nm, ls="none")
    ax.axvline(0.5, ls="--", color=MUTED, lw=1); ax.text(0.505, -0.55, "chance", color=MUTED, ha="left", fontsize=8)
    ax.set_yticks(range(len(sc))); ax.set_yticklabels([lab(s) for s in sc]); ax.invert_yaxis()
    ax.set_xlim(0.35, 1.02); ax.set_xlabel("AUROC (95% CI)"); ax.grid(axis="x", color="#e6e6e6", lw=0.6); ax.set_axisbelow(True)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.08), frameon=False, fontsize=9); ax.set_title(title, loc="left", fontsize=11)
    save(fig, "auroc", split)

CNAMES = ["delta_hybrid[combined]", "delta_hybrid[structured]", "delta_hybrid[fusion]", "action_stats-action",
          "combined_stats-action_stats", "structured-combined_stats", "combined-fusion",
          "premium-structured", "premium-action_stats"]

def forest(items, metrics, title, fname, split, xlabel="delta (95% CI)"):
    fig, axs = plt.subplots(1, len(metrics), figsize=(5 * len(metrics) + 2, 0.5 * max(len(items), 1) + 1.8), sharey=True, squeeze=False)
    for ax, (m, mt) in zip(axs[0], metrics):
        for i, (n, c) in enumerate(items):
            e = c.get(m)
            if not e: continue
            lo, hi = e["ci"]
            if lo is None or hi is None: continue
            col = C1 if (lo > 0 or hi < 0) else MUTED
            ax.plot([lo, hi], [i, i], color=col, lw=1.5); ax.plot([e["delta"]], [i], "o", color=col, ms=6, mec="white")
        ax.axvline(0, color=INK, lw=1); ax.set_title(mt, fontsize=10, loc="left"); ax.set_xlabel(xlabel)
        ax.grid(axis="x", color="#e6e6e6", lw=0.6); ax.set_axisbelow(True)
    axs[0][0].set_yticks(range(len(items))); axs[0][0].set_yticklabels([n for n, _ in items]); axs[0][0].invert_yaxis()
    fig.suptitle(title + "  (blue = CI excludes 0)", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(); save(fig, fname, split)

def contrasts(d, title, split):
    items = []
    for n in CNAMES:
        c = {m: d["contrasts"].get(f"{n}:{m}") for m in ("run_auroc", "within_market_auroc")}
        if any(c.values()): items.append((n, c))
    forest(items, [("run_auroc", "run AUROC"), ("within_market_auroc", "within-market AUROC")], title, "contrasts", split)

def flagrates(d, title, split):
    fr = d["flag_rate_by_stratum"]; strata = [s for s in ["private_y1", "legit", "none_all", "all_negatives"] if s in fr]
    scs = ["text", "action", "combined", "structured", "premium"]
    cols = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#555555"]
    fig, ax = plt.subplots(figsize=(8.5, 4.5)); w = 0.15
    for j, (s, c) in enumerate(zip(scs, cols)):
        xs, pt, lo, hi = [], [], [], []
        for i, st in enumerate(strata):
            v = fr[st].get(s)
            if v: xs.append(i + (j - 2) * w); pt.append(v[0]); lo.append(v[0] - v[1]); hi.append(v[2] - v[0])
        ax.errorbar(xs, pt, yerr=[lo, hi], fmt="o", color=c, ms=6, lw=1.5, mec="white", label=lab(s))
    ax.set_xticks(range(len(strata))); ax.set_xticklabels([f"{s}\n(n={fr[s]['n']})" for s in strata])
    ax.set_ylim(-0.03, 1.03); ax.set_ylabel("flag rate at dev threshold (Wilson 95% CI)")
    ax.grid(axis="y", color="#e6e6e6", lw=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    ax.set_title(title, loc="left", fontsize=11); save(fig, "flagrates", split)

def shuffle(sh, split):
    ims = sh.get("intact_minus_shuffled", sh)
    items = []
    for n, v in ims.items():
        if isinstance(v, dict) and "delta" in v and "ci" in v: items.append((n, {"x": v}))
    if not items: print("shuffle: no intact_minus_shuffled entries found"); return
    forest(items, [("x", "intact minus shuffled")], f"Shuffle control (n={sh.get('n_common', sh.get('n_runs', '?'))})", "shuffle", None, "intact - shuffled (95% CI)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--split", default="dev"); sp = ap.parse_args().split
    d = load(f"{A}/final_{TAG}_{sp}.json")
    t = f"{sp.upper()} split (n={d['n_runs']})"
    auroc(d, t, sp); contrasts(d, t, sp); flagrates(d, t, sp)
    sh = load(f"{A}/shuffle_{TAG}_test.json")
    if sh: shuffle(sh, sp)
