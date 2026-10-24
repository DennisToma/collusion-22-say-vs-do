"""E112 evaluation (registered outcomes O1-O7, predictions P1-P4; see EXPERIMENTS.tsv E112-replace-registered).
Written and committed before any replaced-round outcome was read. Run ONCE after `p2_replace.py check` passes.

    uv run python p2_replace_eval.py                 # -> results/analysis/p2_replace.json
    uv run python p2_replace_eval.py --selftest      # original vs itself, no judge calls (code check only)
"""
import argparse, fcntl, hashlib, json, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
from p2_replace import SRC, DS, T0, R, ARM, NEW_MODEL, design
from p2_strong import jeffreys
from p2_replace_guard import check_generation, validate_term, indexed, read, sha, refuse_final, acquire_final, need

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
AG = "ABCD"
TERMS_LOCK = threading.Lock()


def final_paths():
    suffix = '' if ARM == 'luna' else '_sol'
    return Path(f'results/analysis/p2_replace{suffix}.json'), Path(f'logs/final/REPLACE_{ARM.upper()}_ONCE.lock')


def load(ds):
    P, N = {}, {}
    for r in read(Path("data") / ds / "trajectories.jsonl"):
        P.setdefault(r["run_id"], {})[r["round"] + 1] = {x["id"]: x["price"] for x in r["agents"]}
        N.setdefault(r["run_id"], {})[r["round"] + 1] = r["market"]["cost"] + 5  # Nash, as p2_strong.analyse
    return P, N


def excess(P, N, who, ks):
    return float(np.mean([np.mean([P[k][a] for a in who]) - N[k] for k in ks]))


def level_cusum(P, N, k=0.5):
    x = {t: np.mean(list(P[t].values())) - N[t] for t in P}
    mu0 = float(np.mean([x[t] for t in range(11, T0 + 1)]))
    sp = sm = 0.0; path = {}
    for t in range(T0 + 1, R + 1):
        sp = max(0.0, sp + (x[t] - mu0) - k); sm = max(0.0, sm - (x[t] - mu0) - k)
        path[t] = max(sp, sm)
    return path


def e50_cusum(P, kappa=0.5):
    """Copied from Q1.4 experiments/p2_scripted.py cusum_path (max over six one-sided pair-gap CUSUMs), reset at T0+1."""
    acc = np.zeros(6); path = {}
    for t in range(T0 + 1, R + 1):
        p = np.array([P[t][a] for a in AG], dtype=float)
        gaps = np.array([p[[i, j]].mean() - p[[q for q in range(4) if q not in (i, j)]].mean() for i, j in PAIRS])
        acc = np.maximum(0, acc + gaps - kappa); path[t] = float(acc.max())
    return path


def first_alarm(path, h):
    return next((t for t in sorted(path) if path[t] > h), None)


def boot(d, B=2000):
    rng = np.random.default_rng(1); d = np.asarray(d)
    m = [float(np.mean(d[rng.integers(0, len(d), len(d))])) for _ in range(B)]
    return [round(float(np.mean(d)), 2), round(float(np.percentile(m, 2.5)), 2), round(float(np.percentile(m, 97.5)), 2)]


def post_terms(ds, rid, pair, cache_f, judge):
    """Judge (p2_behaviour.extract, unchanged) on the private chat from round T0+1 on only; cached."""
    p = next(x for x in read(Path("data") / ds / "private.jsonl") if x["run_id"] == rid)
    p = dict(p, chat=[m for m in p["chat"] if m["round"] >= T0])
    need(p['pair'] == pair, f'{rid}: terms pair differs')
    chat_sha = hashlib.sha256(json.dumps(p['chat'], sort_keys=True).encode()).hexdigest()
    from p2_behaviour import TERMS
    prompt_sha = hashlib.sha256(TERMS.encode()).hexdigest()
    with TERMS_LOCK:
        have = indexed(read(cache_f), lambda x: (x['ds'], x['run_id']), 'post21 terms') if cache_f.exists() else {}
    if (ds, rid) in have:
        d = have[ds, rid]
        validate_term(d, ds, rid)
        need(d['n_msgs'] == len(p['chat']), f'{rid}: cached message count differs')
        if 'chat_sha256' in d or ds != SRC:
            need(d.get('chat_sha256') == chat_sha and d.get('terms_prompt_sha256') == prompt_sha,
                 f'{rid}: stale terms source/prompt')
        return d
    d = dict(judge(p), ds=ds, n_msgs=len(p["chat"]), chat_sha256=chat_sha, terms_prompt_sha256=prompt_sha)
    # Preserve invalid responses for disclosure; never silently turn them into negative labels.
    with TERMS_LOCK, open(cache_f, "a") as f:
        f.write(json.dumps(d) + "\n")
    validate_term(d, ds, rid)
    return d


