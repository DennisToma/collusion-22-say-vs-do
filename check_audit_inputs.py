"""Reconstruct cached auditor prompts without running auditors or changing caches.

    uv run python check_audit_inputs.py
    uv run python check_audit_inputs.py --record  # one-time post-hoc receipt

Imports the frozen prompt renderer, not its command-line entry point. Requires
the pinned NumPy environment; no LLM calls, score/CI computation, or writes by
default. Old rows lacking prompt_sha are checked by length only; that cannot
authenticate their historical prompt content. Receipt SHA-256 values are post-hoc;
recorded prompt hashes are 64-bit prefixes, not full SHA-256 digests.
"""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
RECEIPT = "data/audit_input_receipt.json"
VIEWS = ("text", "action", "combined", "structured", "action_stats", "combined_stats")
DATASETS = {"llm_v3": 125, "llm_v3rep": 30, "llm_v3fp": 16,
            "llm_v3mon": 20, "llm_v3plc": 15}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def records(root, name):
    rows = [json.loads(s) for s in (root / name).read_text().splitlines() if s.strip()]
    by_id = {r["run_id"]: r for r in rows}
    require(len(by_id) == len(rows), f"duplicate run ID: {name}")
    return by_id


def inventory():
    files = {}
    for ds in DATASETS:
        ids = {f"{ds}_{i:04d}" for i in range(DATASETS[ds])}
        # Placebo uses the private replication indices, supplied by the ground truth.
        if ds == "llm_v3plc":
            ids = None
        for view in VIEWS:
            files[f"results/llm_auditor/{ds}/gpt-6.1-sol/{view}_orig.jsonl"] = ids
    for view in VIEWS:
        files[f"results/llm_auditor/llm_v3/claude-sonnet-5-5/{view}_orig.jsonl"] = {
            f"llm_v3_{i:04d}" for i in range(125) if i % 3 == 0}
    for ds in ("llm_v3", "llm_v3rep"):
        files[f"results/llm_auditor/{ds}/gpt-6.1-sol/action_stats_hint_orig.jsonl"] = {
            f"{ds}_{i:04d}" for i in range(DATASETS[ds])}
    for view in ("combined", "structured"):
        for seed in range(3):
            files[f"results/llm_auditor/llm_v3/gpt-6.1-sol/{view}_shuffle_s{seed}.jsonl"] = {
                f"llm_v3_{i:04d}" for i in range(30, 125)}
    return files


def source_inventory():
    names = set(inventory()) | {"check_audit_inputs.py", "auditors.py", "llm.py", "pyproject.toml", "uv.lock"}
    names.update(f"data/{ds}/{stem}.jsonl" for ds in DATASETS
                 for stem in ("ground_truth", "trajectories", "public_info"))
    names.add("data/llm_v3/labels.jsonl")
    names.update(f"results/llm_auditor/llm_v3/shuffle_donors_s{seed}.json" for seed in range(3))
    return names


def check_public_info(gt, info, context):
    require(set(info) == set(gt), f"{context}: public info coverage")
    for rid, g in gt.items():
        pair = g["assigned_pair"]
        notice = (f"Public information: firms {pair[0]} and {pair[1]} operate a publicly announced joint shipping "
                  "partnership that lowers both of their unit costs by 1.") if g["condition"] == "legit" else ""
        require(info[rid] == {"run_id": rid, "public_info": notice,
                            "cost_offset": {a: -1 if notice and a in pair else 0 for a in "ABCD"}},
                f"{rid}: public partnership metadata differs from setup")


def check_donors(dm, runs, gt, labels, seed):
    require(dm["seed"] == seed and set(dm["map"]) == set(runs), f"shuffle {seed}: donor coverage/seed")
    demand = {"low": -1, "normal": 0, "high": 1}
    for rid, m in dm["map"].items():
        donor, amap = m["donor"], m["amap"]
        require(donor in runs and donor != rid, f"{rid}: invalid/self shuffle donor")
        require(gt[rid]["condition"] == gt[donor]["condition"] and m["same_condition"] is True,
                f"{rid}: shuffle crosses conditions")
        positive = lambda r: labels[r]["agreement"] in ("explicit", "info_exchange")
        require(positive(rid) == positive(donor), f"{rid}: shuffle crosses labels")
        require(set(amap) == set("ABCD") and set(amap.values()) == set("ABCD"),
                f"{rid}: shuffle firm map is not a permutation")
        require({amap[a] for a in gt[rid]["assigned_pair"]} == set(gt[donor]["assigned_pair"]),
                f"{rid}: shuffle does not align designated pairs")
        require(len(runs[rid]) == len(runs[donor]), f"{rid}: shuffle round count")
        distance = sum(abs(a["market"]["cost"] - b["market"]["cost"]) +
                       abs(demand[a["market"]["demand_shock"]] - demand[b["market"]["demand_shock"]])
                       for a, b in zip(runs[rid], runs[donor]))
        require(distance == m["ctx_l1"], f"{rid}: shuffle context distance")


