"""Message<->action shuffle ablation on LLM data (DIRECTION directive 3). Frozen before the shuffle audits exist.

For each shuffle seed s (frozen donor map results/llm_auditor/<ds>/shuffle_donors_s<s>.json: same label & condition,
nearest cost/demand path), views V in {combined, structured, text} were re-audited with the donor run's public
messages (firm letters remapped so the donor pair lands on the recipient pair). Action scores are unchanged by
construction, so the `action` comparator reuses the intact audit.
Reported on the locked test runs (index >= 30) that have intact + all-seed shuffled audits:
  per view: intact metric, shuffled metric (mean over seeds), and the paired intact-minus-shuffled difference with a
  class-stratified run bootstrap (seed-averaged shuffled score per run/pair).
  Δ_hybrid under shuffle: shuffled(view) − max(shuffled text, intact action).
If hybrids use cross-modal consistency, intact − shuffled > 0 for combined/structured. If text is uninformative, the
expected result is ≈ 0.

    uv run python shuffle_analysis.py --seeds 0,1,2
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import load_jsonl
from final_analysis import metrics, ci, idx, DEV_MAX


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--views", default="combined,structured,text")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    seeds = [int(s) for s in a.seeds.split(",")]
    load = lambda v, var: {x["run_id"]: x for x in load_jsonl(d / f"{v}_{var}.jsonl")}
    S, out = {}, {"seeds": seeds, "views": {}}
    intact_action = load("action", "orig")
    S["action"] = {r: {"scores": x["scores"], "run": x["collusion_present"]} for r, x in intact_action.items()}
    for v in a.views.split(","):
        I = load(v, "orig")
        Sh = [load(v, f"shuffle_s{s}") for s in seeds]
        Sh = [x for x in Sh if x]
        if not Sh:
            continue
        ids = sorted(r for r in labs if idx(r) >= DEV_MAX and r in I and all(r in x for x in Sh))
        S[v] = {r: {"scores": I[r]["scores"], "run": I[r]["collusion_present"]} for r in ids}
        S[v + "_shuf"] = {r: {"scores": {p: float(np.mean([x[r]["scores"][p] for x in Sh])) for p in I[r]["scores"]},
                              "run": float(np.mean([x[r]["collusion_present"] for x in Sh]))} for r in ids}
        out["views"][v] = {"n_runs": len(ids), "n_seeds_present": len(Sh)}
    vs = list(out["views"])
    ids = sorted(set.intersection(*[set(S[v]) for v in vs] + [set(S["action"])])) if vs else []
    out["n_common"] = len(ids)
    if not ids:
        print("no shuffled audits yet"); return
    rng = np.random.default_rng(0)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    pt = metrics(ids, S, labs)
    bs = [metrics(list(rng.choice(P, len(P))) + list(rng.choice(N, len(N))), S, labs) for _ in range(a.boot)]
    M = ("run_auroc", "within_market_auroc", "pair_auroc")
    out["n_pos"] = len(P)
    out["point_ci"] = {k: {m: [round(pt[k][m], 4)] + ci([b[k][m] for b in bs]) for m in M} for k in pt}
    out["intact_minus_shuffled"] = {f"{v}:{m}": {"delta": round(pt[v][m] - pt[v + "_shuf"][m], 4),
                                                 "ci": ci([b[v][m] - b[v + "_shuf"][m] for b in bs])} for v in vs for m in M}
    if "text" in vs:
        for v in vs:
            if v != "text":
                f = lambda x, m: x[v + "_shuf"][m] - max(x["text_shuf"][m], x["action"][m])
                for m in M:
                    out.setdefault("delta_hybrid_shuffled", {})[f"{v}:{m}"] = {"delta": round(f(pt, m), 4), "ci": ci([f(b, m) for b in bs])}
    dm = [json.loads((Path("results/llm_auditor") / a.ds / f"shuffle_donors_s{s}.json").read_text()) for s in seeds
          if (Path("results/llm_auditor") / a.ds / f"shuffle_donors_s{s}.json").exists()]
    out["donor_quality"] = [{"seed": x["seed"], "same_condition": float(np.mean([m["same_condition"] for m in x["map"].values()])),
                             "mean_ctx_l1": round(float(np.mean([m["ctx_l1"] for m in x["map"].values()])), 2)} for x in dm]
    fn = Path("results/analysis") / f"shuffle_{a.ds}_{a.auditor}_test.json"
    fn.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("n_common", "n_pos", "intact_minus_shuffled")}, indent=1))


if __name__ == "__main__":
    main()
