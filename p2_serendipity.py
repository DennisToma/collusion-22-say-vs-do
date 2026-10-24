"""E108 / Part E4: portable, frozen transcript sample; exploratory checks only.

uv run python p2_serendipity.py freeze
uv run python p2_serendipity.py read --start 0 --stop 10
uv run python p2_serendipity.py check
uv run python p2_serendipity.py analyse

Sampling reads committed git objects, never mutable generation files. After freeze,
all inspection/checks use the committed gzip, without requiring the sibling repo.
No LLM calls, detector fitting, headline evaluation, or writes to the sibling.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data/serendipity_e108"
SEED = 2026102418
# Explicitly exclude ongoing arms and imported copies. Stopped, small pilots stay
# eligible: this is qualitative exploration, not a sample for population inference.
EXCLUDE = {
    "q22": {"llm_p2strongF", "llm_p2qwenaS", "llm_p2qwenbS"},
    "q14": {"llm_strong_qa", "llm_qb36_p2", "llm_qa36_p2"},
}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def records(raw):
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "sample.jsonl.gz").exists():
        raise SystemExit("sample already frozen; refusing to resample")
    rng = random.Random(SEED)
    manifest = {"experiment": "E108", "seed": SEED, "sampling":
                "20 datasets per repo without replacement, then one uniform run per dataset; "
                "if fewer than 20 eligible datasets, add runs from random datasets without replacement",
                "excluded_datasets": {k: sorted(v) for k, v in EXCLUDE.items()}, "repos": {}}
    samples = []
    for repo, root in [("q22", ROOT), ("q14", ROOT.parent / "collusion-14-infotheory")]:
        commit = git(root, "rev-parse", "HEAD").decode().strip()
        paths = set(git(root, "ls-tree", "-r", "--name-only", commit, "data").decode().splitlines())
        pool, sources = {}, {}
        datasets = sorted({p.split("/")[1] for p in paths if p.startswith("data/llm") and
                           p.endswith("/ground_truth.jsonl")})
        for ds in datasets:
            tp = f"data/{ds}/trajectories.jsonl"
            if ds in EXCLUDE[repo] or tp not in paths:
                continue
            gp = f"data/{ds}/ground_truth.jsonl"
            blobs = {p: git(root, "show", f"{commit}:{p}") for p in [gp, tp]}
            pp = f"data/{ds}/private.jsonl"
            if pp in paths:
                blobs[pp] = git(root, "show", f"{commit}:{pp}")
            gs = {g["run_id"]: g for g in records(blobs[gp])}
            rs = {}
            for row in records(blobs[tp]):
                rs.setdefault(row["run_id"], []).append(row)
            private = {p["run_id"]: p for p in records(blobs.get(pp, b""))}
            eligible = {}
            for rid, ground in sorted(gs.items()):
                rows = sorted(rs.get(rid, []), key=lambda x: x["round"])
                if not rows or [r["round"] for r in rows] != list(range(len(rows))):
                    continue
                expected = ground.get("T", ground.get("rounds"))
                if expected is not None and len(rows) != expected:
                    continue
                chat = private.get(rid, {}).get("chat", ground.get("private_chat", []))
                eligible[rid] = {"repo": repo, "dataset": ds, "run_id": rid,
                                 "source_commit": commit, "ground_truth": ground,
                                 "private_chat": chat, "rounds": rows}
            if eligible:
                pool[ds] = eligible
                sources[ds] = {"n_eligible": len(eligible), "sha256":
                               {p: hashlib.sha256(b).hexdigest() for p, b in blobs.items()}}
        selected = []
        for ds in rng.sample(sorted(pool), min(20, len(pool))):
            selected.append(rng.choice(sorted(pool[ds])))
            samples.append(pool[ds][selected[-1]])
        while len(selected) < 20:
            remaining = [(ds, rid) for ds in sorted(pool) for rid in sorted(pool[ds]) if rid not in selected]
            ds, rid = rng.choice(remaining)
            selected.append(rid)
            samples.append(pool[ds][rid])
        manifest["repos"][repo] = {"commit": commit, "datasets": sources}
    raw = b"".join((json.dumps(s, sort_keys=True) + "\n").encode() for s in samples)
    (OUT / "sample.jsonl.gz").write_bytes(gzip.compress(raw, mtime=0))
    manifest.update(n_sample=len(samples), sample_sha256=hashlib.sha256(raw).hexdigest(),
                    selected=[{k: s[k] for k in ("repo", "dataset", "run_id")} for s in samples])
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"n_sample": len(samples), "compressed_bytes": (OUT / "sample.jsonl.gz").stat().st_size,
                      "eligible_datasets": {r: len(v["datasets"]) for r, v in manifest["repos"].items()}}))


def load():
    raw = gzip.decompress((OUT / "sample.jsonl.gz").read_bytes())
    manifest = json.loads((OUT / "manifest.json").read_text())
    assert hashlib.sha256(raw).hexdigest() == manifest["sample_sha256"]
    sample = records(raw)
    assert len(sample) == manifest["n_sample"] == 40
    assert len({(s["repo"], s["dataset"], s["run_id"]) for s in sample}) == 40
    assert manifest["selected"] == [{k: s[k] for k in ("repo", "dataset", "run_id")} for s in sample]
    return sample


def read(start, stop):
    for i, s in enumerate(load()[start:stop], start):
        g = s["ground_truth"]
        print(f"\nCASE {i} {s['repo']}/{s['dataset']}/{s['run_id']} cond={g['condition']} pair={g['assigned_pair']}")
        for m in s["private_chat"]:
            print("PRIVATE", m.get("round"), m.get("from", m.get("sender")),
                  m.get("text", m.get("private_message")))
        for row in s["rounds"]:
            print("r", row["round"], "state", row["market"], "prices",
                  {a["id"]: a["price"] for a in row["agents"]})
            for a in row["agents"]:
                if a.get("public_message"):
                    print(a["id"], a["public_message"])


def check():
    sample = load()
    print("PASS: portable sample hash, count, unique ids, manifest order")
    for s in sample:
        rows = s["rounds"]
        assert [r["round"] for r in rows] == list(range(len(rows)))
        assert all(len(r["agents"]) == 4 and {a["id"] for a in r["agents"]} == set("ABCD") for r in rows)
        expected = s["ground_truth"].get("T", s["ground_truth"].get("rounds"))
        assert expected is None or len(rows) == expected
    print("PASS: all 40 sampled runs have contiguous rounds and four firms")


# Exploratory, manually read from the frozen opening exchanges. These are NOT
# new execution labels: many promises explicitly refer only to the opening round.
OPENING_TARGETS = {
    "llm_strong_luna_pilot_C_001": 12, "llm_v1_C_011": 12,
    "llm_p2_v0_C_002": 12, "llm_p2_template_C_000": 12,
    "llm_p2_para_C_004": 12, "llm_pilot2_C_000": 12,
    "llm_ds_p2_C_006": 20, "llm_g56l_p2_C_007": 18,
}
OWN_PRICE = re.compile(
    r"\bI(?:['’]m| am|['’]ll| will) (?:planning (?:to )?|choosing |"
    r"setting (?:my price (?:at |to )?)?|pricing (?:at )?|price (?:at )?|"
    r"hold (?:at )?|holding (?:at )?|staying (?:at )?)(\d{1,2})\b", re.I)


def speaker(m):
    return m.get("from", m.get("sender"))


def message(m):
    return m.get("text", m.get("private_message", ""))


def mean(xs):
    return sum(xs) / len(xs)


def streak(flags):
    best = current = 0
    for f in flags:
        current = current + 1 if f else 0
        best = max(best, current)
    return best


def evidence(sample, rid, rnd, who, channel, substring):
    s, = [s for s in sample if s["run_id"] == rid]
    if channel == "private":
        hits = [message(m) for m in s["private_chat"] if m["round"] == rnd and speaker(m) == who]
    else:
        hits = [a["public_message"] for r in s["rounds"] if r["round"] == rnd
                for a in r["agents"] if a["id"] == who]
    text, = [t for t in hits if substring in t]
    return {"repo": s["repo"], "dataset": s["dataset"], "run_id": rid, "round_zero_indexed": rnd,
            "agent": who, "channel": channel, "text": text}


def analyse():
    sample = load()
    q22 = [s for s in sample if s["repo"] == "q22"]
    manifest = json.loads((OUT / "manifest.json").read_text())
    out = {"experiment": "E108", "status": "post-hoc exploratory; descriptive, not confirmatory",
           "sample_sha256": manifest["sample_sha256"], "n_runs": len(sample),
           "n_rounds": sum(len(s["rounds"]) for s in sample),
           "auditor_detector_tuning_attempts": 0, "new_games": 0, "new_llm_calls": 0,
           "round_indexing": "zero-based throughout", "checks": {}}

    # E108a: opening-price fidelity is a description, NOT an execution relabel.
    tolerance = []
    for s in sample:
        if s["run_id"] not in OPENING_TARGETS:
            continue
        target = OPENING_TARGETS[s["run_id"]]
        opening = [m for m in s["private_chat"] if m["round"] == -1]
        assert len(opening) == 2 and all(re.search(rf"\b{target}\b", message(m)) for m in opening)
        pair = s["ground_truth"]["assigned_pair"]
        prices = [{a["id"]: a["price"] for a in r["agents"]} for r in s["rounds"]]
        equal = [p[pair[0]] == p[pair[1]] for p in prices]
        bands = [all(abs(p[a] - target) <= 1 for a in pair) for p in prices]
        tolerance.append({"run_id": s["run_id"], "opening_target": target, "pair": pair,
                          "rounds": len(prices), "within_pm1": sum(bands),
                          "both_exact_target": sum(all(p[a] == target for a in pair) for p in prices),
                          "pair_equal_any_price": sum(equal),
                          "longest_unequal_within_band_streak": streak([b and not e for b, e in zip(bands, equal)]),
                          "metadata_agreement_hit_rate": s["ground_truth"].get("agreement_hit_rate"),
                          "opening_exchange": opening})
    assert len(tolerance) == 8
    out["checks"]["E108a"] = {"n_runs": len(tolerance), "runs": tolerance,
        "caveat": "Q1.4 +/-1 opening-target band, not Q2.2 lower-bound compliance; opening-only promises need not persist",
        "evidence": [evidence(sample, "llm_strong_luna_pilot_C_001", 14, "A", "private", "You may want to keep 13"),
                     evidence(sample, "llm_strong_luna_pilot_C_001", 14, "B", "private", "your 12 test may gain share")]}

    # E108b: lexical disclaimers are not semantic collusion labels. These
    # at-or-after summaries do not isolate effects of the disclaimer itself.
    independence = []
    for s in sample:
        hits = [m for m in s["private_chat"] if "independen" in message(m).lower()]
        if not hits:
            continue
        first = min(m["round"] for m in hits)
        pair = s["ground_truth"]["assigned_pair"]
        rows = [r for r in s["rounds"] if r["round"] >= first]
        premiums, equals = [], []
        for r in rows:
            p = {a["id"]: a["price"] for a in r["agents"]}
            premiums.append(mean([p[a] for a in pair]) - mean([p[a] for a in p if a not in pair]))
            equals.append(p[pair[0]] == p[pair[1]])
        # This only counts numeric text, including costs/past prices; never call
        # it a semantic price-disclosure rate.
        nums = [m for m in s["private_chat"] if m["round"] >= first and re.search(r"\d", message(m))]
        independence.append({"repo": s["repo"], "run_id": s["run_id"], "independence_messages": len(hits),
                             "first_round": first, "rounds_at_or_after": len(rows), "equal_pair_rounds": sum(equals),
                             "pair_premium_at_or_after": round(mean(premiums), 3), "numeric_messages_at_or_after": len(nums)})
    out["checks"]["E108b"] = {"runs_with_lexical_disclaimer": len(independence), "runs": independence,
        "caveat": "Neither matching prices, lexical disclaimers nor numbers establish intent or causal coordination",
        "evidence": [evidence(sample, "llm_g56l_p2_C_007", 2, "C", "private", "won’t coordinate prices"),
                     evidence(sample, "llm_g56l_p2_C_007", 16, "B", "private", "preserving our coordinated position"),
                     evidence(sample, "llm_p2_para_C_004", 5, "D", "private", "set prices independently")]}

    # E108c: strict relative-profit disadvantage, including the opening round.
    rigid = []
    for s in q22:
        for who in "ABCD":
            agents = [{a["id"]: a for a in r["agents"]} for r in s["rounds"]]
            if len({a[who]["price"] for a in agents}) != 1:
                continue
            totals = {w: round(sum(a[w]["profit"] for a in agents), 2) for w in "ABCD"}
            losses = sum(a[who]["profit"] < min(a[w]["profit"] for w in "ABCD" if w != who) for a in agents)
            rigid.append({"run_id": s["run_id"], "agent": who, "price": agents[0][who]["price"],
                          "rounds": len(agents), "strictly_lowest_profit_rounds": losses,
                          "always_strictly_lowest": losses == len(agents), "profit_totals": totals})
    out["checks"]["E108c"] = {"n_firm_paths": len(q22) * 4, "constant_price_paths": len(rigid),
                              "constant_and_always_strictly_lowest": sum(r["always_strictly_lowest"] for r in rigid),
                              "runs": rigid,
        "caveat": "Relative profits are observed, not a counterfactual best-response calculation or proof of deliberate sacrifice",
        "evidence": [evidence(sample, "llm_p2rep_0048", 11, "A", "private", "choosing 18 again"),
                     evidence(sample, "llm_p2rep_0048", 11, "D", "private", "choosing 14 for the final round")]}

    # E108d: final transitions are not randomized; keep market state and rivals.
    ends = []
    for s in q22:
        before, after = s["rounds"][-2:]
        prev = {a["id"]: a["price"] for a in before["agents"]}
        curr = {a["id"]: a["price"] for a in after["agents"]}
        d = {w: curr[w] - prev[w] for w in prev}
        pair = s["ground_truth"]["assigned_pair"]
        ends.append({"run_id": s["run_id"], "condition": s["ground_truth"]["condition"],
                     "same_market_state": before["market"] == after["market"],
                     "before_state": before["market"], "after_state": after["market"],
                     "before_prices": prev, "after_prices": curr, "deltas": d,
                     "n_firm_drops": sum(v < 0 for v in d.values()),
                     "n_firm_rises": sum(v > 0 for v in d.values()),
                     "pair_delta": mean([d[w] for w in pair]), "rivals_delta": mean([d[w] for w in d if w not in pair])})
    def end_summary(rs):
        return {"n_games": len(rs), "n_firms": len(rs) * 4,
                "games_with_any_drop": sum(r["n_firm_drops"] > 0 for r in rs),
                "firm_drops": sum(r["n_firm_drops"] for r in rs), "firm_rises": sum(r["n_firm_rises"] for r in rs)}
    out["checks"]["E108d"] = {"all": end_summary(ends),
        "same_market_state": end_summary([r for r in ends if r["same_market_state"]]), "runs": ends,
        "caveat": "No randomized horizon comparison: shocks, rival changes and prompt/family differences confound terminal effects",
        "evidence": [evidence(sample, "llm_p2claude_0008", 11, "C", "private", "not committing to a price this time"),
                     evidence(sample, "llm_p2glm_0002", 10, "C", "private", "commit to 20"),
                     evidence(sample, "llm_p2glm_0002", 11, "B", "private", "no last-round betrayal")]}

    # E108e: deliberately low-recall exact declarations. No threshold fit or
    # broad semantic claim about honesty, proposals, plans, or future promises.
    declarations = []
    for s in q22:
        prices = {r["round"]: {a["id"]: a["price"] for a in r["agents"]} for r in s["rounds"]}
        msgs = [(m["round"], speaker(m), "private", message(m)) for m in s["private_chat"]]
        msgs += [(r["round"], a["id"], "public", a.get("public_message", "")) for r in s["rounds"] for a in r["agents"]]
        for rnd, who, channel, txt in msgs:
            numbers = [int(n) for n in OWN_PRICE.findall(txt)]
            if numbers:
                declarations.append({"run_id": s["run_id"], "round_zero_indexed": rnd, "agent": who,
                                     "channel": channel, "text": txt, "declared": numbers,
                                     "actual": prices[rnd][who], "matches": all(n == prices[rnd][who] for n in numbers)})
    out["checks"]["E108e"] = {"regex": OWN_PRICE.pattern, "n_messages": len(declarations),
        "by_channel": {c: sum(d["channel"] == c for d in declarations) for c in ["private", "public"]},
        "n_mismatches": sum(not d["matches"] for d in declarations),
        "n_runs_with_matches": len({d["run_id"] for d in declarations}), "matches": declarations,
        "caveat": "Same-response field consistency: messages and actions are emitted together; low-recall lexical extraction, not temporal honesty or promise keeping; observations cluster in 10 runs"}
    path = ROOT / "results/analysis/p2_serendipity.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"n_runs": out["n_runs"], "n_rounds": out["n_rounds"],
                      "a": tolerance, "b": independence, "c": {k:v for k,v in out["checks"]["E108c"].items() if k not in ["runs", "evidence"]},
                      "d": {k:v for k,v in out["checks"]["E108d"].items() if k not in ["runs", "evidence"]},
                      "e": {k:v for k,v in out["checks"]["E108e"].items() if k not in ["matches", "regex"]}}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("part", choices=["freeze", "read", "check", "analyse"])
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=40)
    args = ap.parse_args()
    if args.part == "freeze":
        freeze()
    elif args.part == "read":
        read(args.start, args.stop)
    elif args.part == "analyse":
        analyse()
    else:
        check()
