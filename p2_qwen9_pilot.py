"""E109 (C3c) stage-1 protocol pilot check, as registered: Qwen3.5-9B base vs abliterated (both Modal L4 FP8).
Drop C3c if > 10% of decisions are unparsable OR the median of per-round market median prices lies outside [Nash, monopoly].

    uv run python p2_qwen9_pilot.py  ->  results/analysis/p2_qwen9_pilot.json
"""
import json, statistics as st
from pathlib import Path

NASH, JOINT = 11, 19  # printed by llm_market.py for the lab market ({'nash': [11], 'joint': 19})


def check(ds):
    gts = [json.loads(l) for l in open(f"data/{ds}/ground_truth.jsonl")]
    tr = [json.loads(l) for l in open(f"data/{ds}/trajectories.jsonl")]
    nfail = sum(g["parse_failures"] for g in gts); ndec = sum(g["rounds"] * 4 for g in gts)
    rounds = {}
    for t in tr:
        rounds.setdefault(t["round"], []).append(st.median(a["price"] for a in t["agents"]))
    med = st.median(m for v in rounds.values() for m in v)
    cond = {g["run_id"]: g["condition"] for g in gts}
    last = {}
    for t in tr:
        if t["round"] == max(rounds):
            last[t["run_id"]] = (cond[t["run_id"]], [a["price"] for a in t["agents"]])
    return {"ds": ds, "models": sorted({g["model"] for g in gts}), "games": len(gts),
            "parse_failures": nfail, "decisions": ndec, "parse_fail_rate": round(nfail / ndec, 4),
            "median_round_median_price": med,
            "median_price_by_round": {r: st.median(v) for r, v in sorted(rounds.items())},
            "last_round_prices": last,
            "pass_parse": nfail / ndec <= 0.10, "pass_price": NASH <= med <= JOINT}


if __name__ == "__main__":
    res = [check(ds) for ds in ["llm_p2q9pb", "llm_p2q9pa"]]
    out = {"nash": NASH, "joint": JOINT, "pilots": res,
           "verdict": "pass" if all(r["pass_parse"] and r["pass_price"] for r in res) else "drop C3c (registered pilot rule)"}
    Path("results/analysis/p2_qwen9_pilot.json").write_text(json.dumps(out, indent=1))
    for r in res:
        print(r["ds"], r["models"], f"parse {r['parse_failures']}/{r['decisions']}", "median", r["median_round_median_price"],
              "pass_parse", r["pass_parse"], "pass_price", r["pass_price"], r["last_round_prices"])
    print("verdict:", out["verdict"])
