"""Challenge literal-source checks without claiming semantic evidence accuracy."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import check_evidence_sources as checker
import test_handoff


class LiteralSourceTests(unittest.TestCase):
    def test_quote_styles_short_spans_apostrophes_and_nested_quotes(self):
        text = 'A’s statement says “Measured price”; D\'s says "We can\'t promise" and \'fair value\'. ‘Good terms’ too.'
        self.assertEqual(checker.quoted_spans(text),
                         ['Measured price', "We can't promise", 'fair value', 'Good terms'])
        self.assertEqual(checker.quoted_spans('A’s and D\'s prices rose; firms’ messages agree.'), [])
        self.assertEqual(checker.quoted_spans('"Our ‘value’ today"'), ["Our ‘value’ today"])
        self.assertEqual(checker.quoted_spans('"Fair\nprice" and \'good\nterms\''), ['Fair\nprice', 'good\nterms'])
        self.assertEqual(checker.quoted_spans('"$15" or \'12\''), ['$15', '12'])
        # Delimiter-only parsing cannot disambiguate a same-style plural possessive.
        self.assertEqual(checker.quoted_spans("'firms' prices remain high'"), ['firms'])
        for value in (None, 12, {}):
            with self.assertRaisesRegex(ValueError, 'observation must be a string'):
                checker.quoted_spans(value)

    def test_literal_match_normalizes_case_spaces_unicode_but_keeps_punctuation(self):
        self.assertTrue(checker.contains('We use a ＦＡＩＲ\n   price.', 'fair price'))
        self.assertFalse(checker.contains('We evaluate prices.', 'value'))
        self.assertFalse(checker.contains('We offer fair-price terms.', 'fair price'))
        self.assertFalse(checker.contains('No quotation here.', ''))

    def test_source_locations_and_precedence_are_explicit(self):
        rounds = {1: {"A": {"public_message": "fair price"}, "B": {"public_message": "fair price"}},
                  2: {"A": {"public_message": "other offer"}, "B": {"public_message": "rival value"}}}
        self.assertEqual(checker.locate('fair price', rounds, 'A', 1)['location'], 'cited_firm_round')
        self.assertEqual(checker.locate('fair price', rounds, 'A', 2)['location'], 'cited_firm_other_round')
        self.assertEqual(checker.locate('rival value', rounds, 'A', 2)['location'], 'other_firm_cited_round')
        self.assertEqual(checker.locate('rival value', rounds, 'A', 1)['location'], 'other_firm_other_round')
        self.assertEqual(checker.locate('invented phrase', rounds, 'A', 1)['location'], 'not_found')
        # A match must stay within one public message, not cross a round boundary.
        self.assertEqual(checker.locate('price other', rounds, 'A', 1)['hits'], [])
        self.assertEqual(len(checker.locate('fair price', rounds, 'A', 1)['hits']), 2)
        for t in ('1', True, 1.0, None, 99):
            self.assertEqual(checker.locate('fair price', rounds, 'A', t)['location'], 'invalid_anchor')
        for f in ('AB', None, [], {}):
            self.assertEqual(checker.locate('fair price', rounds, f, 1)['location'], 'invalid_anchor')

    def test_invalid_anchors_and_unquoted_items_stay_in_coverage_denominator(self):
        rounds = {"sample_0000": {1: {"A": {"public_message": 'fair price'}}}}
        ev = [{"round": 1, "firm": 'A', "observation": 'Paraphrase only.'},
              {"round": '1', "firm": 'A', "observation": '"fair price"'},
              {"round": 1, "firm": 'AB', "observation": 'Other claim.'}]
        data = {"sample": {"ids": ['sample_0000'], "rounds": rounds,
                           "audits": {v: {"sample_0000": {"evidence": copy.deepcopy(ev)}} for v in checker.VIEWS}}}
        result = checker.inspect(data, {})
        for s in result['cohorts']['sample'].values():
            self.assertEqual(s['n_items'], 3)
            self.assertEqual(s['well_formed_source_items'], 1)
            self.assertEqual(s['items_with_marked_span'], 1)
        self.assertTrue(all(s['well_formed_anchor'] is False for s in result['marked_spans']))
        self.assertTrue(all(s['location'] == 'invalid_anchor' for s in result['marked_spans']))

    def test_renderer_escapes_cached_text_and_never_exports_injected_private_fields(self):
        agent = {"public_message": '<script>alert("public")</script>', "price": 12,
                 "quantity": 3, "profit": 18, "private_message": 'PRIVATE_SENTINEL'}
        ev = {"round": 1, "firm": 'A', "observation": '<img src=x onerror=alert(1)>'}
        data = {"sample": {"ids": ['sample_0000'], "rounds": {"sample_0000": {1: {'A': agent}}},
                           "markets": {"sample_0000": {1: {"cost": 6}}},
                           "info": {"sample_0000": {"public_info": '<private>'}},
                           "audits": {v: {"sample_0000": {"evidence": [ev], "scores": {"AB": 20},
                                                            "collusion_present": 20}} for v in checker.VIEWS}}}
        result = checker.inspect(data, {})
        document = checker.render_html(data, result)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', document)
        self.assertNotIn('<img src=x', document)
        self.assertNotIn('PRIVATE_SENTINEL', document)
        self.assertEqual(document.count('<script>'), 1)  # Only the renderer's fixed filtering script.


class SourceLedgerIntegrationTests(unittest.TestCase):
    setUp = test_handoff.HandoffTests.setUp
    run_copy = test_handoff.HandoffTests.run_copy
    state = test_handoff.HandoffTests.state

    def test_freshness_check_is_write_free_without_dependencies(self):
        before = self.state()
        result = self.run_copy(sys.executable, '-S', 'check_evidence_sources.py', '--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.state())

    def test_same_length_source_change_invalidates_ledger(self):
        path = self.root / 'results/llm_auditor/llm_v3/gpt-6.1-sol/text_orig.jsonl'
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        row = next(r for r in rows if r['run_id'] == 'llm_v3_0030')
        obs = row['evidence'][0]['observation']
        row['evidence'][0]['observation'] = ('X' if obs[0] != 'X' else 'Y') + obs[1:]
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        before = self.state()
        result = self.run_copy(sys.executable, '-S', 'check_evidence_sources.py', '--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('stale evidence source ledger', result.stderr)
        self.assertEqual(before, self.state())

    def test_public_setup_change_invalidates_ledger(self):
        path = self.root / 'data/llm_v3rep/public_info.jsonl'
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[0]['public_info'] += ' Modified public setup.'
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        result = self.run_copy(sys.executable, '-S', 'check_evidence_sources.py', '--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('stale evidence source ledger', result.stderr)

    def test_coverage_prose_must_match_source_counts(self):
        path = self.root / 'REPORT.md'
        path.write_text(path.read_text().replace('2,229 evidence items', '2,228 evidence items'))
        result = self.run_copy(sys.executable, '-S', 'check_evidence_sources.py', '--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('coverage prose differs', result.stderr)


if __name__ == '__main__':
    unittest.main()
