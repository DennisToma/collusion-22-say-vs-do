"""Integrity/guard regression checks in disposable copies; no experiment is run.

uv run python -m unittest discover -s tests -v
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import verify_artifacts as verifier


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="say-vs-do-handoff-", dir="/var/tmp")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        paths = verifier.snapshot_paths(ROOT) + [verifier.MANIFEST, "REPORT.md", "REPORT_APPENDIX.md", "README.md"]
        for name in paths:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dest)

    def run_copy(self, *args):
        return subprocess.run(args, cwd=self.root, capture_output=True, text=True,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=30)

    def state(self):
        return {p.relative_to(self.root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file()}

    def test_offline_verifier_is_write_free_in_export_without_logs(self):
        self.assertFalse((self.root / "logs").exists())
        before = self.state()
        # Deliberately allow bytecode writes: verifier itself must prevent them.
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run([sys.executable, "verify_artifacts.py"], cwd=self.root,
                                capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS:", result.stdout)
        self.assertEqual(before, self.state())

    def test_changed_cache_is_rejected(self):
        path = self.root / "results/llm_auditor/llm_v3/gpt-6.1-sol/text_orig.jsonl"
        path.write_bytes(path.read_bytes() + b"\n")
        result = self.run_copy(sys.executable, "verify_artifacts.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SHA-256 mismatch", result.stderr)

    def test_presentation_freshness_check_is_write_free(self):
        before = self.state()
        result = self.run_copy(sys.executable, "build_presentation.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.state())

    def test_presentation_edit_is_rejected_by_freshness_check(self):
        path = self.root / "PRESENTATION.html"
        path.write_text(path.read_text().replace("no resolved detection gain", "proven equivalence"))
        before = self.state()
        result = self.run_copy(sys.executable, "build_presentation.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale or missing PRESENTATION.html", result.stderr)
        self.assertEqual(before, self.state())

    def test_export_receipt_check_is_write_free_without_optional_dependencies(self):
        before = self.state()
        # -S disables site-packages: checking exports requires only stdlib.
        result = self.run_copy(sys.executable, "-S", "build_handoff.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.state())

    def test_report_prose_edit_invalidates_export(self):
        path = self.root / "REPORT.md"
        path.write_text(path.read_text().replace("no resolved run-level detection gain", "proven equivalence"))
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "build_handoff.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale handoff inputs", result.stderr)
        self.assertEqual(before, self.state())

    def test_pdf_edit_is_rejected_by_export_check(self):
        path = self.root / "PRESENTATION.pdf"
        path.write_bytes(path.read_bytes() + b"changed")
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "build_handoff.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("handoff SHA-256 mismatch: PRESENTATION.pdf", result.stderr)
        self.assertEqual(before, self.state())

    def test_missing_figure_is_rejected(self):
        (self.root / "figures/summary.png").unlink()
        result = self.run_copy(sys.executable, "verify_artifacts.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact inventory changed", result.stderr)

    def test_duplicate_round_is_rejected_independently_of_manifest(self):
        path = self.root / "data/llm_v3/trajectories.jsonl"
        with path.open("a") as out:
            out.write(path.read_text().splitlines()[0] + "\n")
        with self.assertRaisesRegex(ValueError, "duplicate round"):
            verifier.check_dataset(self.root, "llm_v3", 125, {"private": 70, "none": 35, "legit": 20})

    def test_report_table_edit_is_rejected(self):
        path = self.root / "REPORT.md"
        path.write_text(path.read_text().replace("| text | 0.47 [0.36, 0.58]", "| text | 0.99 [0.98, 1.00]"))
        result = self.run_copy(sys.executable, "verify_artifacts.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("REPORT primary table differs: text", result.stderr)

    def test_all_entrypoints_refuse_without_local_locks(self):
        before = self.state()
        for cmd in (["bash", "finalize_test.sh"],
                    [sys.executable, "final_analysis.py", "--split", "test"],
                    [sys.executable, "final_analysis.py", "--split", "all"],
                    [sys.executable, "replication.py"],
                    [sys.executable, "replication.py", "--allow-partial"],
                    [sys.executable, "replication.py", "--max-idx", "15"],
                    [sys.executable, "replication.py", "--ds", "llm_v3"],
                    [sys.executable, "replication.py", "--ds", "llm_v3", "--max-idx", "31"]):
            with self.subTest(command=cmd):
                result = self.run_copy(*cmd)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("refusing to rerun", result.stderr)
                self.assertEqual(before, self.state())
        self.assertFalse((self.root / "logs").exists())

    def test_corrupted_completed_result_fails_closed(self):
        path = self.root / "results/analysis/final_llm_v3_gpt-6.1-sol_test.json"
        path.write_bytes(path.read_bytes() + b"\n")
        before = self.state()
        result = self.run_copy("bash", "finalize_test.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("differs from the committed receipt", result.stderr)
        self.assertEqual(before, self.state())
        self.assertFalse((self.root / "logs").exists())

    def test_deleted_receipt_does_not_unlock_saved_result(self):
        (self.root / "data/evaluation_receipt.json").unlink()
        result = self.run_copy("bash", "finalize_test.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("saved result exists without a completion receipt", result.stderr)
        self.assertFalse((self.root / "logs").exists())

    def test_invalid_receipt_state_fails_closed(self):
        path = self.root / "data/evaluation_receipt.json"
        receipt = json.loads(path.read_text())
        receipt["evaluations"]["headline"]["state"] = "pending"
        path.write_text(json.dumps(receipt))
        result = self.run_copy("bash", "finalize_test.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid completion receipt", result.stderr)
        self.assertFalse((self.root / "logs").exists())


if __name__ == "__main__":
    unittest.main()
