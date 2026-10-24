"""E95 coverage freeze must preserve sources as unrelated audits accumulate."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import p2_family3way as f


class FamilyScopeTests(unittest.TestCase):
    def setUp(self):
        self.rows = [dict(run_id=f'run{i}', collusion_present=i * 20) for i in (2, 1)]
        self.scope = {'views': {'ds': {'text': {'n': 2, 'rows_sha256': {
            x['run_id']: hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest() for x in self.rows}}}}}

    def get(self, rows, view='text'):
        return f.scoped_audits('ds', view, iter(rows), self.scope)

    def test_later_rows_and_reordering_do_not_change_frozen_order(self):
        self.assertEqual(self.get([self.rows[1], dict(run_id='later'), self.rows[0]]), self.rows)

    def test_changed_score_refused(self):
        with self.assertRaisesRegex(AssertionError, 'changed'):
            self.get([dict(self.rows[0], collusion_present=99), self.rows[1]])

    def test_missing_or_duplicate_source_refused(self):
        for rows, message in ((self.rows[:1], 'missing'), (self.rows + self.rows[:1], 'duplicate')):
            with self.subTest(message=message), self.assertRaisesRegex(AssertionError, message):
                self.get(rows)

    def test_later_view_excluded(self):
        self.assertIsNone(self.get(self.rows, view='combined_stats'))

    def test_committed_scope_is_explicitly_posthoc(self):
        scope = json.loads((ROOT / f.SCOPE).read_text())
        self.assertIn('post-hoc', scope['kind'])
        self.assertEqual(scope['views']['llm_p2cue']['action_stats']['n'], 9)
        self.assertNotIn('combined_stats', scope['views']['llm_p2cue'])


if __name__ == '__main__':
    unittest.main()
