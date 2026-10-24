"""E87 follow-up (Opus review, post hoc, no LLM calls): static competitive benchmark for the legitimate-asymmetry arms.
Continuous Bertrand-Nash of the simulator's logit demand (llm_market.demand: mu=4, a=16, outside good) via the FOC
fixed point p_i = c_i + mu / (1 - s_i), for common costs 5..8: highcost = pair cost +2, quality = pair quality +2.
Reports the asymmetric pair's competitive premium (pair mean - other-two mean) vs the frozen premium threshold, and the
competitive own-price pass-through of the +2 cost.

    uv run python p2_asym_nash.py   # -> results/analysis/p2_asym_nash.json
"""
import json, math
from pathlib import Path
from llm_market import A_Q, MU

TH = json.load(open("results/analysis/final_llm_v3_gpt-6.1-sol_dev.json"))["thresholds_dev_youden"]["premium"]


def nash(cost, quality):
    p = [c + MU for c in cost]
    for _ in range(5000):
        ex = [math.exp((A_Q + g - x) / MU) for x, g in zip(p, quality)]
        den = sum(ex) + 1.0
        p = [c + MU / (1 - e / den) for c, e in zip(cost, ex)]
    return p


out = {"frozen_premium_threshold": round(TH, 3), "by_cost": {}}
for c in (5, 6, 7, 8):
    sym = nash([c] * 4, [0] * 4)
    hc = nash([c + 2, c + 2, c, c], [0] * 4)
    ql = nash([c] * 4, [2, 2, 0, 0])
    out["by_cost"][c] = {"symmetric": round(sym[0], 3),
                         "highcost_pair_premium": round((hc[0] + hc[1]) / 2 - (hc[2] + hc[3]) / 2, 3),
                         "highcost_own_passthrough": round((hc[0] - sym[0]) / 2, 3),
                         "quality_pair_premium": round((ql[0] + ql[1]) / 2 - (ql[2] + ql[3]) / 2, 3)}
Path("results/analysis/p2_asym_nash.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
