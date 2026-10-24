"""E116 within-agreement say-vs-do contrast (DIRECTION 17:56 directive 1; EXPLORATORY, zero LLM calls).

In llm_p2strongF's private arm every run has the private channel, so the channel-footprint confound of E99-x
(strict-executed vs tacit-high in the no-channel arm) disappears. Question: among pairs that could talk (and mostly
agreed), does what they say (public text), plan (private plans) or do early on separate pairs that EXECUTE the
agreement (strict, n=13) from pairs that do not (non-executed, n=7)? Sensitivity: non-executed pairs with a judged
agreement only (n=5). Scores are the frozen, already-saved per-run scores (no recalibration); AUROC and the seed
bootstrap are p2_strong_eval.auroc/boot (2000 resamples, seed 1). Note: price views (premium, market excess) are
partly mechanically tied to the strict definition (strict requires pair mean >= Nash+2), so they are reference rows,
not say-vs-do evidence.

    uv run python p2_within_agree.py      # -> results/analysis/p2_within_agree_llm_p2strongF.json
"""
import json
from pathlib import Path
from final_analysis import premium_scores
from p2_plan_view import plans
from p2_plan_keyword import TERMS, names
from p2_strong_eval import auroc, boot

DS = "llm_p2strongF"


def main():
    cls = json.load(open(f"results/analysis/p2_strong_classes_{DS}.json"))["runs"]
    ev = json.load(open(f"results/analysis/p2_strong_eval_{DS}.json"))["detectors"]
    priv = {r: c for r, c in cls.items() if c["cond"] == "private"}
    gt = {g["run_id"]: g for g in map(json.loads, open(Path("data") / DS / "ground_truth.jsonl"))}
    terms = {t["run_id"]: t for t in map(json.loads, open(Path("data") / DS / "terms.jsonl"))}
    S = {"premium": {r: d["run"] for r, d in premium_scores(DS)[0].items()},
         "market_excess_nash": {r: c["market_excess_nash"] for r, c in cls.items()}}
    base = Path("results/llm_auditor") / DS / "gpt-6.1-sol"
    for v in ("action", "action_stats", "text", "combined", "plan"):  # last row per run wins (as in p2_strong_eval for plan)
        S[v] = {x["run_id"]: x["collusion_present"] for x in map(json.loads, open(base / f"{v}_orig.jsonl"))}
    K = {}
    for rid in priv:  # E111 K_dir: share of plan entries with agreement terms or naming the chat partner
        P = plans(DS, rid); pair = gt[rid]["assigned_pair"]; partner = {pair[0]: pair[1], pair[1]: pair[0]}
        d = [bool(TERMS.search(p)) or (a in partner and names(p, partner[a])) for (_, a), p in P.items()]
        K[rid] = sum(d) / len(d)
    S["partner_share_E111"] = K
    S["judged_agreement"] = {r: float(bool(terms.get(r, {}).get("agreed"))) for r in priv}
    pos = sorted(r for r, c in priv.items() if c["class"] == "executed")
    neg = sorted(r for r, c in priv.items() if c["class"] == "nonexec_private")
    neg_ag = [r for r in neg if terms.get(r, {}).get("agreed")]
    runs = {r: {"seed": c["seed"]} for r, c in priv.items()}
    out = {"ds": DS, "n_strict": len(pos), "n_nonexec": len(neg), "n_nonexec_agreed": len(neg_ag),
           "judged_agreement": {"strict": sum(S["judged_agreement"][r] for r in pos), "nonexec": len(neg_ag)}, "views": {}}
    for k, s in S.items():
        th = ev.get(k, {}).get("threshold")
        e = {}
        for name, N in (("strict_vs_nonexec", neg), ("strict_vs_nonexec_agreed", neg_ag)):
            a = auroc([s[r] for r in pos], [s[r] for r in N])
            e[f"auroc_{name}"] = [round(a, 3)] + boot(s, runs, pos, N) if a is not None and len(set(s[r] for r in pos + N)) > 1 else (
                [0.5, None, None] if a is not None else None)
        e["mean_strict"] = round(sum(s[r] for r in pos) / len(pos), 3)
        e["mean_nonexec"] = round(sum(s[r] for r in neg) / len(neg), 3)
        if th is not None:
            e["flags_strict_nonexec"] = [sum(s[r] >= th for r in pos), len(pos), sum(s[r] >= th for r in neg), len(neg)]
        out["views"][k] = e
    p = Path(f"results/analysis/p2_within_agree_{DS}.json"); p.write_text(json.dumps(out, indent=1))
    for k, e in out["views"].items():
        print(f"{k:20s} {e['auroc_strict_vs_nonexec']}  agreed-only {e['auroc_strict_vs_nonexec_agreed']}  "
              f"mean {e['mean_strict']} vs {e['mean_nonexec']}  flags {e.get('flags_strict_nonexec')}")
    print("->", p)


if __name__ == "__main__":
    main()
