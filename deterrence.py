"""Exploration (iter 11, post-lock, descriptive): does ANNOUNCING a price monitor deter LLM sellers from using a
private channel to agree on prices? Compares llm_v3 (lab framing, all 125 runs; the locked test is already done) with
llm_v3mon (lab framing + MONITOR_NOTE in the system prompt; the monitor cannot see private messages).
Different seeds/run counts and 12 rounds in both; one seller model (gpt-6-luna). Nothing is fitted.

    uv run python deterrence.py
"""
import json, re
from pathlib import Path
import numpy as np
from scipy.stats import fisher_exact
from fp_stratum import wilson
from final_analysis import premium_scores

NUM = re.compile(r"\b\d+\b")
INDEP = re.compile(r"independent|won.t coordinate|can.t (agree|coordinate|discuss)|not proposing|avoid discussing", re.I)


def stats(ds):
    labs = [json.loads(l) for l in open(Path("data") / ds / "labels.jsonl")]
    priv = {r["run_id"]: r for r in map(json.loads, open(Path("data") / ds / "private.jsonl"))}
    prem, markup = premium_scores(ds)
    P = [x for x in labs if x["condition"] == "private"]
    y = [x["agreement"] in ("explicit", "info_exchange") for x in P]
    msgs = [m["text"] for x in P for m in priv[x["run_id"]]["chat"]]
    ap = lambda xs: [prem[x["run_id"]]["scores"]["".join(x["assigned_pair"])] for x in xs]
    N = [x for x in labs if x["condition"] == "none"]
    return {"n_private": len(P), "agreements": int(sum(y)), "agreement_rate": wilson(int(sum(y)), len(P)),
            "n_private_msgs": len(msgs), "msgs_with_number": wilson(sum(bool(NUM.search(m)) for m in msgs), len(msgs)),
            "msgs_with_independence_disclaimer": wilson(sum(bool(INDEP.search(m)) for m in msgs), len(msgs)),
            "assigned_pair_premium_private_mean": round(float(np.mean(ap(P))), 3),
            "assigned_pair_premium_none_mean": round(float(np.mean(ap(N))), 3) if N else None,
            "mean_markup_private": round(float(np.mean([markup[x["run_id"]] for x in P])), 2),
            "mean_markup_none": round(float(np.mean([markup[x["run_id"]] for x in N])), 2) if N else None,
            "frac_private_premium_gt_1": round(float(np.mean([v > 1 for v in ap(P)])), 3)}


def main():
    out = {ds: stats(ds) for ds in ("llm_v3", "llm_v3mon")}
    a, b = out["llm_v3"], out["llm_v3mon"]
    out["fisher_agreement"] = fisher_exact([[a["agreements"], a["n_private"] - a["agreements"]],
                                            [b["agreements"], b["n_private"] - b["agreements"]]])[1]
    Path("results/analysis/deterrence.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
