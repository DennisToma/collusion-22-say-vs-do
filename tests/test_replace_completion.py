"""E115 corruption/regression tests on generated fixtures only; no real metrics or calls."""
from contextlib import redirect_stdout
import copy
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import p2_replace
import p2_replace_eval as evaluator
import p2_replace_guard as guard
from p2_behaviour import TERMS

DS = 'llm_p2replS'


def dump(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(x) + '\n' for x in rows))


class ReplaceCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir='/var/tmp', prefix='replace_test_')
        self.addCleanup(self.temp.cleanup)
        old = Path.cwd(); os.chdir(self.temp.name); self.addCleanup(os.chdir, old)
        for module in (p2_replace, evaluator):
            for k, v in dict(DS=DS, ARM='sol', NEW_MODEL='gpt-6.1-sol').items():
                self.enterContext(patch.object(module, k, v))
        self.enterContext(patch('p2_behaviour.chat', side_effect=AssertionError('unexpected model call')))
        self.data = {}
        for ds in (guard.SRC, DS):
            gt, traj, priv = [], [], []
            for i in range(40):
                if ds == DS and i % 2 and i >= 20:
                    continue
                rid = f'{ds}_{i:04d}'; seed = 9800000 + i // 2; cond = 'private' if i % 2 == 0 else 'none'
                pair = sorted(random.Random(seed).sample(guard.AG, 2))
                firm = random.Random(seed * 7 + 1).choice(pair if cond == 'private' else guard.AG)
                g = dict(run_id=rid, seed=seed, condition=cond, assigned_pair=pair, rounds=40, framing='strong',
                         sysvar=0, backend='codex', private_channel_enabled=cond == 'private', parse_failures=0,
                         model='gpt-6-luna' if ds == guard.SRC else 'gpt-6-luna,gpt-6.1-sol')
                if ds == DS: g['replaced'] = dict(round0=20, firm=firm, model='gpt-6.1-sol')
                gt.append(g); raw, plans, chat = [], {}, []
                for t in range(40):
                    agents = []
                    for a in guard.AG:
                        fresh = ds == DS and t >= 20 and a == firm
                        price = 14 if fresh else 16
                        msg = 'independent'; pm = 'floor 16' if a in pair and cond == 'private' else ''
                        dec = dict(key=f'{t}:{a}', price=price, public_message=msg, private_message=pm, plan='steady',
                                   backend='codex', model='gpt-6.1-sol' if fresh else 'gpt-6-luna', parse_ok=True)
                        raw.append(dec); plans[f'{t}:{a}'] = 'steady'
                        agents.append(dict(id=a, price=price, public_message=msg, quantity=1, profit=price-6))
                    traj.append(dict(run_id=rid, round=t, market=dict(cost=6, demand_shock='normal'), agents=agents))
                    if cond == 'private':
                        chat.extend(dict(round=t, **{'from': a}, to=next(b for b in pair if b != a), text='floor 16') for a in pair)
                priv.append(dict(run_id=rid, pair=pair, chat=chat, plans=plans))
                dump(Path('data') / ds / 'raw' / f'{rid}.jsonl', raw)
            self.data[ds] = dict(gt=gt, traj=traj, priv=priv)
        self.write_data()
        self.cache = Path('data/llm_p2repl/terms_post21.jsonl')
        rows = []
        for ds, data in self.data.items():
            for p in data['priv']:
                i = int(p['run_id'].rsplit('_', 1)[1])
                if i % 2: continue
                post = [m for m in p['chat'] if m['round'] >= 20]
                row = dict(ds=ds, run_id=p['run_id'], agreed=True, price_floor=16, round=21,
                           n_msgs=len(post), judge_model='gpt-6.1-sol')
                if ds == DS:
                    row.update(chat_sha256=hashlib.sha256(json.dumps(post, sort_keys=True).encode()).hexdigest(),
                               terms_prompt_sha256=hashlib.sha256(TERMS.encode()).hexdigest())
                rows.append(row)
        dump(self.cache, rows)
        Path('results/analysis').mkdir(parents=True)

    def write_data(self):
        for ds, d in self.data.items():
            for fn, key in [('ground_truth', 'gt'), ('trajectories', 'traj'), ('private', 'priv')]:
                dump(Path('data') / ds / f'{fn}.jsonl', d[key])

    def gate(self, complete=True):
        return guard.check_generation(DS, 'gpt-6.1-sol', complete)

    def run_main(self, *args):
        with patch.object(sys, 'argv', ['p2_replace_eval.py', *args]), redirect_stdout(io.StringIO()) as stream:
            evaluator.main()
        return stream.getvalue()

    def test_complete_and_partial_generation(self):
        self.assertEqual(self.gate()['n_complete'], 30)
        self.data[DS]['gt'].pop(); self.write_data()
        with self.assertRaisesRegex(ValueError, 'exactly 30'):
            self.gate()
        self.assertEqual(self.gate(False)['n_complete'], 29)

    def test_duplicate_or_missing_round_rejected(self):
        rows = self.data[DS]['traj']; saved = copy.deepcopy(rows)
        rows.append(rows[0]); self.write_data()
        with self.assertRaisesRegex(ValueError, 'duplicate'): self.gate()
        self.data[DS]['traj'] = saved[:-1]; self.write_data()
        with self.assertRaisesRegex(ValueError, 'round coverage'): self.gate()

    def test_metadata_seed_replacement_and_fallback_rejected(self):
        row = self.data[DS]['gt'][0]; saved = copy.deepcopy(row)
        for key, value in [('seed', 42), ('rounds', 39), ('model', 'gpt-6-luna'), ('replaced', dict(round0=19, firm='A'))]:
            row.update(saved); row[key] = value; self.write_data()
            with self.subTest(key=key), self.assertRaises(ValueError): self.gate()

    def test_state_path_and_prefix_rejected(self):
        rows = self.data[DS]['traj']
        rows[20]['market']['cost'] = 7; self.write_data()
        with self.assertRaisesRegex(ValueError, 'market path'): self.gate()
        rows[20]['market']['cost'] = 6; rows[0]['agents'][0]['profit'] = 99; self.write_data()
        with self.assertRaisesRegex(ValueError, 'trajectory prefix'): self.gate()

    def test_raw_duplicate_missing_and_model_rejected(self):
        p = Path('data') / DS / 'raw' / f'{DS}_0000.jsonl'; rows = guard.read(p)
        for changed, message in [(rows + rows[:1], 'duplicate'), (rows[:-1], 'coverage'),
                                 ([dict(rows[0], model='fallback')] + rows[1:], 'model/fallback')]:
            dump(p, changed)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message): self.gate()

    def test_public_private_and_plan_corruption_rejected(self):
        p = self.data[DS]['priv'][0]; saved = copy.deepcopy(p)
        p['chat'][0]['text'] = 'changed'; self.write_data()
        with self.assertRaisesRegex(ValueError, 'private chat'): self.gate()
        p.update(saved); p['plans']['0:A'] = 'changed'; self.write_data()
        with self.assertRaisesRegex(ValueError, 'plans'): self.gate()
        p.update(copy.deepcopy(saved)); self.data[DS]['traj'][0]['agents'][0]['public_message'] = 'changed'; self.write_data()
        with self.assertRaisesRegex(ValueError, 'public message'): self.gate()

    def test_unparsed_and_invalid_terms_are_not_negative_labels(self):
        base = dict(ds=DS, run_id='x', agreed=True, price_floor=16, round=21, n_msgs=40, judge_model='gpt-6.1-sol')
        for key, value in [('agreed', None), ('agreed', 'false'), ('price_floor', None), ('price_floor', True),
                           ('round', 20), ('judge_model', 'fallback'), ('n_msgs', None)]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                guard.validate_term(dict(base, **{key: value}), DS, 'x')
        guard.validate_term(dict(base, agreed=False, price_floor=None, round=None), DS, 'x')

    def test_stale_duplicate_and_legacy_term_cache(self):
        rid = f'{DS}_0000'; pair = self.data[DS]['priv'][0]['pair']
        rows = guard.read(self.cache)
        source = f'{guard.SRC}_0000'
        evaluator.post_terms(guard.SRC, source, pair, self.cache, None)  # original E112 legacy rows remain usable
        for mode in ('duplicate', 'stale', 'missing_hash'):
            changed = copy.deepcopy(rows)
            r = next(x for x in changed if x['ds'] == DS and x['run_id'] == rid)
            if mode == 'duplicate': changed.append(r)
            elif mode == 'stale': r['chat_sha256'] = 'changed'
            else: r.pop('chat_sha256')
            dump(self.cache, changed)
            with self.subTest(mode=mode), self.assertRaises(ValueError): evaluator.post_terms(DS, rid, pair, self.cache, None)

    def test_check_only_read_only_no_calls_and_no_metrics(self):
        before = {str(p): p.read_bytes() for p in Path('.').rglob('*') if p.is_file()}
        with patch.object(evaluator, 'load', side_effect=AssertionError('metrics must not load')):
            self.assertIn('generation complete', self.run_main('--check-only'))
        self.assertEqual(before, {str(p): p.read_bytes() for p in Path('.').rglob('*') if p.is_file()})

    def test_run_once_and_known_synthetic_outcomes(self):
        self.run_main()
        result, lock = evaluator.final_paths(); data = json.loads(result.read_text())
        self.assertEqual(data['arms']['private']['O1_market_repl_minus_orig'], [-0.5, -0.5, -0.5])
        self.assertEqual(data['arms']['private']['O3_firm_repl_minus_orig'], [-2.0, -2.0, -2.0])
        self.assertEqual(data['arms']['private']['O4_reagreement_floor_ge13']['repl'], [20, 20])
        self.assertEqual(data['verdicts'], dict(S1_newcomer_own_excess_CI_includes_0_private=False,
                         S2_level_survives=True, S3_reagree_le9of20=False, S4_level_cusum_le4of30=True))
        self.assertEqual(data['input_receipt']['legacy_original_terms_without_chat_hash'], 20)
        before = result.read_bytes()
        with self.assertRaisesRegex(ValueError, 'refusing rerun'): self.run_main()
        import shutil
        shutil.rmtree(lock)
        with self.assertRaisesRegex(ValueError, 'refusing rerun'): self.run_main()  # clone has no local lock
        self.assertEqual(result.read_bytes(), before)

    def test_lock_retained_after_computation_failure(self):
        with patch.object(evaluator, 'load', side_effect=ValueError('injected failure')):
            with self.assertRaisesRegex(ValueError, 'injected failure'): self.run_main()
        result, lock = evaluator.final_paths()
        self.assertTrue(lock.exists()); self.assertFalse(result.exists())
        with self.assertRaisesRegex(ValueError, 'refusing rerun'): self.run_main()

    def test_invalid_cached_term_fails_before_metric_and_lock(self):
        rows = guard.read(self.cache); rows[0]['agreed'] = None; dump(self.cache, rows)
        with patch.object(evaluator, 'load', side_effect=AssertionError('metrics must not load')):
            with self.assertRaisesRegex(ValueError, 'unparsed agreement'): self.run_main()
        result, lock = evaluator.final_paths()
        self.assertFalse(lock.exists()); self.assertFalse(result.exists())

    def test_only_declared_reconstruction_is_retained_and_disclosed(self):
        p = Path('data') / DS / 'raw' / f'{DS}_0014.jsonl'
        rows = guard.read(p)
        for row in rows[-4:]: row['reconstructed'] = 'declared recovery from saved fields'
        dump(p, rows)
        self.assertEqual(self.gate()['reconstructed_decisions'], {f'{DS}_0014': [f'39:{a}' for a in 'ABCD']})
        rows[0]['reconstructed'] = 'new damage'; dump(p, rows)
        with self.assertRaisesRegex(ValueError, 'undeclared raw reconstruction'): self.gate()

    def test_concurrent_preparer_refused_before_any_label_or_metric(self):
        p = Path('logs/final/REPLACE_TERMS_PREPARE.flock'); p.parent.mkdir(parents=True)
        with p.open('a') as held:
            fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with patch.object(evaluator, 'post_terms', side_effect=AssertionError('must not label')):
                with self.assertRaises(BlockingIOError): self.run_main()
        result, lock = evaluator.final_paths()
        self.assertFalse(lock.exists()); self.assertFalse(result.exists())

    def test_new_valid_negative_terms_are_cached_and_invalid_responses_preserved(self):
        rid = f'{DS}_0000'; pair = self.data[DS]['priv'][0]['pair']
        rows = [x for x in guard.read(self.cache) if (x['ds'], x['run_id']) != (DS, rid)]
        dump(self.cache, rows)
        judge = lambda p: dict(run_id=p['run_id'], agreed=False, price_floor=None, round=None, judge_model='gpt-6.1-sol')
        out = evaluator.post_terms(DS, rid, pair, self.cache, judge)
        self.assertFalse(out['agreed']); self.assertIn('chat_sha256', out)
        self.assertEqual(evaluator.post_terms(DS, rid, pair, self.cache, None), out)
        dump(self.cache, rows)
        bad_judge = lambda p: dict(run_id=p['run_id'], agreed=None, judge_model='gpt-6.1-sol')
        with self.assertRaisesRegex(ValueError, 'unparsed agreement'): evaluator.post_terms(DS, rid, pair, self.cache, bad_judge)
        self.assertIsNone(guard.read(self.cache)[-1]['agreed'])


if __name__ == '__main__': unittest.main()
