"""Prompt provenance checks in disposable copies; never call a model or score runs."""
import copy
from collections import defaultdict
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import auditors
import check_audit_inputs as checker
import test_handoff
import verify_artifacts as verifier


def public_runs():
    runs = defaultdict(list)
    for line in (ROOT / "data/llm_v3/trajectories.jsonl").read_text().splitlines():
        row = json.loads(line)
        runs[row["run_id"]].append(row)
    for rows in runs.values():
        rows.sort(key=lambda row: row["round"])
    return runs


class PromptInputTests(unittest.TestCase):
    def setUp(self):
        self.rows = public_runs()["llm_v3_0001"]
        self.info = checker.records(ROOT, "data/llm_v3/public_info.jsonl")["llm_v3_0001"]

    def test_boundary_check_rejects_private_field_leak(self):
        original = auditors.prompt_for

        def leak(rows, view, info, variant):
            return original(rows, view, info, variant) + rows[0].get("private_message", "")

        with patch.object(auditors, "prompt_for", side_effect=leak):
            with self.assertRaisesRegex(ValueError, "private fields affect prompt"):
                checker.check_boundaries(auditors, self.rows, self.info, "combined", "orig")

    def test_boundary_check_rejects_message_leak_in_action_view(self):
        original = auditors.prompt_for

        def leak(rows, view, info, variant):
            return original(rows, view, info, variant) + rows[0]["agents"][0]["public_message"]

        with patch.object(auditors, "prompt_for", side_effect=leak):
            with self.assertRaisesRegex(ValueError, "public messages affect action-only prompt"):
                checker.check_boundaries(auditors, self.rows, self.info, "action_stats", "orig")

    def test_boundary_check_rejects_price_leak_in_text_view(self):
        original = auditors.prompt_for

        def leak(rows, view, info, variant):
            return original(rows, view, info, variant) + str(rows[0]["agents"][0]["price"])

        with patch.object(auditors, "prompt_for", side_effect=leak):
            with self.assertRaisesRegex(ValueError, "numeric actions affect text-only prompt"):
                checker.check_boundaries(auditors, self.rows, self.info, "text", "orig")

    def test_partnership_notice_must_match_public_setup(self):
        gt = checker.records(ROOT, "data/llm_v3/ground_truth.jsonl")
        info = checker.records(ROOT, "data/llm_v3/public_info.jsonl")
        info["llm_v3_0001"]["public_info"] = ""
        with self.assertRaisesRegex(ValueError, "partnership metadata differs"):
            checker.check_public_info(gt, info, "llm_v3")

    def test_positive_control_rejects_dropped_modality(self):
        with patch.object(auditors, "prompt_for", return_value="empty"):
            with self.assertRaisesRegex(ValueError, "public messages omitted"):
                checker.check_boundaries(auditors, self.rows, self.info, "combined", "orig")

    def test_shuffle_must_preserve_recipient_actions(self):
        dm = json.loads((ROOT / "results/llm_auditor/llm_v3/shuffle_donors_s0.json").read_text())
        runs = public_runs()
        changed = auditors.shuffled(runs, dm)
        changed["llm_v3_0000"][0]["agents"][0]["price"] += 1
        with self.assertRaisesRegex(ValueError, "shuffle altered recipient actions/state"):
            checker.check_shuffled(runs, changed, dm)

    def test_donor_must_align_pairs_and_preserve_conditions(self):
        dm = json.loads((ROOT / "results/llm_auditor/llm_v3/shuffle_donors_s0.json").read_text())
        runs = public_runs()
        gt = checker.records(ROOT, "data/llm_v3/ground_truth.jsonl")
        labels = checker.records(ROOT, "data/llm_v3/labels.jsonl")
        bad = copy.deepcopy(dm)
        bad["map"]["llm_v3_0000"]["amap"] = dict.fromkeys("ABCD", "A")
        with self.assertRaisesRegex(ValueError, "not a permutation"):
            checker.check_donors(bad, runs, gt, labels, 0)
        bad = copy.deepcopy(dm)
        bad["map"]["llm_v3_0000"]["donor"] = "llm_v3_0001"
        with self.assertRaisesRegex(ValueError, "crosses conditions"):
            checker.check_donors(bad, runs, gt, labels, 0)


class ProvenanceIntegrationTests(unittest.TestCase):
    setUp = test_handoff.HandoffTests.setUp
    run_copy = test_handoff.HandoffTests.run_copy
    state = test_handoff.HandoffTests.state

    def test_reconstruction_is_write_free_from_another_working_directory(self):
        before = self.state()
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run([sys.executable, str(self.root / "check_audit_inputs.py")],
                                cwd="/var/tmp", capture_output=True, text=True, env=env, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2058", result.stdout)
        self.assertIn("310", result.stdout)
        self.assertEqual(before, self.state())

    def test_equal_length_public_message_change_is_rejected(self):
        path = self.root / "data/llm_v3rep/trajectories.jsonl"
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        old = rows[0]["agents"][0]["public_message"]
        rows[0]["agents"][0]["public_message"] = ("X" if old[0] != "X" else "Y") + old[1:]
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        result = self.run_copy(sys.executable, "check_audit_inputs.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prompt hash mismatch", result.stderr)

    def test_alternate_root_cannot_attest_a_different_renderer(self):
        with self.assertRaisesRegex(ValueError, "renderer root mismatch"):
            checker.audit(self.root)

    def test_recorded_hash_cannot_be_downgraded_to_length_only(self):
        path = self.root / "results/llm_auditor/llm_v3rep/gpt-6.1-sol/text_orig.jsonl"
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        del rows[0]["prompt_sha"]
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        result = self.run_copy(sys.executable, "check_audit_inputs.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("recorded hash coverage changed", result.stderr)

    def test_missing_or_stale_receipt_fails_without_writes(self):
        receipt = self.root / checker.RECEIPT
        original = receipt.read_text()
        receipt.unlink()
        before = self.state()
        result = self.run_copy(sys.executable, "check_audit_inputs.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing post-hoc audit input receipt", result.stderr)
        self.assertEqual(before, self.state())
        data = json.loads(original)
        data["scope"] += " changed"
        receipt.write_text(json.dumps(data))
        before = self.state()
        result = self.run_copy(sys.executable, "check_audit_inputs.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("audit input receipt is stale", result.stderr)
        self.assertEqual(before, self.state())

    def test_receipt_requires_all_sources_and_real_per_file_counts(self):
        receipt = self.root / checker.RECEIPT
        original = json.loads(receipt.read_text())
        changed = copy.deepcopy(original)
        del changed["sources_sha256"]["data/llm_v3/trajectories.jsonl"]
        receipt.write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "receipt source coverage"):
            verifier.check_audit_input_receipt(self.root)
        changed = copy.deepcopy(original)
        name = next(iter(changed["files"]))
        changed["files"][name] = {"recorded_hash_match": 2213}
        receipt.write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "receipt per-file counts"):
            verifier.check_audit_input_receipt(self.root)


if __name__ == "__main__":
    unittest.main()
