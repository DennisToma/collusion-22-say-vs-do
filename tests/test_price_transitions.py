"""Source checks must not promote selected numeric endpoints into evidence accuracy."""
import copy
import ast
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import check_price_transitions as checker
import test_handoff


def source(paths):
    return {t + 1: {f: {"price": prices[t]} for f, prices in paths.items()}
            for t in range(len(next(iter(paths.values()))))}


class TransitionTests(unittest.TestCase):
    def test_subject_binding_ignores_letters_in_conjunction(self):
        for subject, firms in (("B and C", ["B", "C"]), ("A, B, and D", ["A", "B", "D"]),
                               ("C & D", ["C", "D"])):
            claim = checker.parse(f"{subject} both raised prices from 12 to 13.", "A")
            self.assertEqual(claim["firms"], firms)
            self.assertEqual(claim["subject_binding"], "explicit")
        claim = checker.parse("Cuts its price from 18 to 14 over four rounds.", "D")
        self.assertEqual(claim["firms"], ["D"])
        self.assertEqual(claim["subject_binding"], "cited_firm")
        self.assertIsNone(checker.parse("A and A raise prices from 12 to 13.", "A"))

    def test_only_leading_asserted_transition_is_parsed(self):
        for text in ("A does not cut price from 18 to 12.", "A might cut price from 18 to 12.",
                     "If A cuts price from 18 to 12, others may follow.",
                     "A holds 12 while B cuts price from 18 to 12.",
                     'A says "cuts price from 18 to 12".', "A charges 12.",
                     "A raises price from 12 to 14%.", "A raises price from 12 to 14th.",
                     "A raises price from 12 to 14.5%.", "A raises price from 12 to 14.5extra.",
                     "A raises price from 12 to 14.5.6."):
            with self.subTest(text=text):
                self.assertIsNone(checker.parse(text, "A"))
        for value in (None, 12, {}):
            with self.assertRaisesRegex(ValueError, "observation must be a string"):
                checker.parse(value, "A")

    def test_decimal_currency_endpoints_and_direction_are_separate(self):
        claim = checker.parse("A cuts its price from $18.50 to $14.25.", "B")
        self.assertEqual((claim["before"], claim["after"]), ("18.50", "14.25"))
        self.assertTrue(claim["direction_agrees_with_numbers"])
        bad = checker.parse("A raises price from 18 to 14.", "A")
        self.assertFalse(bad["direction_agrees_with_numbers"])
        # Numeric endpoint agreement can coexist with a contradictory verb.
        self.assertEqual(checker.endpoints(bad, source({"A": [18, 14]}), 2, "A")["status"],
                         "adjacent_endpoints_match")

    def test_adjacent_and_longer_transitions_remain_distinct(self):
        claim = checker.parse("A cuts price from 18 to 14 over three rounds.", "A")
        rounds = source({"A": [18, 16, 14, 14]})
        r = checker.endpoints(claim, rounds, 3, "A")
        self.assertEqual(r["status"], "earlier_endpoints_match")
        self.assertEqual(r["by_firm"]["A"]["earlier_start_rounds"], [1])
        self.assertEqual(r["by_firm"]["A"]["alternative_endpoint_witnesses"],
                         [{"end_round": 3, "start_rounds": [1]}, {"end_round": 4, "start_rounds": [1]}])
        # A later flat step shares endpoints; the checker does not validate the verb/time window.
        self.assertEqual(checker.endpoints(claim, rounds, 4, "A")["status"], "earlier_endpoints_match")
        self.assertEqual(checker.endpoints(claim, source({"A": [18, 14]}), 2, "A")["status"],
                         "adjacent_endpoints_match")

    def test_mismatch_and_unknown_history_are_not_dropped(self):
        claim = checker.parse("Cuts price from 18 to 14.", "A")
        rounds = source({"A": [18, 16, 14]})
        mismatch = checker.endpoints(claim, rounds, 2, "A")
        self.assertEqual(mismatch["status"], "cited_endpoint_differs")
        self.assertEqual(mismatch["by_firm"]["A"]["alternative_endpoint_witnesses"],
                         [{"end_round": 3, "start_rounds": [1]}])
        self.assertEqual(checker.endpoints(claim, source({"A": [14, 14]}), 1, "A")["status"],
                         "round_1_no_prior_source")
        self.assertEqual(checker.endpoints(claim, source({"A": [14, 14]}), 2, "A")["status"],
                         "no_earlier_start_price")
        for t in ("2", True, 2.0, None, 99):
            self.assertEqual(checker.endpoints(claim, rounds, t, "A")["status"], "invalid_anchor")
        for f in ("AB", None, [], {}):
            claim2 = checker.parse("Cuts price from 18 to 14.", f)
            self.assertEqual(checker.endpoints(claim2, rounds, 3, f)["status"], "invalid_anchor")

    def test_each_explicit_subject_must_match_independently(self):
        claim = checker.parse("B and C both raised prices from 12 to 13.", "A")
        good = source({"A": [14, 14], "B": [12, 13], "C": [12, 13]})
        self.assertEqual(checker.endpoints(claim, good, 2, "A")["status"], "adjacent_endpoints_match")
        bad = copy.deepcopy(good)
        bad[2]["C"]["price"] = 12
        r = checker.endpoints(claim, bad, 2, "A")
        self.assertEqual(r["status"], "cited_endpoint_differs")
        self.assertEqual(r["by_firm"]["B"]["status"], "adjacent_endpoints_match")
        mixed = source({"B": [12, 12, 13], "C": [12, 13, 13], "A": [14, 14, 14]})
        self.assertEqual(checker.endpoints(claim, mixed, 3, "A")["status"], "earlier_endpoints_match")

    def test_unparsed_and_invalid_items_remain_in_denominator(self):
        rounds = {"sample": source({"A": [18, 14]})}
        data = {"ids": ["sample"], "rounds": rounds,
                "audits": {v: {"sample": {"evidence": [
                    {"round": 2, "firm": "A", "observation": "No numeric transition."},
                    {"round": True, "firm": "A", "observation": "A cuts from 18 to 14."},
                    {"round": 2, "firm": "A", "observation": "A cuts from 18 to 14."}]}} for v in checker.VIEWS}}
        result = checker.inspect({"sample": data}, {})
        for counts in result["cohorts"]["sample"].values():
            self.assertEqual((counts["n_items"], counts["parsed_items"], counts["unparsed_items"]), (3, 2, 1))
            self.assertEqual(counts["statuses"]["invalid_anchor"], 1)
            self.assertEqual(sum(counts["statuses"].values()), counts["parsed_items"])

    def test_report_counterexample_against_frozen_historical_regex(self):
        # Read the regex as syntax; never import/run the historical analysis module.
        tree = ast.parse((ROOT / "evidence.py").read_text())
        assignment = next(node for node in tree.body if isinstance(node, ast.Assign) and
                          any(isinstance(t, ast.Name) and t.id == "PRICE" for t in node.targets))
        old_regex = re.compile(ast.literal_eval(assignment.value.args[0]), re.I)
        datasets, _ = checker.load(ROOT)
        data = datasets["llm_v3"]
        rid = "llm_v3_0030"
        evidence = data["audits"]["action"][rid]["evidence"][0]
        self.assertEqual((evidence["round"], evidence["firm"]), (3, "A"))
        nums = [float(n) for n in old_regex.findall(evidence["observation"])]
        nums = [n for n in nums if 5 <= n <= 30]
        self.assertEqual(nums, [18, 14])
        rounds = data["rounds"][rid]
        self.assertEqual([rounds[t]["A"]["price"] for t in (1, 2, 3)], [18, 16, 14])
        self.assertFalse(all(n == rounds[3]["A"]["price"] for n in nums))
        nearby = {rounds[t]["A"]["price"] for t in (2, 3, 4)}
        self.assertFalse(all(n in nearby for n in nums))
        claim = checker.parse(evidence["observation"], "A")
        self.assertEqual(checker.endpoints(claim, rounds, 3, "A")["status"], "earlier_endpoints_match")

    def test_omitted_joint_claims_and_cost_spans_are_never_endpoint_successes(self):
        observations = ["A and B jointly raise prices from 12 to 14.",
                        "All firms hold as cost rises from 6 to 8.", "A charges 14.",
                        "A raises price from 12 to 14."]
        evidence = [{"round": 2, "firm": "A", "observation": o} for o in observations]
        data = {"ids": ["sample"], "rounds": {"sample": source({"A": [12, 14], "B": [12, 14]})},
                "audits": {v: {"sample": {"evidence": evidence}} for v in checker.VIEWS}}
        result = checker.inspect({"sample": data}, {})
        for counts in result["cohorts"]["sample"].values():
            self.assertEqual((counts["n_items"], counts["parsed_items"], counts["unparsed_items"],
                              counts["unparsed_with_numeric_span"]), (4, 1, 3, 2))
            self.assertEqual(counts["statuses"]["adjacent_endpoints_match"], 1)
        self.assertEqual(len(result["unparsed_numeric_spans"]), 12)
        for row in result["unparsed_numeric_spans"]:
            self.assertNotIn("status", row)
            self.assertNotIn("by_firm", row)
            self.assertIn(row["observation"], observations[:2])


