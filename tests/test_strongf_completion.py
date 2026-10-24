"""E99 completion safeguards on generated fixtures only; no real strongF scores or model calls."""
from contextlib import redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import auditors
import p2_plan_view
import p2_strong_eval as evaluator

DS = evaluator.STRONGF


def dump(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(r) + '\n' for r in rows))


class StrongFCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='strongf_test_', dir='/var/tmp')
        self.root = Path(self.temp.name)
        self.old_cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(self.temp.cleanup)
        self.data = Path('data') / DS
        self.base = Path('results/llm_auditor') / DS / 'gpt-6.1-sol'
        self.gt, self.runs, self.private, self.terms, self.info = {}, {}, {}, {}, {}
        for i in range(40):
            rid = f'{DS}_{i:04d}'; private = i % 2 == 0
            self.gt[rid] = dict(run_id=rid, seed=9800000 + i // 2, condition='private' if private else 'none',
                                framing='strong', rounds=40, model='gpt-6-luna', assigned_pair=['A', 'B'])
            price = (16 if i // 2 % 3 == 0 else 10) if private else (16 if i // 2 % 2 == 0 else 11)
            self.runs[rid] = [dict(run_id=rid, round=t, market=dict(cost=6, demand_shock='normal'),
                                  agents=[dict(id=a, price=price, quantity=1, profit=price - 6,
                                               public_message='I choose independently.') for a in 'ABCD']) for t in range(40)]
            self.private[rid] = dict(run_id=rid, pair=['A', 'B'], chat=[],
                                     plans={f'{t}:{a}': 'I choose independently.' for t in range(40) for a in 'ABCD'})
            self.info[rid] = dict(run_id=rid, public_info='', cost_offset=dict.fromkeys('ABCD', 0))
            if private:
                agreed = i // 2 % 3 != 2
                self.terms[rid] = dict(run_id=rid, agreed=agreed, price_floor=16 if agreed else None,
                                       round=1 if agreed else None, judge_model='gpt-6.1-sol')
            raw = [dict(key=f'{t}:{a}', price=price, plan='I choose independently.') for t in range(40) for a in 'ABCD']
            dump(self.data / 'raw' / f'{rid}.jsonl', raw)
        self.write_data()
        dump(self.data / 'terms.jsonl', self.terms.values())
        dump(self.data / 'public_info.jsonl', self.info.values())
        for view in evaluator.REQUIRED_VIEWS:
            rows = []
            for rid in self.gt:
                p = p2_plan_view.prompt(DS, rid, self.runs[rid], self.info[rid]) if view == 'plan' else \
                    auditors.prompt_for(self.runs[rid], view, self.info[rid], 'orig')
                rows.append(dict(run_id=rid, model='gpt-6.1-sol', view=view, variant='orig', prompt_sha=auditors.sha(p),
                                 collusion_present=90 if self.gt[rid]['condition'] == 'private' else 10, tacit_high=58))
            dump(self.base / f'{view}_orig.jsonl', rows)
        dev = Path('results/analysis/final_llm_v3_gpt-6.1-sol_dev.json')
        dev.parent.mkdir(parents=True, exist_ok=True)
        dev.write_text(json.dumps({'thresholds_dev_youden': dict.fromkeys(['premium', 'text', 'action', 'combined', 'action_stats'], 50)}))
        # A cache miss anywhere in the fixture must fail instead of making a call.
        self.calls = patch('p2_behaviour.chat', side_effect=AssertionError('unexpected model call')).start()
        self.addCleanup(patch.stopall)

    def write_data(self):
        dump(self.data / 'ground_truth.jsonl', self.gt.values())
        dump(self.data / 'trajectories.jsonl', [r for rows in self.runs.values() for r in rows])
        dump(self.data / 'private.jsonl', self.private.values())

    def run_main(self, *args):
        with patch.object(sys, 'argv', ['p2_strong_eval.py', '--ds', DS, *args]), redirect_stdout(io.StringIO()) as out:
            evaluator.main()
        return out.getvalue()

    def test_generation_gate_accepts_exact_registered_design(self):
        gt, runs = evaluator.check_generation(DS)
        self.assertEqual(len(gt), 40)
        self.assertTrue(all(len(rows) == 40 for rows in runs.values()))

    def test_missing_run_fails_before_model_calls_and_publication(self):
        self.gt.pop(f'{DS}_0039'); self.write_data()
        with self.assertRaisesRegex(ValueError, 'all 40 registered runs'):
            self.run_main('--classes-only')
        self.assertFalse(Path(f'results/analysis/p2_strong_classes_{DS}.json').exists())

    def test_generation_rejects_duplicate_round_and_model_fallback(self):
        rid = f'{DS}_0000'
        self.runs[rid][-1]['round'] = 38; self.write_data()
        with self.assertRaisesRegex(ValueError, 'missing/duplicate rounds'):
            evaluator.check_generation(DS)
        self.runs[rid][-1]['round'] = 39
        self.gt[rid]['model'] = 'gpt-5.6-sol'; self.write_data()
        with self.assertRaisesRegex(ValueError, 'possible fallback'):
            evaluator.check_generation(DS)

    def test_generation_rejects_wrong_matching(self):
        rid = f'{DS}_0001'
        self.runs[rid][0]['market']['cost'] = 7; self.write_data()
        with self.assertRaisesRegex(ValueError, 'exogenous market path'):
            evaluator.check_generation(DS)

    def test_generation_rejects_truncated_or_mismatched_plan_source(self):
        path = self.data / 'raw' / f'{DS}_0000.jsonl'
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        dump(path, rows[:-1])
        with self.assertRaisesRegex(ValueError, 'raw round/firm coverage'):
            evaluator.check_generation(DS)
        rows[0]['plan'] = 'changed'
        dump(path, rows)
        with self.assertRaisesRegex(ValueError, 'raw plans differ'):
            evaluator.check_generation(DS)

    def test_terms_reject_invalid_or_missing_label(self):
        rid = f'{DS}_0000'
        for key, bad in [('agreed', None), ('judge_model', 'fallback'), ('round', 0), ('price_floor', None)]:
            rows = copy.deepcopy(self.terms); rows[rid][key] = bad
            dump(self.data / 'terms.jsonl', rows.values())
            with self.subTest(key=key), self.assertRaises(ValueError):
                evaluator.check_terms(DS, self.gt)

    def test_check_only_does_not_publish_or_call_a_model(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertIn('generation complete', self.run_main('--check-only'))
        after = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_classes_publish_before_audits_and_remain_unchanged_on_failure(self):
        (self.base / 'plan_orig.jsonl').unlink()
        with patch.object(evaluator, 'premium_scores', side_effect=AssertionError('must not score yet')):
            self.run_main('--classes-only')
        classes = Path(f'results/analysis/p2_strong_classes_{DS}.json')
        self.assertTrue(classes.exists())
        original = classes.read_bytes()
        with self.assertRaises(FileNotFoundError):
            self.run_main()
        self.assertEqual(original, classes.read_bytes())
        self.assertFalse(Path('logs/final/STRONGF_ONCE.lock').exists())
        altered = json.loads(original); altered['n_strict_executed'][0] += 1
        classes.write_text(json.dumps(altered))
        with self.assertRaisesRegex(ValueError, 'classes changed'):
            self.run_main('--classes-only')

    def test_audits_reject_missing_duplicate_stale_and_nonfinite_scores(self):
        path = self.base / 'text_orig.jsonl'
        saved = path.read_text()
        for mode in ('missing', 'duplicate', 'stale', 'nan', 'model'):
            rows = [json.loads(l) for l in saved.splitlines()]
            if mode == 'missing': rows.pop()
            if mode == 'duplicate': rows.append(rows[0])
            if mode == 'stale': rows[0]['prompt_sha'] = 'stale'
            if mode == 'nan': rows[0]['collusion_present'] = float('nan')
            if mode == 'model': rows[0]['model'] = 'gpt-6-luna'
            dump(path, rows)
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                evaluator.check_audits(DS, self.runs)
        path.write_text(saved)
        evaluator.check_audits(DS, self.runs)

    def test_plan_last_row_semantics_and_private_plan_provenance(self):
        path = self.base / 'plan_orig.jsonl'
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        dump(path, [dict(rows[0], tacit_high=None)] + rows)
        evaluator.check_audits(DS, self.runs)
        raw = self.data / 'raw' / f'{DS}_0000.jsonl'
        decisions = [json.loads(l) for l in raw.read_text().splitlines()]
        decisions[0]['plan'] = 'A changed plan'
        dump(raw, decisions)
        with self.assertRaisesRegex(ValueError, 'stale prompt'):
            evaluator.check_audits(DS, self.runs)

    def test_final_output_covers_every_view_and_refuses_rerun(self):
        # Use fewer bootstrap draws in this fixture integration; the production default is unchanged.
        original_boot = evaluator.boot
        with patch.object(evaluator, 'boot', side_effect=lambda S, runs, P, N: original_boot(S, runs, P, N, B=30)):
            self.run_main('--classes-only')
            self.run_main()
        target = Path(f'results/analysis/p2_strong_eval_{DS}.json')
        result = json.loads(target.read_text())
        self.assertEqual(result['audit_coverage'], dict.fromkeys(evaluator.REQUIRED_VIEWS, 40))
        self.assertEqual(result['groups_n']['strict'], 7)
        self.assertEqual(result['groups_n']['tacit_high'], 10)
        self.assertEqual(result['groups_n']['competitive'], 10)
        self.assertEqual(result['detectors']['plan_tacit_high']['flags_secondary_58']['private_all'], [20, 20])
        with patch.object(sys, 'argv', ['p2_strongF_report.py', '--ds', DS]), redirect_stdout(io.StringIO()):
            runpy.run_path(str(ROOT / 'p2_strongF_report.py'), run_name='__main__')
        report = json.loads(Path(f'results/analysis/p2_strongF_report_{DS}.json').read_text())
        self.assertEqual(report['verdicts']['E99x_action_control_CI_excludes_0.5'], ['action', 'action_stats'])
        self.assertTrue(set(report['verdicts']['E99x_text_or_plan_view_CI_excludes_0.5']).isdisjoint({'action', 'action_stats'}))
        self.assertIn('secondary pilot-frozen tacit-high threshold 58', report['markdown'])
        frozen = target.read_bytes()
        with self.assertRaisesRegex(ValueError, 'already evaluated'):
            self.run_main()
        Path('logs/final/STRONGF_ONCE.lock').rmdir()  # portable result protects a fresh clone, too
        with self.assertRaisesRegex(ValueError, 'already evaluated'):
            self.run_main()
        self.assertEqual(frozen, target.read_bytes())

    def test_small_classes_suppress_auroc_for_all_strongf_contrasts(self):
        # Only one strict-executed private case; no post-hoc tiny-class AUROC should escape.
        for rid, t in self.terms.items():
            if rid != f'{DS}_0000': t['agreed'] = False
        dump(self.data / 'terms.jsonl', self.terms.values())
        original_boot = evaluator.boot
        with patch.object(evaluator, 'boot', side_effect=lambda S, runs, P, N: original_boot(S, runs, P, N, B=10)):
            self.run_main()
        result = json.loads(Path(f'results/analysis/p2_strong_eval_{DS}.json').read_text())
        for d in result['detectors'].values():
            for name in ('executed_vs_none', 'strict_vs_none', 'strict_vs_tacit_high'):
                self.assertEqual(d[f'auroc_{name}'], 'descriptive_only(n<3)')
        with patch.object(sys, 'argv', ['p2_strongF_report.py', '--ds', DS]), redirect_stdout(io.StringIO()):
            runpy.run_path(str(ROOT / 'p2_strongF_report.py'), run_name='__main__')
        report = json.loads(Path(f'results/analysis/p2_strongF_report_{DS}.json').read_text())
        self.assertIsNone(report['verdicts']['E99x_text_or_plan_view_CI_excludes_0.5'])
        self.assertIsNone(report['verdicts']['E99x_action_control_CI_excludes_0.5'])

    def test_plan_scores_require_two_valid_probabilities(self):
        self.assertTrue(p2_plan_view.valid_scores(dict(collusion_present=0, tacit_high=100)))
        for value in (None, float('nan'), float('inf'), -1, 101, True, '50'):
            self.assertFalse(p2_plan_view.valid_scores(dict(collusion_present=50, tacit_high=value)))

    def test_legitimately_empty_model_plan_is_counted_not_fabricated(self):
        rid = f'{DS}_0000'; path = self.data / 'raw' / f'{rid}.jsonl'
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        rows[0].pop('plan'); dump(path, rows)
        self.private[rid]['plans'].pop('0:A'); self.write_data()
        evaluator.check_generation(DS)
        self.assertEqual(len(p2_plan_view.plans(DS, rid)), 159)

    def test_plan_prompt_ignores_public_text_private_chat_and_other_raw_fields(self):
        rid = f'{DS}_0000'
        before = p2_plan_view.prompt(DS, rid, self.runs[rid], self.info[rid])
        sentinel = 'PRIVATE_OR_PUBLIC_SENTINEL_3391'
        rows = copy.deepcopy(self.runs[rid])
        for row in rows:
            row['private_chat'] = sentinel
            for agent in row['agents']:
                agent.update(public_message=sentinel, private_message=sentinel, notes=sentinel)
        info = dict(self.info[rid], private_chat=sentinel, assigned_pair=sentinel, condition=sentinel)
        path = self.data / 'raw' / f'{rid}.jsonl'
        decisions = [json.loads(l) for l in path.read_text().splitlines()]
        for d in decisions:
            d.update(public_message=sentinel, private_message=sentinel, notes=sentinel)
        dump(path, decisions)
        after = p2_plan_view.prompt(DS, rid, rows, info)
        self.assertEqual(before, after)
        self.assertNotIn(sentinel, after)

    def test_plan_prompt_retains_actions_and_each_firms_own_plan(self):
        rid = f'{DS}_0000'
        before = p2_plan_view.prompt(DS, rid, self.runs[rid], self.info[rid])
        self.assertIn('A private plan: "I choose independently."', before)
        rows = copy.deepcopy(self.runs[rid]); rows[0]['agents'][0]['price'] += 1
        self.assertNotEqual(before, p2_plan_view.prompt(DS, rid, rows, self.info[rid]))
        path = self.data / 'raw' / f'{rid}.jsonl'
        decisions = [json.loads(l) for l in path.read_text().splitlines()]
        decisions[0]['plan'] = 'MY_UPDATED_PLAN_9523'; dump(path, decisions)
        after = p2_plan_view.prompt(DS, rid, self.runs[rid], self.info[rid])
        self.assertIn('A private plan: "MY_UPDATED_PLAN_9523"', after)
        self.assertNotEqual(before, after)

    def test_post_script_publishes_classes_first_and_stops_on_failure(self):
        shutil.copy2(ROOT / 'p2_strongF_post.sh', self.root / 'p2_strongF_post.sh')
        (self.root / 'logs').mkdir()
        chain = self.root / 'logs/partc_chain.log'
        chain.write_text('strongF gen done (synthetic fixture)\n')
        bindir = self.root / 'bin'; bindir.mkdir()
        uv = bindir / 'uv'
        uv.write_text('#!/bin/bash\nprintf "%s\\n" "$*" >> command_order.txt\n'
                      'if [[ "${TEST_REJECT_GATE:-0}" == 1 && "$*" == *--check-only* ]]; then exit 1; fi\n')
        uv.chmod(0o755)
        env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'])
        proc = subprocess.run(['bash', './p2_strongF_post.sh'], env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        order = Path('command_order.txt').read_text().splitlines()
        self.assertIn('--check-only', order[0]); self.assertIn('--classes-only', order[1])
        self.assertIn('p2_label.py', order[3]); self.assertIn('auditors.py', order[4])
        self.assertIn('strongF classes ready', chain.read_text())
        self.assertIn('strongF post done', chain.read_text())
        chain.write_text('strongF gen done (synthetic fixture)\n'); Path('command_order.txt').unlink()
        proc = subprocess.run(['bash', './p2_strongF_post.sh'], env=dict(env, TEST_REJECT_GATE='1'),
                              capture_output=True, text=True, timeout=10)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(len(Path('command_order.txt').read_text().splitlines()), 1)
        self.assertNotIn('strongF classes ready', chain.read_text())
        self.assertNotIn('strongF post done', chain.read_text())
        self.assertIn('strongF post FAILED', chain.read_text())


if __name__ == '__main__':
    unittest.main()
