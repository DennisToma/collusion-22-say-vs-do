"""Check the frozen Q2.2 source handoff for the merged submission, without writes.

    python3 -S check_merge_sources.py

This verifies saved JSON values and source hashes, not metrics or the latest merge
draft. The receipt identifies the exact draft reviewed; findings are human review.
No numerical dependencies, sibling writes, network, subprocesses, or model calls.
"""
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "results/analysis/merge_source_audit_i116.json"


def rounded(value, digits):
    if isinstance(value, list):
        return [rounded(x, digits) for x in value]
    if digits is None:
        return value
    return float(Decimal(str(value)).quantize(Decimal(1).scaleb(-digits),
                                             rounding=ROUND_HALF_UP))


def check():
    receipt = json.loads(RECEIPT.read_text())
    failures = []
    group_ids = [group["id"] for group in receipt["groups"]]
    if sorted(group_ids) != sorted(f"M{i}" for i in range(1, 17)):
        failures.append("source groups must contain M1 through M16 exactly once")
    documents = {}
    for relative, expected_hash in receipt["source_sha256"].items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing source: {relative}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_hash:
            failures.append(f"changed source: {relative}")
        documents[relative] = json.loads(data)
    n_values = 0
    for group in receipt["groups"]:
        for item in group["checks"]:
            n_values += 1
            try:
                actual = documents[item["file"]]
                for key in item["path"]:
                    actual = actual[key]
                actual = rounded(actual, item["digits"])
                if actual != item["expected"]:
                    failures.append(f"{group['id']} {item['path']}: "
                                    f"{actual!r} != {item['expected']!r}")
            except (KeyError, IndexError, TypeError) as error:
                failures.append(f"{group['id']} {item['path']}: {error}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"PASS: {len(receipt['groups'])}/16 source groups, {n_values} saved-value "
          f"checks, {len(documents)} source hashes; no metrics recomputed")
    print("Reviewed draft SHA256: " + receipt["reviewed_drafts"]["SUBMISSION.md"]["sha256"])
    print("Human wording findings remain recommendations; this does not certify the latest draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