def check_shuffled(original, shuffled, dm):
    require(set(original) == set(shuffled), "shuffle output run coverage")
    for rid, rows in shuffled.items():
        mapping = dm["map"][rid]
        inverse = {v: k for k, v in mapping["amap"].items()}
        require(len(rows) == len(original[rid]), f"{rid}: shuffled round count")
        for before, after, donor in zip(original[rid], rows, original[mapping["donor"]]):
            # Independently check the full row, so any changed prices, state,
            # quantities, profits or extra metadata are rejected.
            expected = copy.deepcopy(before)
            messages = {a["id"]: a["public_message"] for a in donor["agents"]}
            for agent in expected["agents"]:
                message = messages[mapping["amap"][agent["id"]]]
                agent["public_message"] = re.sub(r"\b([ABCD])\b", lambda m: inverse[m.group(1)], message)
            require(after == expected, f"{rid}: shuffle altered recipient actions/state or misassigned text")


def check_boundaries(renderer, rows, info, view, variant):
    """Noninterference checks on copies, using the unchanged production renderer."""
    prompt = renderer.prompt_for(rows, view, info, variant)
    changed = copy.deepcopy(rows)
    changed_info = copy.deepcopy(info)
    sentinel = "AUDIT_PRIVATE_SENTINEL_79dbe2"
    private_keys = ("private_message", "agreement", "assigned_pair", "condition", "notes", "chat", "pair", "label", "y")
    changed_info.update(dict.fromkeys(private_keys, sentinel))
    for row in changed:
        row.update(dict.fromkeys(private_keys, sentinel))
        for agent in row["agents"]:
            agent.update(private_message=sentinel, notes=sentinel, agreement=sentinel)
    require(renderer.prompt_for(changed, view, changed_info, variant) == prompt and sentinel not in prompt,
            f"{view}/{variant}: private fields affect prompt")
    if view in ("action", "action_stats", "action_stats_hint"):
        for row in changed:
            for agent in row["agents"]:
                agent["public_message"] = "I price at 30. " + sentinel
        require(renderer.prompt_for(changed, view, info, variant) == prompt,
                f"{view}/{variant}: public messages affect action-only prompt")
    if view == "text":
        for row in changed:
            row["market"].update(cost=999, demand_shock=sentinel)
            for agent in row["agents"]:
                agent.update(price=30, quantity=999, profit=999)
        require(renderer.prompt_for(changed, view, info, variant) == prompt,
                f"{view}/{variant}: numeric actions affect text-only prompt")
    # Positive controls: boundaries alone would also pass a renderer that dropped
    # a whole modality. Check that the original observable streams are retained.
    if view not in ("action", "action_stats", "action_stats_hint"):
        require(all(f"{a['id']} says: \"{a['public_message']}\"" in prompt
                    for row in rows for a in row["agents"]), f"{view}/{variant}: public messages omitted")
    if view != "text":
        require(all(f"{a['id']} price {a['price']}, units {a['quantity']}, profit {a['profit']}" in prompt
                    for row in rows for a in row["agents"]), f"{view}/{variant}: numeric actions omitted")
    return prompt


