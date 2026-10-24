"""Verify the figure's numerical source record without rendering or evaluating detectors."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import check_mechanism_sources as checker
import test_handoff


class MechanismNumericalTests(unittest.TestCase):
    def test_literal_cohort_membership_and_published_captions(self):
        saved = json.loads((ROOT / checker.OUTPUT).read_text())
        cohorts = {}
        for split, groups in saved["splits"].items():
            cohorts[split] = set().union(*(set(g["late_premium_by_run"]) for g in groups.values()))
        self.assertEqual(cohorts["dev"], {f"llm_v3_{i:04d}" for i in range(30)})
        self.assertEqual(cohorts["test"], {f"llm_v3_{i:04d}" for i in range(30, 125)})
        self.assertEqual(cohorts["all"], cohorts["dev"] | cohorts["test"])
        self.assertFalse(cohorts["dev"] & cohorts["test"])
        self.assertEqual(checker.captions(saved), {
            "test": "Descriptive test: late-window (rounds 9–12) pair-minus-rivals premium +1.02 "
                    "(none -0.02, legit +0.08), positive in 44/50 private runs.",
            "dev": "Descriptive dev: private pairs' mean opening price 17.35 vs 12.53 for rivals; "
                   "late-window (rounds 9–12) pair-minus-rivals premium +0.90 "
                   "(none -0.07, legit +0.15), positive in 12/20 private runs."})

    def test_all_summaries_match_historical_numpy_calculations(self):
        # Independent execution of the numerical expressions in fig_mechanism.py;
        # importing that script would also render a PNG, so do not import it.
        import numpy as np
        gt, prices = checker.load(ROOT)
        saved = json.loads((ROOT / checker.OUTPUT).read_text())
        for split, groups in saved["splits"].items():
            for condition, summary in groups.items():
                ids = sorted(rid for rid, g in gt.items() if g["condition"] == condition and
                             (split == "all" or (int(rid[-4:]) < 30) == (split == "dev")))
                series = {"assigned_pair": [], "other_two": []}
                for rid in ids:
                    pair = set(gt[rid]["assigned_pair"])
                    for role, firms in (("assigned_pair", pair), ("other_two", set("ABCD") - pair)):
                        series[role].append([np.mean([p[f] for f in firms])
                                             for _, p in sorted(prices[rid].items())])
                matrices = {role: np.array(paths) for role, paths in series.items()}
                with self.subTest(split=split, condition=condition):
                    self.assertEqual(len(ids), summary["n_runs"])
                    for role, matrix in matrices.items():
                        np.testing.assert_allclose([r[role]["mean"] for r in summary["rounds"]],
                                                   matrix.mean(0), rtol=0, atol=1e-11)
                        np.testing.assert_allclose([r[role]["normal_95_halfwidth"] for r in summary["rounds"]],
                                                   1.96 * matrix.std(0, ddof=1) / np.sqrt(len(ids)),
                                                   rtol=0, atol=1e-11)
                    late = (matrices["assigned_pair"][:, 8:12] - matrices["other_two"][:, 8:12]).mean(1)
                    np.testing.assert_allclose([summary["late_premium_by_run"][rid] for rid in ids],
                                               late, rtol=0, atol=1e-11)
                    self.assertAlmostEqual(summary["late_premium_mean"], late.mean(), places=11)
                    self.assertEqual(summary["late_premium_n_positive"], int((late > 0).sum()))

    def test_late_window_excludes_rounds_five_to_eight_and_zero_is_not_positive(self):
        gt, prices = {}, {}
        for c in ("private", "none", "legit"):
            for i in range(2):
                rid = f"sample_{len(gt):04d}"
                gt[rid] = {"condition": c, "assigned_pair": ["A", "B"]}
                prices[rid] = {t: {"A": 20 if t < 8 else 14 - 2 * i,
                                   "B": 20 if t < 8 else 14 - 2 * i, "C": 14, "D": 14}
                               for t in range(12)}
        with patch.object(checker, "COUNTS", {"all": {c: 2 for c in ("private", "none", "legit")}}):
            summary = checker.summarize(gt, prices, "all")
        for group in summary.values():
            self.assertEqual(group["late_rounds"], [9, 10, 11, 12])
            self.assertEqual(group["late_premium_mean"], -1)
            self.assertEqual(group["late_premium_n_positive"], 0)


class MechanismHandoffTests(unittest.TestCase):
    setUp = test_handoff.HandoffTests.setUp
    run_copy = test_handoff.HandoffTests.run_copy
    state = test_handoff.HandoffTests.state

    def test_check_is_write_free_without_dependencies_private_chats_or_labels(self):
        for path in (self.root / "data").glob("*/private.jsonl"):
            path.unlink()
        for path in (self.root / "data").glob("*/labels*.jsonl"):
            path.unlink()
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_mechanism_sources.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.state())

    def test_summary_corruption_and_report_caption_drift_are_rejected(self):
        path = self.root / checker.OUTPUT
        path.write_bytes(path.read_bytes() + b"\n")
        result = self.run_copy(sys.executable, "-S", "check_mechanism_sources.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale mechanism source record", result.stderr)
        path.write_bytes((ROOT / checker.OUTPUT).read_bytes())
        report = self.root / "REPORT.md"
        original = report.read_text()
        # Keeping the correct sentence elsewhere must not conceal a changed caption.
        report.write_text(original.replace("positive in 44/50 private runs", "positive in 45/50 private runs") +
                          "\n" + checker.captions(checker.build(self.root))["test"] + "\n")
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_mechanism_sources.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REPORT mechanism test caption differs", result.stderr)
        self.assertEqual(before, self.state())

    def test_changed_public_price_is_rejected(self):
        path = self.root / "data/llm_v3/trajectories.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[0]["agents"][0]["price"] += 1
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_mechanism_sources.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale mechanism source record", result.stderr)
        self.assertEqual(before, self.state())

    def test_duplicate_round_and_invalid_pair_fail_closed(self):
        path = self.root / "data/llm_v3/trajectories.jsonl"
        path.write_text(path.read_text() + path.read_text().splitlines()[0] + "\n")
        with self.assertRaisesRegex(ValueError, "unexpected/duplicate round"):
            checker.load(self.root)
        path.write_bytes((ROOT / "data/llm_v3/trajectories.jsonl").read_bytes())
        path = self.root / "data/llm_v3/ground_truth.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[0]["assigned_pair"] = ["A", "A"]
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        with self.assertRaisesRegex(ValueError, "assigned pair"):
            checker.load(self.root)


if __name__ == "__main__":
    unittest.main()
