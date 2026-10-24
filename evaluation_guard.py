"""Portable completion guard for the two evaluations that must never be rerun.

Local logs/ locks are ignored by git. The committed receipt records completed outputs
so a fresh clone preserves the same protection. This is a post-hoc completion receipt,
not evidence of pre-registration. No metrics are computed here.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = {"headline": "results/analysis/final_llm_v3_gpt-6.1-sol_test.json",
           "replication": "results/analysis/replication_llm_v3rep.json"}


def completed(name, root=ROOT):
    path = root / "data/evaluation_receipt.json"
    if not path.exists():
        if (root / RESULTS[name]).exists():
            raise ValueError(f"{name}: saved result exists without a completion receipt; refusing to rerun")
        return False
    receipt = json.loads(path.read_text())
    record = receipt["evaluations"][name]
    if record["state"] != "complete" or record["result"] != RESULTS[name]:
        raise ValueError(f"{name}: invalid completion receipt; refusing to rerun")
    result = root / record["result"]
    actual = hashlib.sha256(result.read_bytes()).hexdigest()
    if actual != record["sha256"]:
        raise ValueError(f"{name}: completed result differs from the committed receipt")
    return True


def refuse_completed(name):
    if completed(name):
        raise SystemExit(f"{name} is complete (data/evaluation_receipt.json); refusing to rerun. "
                         "Use python3 verify_artifacts.py to inspect the saved artifacts.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", choices=["headline", "replication"])
    args = ap.parse_args()
    refuse_completed(args.name)