def audit(root=ROOT, *, record=False):
    # Import only, never auditors.main(): its historical --verify path regenerates
    # public_info.jsonl and creates output directories before checking the cache.
    import auditors as renderer
    require(root.resolve() == ROOT.resolve() and
            Path(renderer.__file__).resolve() == (root / "auditors.py").resolve(),
            "renderer root mismatch; execute the checker inside the target checkout")
    receipt_path = root / RECEIPT
    require(record or receipt_path.is_file(), "missing post-hoc audit input receipt")
    preserved = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    expected = inventory()
    actual = {p.relative_to(root).as_posix() for p in (root / "results/llm_auditor").glob("*/*/*.jsonl")}
    require(actual == set(expected), "auditor file inventory differs from the frozen handoff")
    source_names = source_inventory()
    data = {}
    for ds, count in DATASETS.items():
        names = [f"data/{ds}/{s}.jsonl" for s in ("ground_truth", "trajectories", "public_info")]
        source_names.update(names)
        gt, info = records(root, names[0]), records(root, names[2])
        require(len(gt) == count, f"{ds}: run count")
        check_public_info(gt, info, ds)
        runs = defaultdict(list)
        for line in (root / names[1]).read_text().splitlines():
            r = json.loads(line)
            runs[r["run_id"]].append(r)
        require(set(runs) == set(gt), f"{ds}: trajectory coverage")
        for rid, rows in runs.items():
            rows.sort(key=lambda r: r["round"])
            require([r["round"] for r in rows] == list(range(12)), f"{rid}: round coverage")
        data[ds] = (gt, info, {"orig": runs})
    ds = "llm_v3"
    labels_name = f"data/{ds}/labels.jsonl"
    labels = records(root, labels_name)
    source_names.add(labels_name)
    gt, info, variants = data[ds]
    for seed in range(3):
        name = f"results/llm_auditor/{ds}/shuffle_donors_s{seed}.json"
        dm = json.loads((root / name).read_text())
        check_donors(dm, variants["orig"], gt, labels, seed)
        variants[f"shuffle_s{seed}"] = renderer.shuffled(variants["orig"], dm)
        check_shuffled(variants["orig"], variants[f"shuffle_s{seed}"], dm)
        source_names.add(name)
    totals, legacy, summaries, coverage = Counter(), Counter(), {}, {}
    for name, wanted in sorted(expected.items()):
        ds, model, filename = Path(name).parts[-3:]
        match = re.fullmatch(r"(.+)_(orig|shuffle_s[012])\.jsonl", filename)
        view, variant = match.groups()
        gt, info, variants = data[ds]
        cached = records(root, name)
        coverage[name] = sorted(rid for rid, row in cached.items() if "prompt_sha" in row)
        if preserved is not None:
            require(coverage[name] == preserved["prompt_hash_coverage"][name],
                    f"{name}: recorded hash coverage changed")
        require(set(cached) == (set(gt) if wanted is None else wanted), f"{name}: exact run coverage")
        counts = Counter()
        for rid, row in cached.items():
            require((row["model"], row["view"], row["variant"]) == (model, view, variant),
                    f"{name}/{rid}: cache provenance metadata")
            prompt = check_boundaries(renderer, variants[variant][rid], info[rid], view, variant)
            require(row["chars"] == len(prompt), f"{name}/{rid}: prompt length mismatch")
            method = "recorded_hash_match" if "prompt_sha" in row else "length_only_match"
            if "prompt_sha" in row:
                require(isinstance(row["prompt_sha"], str) and re.fullmatch(r"[0-9a-f]{16}", row["prompt_sha"]) and
                        row["prompt_sha"] == renderer.sha(prompt), f"{name}/{rid}: prompt hash mismatch")
            else:
                cohort = ("cross_family" if model.startswith("claude") else
                          "headline_test" if int(rid.rsplit("_", 1)[1]) >= 30 else "headline_dev")
                legacy[cohort] += 1
            counts[method] += 1
        summaries[name] = dict(sorted(counts.items()))
        totals.update(counts)
        source_names.add(name)
    return {"schema_version": 1, "post_hoc": True,
            "scope": "Current prompt reconstruction and renderer noninterference; recorded hashes are 64-bit prefixes. Not historical proof for length-only rows, seller-call isolation, semantic evidence accuracy, or pre-registration.",
            "totals": dict(sorted(totals.items())), "legacy_length_only_by_cohort": dict(sorted(legacy.items())),
            "files": summaries, "prompt_hash_coverage": coverage,
            "sources_sha256": {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in sorted(source_names)}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--record", action="store_true", help="write a new post-hoc receipt; refuses overwrite")
    args = ap.parse_args()
    try:
        result = audit(record=args.record)
        if args.record:
            with (ROOT / RECEIPT).open("x") as out:
                out.write(json.dumps(result, indent=2) + "\n")
        else:
            require((ROOT / RECEIPT).is_file(), "missing post-hoc audit input receipt")
            require(result == json.loads((ROOT / RECEIPT).read_text()), "audit input receipt is stale")
        print(f"PASS: {len(result['files'])} caches; {result['totals']}; current renderer boundaries and frozen donor metadata checked.")
        print(f"Length-only cohorts: {result['legacy_length_only_by_cohort']}. No historical content authentication for these rows.")
        print("No LLM calls, metrics or cache edits.")
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
