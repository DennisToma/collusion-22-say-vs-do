"""E133 (registered 2026-10-25 02:32, ledger row E133-reg, before computing): does early PRIVATE talk forecast late execution?

Zero LLM calls. Primary set: Q1.4's E70 grid channel games with a judged agreement (Q1.4 judge file, read-only; sibling
trajectories pinned by data/ext_llm_grid_p2/SHA256SUMS). Outcome late_exec = Q1.4 E70 executed rule restricted to the late
window (rounds 10-19, 0-indexed): both pair firms >= agreed-1 in >= 1/2 of those rounds AND pair mean - Nash >= 2.
Predictors use rounds -1..5 only (gap 6-9). (b) action-only: pair markup and pair price SD; (a) say-do: share of private
messages stating a price, mean |price - last privately stated price|, share with defection/renegotiation words (frozen RX).
Primary estimand: AUROC(a+b) - AUROC(b), leave-one-cell-out logistic, game bootstrap of out-of-fold scores.
Secondary (never pooled): strongF private arm, own strict class (full-game label), leave-one-out.

  uv run python p2_e133_privileged.py   # -> results/analysis/e133_privileged.json
"""
import hashlib, json, re
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from p2_cue import auc, boot_auc
from p2_e1_audit import SIB

OUTF = Path("results/analysis/e133_privileged.json")
NASH = {6: 10, 8: 12}  # Q1.4 experiments/llm_eval.py
PRICE_RX = re.compile(r"(?<!round )(?<!rounds )\$?\b(\d{1,2}(?:\.\d+)?)\b", re.I)
DEFECT_RX = re.compile(r"\b(undercut\w*|defect\w*|cheat\w*|deviat\w*|renegotiat\w*|betray\w*|punish\w*|retaliat\w*|broke|"
                       r"break\w*|lower\w*|cut\w*|drop\w*)\b", re.I)
A_FEATS, B_FEATS = ["say_price_share", "say_do_gap", "defect_share"], ["markup_0_5", "pair_sd_0_5"]


def stated(msg):
    v = [float(m) for m in PRICE_RX.findall(msg or "") if 5 <= float(m) <= 40]
    return v[-1] if v else None


def feats(msgs, prices, pair, nash, early):
    """msgs: list of (t_eff, sender, text) where t_eff = last round whose price the message can precede (sent before
    pricing round t_eff+1); prices: {round: {id: price}}; early: pricing rounds used (0..5)."""
    em = [m for m in msgs if m[0] <= early[-1]]
    say = [stated(m[2]) for m in em]
    gaps = []
    for a in pair:
        for t in early:
            prior = [stated(m[2]) for m in msgs if m[1] == a and m[0] < t and stated(m[2]) is not None]
            if prior:
                gaps.append(abs(prices[t][a] - prior[-1]))
    pp = [prices[t][a] for t in early for a in pair]
    return {"say_price_share": float(np.mean([s is not None for s in say])) if em else 0.0,
            "say_do_gap": float(np.mean(gaps)) if gaps else None,
            "defect_share": float(np.mean([bool(DEFECT_RX.search(m[2])) for m in em])) if em else 0.0,
            "markup_0_5": float(np.mean(pp) - np.mean([nash[t] for t in early])),
            "pair_sd_0_5": float(np.std(pp))}


def grid_rows():
    sums = dict(reversed(l.split()) for l in open("data/ext_llm_grid_p2/SHA256SUMS"))
    rows, hashes = [], {}
    for i in range(16):
        name = f"llm_grid_p2_c{i:02d}"; d = SIB / "data" / name
        raw = (d / "trajectories.jsonl").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sums[f"{name}/trajectories.jsonl"], name
        jp = SIB / "results/llm_judge" / f"{name}.jsonl"
        hashes[name] = hashlib.sha256(jp.read_bytes()).hexdigest()
        lab = {j["run_id"]: j for j in map(json.loads, open(jp))}
        traj = {}
        for r in map(json.loads, raw.decode().splitlines()):
            traj.setdefault(r["run_id"], []).append(r)
        for g in map(json.loads, open(d / "ground_truth.jsonl")):
            rid = g["run_id"]
            if not g.get("private_channel_enabled") or rid not in traj:
                continue
            lb = lab.get(rid)
            if lb is None or lb.get("agreement") != "yes" or lb.get("agreed_price") is None:
                continue
            rs = sorted(traj[rid], key=lambda r: r["round"])
            if len(rs) != 20:
                continue
            prices = {r["round"]: {a["id"]: a["price"] for a in r["agents"]} for r in rs}
            nash = {r["round"]: NASH[r["market"]["cost"]] for r in rs}
            pair = g["assigned_pair"]
            # round -1 chat precedes round 0; a round-t private_message accompanies price t (precedes t+1)
            msgs = [(-1, m["sender"], m["private_message"]) for m in g.get("private_chat", []) if m["round"] == -1]
            msgs += [(r["round"], a["id"], a.get("private_message") or "") for r in rs for a in r["agents"]
                     if a["id"] in pair and (a.get("private_message") or "").strip()]
            x = feats(msgs, prices, pair, nash, list(range(6)))
            late = range(10, 20); ap = lb["agreed_price"]
            held = np.mean([all(prices[t][a] >= ap - 1 for a in pair) for t in late]) >= .5
            lvl = np.mean([prices[t][a] for t in late for a in pair]) - np.mean([nash[t] for t in late])
            x.update(run_id=rid, cell=f"c{i:02d}", y=int(bool(held and lvl >= 2)),
                     defect_any=bool(any(DEFECT_RX.search(m[2]) for m in msgs)))
            rows.append(x)
    return rows, hashes


