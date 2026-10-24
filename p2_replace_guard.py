"""E115 completion safeguards; no outcomes, thresholds, prompts or estimators live here.

Validation is read-only. Partial checks inspect only ground-truth-complete games, since
trajectory/private rows are appended before ground truth by the live generator.
"""
import hashlib
import json
import random
from pathlib import Path

AG = list('ABCD')
SRC = 'llm_p2strongF'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path, live=False):
    lines = path.read_bytes().splitlines(keepends=True)
    if live and lines and not lines[-1].endswith(b'\n'):
        lines.pop()
    return [json.loads(x) for x in lines]


def indexed(rows, key, label):
    out = {}
    for row in rows:
        k = key(row)
        if k in out:
            raise ValueError(f'{label}: duplicate {k}')
        out[k] = row
    return out


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check_generation(ds, newcomer, complete=True):
    """Check raw provenance and exact design, without printing any price or label."""
    want = {f'{ds}_{i:04d}' for i in range(40) if i % 2 == 0 or i < 20}
    D, O = Path('data') / ds, Path('data') / SRC
    source_gt = indexed(read(O / 'ground_truth.jsonl'), lambda x: x['run_id'], 'source ground truth')
    need(set(source_gt) == {f'{SRC}_{i:04d}' for i in range(40)}, 'source must contain exactly 40 registered games')
    gts = indexed(read(D / 'ground_truth.jsonl', live=not complete), lambda x: x['run_id'], 'replacement ground truth')
    need(set(gts) == want if complete else set(gts) <= want,
         f'{ds}: need exactly 30 registered games (have {len(gts)})' if complete else f'{ds}: unexpected game')
    receipt = {'ds': ds, 'complete': complete, 'n_complete': len(gts), 'sources_sha256': {},
               'reconstructed_decisions': {}, 'reconstruction_caveat':
               'Reconstructed rows check saved-field consistency only; their model/parse metadata are inferred, not independently authenticated.'}
    bundles = {}
    for name, path in ((SRC, O), (ds, D)):
        live = name == ds and not complete
        paths = [path / n for n in ('ground_truth.jsonl', 'trajectories.jsonl', 'private.jsonl')]
        records = indexed(read(paths[1], live), lambda x: (x['run_id'], x['round']), f'{name} trajectory')
        private = indexed(read(paths[2], live), lambda x: x['run_id'], f'{name} private')
        if complete or name == SRC:
            cohort = set(source_gt) if name == SRC else want
            need(set(records) == {(r, t) for r in cohort for t in range(40)}, f'{name}: exact round coverage')
            need(set(private) == cohort, f'{name}: exact private coverage')
        bundles[name] = records, private
        receipt['sources_sha256'].update({str(p): sha(p) for p in paths})
    for rid, g in sorted(gts.items()):
        i = int(rid.rsplit('_', 1)[1]); seed = 9800000 + i // 2
        src = f'{SRC}_{i:04d}'; pair = sorted(random.Random(seed).sample(AG, 2))
        cond = 'private' if i % 2 == 0 else 'none'
        firm = random.Random(seed * 7 + 1).choice(pair if cond == 'private' else AG)
        for name, run, meta in ((SRC, src, source_gt[src]), (ds, rid, g)):
            need(meta['seed'] == seed and meta['condition'] == cond and meta['assigned_pair'] == pair,
                 f'{run}: registered seed/condition/pair mismatch')
            need(meta.get('rounds') == 40 and meta.get('framing') == 'strong' and meta.get('sysvar') == 0
                 and meta.get('backend') == 'codex' and meta.get('lang', 'en') == 'en', f'{run}: generator metadata')
            need(meta.get('private_channel_enabled') is (cond == 'private'), f'{run}: private channel metadata')
            expected_models = {'gpt-6-luna', newcomer} if name == ds else {'gpt-6-luna'}
            need(set(meta['model'].split(',')) == expected_models, f'{run}: model metadata/fallback')
            if name == ds:
                repl = meta.get('replaced', {})
                need(repl.get('round0') == 20 and repl.get('firm') == firm and
                     repl.get('model', 'gpt-6-luna') == newcomer, f'{run}: replacement metadata')
            records, private = bundles[name]
            need(run in private and private[run]['pair'] == pair, f'{run}: missing private record/pair')
            raw_path = Path('data') / name / 'raw' / f'{run}.jsonl'
            raw_lines = raw_path.read_text().splitlines()
            raw = indexed([json.loads(x) for x in raw_lines], lambda x: x['key'], f'{run} raw')
            need(set(raw) == {f'{t}:{a}' for t in range(40) for a in AG}, f'{run}: raw round/firm coverage')
            reconstructed = sorted(k for k, row in raw.items() if row.get('reconstructed'))
            if reconstructed:
                need(name == 'llm_p2replS' and run == 'llm_p2replS_0014' and
                     reconstructed == [f'39:{a}' for a in AG], f'{run}: undeclared raw reconstruction')
                receipt['reconstructed_decisions'][run] = reconstructed
            receipt['sources_sha256'][str(raw_path)] = sha(raw_path)
            chat = []
            for t in range(40):
                need((run, t) in records, f'{run}: missing trajectory round {t}')
                row = records[run, t]
                need(sorted(a['id'] for a in row['agents']) == AG, f'{run}: firm coverage')
                for a in row['agents']:
                    dec = raw[f"{t}:{a['id']}"]
                    model = newcomer if name == ds and t >= 20 and a['id'] == firm else 'gpt-6-luna'
                    need(dec.get('model') == model and dec.get('backend') == 'codex', f'{run}: per-decision model/fallback')
                    need(type(dec.get('parse_ok')) is bool, f'{run}: missing parse status')
                    need(type(dec.get('price')) is int and 6 <= dec['price'] <= 30 and a['price'] == dec['price'],
                         f'{run}: raw price differs')
                    need(a.get('public_message', '') == str(dec.get('public_message') or '').strip(), f'{run}: raw public message differs')
                if cond == 'private':
                    for a in pair:
                        msg = str(raw[f'{t}:{a}'].get('private_message') or '').strip()
                        if msg:
                            chat.append({'round': t, 'from': a, 'to': next(b for b in pair if b != a), 'text': msg})
            need(private[run]['chat'] == chat, f'{run}: raw private chat differs')
            plans = {k: v['plan'] for k, v in raw.items() if v.get('plan')}
            need(private[run].get('plans', {}) == plans, f'{run}: raw private plans differ')
            need(meta.get('parse_failures') == sum(not x['parse_ok'] for x in raw.values()), f'{run}: parse failure count')
            if name == SRC:
                original_lines = raw_lines
            else:
                need(raw_lines[:80] == original_lines[:80], f'{run}: raw prefix differs')
                for t in range(40):
                    original = bundles[SRC][0][src, t]
                    need(records[run, t]['market'] == original['market'], f'{run}: exogenous market path differs')
                    if t < 20:
                        need({k: v for k, v in records[run, t].items() if k != 'run_id'} ==
                             {k: v for k, v in original.items() if k != 'run_id'}, f'{run}: trajectory prefix differs')
    return receipt


def validate_term(row, ds, rid):
    need(row.get('ds') == ds and row.get('run_id') == rid, f'{rid}: terms identity')
    need(row.get('judge_model') == 'gpt-6.1-sol', f'{rid}: terms judge fallback')
    need(type(row.get('agreed')) is bool, f'{rid}: unparsed agreement')
    if row['agreed']:
        need(type(row.get('price_floor')) is int and 6 <= row['price_floor'] <= 30, f'{rid}: invalid floor')
        need(type(row.get('round')) is int and 21 <= row['round'] <= 40, f'{rid}: invalid agreement round')
    need(type(row.get('n_msgs')) is int and row['n_msgs'] >= 0, f'{rid}: missing message count')


def refuse_final(result, lock):
    need(not result.exists() and not lock.exists(), 'replacement final result or evaluation lock exists; refusing rerun')


def acquire_final(result, lock):
    refuse_final(result, lock)
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.mkdir()  # exclusive; retained on any failure after evaluation begins
