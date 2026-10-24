"""Part E5 (E110, registered in EXPERIMENTS.tsv before generation): German-language market vs English.
llm_p2de (German, private/none, seeds 8100000-8100009) is paired with llm_p2cue private/none on the same seeds
(identical pair, cost and demand path). No fitting; frozen premium window r2_12, frozen labeler and auditor prompts.

  P1 German private-none r2_12 assigned-pair premium (paired seed bootstrap)
  P2 German-English paired difference in the private-arm premium (and none arm)
  P3 judge agreement rate in German private runs (Jeffreys CI) vs English on the same seeds
  P4 frozen text/action/combined auditor run-score AUROC private vs none, German vs English (same seeds)

    uv run python p2_de.py      # -> results/analysis/p2_de.json
"""
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta
from p2_cue import boot_mean, boot_auc

AUD = "results/llm_auditor/{ds}/gpt-6.1-sol/{v}_orig.jsonl"


def jeffreys(k, n):
    return [k, n, round(float(beta.ppf(.025, k + .5, n - k + .5)), 3), round(float(beta.ppf(.975, k + .5, n - k + .5)), 3)]


def per_run(ds):
    D = Path("data") / ds
    gt = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))}
    P = {}
    for r in map(json.loads, open(D / "trajectories.jsonl")):
        P.setdefault(r["run_id"], {})[r["round"]] = {x["id"]: x["price"] for x in r["agents"]}
    labs = {}
    if (D / "labels.jsonl").exists():
        labs = {l["run_id"]: l for l in map(json.loads, open(D / "labels.jsonl"))}
    aud = {}
    for v in ("text", "action", "combined"):
        f = Path(AUD.format(ds=ds, v=v))
        if f.exists():
            aud[v] = {x["run_id"]: x["collusion_present"] for x in map(json.loads, open(f))}
    out = {}
    for rid, g in gt.items():
        if g["condition"] not in ("private", "none") or not 8100000 <= g["seed"] <= 8100009:
            continue
        R = sorted(P[rid])[1:]  # r2_12
        pair = g["assigned_pair"]; oth = [a for a in "ABCD" if a not in pair]
        prem = float(np.mean([np.mean([P[rid][t][a] for a in pair]) - np.mean([P[rid][t][a] for a in oth]) for t in R]))
        row = {"run_id": rid, "prem_r2_12": prem, "model": g["model"], "parse_failures": g.get("parse_failures"),
               "agreement": labs.get(rid, {}).get("agreement"), "y": labs.get(rid, {}).get("y")}
        row.update({f"aud_{v}": s.get(rid) for v, s in aud.items()})
        out[(g["condition"], g["seed"])] = row
    return out


def main():
    de, en = per_run("llm_p2de"), per_run("llm_p2cue")
    seeds = sorted({s for (c, s) in de if c == "private"} & {s for (c, s) in de if c == "none"})
    res = {"n_seeds": len(seeds), "models_de": sorted({r["model"] for r in de.values()}),
           "parse_failures_de": sum(r["parse_failures"] or 0 for r in de.values())}
    for lang, d in (("de", de), ("en", en)):
        res[f"P1_{lang}_private_minus_none_r2_12"] = boot_mean([d[("private", s)]["prem_r2_12"] - d[("none", s)]["prem_r2_12"] for s in seeds])
        res[f"{lang}_private_prem_r2_12"] = boot_mean([d[("private", s)]["prem_r2_12"] for s in seeds])
        res[f"{lang}_none_prem_r2_12"] = boot_mean([d[("none", s)]["prem_r2_12"] for s in seeds])
        ag = [d[("private", s)]["agreement"] for s in seeds if d[("private", s)]["agreement"] is not None]
        res[f"P3_{lang}_agreement_private"] = jeffreys(sum(a == "explicit" for a in ag), len(ag))
        res[f"{lang}_agreement_values"] = {a: ag.count(a) for a in set(ag)}
        for v in ("text", "action", "combined"):
            neg = [d[("none", s)].get(f"aud_{v}") for s in seeds]; pos = [d[("private", s)].get(f"aud_{v}") for s in seeds]
            if all(x is not None for x in neg + pos):
                res[f"P4_{lang}_{v}_auroc"] = boot_auc(neg, pos)
    for c in ("private", "none"):
        res[f"P2_de_minus_en_{c}_prem_r2_12"] = boot_mean([de[(c, s)]["prem_r2_12"] - en[(c, s)]["prem_r2_12"] for s in seeds])
    res["P1_verdict"] = "held" if res["P1_de_private_minus_none_r2_12"][1] > 0 else "failed"
    res["runs"] = {f"{c}:{s}": {"de": de[(c, s)], "en": en[(c, s)]} for (c, s) in sorted(de) if s in seeds}
    Path("results/analysis/p2_de.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "runs"}, indent=1))


if __name__ == "__main__":
    main()