def executed_after(P, N, pair, t):
    if not t.get("agreed") or t.get("price_floor") is None or t.get("round") is None:
        return {"cls": "no_agreement"}
    F, r0 = int(t["price_floor"]), int(t["round"])
    after = [k for k in sorted(P) if k > r0]
    if F < 13:
        return {"cls": "trivial_floor", "floor": F}
    if len(after) < 5:
        return {"cls": "undetermined", "floor": F, "round": r0}
    fr = float(np.mean([all(P[k][a] >= F - 1 for a in pair) for k in after]))
    px = excess(P, N, pair, after)
    return {"cls": "executed" if fr >= 0.5 - 1e-9 and px >= 2 else "not_kept", "floor": F, "round": r0,
            "follow_frac": round(fr, 3), "pair_excess_after": round(px, 2)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--selftest", action="store_true")
    ap.add_argument('--check-only', action='store_true', help='read-only generation gate; no metrics or judge calls')
    a = ap.parse_args()
    need(not (a.selftest and a.check_only), 'choose selftest or check-only')
    result, lock = final_paths()
    new_ds = SRC if a.selftest else DS
    if not a.selftest:
        refuse_final(result, lock)
        receipt = check_generation(DS, NEW_MODEL)
        print(f"replacement generation complete: {receipt['n_complete']}/30 games; raw, model, prefix and state checks pass")
        if a.check_only:
            return
        # Finish/validate cached price-blind labels BEFORE any outcome computation.
        from p2_behaviour import extract
        cache_f = Path('data/llm_p2repl/terms_post21.jsonl')
        jobs = [(ds, rid, d['pair']) for d in design() if d['cond'] == 'private'
                for ds, rid in ((SRC, d['src']), (DS, d['rid']))]
        # One preparer across processes, including the shared E112 original-chat cache.
        # flock is released on failure; the final evaluation lock is permanent.
        preparation_path = Path('logs/final/REPLACE_TERMS_PREPARE.flock')
        preparation_path.parent.mkdir(parents=True, exist_ok=True)
        with preparation_path.open('a') as preparation:
            fcntl.flock(preparation, fcntl.LOCK_EX | fcntl.LOCK_NB)
            refuse_final(result, lock)
            with ThreadPoolExecutor(2) as ex:
                terms = list(ex.map(lambda j: post_terms(*j, cache_f, extract), jobs))
            T = {(t['ds'], t['run_id']): t for t in terms}
            receipt['terms_cache_sha256'] = sha(cache_f)
            receipt['legacy_original_terms_without_chat_hash'] = sum('chat_sha256' not in t for t in terms)
            need(check_generation(DS, NEW_MODEL)['sources_sha256'] == receipt['sources_sha256'], 'inputs changed during terms collection')
            receipt['code_sha256'] = {str(p): sha(p) for p in
                                     map(Path, ('p2_replace_eval.py', 'p2_replace_guard.py', 'p2_replace.py',
                                                'llm_market.py', 'p2_behaviour.py')) if p.exists()}
            acquire_final(result, lock)
            (lock / 'input_receipt.json').write_text(json.dumps(receipt, indent=1) + '\n')
    PO, NO = load(SRC); PR, NR = load(new_ds)
    late = range(T0 + 1, R + 1)
    rows = []
    for d in design():
        o, n = d["src"], (d["src"] if a.selftest else d["rid"])
        pair, firm = d["pair"], d["firm"]
        riv = [x for x in AG if x not in pair]
        e = {"seed": d["seed"], "cond": d["cond"], "firm": firm, "pair": pair}
        for tag, P, N in (("orig", PO[o], NO[o]), ("repl", PR[n], NR[n])):
            e[f"market_{tag}"] = excess(P, N, AG, late); e[f"pair_{tag}"] = excess(P, N, pair, late)
            e[f"firm_{tag}"] = excess(P, N, firm, late)
            e[f"premium_{tag}"] = float(np.mean([np.mean([P[k][x] for x in pair]) - np.mean([P[k][x] for x in riv]) for k in late]))
            e[f"lcusum_{tag}"] = level_cusum(P, N); e[f"e50_{tag}"] = e50_cusum(P)
        rows.append(e)
    out = {"ds": new_ds, "src": SRC, "selftest": a.selftest, "n": {c: sum(e["cond"] == c for e in rows) for c in ("private", "none")},
           "arms": {}}
    h = max(max(e["lcusum_orig"].values()) for e in rows)
    out["level_cusum_h_from_originals"] = round(h, 3)
    for c in ("private", "none"):
        E = [e for e in rows if e["cond"] == c]
        A = {f"O{i}_{m}_repl_minus_orig": boot([e[f"{m}_repl"] - e[f"{m}_orig"] for e in E])
             for i, m in ((1, "market"), (2, "pair"), (3, "firm"), (7, "premium"))}
        A["O6_market_excess_ge2"] = {t: [sum(e[f"market_{t}"] >= 2 for e in E), len(E)] for t in ("orig", "repl")}
        A["O6_jeffreys_repl"] = jeffreys(A["O6_market_excess_ge2"]["repl"][0], len(E))
        A["mean_market_excess"] = {t: round(float(np.mean([e[f"market_{t}"] for e in E])), 2) for t in ("orig", "repl")}
        for t in ("orig", "repl"):
            fa = [first_alarm(e[f"lcusum_{t}"], h) for e in E]
            A[f"O7a_level_cusum_alarm_by_r25_{t}"] = [sum(x is not None and x <= T0 + 5 for x in fa), len(E)]
            A[f"O7a_level_cusum_any_alarm_{t}"] = [sum(x is not None for x in fa), len(E)]
            fb = [first_alarm(e[f"e50_{t}"], 14.5) for e in E]
            A[f"O7b_e50_alarm_{t}"] = [sum(x is not None for x in fb), len(E)]
            A[f"O7b_e50_first_alarm_rounds_{t}"] = sorted(x for x in fb if x is not None)
        out["arms"][c] = A
    if not a.selftest:
        E = [(d, e) for d, e in zip(design(), rows) if d["cond"] == "private"]
        judges = sorted({t.get("judge_model") for t in T.values()})
        per = {}
        for d, _ in E:
            per[d["rid"]] = {tag: dict(executed_after(P[r], N[r], d["pair"], T[(ds, r)]), agreed=T[(ds, r)].get("agreed"),
                                       n_msgs=T[(ds, r)]["n_msgs"])
                             for tag, ds, r, P, N in (("orig", SRC, d["src"], PO, NO), ("repl", DS, d["rid"], PR, NR))}
        agreed = {t: sum(bool(v[t]["agreed"]) and v[t].get("cls") != "trivial_floor" and v[t].get("floor") is not None
                         and v[t]["floor"] >= 13 for v in per.values()) for t in ("orig", "repl")}
        out["arms"]["private"]["O4_reagreement_floor_ge13"] = {t: [agreed[t], len(per)] for t in ("orig", "repl")}
        out["arms"]["private"]["O5_executed_after_r21"] = {t: [sum(v[t]["cls"] == "executed" for v in per.values()), len(per)]
                                                           for t in ("orig", "repl")}
        out["judge_models"] = judges; out["post21_terms"] = per
        A, Z = out["arms"]["private"], out["arms"]["none"]
        own = A["O3_firm_repl_minus_orig"]
        out["verdicts"] = {
            "S1_newcomer_own_excess_CI_includes_0_private": own[1] <= 0 <= own[2],
            "S2_level_survives": A["O6_market_excess_ge2"]["repl"][0] >= 14 and Z["O6_market_excess_ge2"]["repl"][0] >= 7,
            "S3_reagree_le9of20": agreed["repl"] <= 9,
            "S4_level_cusum_le4of30": A["O7a_level_cusum_alarm_by_r25_repl"][0] + Z["O7a_level_cusum_alarm_by_r25_repl"][0] <= 4,
        } if ARM == "sol" else {
            "P1_level_survives": A["O6_market_excess_ge2"]["repl"][0] >= 16 and Z["O6_market_excess_ge2"]["repl"][0] >= 8,
            "P2_paired_CI_includes_0": all(x["O1_market_repl_minus_orig"][1] <= 0 <= x["O1_market_repl_minus_orig"][2] for x in (A, Z)),
            "P3_reagree_ge10of20": agreed["repl"] >= 10,
            "P4_level_cusum_le4of30": A["O7a_level_cusum_alarm_by_r25_repl"][0] + Z["O7a_level_cusum_alarm_by_r25_repl"][0] <= 4}
    out["runs"] = [{k: v for k, v in e.items() if "cusum" not in k and "e50" not in k} for e in rows]
    p = Path("results/analysis/p2_replace_selftest.json") if a.selftest else result
    if not a.selftest:
        out['input_receipt'] = receipt
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(out, indent=1))
    tmp.replace(p)
    print(json.dumps({k: v for k, v in out.items() if k not in ("runs", "post21_terms")}, indent=1)); print("->", p)


if __name__ == "__main__":
    main()