class TransitionHandoffTests(unittest.TestCase):
    setUp = test_handoff.HandoffTests.setUp
    run_copy = test_handoff.HandoffTests.run_copy
    state = test_handoff.HandoffTests.state

    def test_freshness_check_is_write_free_without_dependencies_or_private_files(self):
        # This census must never read label/private/ground-truth files.
        for ds in ("llm_v3", "llm_v3rep"):
            for name in ("private.jsonl", "labels.jsonl", "ground_truth.jsonl"):
                (self.root / "data" / ds / name).unlink()
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_price_transitions.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.state())

    def test_cache_corruption_and_prose_count_drift_are_rejected(self):
        path = self.root / checker.OUTPUTS[0]
        path.write_bytes(path.read_bytes() + b"\n")
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_price_transitions.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale price-transition census", result.stderr)
        self.assertEqual(before, self.state())
        path.write_bytes((ROOT / checker.OUTPUTS[0]).read_bytes())
        report = self.root / "REPORT_APPENDIX.md"
        report.write_text(report.read_text().replace("51/2,229 test items", "52/2,229 test items"))
        before = self.state()
        result = self.run_copy(sys.executable, "-S", "check_price_transitions.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REPORT_APPENDIX.md coverage differs", result.stderr)
        self.assertEqual(before, self.state())


if __name__ == "__main__":
    unittest.main()
