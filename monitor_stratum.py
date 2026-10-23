"""Exploration stratum (iter 8, never pooled into the headline): `data/llm_v3mon` = lab framing + a publicly known
automated price monitor that halves the earnings of flagged pairs (llm_market.py --framing lab_monitored), conditions
private + none. Question: when colluders know that prices are watched, does the price premium (and the LLM views)
still detect / localise them, and does public text become more (or less) useful?
Nothing is fitted here: run-level flag rates use the FROZEN dev Youden thresholds of llm_v3; AUROCs are threshold-free.
Comparator = llm_v3 DEV only (runs 0000-0029): labels, audits and trajectories of llm_v3 are filtered to dev ids
BEFORE anything is parsed or scored, so test runs are never read into memory as scores (codex review_iter8 P1).
The monitor is an ANNOUNCED threat only (prompt treatment): no monitor is run and payouts are not changed.

    uv run python monitor_stratum.py --ds llm_v3mon
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import load_jsonl
from final_analysis import LLM_VIEWS, AG, PAIRS, boot
from fp_stratum import wilson


def keep(rid, max_idx):
    return max_idx is None or int(rid.rsplit("_", 1)[1]) < max_idx


def premium_scores(ds, max_idx=None, start=0):
    """same definition as final_analysis.premium_scores (frozen), but only parses runs with keep(run_id)."""
    P, C = {}, {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        rid = l.split('"run_id": "', 1)[1].split('"', 1)[0]
        if not keep(rid, max_idx):
            continue
        r = json.loads(l)
        P.setdefault(rid, []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
        C.setdefault(rid, []).append(r["market"]["cost"])
    out, markup = {}, {}
    for rid, rows in P.items():
        rows.sort(key=lambda t: t[0])
        pr = {a: np.array([d[a] for _, d in rows[start:]], float) for a in AG}
        sc = {}
        for p in PAIRS:
            o = [a for a in AG if a not in p]
            sc[p] = float(((pr[p[0]] + pr[p[1]]) / 2).mean() - np.mean([pr[a] for a in o], axis=0).mean())
        out[rid] = {"scores": sc, "run": max(sc.values())}
        markup[rid] = float(np.mean([pr[a].mean() for a in AG]) - np.mean(C[rid][start:]))
    return out, markup


VALID = {"private": {"explicit", "info_exchange", "none"}, "none": {"no_channel"}, "legit": {"no_channel"}}


def load(ds, auditor, max_idx=None):
    labs = {}
    for x in load_jsonl(Path("data") / ds / "labels.jsonl"):
        if not keep(x["run_id"], max_idx):
            continue
        assert x["run_id"] not in labs, "duplicate labels"
        assert x.get("agreement") in VALID.get(x.get("condition"), ()), f"invalid label {x['run_id']}: {x.get('condition')}/{x.get('agreement')}"
        labs[x["run_id"]] = dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
    d = Path("results") / "llm_auditor" / ds / auditor
    S = {}
    for v in LLM_VIEWS:
        f = d / f"{v}_orig.jsonl"
        R = [x for x in (load_jsonl(f) if f.exists() else []) if keep(x["run_id"], max_idx)]
        assert len({x["run_id"] for x in R}) == len(R), f"duplicate audits in {v}"
        S[v] = {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in R}
    S["premium"], markup = premium_scores(ds, max_idx)
    S["premium_r2plus"], _ = premium_scores(ds, max_idx, start=1)
    ids = sorted(r for r in labs if all(r in R for R in S.values()))
    return labs, S, markup, ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3mon")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--thresholds", default="results/analysis/final_llm_v3_gpt-6.1-sol_dev.json")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--allow-partial", action="store_true")
    a = ap.parse_args()
    th = json.loads(Path(a.thresholds).read_text())["thresholds_dev_youden"]
    labs, S, markup, ids = load(a.ds, a.auditor)
    assert a.allow_partial or len(ids) == len(labs), f"incomplete audits: {len(ids)}/{len(labs)}"
    bad = [r for r in labs if labs[r]["condition"] not in ("private", "none") or (labs[r]["condition"] == "none" and labs[r]["y"])]
    assert not bad, f"unexpected condition/label: {bad[:5]}"
    groups = {"private_y1": [r for r in ids if labs[r]["y"]],
              "private_y0": [r for r in ids if labs[r]["condition"] == "private" and not labs[r]["y"]],
              "none": [r for r in ids if labs[r]["condition"] == "none"]}
    out = {"dataset": a.ds, "auditor": a.auditor, "n_runs": len(ids), "n_labelled": len(labs),
           "group_n": {g: len(v) for g, v in groups.items()},
           "agreement_counts": {k: sum(labs[r]["agreement"] == k for r in labs) for k in sorted({labs[r]["agreement"] for r in labs})},
           "thresholds_from": a.thresholds, "flag_rate": {}}
    for k in S:
        out["flag_rate"][k] = {g: wilson(sum(S[k][r]["run"] >= th[k] for r in rs), len(rs)) if th.get(k) is not None else None
                               for g, rs in groups.items()}
    # threshold-free metrics on the stratum (y=1 vs all y=0), class-stratified run bootstrap
    if groups["private_y1"] and len(ids) > len(groups["private_y1"]):
        b = boot(ids, S, labs, a.n_boot)
        out["metrics"] = {k: {m: b["point_ci"][k][m] for m in ("run_auroc", "within_market_auroc", "pair_id_acc")} for k in S}
    # channel-matched contrast (codex review_iter8 P2): private y=1 vs private y=0 only
    pr = groups["private_y1"] + groups["private_y0"]
    if groups["private_y1"] and groups["private_y0"]:
        b = boot(pr, S, labs, a.n_boot)
        out["run_auroc_private_y1_vs_y0"] = {k: b["point_ci"][k]["run_auroc"] for k in S}
    # how much did monitoring shrink the colluders' premium? assigned-pair premium (all rounds), vs llm_v3 DEV
    labs0, S0, markup0, ids0 = load("llm_v3", a.auditor, max_idx=30)
    def ap_prem(L, SS, rs):
        return [SS["premium"][r]["scores"]["".join(L[r]["assigned_pair"])] for r in rs]
    out["assigned_pair_premium"] = {
        "mon_private_y1": ap_prem(labs, S, groups["private_y1"]),
        "mon_private_y0": ap_prem(labs, S, groups["private_y0"]),
        "v3dev_private_y1": ap_prem(labs0, S0, [r for r in ids0 if labs0[r]["y"]])}
    out["mean_markup"] = {"mon_" + g: round(float(np.mean([markup[r] for r in rs])), 2) if rs else None for g, rs in groups.items()}
    out["mean_markup"]["v3dev_private_y1"] = round(float(np.mean([markup0[r] for r in ids0 if labs0[r]["y"]])), 2)
    out["mean_markup"]["v3dev_none"] = round(float(np.mean([markup0[r] for r in ids0 if labs0[r]["condition"] == "none"])), 2)
    Path("results/analysis").mkdir(parents=True, exist_ok=True)
    (Path("results/analysis") / f"monitor_stratum_{a.ds}.json").write_text(json.dumps(out, indent=1))
    print(f"{a.ds}: n={len(ids)}/{len(labs)}; groups {out['group_n']}; agreement {out['agreement_counts']}")
    print("assigned-pair premium mean: " + ", ".join(f"{g} {np.mean(v):+.2f} (n={len(v)})" for g, v in out["assigned_pair_premium"].items() if v))
    print("mean markup:", out["mean_markup"])
    for k in S:
        m = out.get("metrics", {}).get(k, {})
        print(f"{k:15s} flag {out['flag_rate'][k]}  run {m.get('run_auroc')} within {m.get('within_market_auroc')}")


if __name__ == "__main__":
    main()