def strongF_rows():
    D = Path("data/llm_p2strongF")
    cls = json.loads(Path("results/analysis/p2_strong_classes_llm_p2strongF.json").read_text())["runs"]
    gt = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))}
    chat = {p["run_id"]: p["chat"] for p in map(json.loads, open(D / "private.jsonl"))}
    P, N = {}, {}
    for r in map(json.loads, open(D / "trajectories.jsonl")):
        P.setdefault(r["run_id"], {})[r["round"]] = {a["id"]: a["price"] for a in r["agents"]}
        N.setdefault(r["run_id"], {})[r["round"]] = r["market"]["cost"] + 5
    rows = []
    for rid, c in sorted(cls.items()):
        if c["cond"] != "private":
            continue
        pair = gt[rid]["assigned_pair"]
        # strongF chat at round t is sent BEFORE pricing round t -> same timing as grid message at t-1
        msgs = [(m["round"] - 1, m["from"], m["text"]) for m in chat.get(rid, []) if m["from"] in pair]
        x = feats(msgs, P[rid], pair, N[rid], list(range(6)))
        x.update(run_id=rid, cell=rid, y=int(c["class"] == "executed"), defect_any=bool(any(DEFECT_RX.search(m[2]) for m in msgs)))
        rows.append(x)
    return rows


def oof(rows, cols):
    X = np.array([[r[c] for c in cols] for r in rows], float); y = np.array([r["y"] for r in rows])
    g = np.array([r["cell"] for r in rows]); s = np.zeros(len(rows))
    for c in np.unique(g):
        te, tr = g == c, g != c
        Xtr, Xte = X[tr].copy(), X[te].copy()
        med = np.nanmedian(Xtr, 0); Xtr = np.where(np.isnan(Xtr), med, Xtr); Xte = np.where(np.isnan(Xte), med, Xte)
        mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
        m = LogisticRegression(C=1.0).fit((Xtr - mu) / sd, y[tr])
        s[te] = m.decision_function((Xte - mu) / sd)
    return s


def analyse(rows, B=2000, seed=0):
    for r in rows:
        if r["say_do_gap"] is None:
            r["say_do_gap"] = np.nan
    y = np.array([r["y"] for r in rows])
    sb, sab = oof(rows, B_FEATS), oof(rows, B_FEATS + A_FEATS)
    sa = oof(rows, A_FEATS)
    A = lambda s, idx: auc(list(s[idx][y[idx] == 0]), list(s[idx][y[idx] == 1]))
    rng = np.random.default_rng(seed); n = len(rows); bs = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        if 0 < y[i].sum() < n:
            bs.append(A(sab, i) - A(sb, i))
    allidx = np.arange(n)
    out = {"n": n, "n_pos": int(y.sum()), "n_neg": int(n - y.sum()),
           "auroc_b": round(A(sb, allidx), 3), "auroc_a": round(A(sa, allidx), 3), "auroc_ab": round(A(sab, allidx), 3),
           "delta_ab_minus_b": [round(A(sab, allidx) - A(sb, allidx), 3), round(float(np.percentile(bs, 2.5)), 3),
                                round(float(np.percentile(bs, 97.5)), 3)],
           "single_feature_auroc": {}, "say_do_gap_missing": int(sum(np.isnan(r["say_do_gap"]) for r in rows)),
           "defect_talk_any_round": {"held": [sum(r["defect_any"] for r in rows if r["y"]), int(y.sum())],
                                     "not_held": [sum(r["defect_any"] for r in rows if not r["y"]), int(n - y.sum())]},
           "means": {f: {"held": round(float(np.nanmean([r[f] for r in rows if r["y"]])), 3),
                         "not_held": round(float(np.nanmean([r[f] for r in rows if not r["y"]])), 3)} for f in A_FEATS + B_FEATS}}
    for f in A_FEATS + B_FEATS:
        v = [(r[f], r["y"]) for r in rows if not np.isnan(r[f])]
        out["single_feature_auroc"][f] = boot_auc([a for a, b in v if not b], [a for a, b in v if b])
    return out


def main():
    rows, hashes = grid_rows()
    res = {"registration": "EXPERIMENTS.tsv E133-reg (2026-10-25 02:32, before computing)", "llm_calls": 0,
           "part_c_llm_view": "skipped (kept zero-call)", "judge_label_sha256": hashes,
           "price_rx": PRICE_RX.pattern, "defect_rx": DEFECT_RX.pattern,
           "primary_e70_grid_late_exec": analyse(rows)}
    ex = {g["run_id"]: g["executed"] for g in json.loads(Path("data/ext_llm_grid_p2_e70/e70_grid.json").read_text())["games"]}
    res["primary_e70_grid_late_exec"]["defect_talk_any_round_q14_e70_rule"] = {  # descriptive, Q1.4's own executed label
        "executed": [sum(r["defect_any"] for r in rows if ex[r["run_id"]]), sum(bool(ex[r["run_id"]]) for r in rows)],
        "agreed_not_executed": [sum(r["defect_any"] for r in rows if not ex[r["run_id"]]), sum(not ex[r["run_id"]] for r in rows)],
        "note": "4 further Q1.4 agreed-not-held games have agreement=yes but no agreed_price (no late outcome definable): excluded"}
    sf = strongF_rows()
    res["secondary_strongF_strict_class"] = analyse(sf)
    res["secondary_strongF_strict_class"]["note"] = "full-game strict label (overlaps rounds 0-5: partial leakage into (b)); LOO CV"
    OUTF.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "judge_label_sha256"}, indent=1))


if __name__ == "__main__":
    main()
