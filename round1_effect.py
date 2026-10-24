"""Post-lock DESCRIPTIVE check (iter 13): round-1 prices are chosen simultaneously with the first private message,
i.e. BEFORE any partner message is seen (llm_market.py: private history is empty in round 1). Any round-1 pair premium
in `private` runs is therefore a unilateral response to being told one has a channel (treatment effect), not the
product of coordination communication. Reports round-1 price by role/condition and the round-1 notes that mention
the partner/channel. Bootstrap CI over runs for mean differences.

    uv run python round1_effect.py --ds llm_v3   # -> results/analysis/round1_effect_<ds>.json
"""
import argparse, json, re
from pathlib import Path
import numpy as np

AG = ["A", "B", "C", "D"]


def bci(x, n=2000, seed=0):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    b = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return [round(float(x.mean()), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ds", default="llm_v3"); a = ap.parse_args()
    D = Path("data") / a.ds
    gt = {}
    for l in open(D / "ground_truth.jsonl"):
        g = json.loads(l); gt[g["run_id"]] = g
    r1 = {}
    for l in open(D / "trajectories.jsonl"):
        r = json.loads(l)
        if r["round"] == 0:
            r1[r["run_id"]] = {x["id"]: x["price"] for x in r["agents"]}
    rows = {}
    for rid, p in r1.items():
        g = gt[rid]; pair = g.get("pair") or g.get("assigned_pair")
        others = [x for x in AG if x not in pair]
        prem = np.mean([p[x] for x in pair]) - np.mean([p[x] for x in others])
        rows.setdefault(g["condition"], []).append({"pair_mean": np.mean([p[x] for x in pair]),
                                                    "others_mean": np.mean([p[x] for x in others]), "premium": prem})
    out = {"ds": a.ds, "by_condition": {}}
    for c, R in rows.items():
        out["by_condition"][c] = {"n": len(R), **{k: bci([r[k] for r in R]) for k in ("pair_mean", "others_mean", "premium")},
                                  "frac_premium_gt0": round(float(np.mean([r["premium"] > 0 for r in R])), 3)}
    # round-1 private messages: share that already state a price number / propose (sent before seeing partner)
    pm = [json.loads(l) for l in open(D / "private.jsonl")]
    m0 = [m["text"] for x in pm for m in x["chat"] if m["round"] == 0]
    out["round1_private_msgs"] = {"n": len(m0), "frac_with_number": round(float(np.mean([bool(re.search(r"\d", t)) for t in m0])), 3),
                                  "examples": m0[:4]}
    Path(f"results/analysis/round1_effect_{a.ds}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
