"""Preserve the numerical sources of the existing mechanism figure and captions.

python3 -S check_mechanism_sources.py          # save descriptive sources only
python3 -S check_mechanism_sources.py --check  # read-only, standard library only

Reconstructs the existing fig_mechanism.py summaries from public prices and
assignment metadata. No labels/private chats, LLMs, detection metrics, bootstrap,
thresholds, or figure rendering. The normal bands are the figure's pointwise
mean +/- 1.96 sample SE, not simultaneous or bootstrap intervals. The resulting
record is post-hoc preservation, not a new experiment or registration.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from statistics import stdev
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
OUTPUT = "results/analysis/mechanism_sources.json"
SOURCES = ("check_mechanism_sources.py", "fig_mechanism.py",
           "data/llm_v3/ground_truth.jsonl", "data/llm_v3/trajectories.jsonl")
COUNTS = {"dev": {"private": 20, "none": 5, "legit": 5},
          "test": {"private": 50, "none": 30, "legit": 15},
          "all": {"private": 70, "none": 35, "legit": 20}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def records(root, name):
    return [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]


def load(root):
    rows = records(root, "data/llm_v3/ground_truth.jsonl")
    gt = {r["run_id"]: r for r in rows}
    require(len(rows) == len(gt) == 125 and set(gt) == {f"llm_v3_{i:04d}" for i in range(125)},
            "mechanism sources: exact 125-run cohort required")
    for rid, g in gt.items():
        require(g["condition"] in COUNTS["all"] and g["rounds"] == 12,
                f"{rid}: condition/round count")
        pair = g["assigned_pair"]
        require(isinstance(pair, list) and len(pair) == 2 and
                len(set(pair)) == 2 and set(pair) <= set("ABCD"), f"{rid}: assigned pair")
    prices = defaultdict(dict)
    for r in records(root, "data/llm_v3/trajectories.jsonl"):
        rid, t = r["run_id"], r["round"]
        require(rid in gt and type(t) is int and 0 <= t < 12 and t not in prices[rid],
                f"{rid}: unexpected/duplicate round")
        agents = r["agents"]
        require(len(agents) == 4 and {a["id"] for a in agents} == set("ABCD"),
                f"{rid}/{t}: four distinct firms required")
        require(all(type(a["price"]) is int and 6 <= a["price"] <= 30 for a in agents),
                f"{rid}/{t}: integer prices in [6,30] required")
        prices[rid][t] = {a["id"]: a["price"] for a in agents}
    require(set(prices) == set(gt) and all(set(v) == set(range(12)) for v in prices.values()),
            "mechanism sources: complete 12-round public paths required")
    return gt, prices


def numeric(value):
    return round(float(value), 12)


def mean(values):
    return sum(values) / len(values)


def summarize(gt, prices, split):
    groups = {}
    for condition in ("private", "none", "legit"):
        ids = sorted(rid for rid, g in gt.items() if g["condition"] == condition and
                     (split == "all" or (int(rid[-4:]) < 30) == (split == "dev")))
        require(len(ids) == COUNTS[split][condition], f"{split}/{condition}: frozen condition count")
        paths = {}
        for rid in ids:
            pair = set(gt[rid]["assigned_pair"])
            paths[rid] = {role: [Fraction(sum(p[f] for f in firms), 2)
                                 for _, p in sorted(prices[rid].items())]
                          for role, firms in (("assigned_pair", pair), ("other_two", set("ABCD") - pair))}
        rounds = []
        for t in range(12):
            row = {"round": t + 1}
            for role in ("assigned_pair", "other_two"):
                values = [paths[rid][role][t] for rid in ids]
                halfwidth = 1.96 * stdev(values) / math.sqrt(len(ids))
                row[role] = {"mean": numeric(mean(values)), "normal_95_halfwidth": numeric(halfwidth)}
            rounds.append(row)
        # Match the original figure's rounds 9-12 (zero-based ids 8..11),
        # deliberately distinct from the label file's rounds 5-12 summary.
        late = {rid: mean([paths[rid]["assigned_pair"][t] - paths[rid]["other_two"][t]
                           for t in range(8, 12)]) for rid in ids}
        groups[condition] = {"n_runs": len(ids), "rounds": rounds,
                             "late_rounds": [9, 10, 11, 12],
                             "late_premium_by_run": {rid: numeric(v) for rid, v in late.items()},
                             "late_premium_mean": numeric(mean(list(late.values()))),
                             "late_premium_n_positive": sum(v > 0 for v in late.values())}
    return groups


def build(root=ROOT):
    gt, prices = load(root)
    return {"schema_version": 1, "post_hoc": True,
            "note": "Numerical sources for existing mechanism figures/captions, not registration. "
                    "Condition summaries, not agreement-driven effects. Bands are pointwise "
                    "mean +/- 1.96 sample SE across runs; no bootstrap or multiplicity adjustment.",
            "sources_sha256": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in SOURCES},
            "splits": {split: summarize(gt, prices, split) for split in COUNTS}}


def captions(result):
    def late(split):
        g = result["splits"][split]
        p = g["private"]
        return (f"late-window (rounds 9–12) pair-minus-rivals premium {p['late_premium_mean']:+.2f} "
                f"(none {g['none']['late_premium_mean']:+.2f}, legit {g['legit']['late_premium_mean']:+.2f}), "
                f"positive in {p['late_premium_n_positive']}/{p['n_runs']} private runs.")
    dev = result["splits"]["dev"]["private"]["rounds"][0]
    return {"test": "Descriptive test: " + late("test"),
            "dev": (f"Descriptive dev: private pairs' mean opening price "
                    f"{dev['assigned_pair']['mean']:.2f} vs {dev['other_two']['mean']:.2f} for rivals; " + late("dev"))}


def encoded(result):
    return (json.dumps(result, indent=2) + "\n").encode()


def check(root=ROOT):
    result = build(root)
    require((root / OUTPUT).read_bytes() == encoded(result), "stale mechanism source record")
    report = (root / "REPORT.md").read_text()
    for split, caption in captions(result).items():
        image = f"![mechanism {split}](figures/mechanism_{split}.png)\n"
        require(report.count(image) == 1, f"REPORT mechanism {split} image missing or duplicated")
        following_line = report.split(image, 1)[1].splitlines()[0]
        require(following_line == f"*{caption}*",
                f"REPORT mechanism {split} caption differs from public sources")
    require(OUTPUT in report, "REPORT missing mechanism JSON source")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    try:
        if not args.check:
            (ROOT / OUTPUT).write_bytes(encoded(build()))
        result = check()
        print("PASS: mechanism sources, pointwise normal bands and report captions; 125 public runs, "
              "12 rounds each; dev/test/all; no detection metrics, model calls or figure changes.")
        for caption in captions(result).values():
            print(caption)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        raise SystemExit(f"FAIL: {exc}")


if __name__ == "__main__":
    main()
