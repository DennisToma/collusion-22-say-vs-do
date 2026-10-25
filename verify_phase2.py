"""Reproduce completed Phase 2 analyses offline in a disposable tracked-file copy.

    uv run python verify_phase2.py

Never invokes sealed evaluations, generation, judges, or auditors. Original saved
results are comparison targets only. The JSON receipt is post-hoc verification,
not pre-registration or an independent statistical implementation. Requires git
and the pinned numerical environment; scratch space is under /var/tmp.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
RECEIPT = Path('results/analysis/phase2_reproduction.json')


def case(script, args=(), outputs=None):
    return {'argv': [script, *args], 'outputs': outputs or [f'results/analysis/{Path(script).stem}.json']}


CASES = [
    case('p2_cue.py', ['--ds', *[f'llm_p2{x}' for x in ('cue', 'claude', 'ds', 'sol', 'para1', 'para2')]],
         [f'results/analysis/p2_cue_llm_p2{x}.json' for x in ('cue', 'claude', 'ds', 'sol', 'para1', 'para2')]),
    case('p2_cue_verdict.py', outputs=['results/analysis/p2_cue_verdict_llm_p2cue.json']),
    case('p2_band.py'), case('p2_aware.py'), case('p2_asym.py'), case('p2_asym_nash.py'),
    case('p2_logbook.py'), case('p2_de.py'), case('p2_prevalence.py'),
    case('p2_family_views.py', ['--ds', 'llm_p2claude', 'llm_p2sol', 'llm_p2ds', 'llm_p2para2', 'llm_p2para1']),
    case('p2_family3way.py'),
    *[case('p2_strong.py', ['--ds', *datasets, '--min-floor', str(floor), '--late', str(late), '--out', out], [out])
      for datasets, floor, late, out in (
          (['llm_p2strongF'], 13, 11, 'results/analysis/p2_strongF.json'),
          (['llm_p2g56sol', 'llm_p2mimo'], 12, 2, 'results/analysis/p2_c2older.json'),
          (['llm_p2qwenb', 'llm_p2qwena'], 12, 2, 'results/analysis/p2_qwen.json'),
          (['llm_p2qwenbS', 'llm_p2qwenaS'], 13, 11, 'results/analysis/p2_qwen_strong.json'))],
    case('p2_qwen_cmp.py'), case('p2_qwen_public.py'), case('p2_strongF_public.py'),
    case('p2_strongF_report.py', outputs=['results/analysis/p2_strongF_report_llm_p2strongF.json']),
    case('p2_plan_keyword.py', outputs=['results/analysis/p2_plan_keyword_llm_p2strongF.json']),
    case('p2_within_agree.py', ['llm_p2strongF', 'llm_p2qwena', 'llm_p2qwenb'],
         [f'results/analysis/p2_within_agree_{d}.json' for d in ('llm_p2strongF', 'llm_p2qwena', 'llm_p2qwenb')]),
    case('p2_strict_sensitivity.py'),
    case('p2_behaviour.py'),
    case('p2_behaviour.py', ['--ds', 'llm_p2rep', '--out', 'results/analysis/p2_behaviour_p2rep.json'],
         ['results/analysis/p2_behaviour_p2rep.json']),
    case('p2_textlr.py'),
    case('p2_pool.py', outputs=['results/analysis/p2_pool_rep.json']),
    # E133 a-e: c/d read the frozen sol cache only (Q22_CACHE_ONLY + llm.chat denied below).
    case('p2_e133_privileged.py', outputs=['results/analysis/e133_privileged.json']),
    case('p2_e133c_llm.py', outputs=['results/analysis/e133c_llm.json']),
    case('p2_e133c_llm.py', ['--noprivate'], ['results/analysis/e133d_noprivate_llm.json']),
    case('p2_e133_cluster.py', outputs=['results/analysis/e133_cluster.json']),
    case('p2_e133e_attr.py', outputs=['results/analysis/e133e_attr.json']),
]

# This harness is executed in a fresh child for every explicitly listed command.
# Blocking at the llm API AND Python audit events also catches direct fallbacks.
HARNESS = '''import os, pathlib, runpy, sys
root = pathlib.Path.cwd().resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root))
import llm
def denied(*args, **kwargs):
    raise RuntimeError("offline reproduction forbids model/network/process calls")
llm.chat = denied
def inside(path):
    if isinstance(path, int):
        return True
    return pathlib.Path(os.fsdecode(path)).resolve().is_relative_to(root)
def guard(event, args):
    if event == "subprocess.Popen":
        raise PermissionError("offline reproduction forbids subprocesses")
    if event.startswith("socket.") or event in ("os.system", "os.exec", "os.posix_spawn", "os.fork", "pty.spawn"):
        denied()
    if event == "open":
        path, mode, flags = args
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing and not inside(path):
            raise RuntimeError("offline reproduction forbids writes outside scratch")
    positions = {"os.remove": (0,), "os.rmdir": (0,), "os.mkdir": (0,), "os.rename": (0, 1), "os.link": (0, 1), "os.symlink": (1,), "os.truncate": (0,), "os.chmod": (0,)}
    if event in positions and any(not inside(args[i]) for i in positions[event]):
        raise RuntimeError("offline reproduction forbids mutation outside scratch")
sys.addaudithook(guard)
script, *args = sys.argv[1:]
sys.argv = [script, *args]
runpy.run_path(script, run_name="__main__")
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(a, b, path='$', limit=12):
    """Exact parsed-JSON comparison: ignore key order/formatting, no numeric tolerance."""
    if type(a) is not type(b):
        return [{'path': path, 'saved': a, 'regenerated': b}]
    if isinstance(a, dict):
        out = []
        for k in sorted(a.keys() | b.keys()):
            if k not in a or k not in b:
                out.append({'path': f'{path}.{k}', 'missing_in': 'saved' if k not in a else 'regenerated'})
            else:
                out.extend(differences(a[k], b[k], f'{path}.{k}', limit))
            if len(out) >= limit:
                break
        return out[:limit]
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'saved_length': len(a), 'regenerated_length': len(b)}]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(differences(x, y, f'{path}[{i}]', limit))
            if len(out) >= limit:
                break
        return out[:limit]
    return [] if a == b else [{'path': path, 'saved': a, 'regenerated': b}]


def tracked_paths(root):
    p = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], check=True, capture_output=True)
    return [Path(os.fsdecode(x)) for x in p.stdout.split(b'\0') if x]


def include(path):
    s = path.as_posix()
    # No active generators or unsealed grid scores are copied or inspected.
    return (path.suffix in ('.py', '.json', '.jsonl', '.toml', '.lock')
            and not s.startswith(('data/llm_p2replS/', 'data/ext_llm_grid_p2/',
                                  'results/llm_auditor/ext_llm_grid_p2/'))
            and path not in (RECEIPT, Path('results/analysis/p2_e1_coverage.json'))
            or s == 'data/ext_llm_grid_p2/SHA256SUMS')  # hash pins only, needed by E133


def run_case(scratch, entry, timeout):
    expected = {p: json.loads((scratch / p).read_text()) for p in entry['outputs']}
    for p in entry['outputs']:
        (scratch / p).unlink()  # A no-op or an incomplete writer cannot pass.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0',
               MPLCONFIGDIR=str(scratch / '.mpl'), TMPDIR=str(scratch / '.tmp'),
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', Q22_CACHE_ONLY='1',
               Q22_SIB=str((ROOT / '..' / 'collusion-14-infotheory').resolve()))  # sibling is read-only input
    (scratch / '.tmp').mkdir(exist_ok=True)
    start = time.monotonic()
    try:
        proc = subprocess.run([sys.executable, '-B', '-c', HARNESS, *entry['argv']],
                              cwd=scratch, env=env, capture_output=True, text=True, timeout=timeout)
        error = proc.stderr[-2500:] if proc.returncode else None
        returncode = proc.returncode
    except subprocess.TimeoutExpired:
        error, returncode = f'command exceeded {timeout}s', None
    outputs = {}
    for name, saved in expected.items():
        p = scratch / name
        if not p.exists():
            outputs[name] = {'state': 'missing'}
            # Restore targets for later dependent checks, but never count as reproduced.
            p.write_text(json.dumps(saved))
            continue
        try:
            diff = differences(saved, json.loads(p.read_text()))
            outputs[name] = {'state': 'mismatch' if diff else 'match', 'differences': diff,
                             'regenerated_sha256': sha(p)}
        except (ValueError, TypeError) as e:
            outputs[name] = {'state': 'invalid_json', 'error': str(e)}
    return {'argv': entry['argv'], 'returncode': returncode, 'error': error,
            'seconds': round(time.monotonic() - start, 2), 'outputs': outputs,
            'passed': returncode == 0 and all(x['state'] == 'match' for x in outputs.values())}


def check_receipt(root=ROOT):
    """Read-only freshness check; never recomputes metrics or imports numerical libraries."""
    receipt = json.loads((root / RECEIPT).read_text())
    changed = [p for p, expected in receipt['input_sha256'].items()
               if not (root / p).is_file() or sha(root / p) != expected]
    if not receipt['passed'] or changed:
        raise ValueError(f'Phase 2 reproduction receipt failed or stale; changed inputs: {changed[:12]}')
    print(f"Phase 2 reproduction receipt current: {receipt['n_commands_passed']}/{receipt['n_commands']} commands, "
          f"{receipt['n_outputs_matched']}/{receipt['n_outputs']} outputs; no metrics recomputed")
    return receipt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout', type=int, default=600, help='per command, seconds')
    ap.add_argument('--check', action='store_true', help='read-only saved receipt freshness, no numerical dependencies')
    a = ap.parse_args()
    if a.check:
        check_receipt()
        return 0
    start = datetime.now(timezone.utc).isoformat()
    paths = sorted({p for p in tracked_paths(ROOT) if include(p)} | {Path(__file__).relative_to(ROOT)})
    before = {str(p): sha(ROOT / p) for p in paths}
    receipt = {'started_utc': start, 'kind': 'post-hoc computational reproduction',
               'git_head': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
               'python': sys.version, 'dependencies': {p: importlib.metadata.version(p) for p in ('numpy', 'scipy', 'scikit-learn', 'matplotlib')},
               'exclusions': ['sealed one-time evaluations E99/E112/E113/E115 and locked v1/replication',
                              'active E113/E115 datasets and caches', 'SALT (raw parquet is not tracked)',
                              'historical interim/pilot outputs; no claim of complete Phase 2 coverage'],
               'comparison': 'exact parsed JSON; no tolerance; declared outputs deleted before execution',
               'input_sha256': before, 'commands': []}
    declared = {p for c in CASES for p in c['outputs']}
    with tempfile.TemporaryDirectory(prefix='q22_phase2_', dir='/var/tmp') as tmp:
        scratch = Path(tmp)
        for rel in paths:
            target = scratch / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)
            if sha(target) != before[str(rel)]:
                raise ValueError(f'source changed while copying: {rel}')
        (scratch / 'figures').mkdir(exist_ok=True)
        for entry in CASES:
            result = run_case(scratch, entry, a.timeout)
            receipt['commands'].append(result)
            print(('PASS' if result['passed'] else 'FAIL'), ' '.join(entry['argv']), flush=True)
            if not result['passed']:
                print(json.dumps(result, indent=1), flush=True)
        receipt['scratch_input_changes'] = [p for p, expected in before.items()
                                           if p not in declared and (not (scratch / p).is_file() or sha(scratch / p) != expected)]
    receipt['original_sources_unchanged'] = all((ROOT / p).exists() and sha(ROOT / p) == v for p, v in before.items())
    receipt['n_commands'] = len(receipt['commands'])
    receipt['n_commands_passed'] = sum(x['passed'] for x in receipt['commands'])
    outputs = [x for c in receipt['commands'] for x in c['outputs'].values()]
    receipt['n_outputs'] = len(outputs)
    receipt['n_outputs_matched'] = sum(x['state'] == 'match' for x in outputs)
    receipt['passed'] = (receipt['original_sources_unchanged'] and not receipt['scratch_input_changes']
                         and all(c['passed'] for c in receipt['commands']))
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    dest = ROOT / RECEIPT
    dest.write_text(json.dumps(receipt, indent=1) + '\n')
    print(f"{receipt['n_commands_passed']}/{receipt['n_commands']} commands; {receipt['n_outputs_matched']}/{receipt['n_outputs']} outputs; originals unchanged: {receipt['original_sources_unchanged']}")
    return 0 if receipt['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
