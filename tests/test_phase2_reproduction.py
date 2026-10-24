"""Offline verifier failure paths, using synthetic files and no scientific data."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
import io

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_phase2 as v


class ReproductionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='repro_test_', dir='/var/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'llm.py').write_text('def chat(*a, **k): raise AssertionError("unguarded call")\n')
        self.output = self.root / 'result.json'
        self.output.write_text('{"estimate": 0.75, "n": 20}')

    def run_script(self, source, timeout=10):
        (self.root / 'analysis.py').write_text(source)
        return v.run_case(self.root, v.case('analysis.py', outputs=['result.json']), timeout)

    def test_exact_json_allows_formatting_and_key_order(self):
        r = self.run_script('from pathlib import Path\nPath("result.json").write_text(\'{"n":20,"estimate":0.75}\')')
        self.assertTrue(r['passed'])

    def test_changed_estimate_is_not_rounded_away(self):
        r = self.run_script('from pathlib import Path\nPath("result.json").write_text(\'{"n":20,"estimate":0.75001}\')')
        self.assertFalse(r['passed'])
        self.assertEqual(r['outputs']['result.json']['differences'][0]['path'], '$.estimate')

    def test_noop_cannot_pass_from_existing_target(self):
        r = self.run_script('pass')
        self.assertFalse(r['passed'])
        self.assertEqual(r['outputs']['result.json']['state'], 'missing')
        self.assertEqual(json.loads(self.output.read_text())['n'], 20)

    def test_invalid_json_and_failed_exit_refused(self):
        r = self.run_script('from pathlib import Path\nPath("result.json").write_text("bad")\nraise ValueError("failure")')
        self.assertFalse(r['passed'])
        self.assertEqual(r['outputs']['result.json']['state'], 'invalid_json')
        self.assertIn('failure', r['error'])

    def test_model_network_and_subprocess_blocked(self):
        for source in ('import llm; llm.chat("x")',
                       'import socket; socket.create_connection(("127.0.0.1", 1))',
                       'import subprocess; subprocess.run(["true"])'):
            with self.subTest(source=source):
                r = self.run_script(source)
                self.assertFalse(r['passed'])
                self.assertIn('forbids', r['error'])

    def test_external_write_and_symlink_escape_blocked(self):
        outside = self.root.parent / (self.root.name + '_escape')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (self.root / 'escape').symlink_to(self.root.parent, target_is_directory=True)
        for path in (str(outside), str(self.root / 'escape' / outside.name)):
            with self.subTest(path=path):
                r = self.run_script(f'from pathlib import Path\nPath({path!r}).write_text("unsafe")')
                self.assertFalse(r['passed']); self.assertFalse(outside.exists())

    def test_external_remove_blocked(self):
        outside = self.root.parent / (self.root.name + '_retain')
        outside.write_text('keep')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        r = self.run_script(f'from pathlib import Path\nPath({str(outside)!r}).unlink()')
        self.assertFalse(r['passed']); self.assertEqual(outside.read_text(), 'keep')

    def test_timeout_is_failure(self):
        r = self.run_script('while True: pass', timeout=0.1)
        self.assertFalse(r['passed']); self.assertIsNone(r['returncode'])

    def test_readonly_receipt_rejects_stale_and_failed_results(self):
        receipt = {'passed': True, 'input_sha256': {'result.json': v.sha(self.output)},
                   'n_commands_passed': 1, 'n_commands': 1, 'n_outputs_matched': 1, 'n_outputs': 1}
        p = self.root / v.RECEIPT; p.parent.mkdir(parents=True)
        p.write_text(json.dumps(receipt))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(v.check_receipt(self.root), receipt)
        self.output.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'stale'):
            v.check_receipt(self.root)
        receipt['input_sha256'] = {}; receipt['passed'] = False
        p.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, 'failed'):
            v.check_receipt(self.root)

    def test_active_inputs_and_sealed_entrypoints_excluded(self):
        for name in ('data/llm_p2replS/private.jsonl', 'data/ext_llm_grid_p2/labels.jsonl',
                     'results/llm_auditor/ext_llm_grid_p2/gpt-6.1-sol/text_orig.jsonl',
                     str(v.RECEIPT), 'results/analysis/p2_e1_coverage.json'):
            self.assertFalse(v.include(Path(name)), name)
        forbidden = {'p2_e1_audit.py', 'p2_replace_eval.py', 'p2_strong_eval.py', 'final_analysis.py', 'replication.py'}
        self.assertFalse(forbidden & {x['argv'][0] for x in v.CASES})
        outputs = [p for c in v.CASES for p in c['outputs']]
        self.assertEqual(len(outputs), len(set(outputs)))


if __name__ == '__main__':
    unittest.main()
