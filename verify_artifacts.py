"""Read-only, offline handoff check; Python standard library only.

Checks the committed SHA-256 manifest, cached dataset/audit coverage, portable
completion receipts, saved CI/contrast consistency, headline report tables, and
the presentation's freshness against its saved JSON inputs.
Never imports an experiment module, recomputes AUROC/CIs, or calls an LLM.
The manifest is recorded after the experiments; it is not pre-registration evidence.

    python3 verify_artifacts.py
    python3 verify_artifacts.py --write-manifest  # maintainer: initial snapshot only
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import sys

# Do this before importing local code: a clean checkout must remain byte-for-byte
# unchanged, including the absence of __pycache__/.
sys.dont_write_bytecode = True
from evaluation_guard import completed

ROOT = Path(__file__).resolve().parent
MANIFEST = "data/artifact_manifest.json"
VIEWS = ("text", "action", "combined", "action_stats", "combined_stats", "structured")
PAIRS = {"".join(p) for p in combinations("ABCD", 2)}
MAIN = "results/analysis/final_llm_v3_gpt-6.1-sol_"
REP = "results/analysis/replication_llm_v3rep.json"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(root, name):
    return json.loads((root / name).read_text())


def rows(root, name):
    return [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]


def unique(records, context):
    result = {r["run_id"]: r for r in records}
    require(len(result) == len(records), f"duplicate run_id: {context}")
    return result


def snapshot_paths(root):
    # Explicit research artifacts; mutable manager reports/logs are deliberately excluded.
    paths = list(root.glob("*.py")) + list(root.glob("*.sh"))
    paths += list((root / "tests").glob("*.py"))
    paths += [root / p for p in ("pyproject.toml", "uv.lock", "SCHEMA.md",
                               "PRESENTATION.html", "PRESENTATION.md",
                               "REPORT.html", "REPORT.pdf", "PRESENTATION.pdf", "EVIDENCE.html",
                               "PRICE_TRANSITIONS.md")]
    for folder in ("data", "results", "figures"):
        paths += [p for p in (root / folder).rglob("*")
                  if p.is_file() and p.suffix in (".json", ".jsonl", ".md", ".png")]
    return sorted({p.relative_to(root).as_posix() for p in paths
                   if p.relative_to(root).as_posix() != MANIFEST})


def check_manifest(root):
    manifest = read(root, MANIFEST)
    expected = manifest["sha256"]
    require(set(snapshot_paths(root)) == set(expected), "artifact inventory changed from manifest")
    for name, want in expected.items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == want,
                f"SHA-256 mismatch: {name}")
    return len(expected)


def check_dataset(root, ds, count, conditions, labelled=True):
    base = f"data/{ds}/"
    gt = unique(rows(root, base + "ground_truth.jsonl"), base + "ground_truth")
    require(len(gt) == count, f"{ds}: expected {count} runs")
    require(Counter(r["condition"] for r in gt.values()) == conditions, f"{ds}: condition counts")
    if ds in ("llm_v3", "llm_v3rep"):
        require(set(gt) == {f"{ds}_{i:04d}" for i in range(count)}, f"{ds}: frozen run IDs")
    trajectory = defaultdict(dict)
    for r in rows(root, base + "trajectories.jsonl"):
        rid, t = r["run_id"], r["round"]
        require(rid in gt and t not in trajectory[rid], f"{ds}: unexpected/duplicate round {rid}/{t}")
        require({a["id"] for a in r["agents"]} == set("ABCD") and len(r["agents"]) == 4,
                f"{ds}: four distinct firms required")
        require(all(6 <= a["price"] <= 30 and "private_message" not in a for a in r["agents"]),
                f"{ds}: public trajectory prices/private-message boundary")
        trajectory[rid][t] = r
    require(set(trajectory) == set(gt), f"{ds}: trajectory coverage")
    require(all(set(ts) == set(range(12)) for ts in trajectory.values()), f"{ds}: 12 unique rounds per run")
    info = unique(rows(root, base + "public_info.jsonl"), base + "public_info")
    require(set(info) == set(gt), f"{ds}: public info coverage")
    for rid, g in gt.items():
        if g["condition"] == "legit":
            require(bool(info[rid]["public_info"]), f"{rid}: missing partnership notice")
    if labelled:
        labels = unique(rows(root, base + "labels.jsonl"), base + "labels")
        require(set(labels) == set(gt), f"{ds}: label coverage")
        for rid, lab in labels.items():
            require(lab["condition"] == gt[rid]["condition"] and
                    lab["assigned_pair"] == gt[rid]["assigned_pair"], f"{rid}: label metadata")
            valid = {"explicit", "info_exchange", "none"} if lab["condition"] == "private" else {"no_channel"}
            require(lab["agreement"] in valid, f"{rid}: invalid/unparsed label")
    for view in VIEWS:
        name = f"results/llm_auditor/{ds}/gpt-6.1-sol/{view}_orig.jsonl"
        audit = unique(rows(root, name), name)
        require(set(audit) == set(gt), f"{ds}/{view}: audit coverage")
        for rid, a in audit.items():
            require(a["model"] == "gpt-6.1-sol" and a["view"] == view and a["variant"] == "orig",
                    f"{rid}/{view}: auditor provenance")
            require(set(a["scores"]) == PAIRS, f"{rid}/{view}: six pair scores")
            require(all(isinstance(x, (int, float)) and 0 <= x <= 100
                        for x in [a["collusion_present"], *a["scores"].values()]), f"{rid}/{view}: finite bounded scores")
            # Earlier caches predate prompt_sha. Record their bytes in the manifest;
            # do not silently promote a prompt-length check to a historical hash check.
            if "prompt_sha" in a:
                require(bool(re.fullmatch(r"[0-9a-f]{16}", a["prompt_sha"])), f"{rid}/{view}: prompt hash format")
    return gt, trajectory


def check_saved_results(root):
    test, dev, rep = (read(root, MAIN + "test.json"), read(root, MAIN + "dev.json"), read(root, REP))
    require((test["n_runs"], test["n_pos"], dev["n_runs"], dev["n_pos"], rep["n_runs"]) == (95, 50, 30, 20, 30),
            "saved split counts")
    require(test["split"] == "test" and not rep["smoke"], "saved evaluation identity")
    require(test["thresholds_dev_youden"] == dev["thresholds_dev_youden"], "test thresholds differ from dev")
    require(test["fusion_w_text"] == dev["fusion_w_text"] == rep["fusion_w_text_dev"], "frozen fusion weight")
    for path, sha in rep["frozen_input_sha256_16"].items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest()[:16] == sha,
                f"replication's original frozen input hash changed: {path}")
    for result in (test, dev, rep):
        pc = result["point_ci"]
        for scorer, metrics in pc.items():
            for metric, (pt, lo, hi) in metrics.items():
                # Percentile intervals need not contain the sample point.
                require(0 <= pt <= 1 and 0 <= lo <= hi <= 1, f"invalid saved CI: {scorer}/{metric}")
        for key, contrast in result["contrasts"].items():
            name, metric = key.rsplit(":", 1)
            if name.startswith("delta_hybrid["):
                scorer = name[len("delta_hybrid["):-1]
                expected = pc[scorer][metric][0] - max(pc[v][metric][0] for v in ("text", "action"))
            elif "-best[" in name:
                scorer, other = name.split("-best[")
                expected = pc[scorer][metric][0] - pc[other[:-1]][metric][0]
            else:
                scorer, other = name.split("-", 1)
                expected = pc[scorer][metric][0] - pc[other][metric][0]
            require(abs(expected - contrast["delta"]) <= 0.00011, f"saved contrast arithmetic: {key}")
            require(-1 <= contrast["ci"][0] <= contrast["ci"][1] <= 1, f"saved contrast CI: {key}")
    require(completed("headline", root) and completed("replication", root), "portable completion receipt")
    report = (root / "REPORT.md").read_text()
    # Exact primary-table rows, formatted from saved values, without rerunning any analysis.
    for scorer, m in test["point_ci"].items():
        vals = [m[k] for k in ("run_auroc", "within_market_auroc", "pair_auroc", "pair_id_acc")]
        line = f"| {scorer} | " + " | ".join(f"{p:.2f} [{lo:.2f}, {hi:.2f}]" for p, lo, hi in vals) + " |"
        require(line in report, f"REPORT primary table differs: {scorer}")
    for name in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", report):
        require((root / name).is_file(), f"missing REPORT figure: {name}")


def check_audit_input_receipt(root):
    # Validate preservation of the separate, NumPy-based prompt reconstruction
    # without importing the auditor or running that reconstruction here.
    receipt = read(root, "data/audit_input_receipt.json")
    require(receipt["schema_version"] == 1 and receipt["post_hoc"] is True,
            "invalid post-hoc audit input receipt")
    from check_audit_inputs import source_inventory
    require(receipt["totals"] == {"recorded_hash_match": 1903, "length_only_match": 310},
            "audit input receipt totals")
    require(receipt["legacy_length_only_by_cohort"] == {"headline_dev": 150, "headline_test": 120, "cross_family": 40},
            "audit input receipt legacy cohorts")
    actual = {p.relative_to(root).as_posix() for p in (root / "results/llm_auditor").glob("*/*/*.jsonl")}
    require(set(receipt["files"]) == actual and len(actual) == 44, "audit input receipt cache coverage")
    require(set(receipt["prompt_hash_coverage"]) == actual, "audit input receipt hash coverage inventory")
    totals = Counter()
    for name, counts in receipt["files"].items():
        cached = rows(root, name)
        actual_counts = Counter("recorded_hash_match" if "prompt_sha" in r else "length_only_match" for r in cached)
        require(dict(actual_counts) == counts, f"audit input receipt per-file counts: {name}")
        require(sorted(r["run_id"] for r in cached if "prompt_sha" in r) == receipt["prompt_hash_coverage"][name],
                f"audit input receipt hash eligibility changed: {name}")
        totals.update(counts)
    require(dict(totals) == receipt["totals"], "audit input receipt file totals")
    sources = receipt["sources_sha256"]
    require(set(sources) == source_inventory(),
            "audit input receipt source coverage")
    for name, want in sources.items():
        path = (root / name).resolve()
        require(path.is_relative_to(root.resolve()), "audit input receipt path outside repository")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == want,
                f"stale audit input receipt: {name}")


def verify(root):
    n = check_manifest(root)
    datasets = {}
    for ds, count, conds, labelled in (
        ("llm_v3", 125, {"private": 70, "none": 35, "legit": 20}, True),
        ("llm_v3rep", 30, {"private": 15, "none": 10, "legit": 5}, True),
        ("llm_v3plc", 15, {"placebo": 15}, False),
        ("llm_v3fp", 16, {"private": 16}, True),
        ("llm_v3mon", 20, {"private": 14, "none": 6}, True),
    ):
        datasets[ds] = check_dataset(root, ds, count, conds, labelled)
    gp, tp = datasets["llm_v3plc"]
    gr, tr = datasets["llm_v3rep"]
    require({r.rsplit("_", 1)[1] for r in gp} ==
            {r.rsplit("_", 1)[1] for r, g in gr.items() if g["condition"] == "private"}, "placebo matching IDs")
    for rid, g in gp.items():
        mate = "llm_v3rep_" + rid.rsplit("_", 1)[1]
        require(g["seed"] == gr[mate]["seed"] and g["assigned_pair"] == gr[mate]["assigned_pair"] and
                g["placebo_undelivered"], f"{rid}: placebo matching metadata")
        require(all(tp[rid][t]["market"] == tr[mate][t]["market"] for t in range(12)), f"{rid}: matched market path")
    hard = unique(rows(root, "data/llm_v3/public_explicit.jsonl"), "hard-set screen")
    require(set(hard) == set(datasets["llm_v3"][0]) and
            all(r["public_explicit"] is False and isinstance(r["llm"], bool) for r in hard.values()), "hard-set coverage")
    check_saved_results(root)
    check_audit_input_receipt(root)
    # The presentation renderer uses only saved values and standard-library code.
    # This checks freshness without writing HTML or importing an experiment module.
    from build_presentation import render
    for name, content in render(root).items():
        require((root / name).read_bytes() == content.encode("utf-8"), f"stale presentation: {name}")
    from build_handoff import check as check_handoff
    check_handoff(root)
    from check_evidence_sources import check as check_sources
    check_sources(root)
    from check_price_transitions import check as check_transitions
    check_transitions(root)
    print(f"PASS: {n} artifact hashes; 206 runs / 2,472 rounds; 1,236 original-view audits; "
          "15 matched placebo paths; frozen inputs/receipts; saved CI/contrast consistency; REPORT table/figures; presentation freshness; offline HTML/PDF provenance; 2,213-audit input receipt; evidence source ledger and price-transition census freshness.")
    print("No LLM calls, writes, refitting, or AUROC/bootstrap recomputation. Manifest is post-hoc, not a registration.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write-manifest", action="store_true", help="create a post-hoc snapshot; refuses overwrite")
    args = ap.parse_args()
    if args.write_manifest:
        names = snapshot_paths(ROOT)
        manifest = {"recorded_utc": datetime.now(timezone.utc).isoformat(),
                    "note": "Post-hoc handoff snapshot; not proof of pre-registration or historical prompt hashes.",
                    "sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in names}}
        with (ROOT / MANIFEST).open("x") as f:
            f.write(json.dumps(manifest, indent=2) + "\n")
    try:
        verify(ROOT)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
