"""E78 wording band (registered): private-none pair premium r2_12 per prompt wording on the SAME 10 matched seeds
(sysvar 0 = llm_p2cue seeds k<10, 1 = llm_p2para1, 2 = llm_p2para2), plus paired between-wording differences of the
private-none effect (seed bootstrap). Reads the frozen p2_cue_<ds>.json outputs; no calls.

    uv run python p2_band.py   # -> results/analysis/p2_band.json
"""
import json
from pathlib import Path
from p2_cue import boot_mean

DS = {"sysvar0 (original)": "llm_p2cue", "sysvar1 (paraphrase 1)": "llm_p2para1", "sysvar2 (paraphrase 2, terse)": "llm_p2para2"}


def effect(ds, key):
    o = json.load(open(f"results/analysis/p2_cue_{ds}.json"))
    pr = {r["seed"]: r[key] for r in o["per_run"]["private"]}; no = {r["seed"]: r[key] for r in o["per_run"]["none"]}
    return {s: pr[s] - no[s] for s in pr if s in no}, o


out = {"note": "E78; premium = assigned-pair premium; paired over matched seeds; seed bootstrap 2000"}
seeds = set.intersection(*[set(effect(d, "prem_r2_12")[0]) for d in DS.values()])
out["seeds"] = sorted(seeds)
E = {}
for name, ds in DS.items():
    e, o = effect(ds, "prem_r2_12"); e1, _ = effect(ds, "prem_r1")
    E[name] = e
    pr = {r["seed"]: r for r in o["per_run"]["private"]}; no = {r["seed"]: r for r in o["per_run"]["none"]}
    out[name] = {"ds": ds, "private_minus_none_prem_r2_12": boot_mean([e[s] for s in seeds]),
                 "private_minus_none_prem_r1": boot_mean([e1[s] for s in seeds]),
                 "flags_private": sum(pr[s]["flag"] for s in seeds), "flags_none": sum(no[s]["flag"] for s in seeds)}
names = list(DS)
for i in range(3):
    for j in range(i + 1, 3):
        out[f"{names[j]} - {names[i]}"] = boot_mean([E[names[j]][s] - E[names[i]][s] for s in seeds])
Path("results/analysis/p2_band.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))


def opening_numbers(ds):
    """Descriptive: first 1-2 digit number in each round-1 private message of `private` runs (the price named)."""
    import re
    cond = {g["run_id"]: g["condition"] for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
    seedof = {g["run_id"]: g["seed"] for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
    v = []
    for l in open(f"data/{ds}/private.jsonl"):
        r = json.loads(l)
        if cond.get(r["run_id"]) != "private" or seedof[r["run_id"]] not in seeds:
            continue
        for m in r["chat"]:
            x = re.search(r"\b(\d{1,2})\b", m["text"]) if m["round"] == 0 else None
            if x:
                v.append(int(x.group(1)))
    import numpy as np
    return {"n_msgs_with_number": len(v), "median": float(np.median(v)) if v else None,
            "share_ge_17": round(sum(x >= 17 for x in v) / len(v), 3) if v else None}


for name, ds in DS.items():
    out[name]["round1_named_price"] = opening_numbers(ds)
Path("results/analysis/p2_band.json").write_text(json.dumps(out, indent=1))
print({n: out[n]["round1_named_price"] for n in DS})


def pair_vs_others(ds):
    """Descriptive decomposition of the premium: mean pair price and mean other-two price, round 1 and rounds 2-12."""
    import numpy as np
    gt = {g["run_id"]: g for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
    acc = {}
    for l in open(f"data/{ds}/trajectories.jsonl"):
        r = json.loads(l); g = gt.get(r["run_id"])
        if not g or g["seed"] not in seeds or g["condition"] not in ("private", "none"):
            continue
        pr = {a["id"]: a["price"] for a in r["agents"]}; pair = g["assigned_pair"]
        k = f"{g['condition']}_{'r1' if r['round'] == 0 else 'r2_12'}"
        acc.setdefault(k, ([], []))
        acc[k][0].append(np.mean([pr[a] for a in pair])); acc[k][1].append(np.mean([pr[a] for a in pr if a not in pair]))
    return {k: {"pair": round(float(np.mean(v[0])), 2), "others": round(float(np.mean(v[1])), 2)} for k, v in sorted(acc.items())}


for name, ds in DS.items():
    out[name]["pair_vs_others_price"] = pair_vs_others(ds)
Path("results/analysis/p2_band.json").write_text(json.dumps(out, indent=1))
print({n: out[n]["pair_vs_others_price"] for n in DS})


def opening_proposal_per_pair(ds):
    """Descriptive: per private run, max of the first 1-2 digit numbers named in the pair's round-1 messages
    (the opening price on the table). Counts pairs whose opening proposal is >= 17 vs <= 13."""
    import re
    gt = {g["run_id"]: g for g in map(json.loads, open(f"data/{ds}/ground_truth.jsonl"))}
    res = {}
    for l in open(f"data/{ds}/private.jsonl"):
        r = json.loads(l); g = gt[r["run_id"]]
        if g["condition"] != "private" or g["seed"] not in seeds:
            continue
        v = [int(x.group(1)) for m in r["chat"] if m["round"] == 0 for x in [re.search(r"\b(\d{1,2})\b", m["text"])] if x]
        res[r["run_id"]] = max(v) if v else None
    vals = [v for v in res.values() if v is not None]
    return {"per_run": res, "n_ge_17": sum(v >= 17 for v in vals), "n_le_13": sum(v <= 13 for v in vals), "n": len(res)}


for name, ds in DS.items():
    out[name]["opening_proposal_per_pair"] = opening_proposal_per_pair(ds)
Path("results/analysis/p2_band.json").write_text(json.dumps(out, indent=1))
print({n: {k: v for k, v in out[n]["opening_proposal_per_pair"].items() if k != "per_run"} for n in DS})
print(out["sysvar2 (paraphrase 2, terse)"]["opening_proposal_per_pair"]["per_run"])
