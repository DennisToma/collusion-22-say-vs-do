"""Phase 2 gap 1 (E77/E78/E79, registered in EXPERIMENTS.tsv before generation): is the pair premium a response to
coordination or to the channel offer / wording? Matched seeds: every condition of seed k shares pair, cost and demand
path (llm_market.py --matched). No fitting; the premium scorer and its threshold are the frozen v1 ones.

Per condition: assigned-pair premium (pair mean - other-two mean) in windows r1 / r2_12 / all; market markup (all-firm
mean price - cost); frozen premium run score (max over 6 pairs) flag rate at the llm_v3 dev threshold and run AUROC vs
none. Paired differences over matched seeds (seed bootstrap, 2000). Agreement rate from labels.jsonl when present.

    uv run python p2_cue.py --ds llm_p2cue      # -> results/analysis/p2_cue_<ds>.json
    uv run python p2_cue.py --ds llm_p2para1 llm_p2para2 llm_p2ds
"""
import argparse, json, random
from itertools import combinations
from pathlib import Path
import numpy as np
from final_analysis import premium_scores

AG = ["A", "B", "C", "D"]
WIN = {"r1": slice(0, 1), "r2_12": slice(1, None), "all": slice(0, None)}


def boot_mean(x, n=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return None
    rng = np.random.default_rng(seed)
    b = rng.choice(x, (n, len(x))).mean(1)
    return [round(float(x.mean()), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def auc(neg, pos):
    if not neg or not pos:
        return None
    return float(np.mean([(p > q) + 0.5 * (p == q) for p in pos for q in neg]))


def boot_auc(neg, pos, n=2000, seed=0):
    rng = np.random.default_rng(seed); neg, pos = np.asarray(neg), np.asarray(pos)
    b = [auc(list(rng.choice(neg, len(neg))), list(rng.choice(pos, len(pos)))) for _ in range(n)]
    return [round(auc(list(neg), list(pos)), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def analyse(ds):
    D = Path("data") / ds
    gt = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))}
    P, C = {}, {}
    for r in map(json.loads, open(D / "trajectories.jsonl")):
        P.setdefault(r["run_id"], {})[r["round"]] = {x["id"]: x["price"] for x in r["agents"]}
        C.setdefault(r["run_id"], {})[r["round"]] = r["market"]["cost"]
    labs = {}
    if (D / "labels.jsonl").exists():
        labs = {l["run_id"]: l for l in map(json.loads, open(D / "labels.jsonl"))}
    thr = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]["premium"]
    S, _ = premium_scores(ds)
    rows = {}
    for rid, g in gt.items():
        R = sorted(P[rid]); pr = {a: np.array([P[rid][t][a] for t in R], float) for a in AG}
        cost = np.array([C[rid][t] for t in R], float)
        pair = g["assigned_pair"]; oth = [a for a in AG if a not in pair]
        row = {"seed": g["seed"], "run_id": rid, "run_score": S[rid]["run"], "flag": S[rid]["run"] >= thr}
        for w, s in WIN.items():
            row[f"prem_{w}"] = float(((pr[pair[0]] + pr[pair[1]]) / 2)[s].mean() - np.mean([pr[o] for o in oth], 0)[s].mean())
            row[f"markup_{w}"] = float(np.mean([pr[a] for a in AG], 0)[s].mean() - cost[s].mean())
        row["did_r2_12_minus_r1"] = row["prem_r2_12"] - row["prem_r1"]
        if g["condition"] == "randpartner":  # E77 amendment: premium ~0 by construction; round-level partner statistic
            gaps = {"next": [], "same": []}
            for t in R[:-1]:
                perm = random.Random(g["seed"] * 100 + t).sample(AG, 4)  # = llm_market.run_game matching
                m = {frozenset(perm[:2]), frozenset(perm[2:])}
                for key, tt in (("next", t + 1), ("same", t)):
                    gap = {frozenset(q): abs(P[rid][tt][q[0]] - P[rid][tt][q[1]]) for q in combinations(AG, 2)}
                    gaps[key].append(np.mean([v for q, v in gap.items() if q in m]) - np.mean([v for q, v in gap.items() if q not in m]))
            row["partner_gap_next"] = float(np.mean(gaps["next"]))  # matched-at-t pair |price gap| at t+1 minus unmatched
            row["partner_gap_same"] = float(np.mean(gaps["same"]))  # same round (messages not yet read): baseline
        if rid in labs:
            row["agreement"] = labs[rid].get("agreement"); row["y"] = labs[rid].get("y")
            if "unilateral_proposals" in labs[rid]:
                row["unilateral_proposals"] = labs[rid]["unilateral_proposals"]
        rows.setdefault(g["condition"], {})[g["seed"]] = row
    out = {"ds": ds, "frozen_dev_threshold": round(float(thr), 3), "model": sorted({g["model"] for g in gt.values()}),
           "n": {c: len(v) for c, v in rows.items()}, "by_condition": {}, "paired": {}, "run_auroc_vs_none": {}}
    keys = [f"prem_{w}" for w in WIN] + [f"markup_{w}" for w in WIN] + ["did_r2_12_minus_r1"]
    for c, R in rows.items():
        v = list(R.values())
        e = {k: boot_mean([r[k] for r in v]) for k in keys}
        e["flag_rate"] = [int(sum(r["flag"] for r in v)), len(v)]
        if c == "randpartner":
            e["NOTE"] = "assigned-pair premium is ~0 by construction here (matched pairs cancel); use partner_gap_*"
            for k in ("partner_gap_next", "partner_gap_same"):
                e[k] = boot_mean([r[k] for r in v])
            e["partner_gap_next_minus_same"] = boot_mean([r["partner_gap_next"] - r["partner_gap_same"] for r in v])
        if any("unilateral_proposals" in r for r in v):
            e["unilateral_proposals_per_run"] = {str(n): sum(r.get("unilateral_proposals") == n for r in v) for n in (0, 1, 2)}
        if any("agreement" in r for r in v):
            ag = [r.get("agreement") for r in v]
            e["agreement_counts"] = {k: ag.count(k) for k in sorted(set(map(str, ag)))}
        out["by_condition"][c] = e
    for ref in ("none", "notes", "private"):
        if ref not in rows:
            continue
        for c in rows:
            if c == ref:
                continue
            common = sorted(set(rows[c]) & set(rows[ref]))
            out["paired"][f"{c}-{ref}"] = {"n": len(common), **{k: boot_mean([rows[c][s][k] - rows[ref][s][k] for s in common])
                                                               for k in keys}}
    # E77-amendment H3: notes-none r2_12 vs half the private-none effect (paired seeds, joint bootstrap)
    if all(c in rows for c in ("private", "notes", "none")):
        com = sorted(set(rows["private"]) & set(rows["notes"]) & set(rows["none"]))
        dp = np.array([rows["private"][s_]["prem_r2_12"] - rows["none"][s_]["prem_r2_12"] for s_ in com])
        dn = np.array([rows["notes"][s_]["prem_r2_12"] - rows["none"][s_]["prem_r2_12"] for s_ in com])
        rng = np.random.default_rng(1); B = rng.integers(0, len(com), (2000, len(com)))
        ratio = [dn[b].mean() / dp[b].mean() if dp[b].mean() != 0 else np.nan for b in B]
        out["H3_notes_over_private_r2_12"] = [round(float(dn.mean() / dp.mean()), 3) if dp.mean() else None,
                                              round(float(np.nanpercentile(ratio, 2.5)), 3), round(float(np.nanpercentile(ratio, 97.5)), 3)]
    if "none" in rows:
        neg = [r["run_score"] for r in rows["none"].values()]
        for c in rows:
            if c != "none":
                out["run_auroc_vs_none"][c] = boot_auc(neg, [r["run_score"] for r in rows[c].values()])
    out["per_run"] = {c: list(R.values()) for c, R in rows.items()}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ds", nargs="+", default=["llm_p2cue"]); a = ap.parse_args()
    for ds in a.ds:
        o = analyse(ds)
        Path(f"results/analysis/p2_cue_{ds}.json").write_text(json.dumps(o, indent=1))
        print(json.dumps({k: v for k, v in o.items() if k != "per_run"}, indent=1))


if __name__ == "__main__":
    main()
