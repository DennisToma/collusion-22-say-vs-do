"""E133e (post hoc robustness, declared before computing: ledger row E133e-reg; DIRECTION 04:15 #1). Zero LLM calls.

Like-for-like attribution of the E133c/E133d LLM forecast. Same population/outcome as p2_e133_privileged.py (n=78,
frozen label SHAs); scores are the saved E133 features and the cached e133c/e133d p_kept values.
 (a) registered single features re-read with direction pre-specified "smaller = held" (registered numbers unchanged);
 (b) raw, unfitted scores vs the no-chat LLM (E133d), paired game bootstrap: -pair_sd_0_5, -say_do_gap,
     early_minus_agreed (post hoc in e133c), and a rule score fixed at registration = share of rounds 0-5 with both pair
     firms >= agreed-1 (judge-label agreed price), tie-broken by pair mean r0-5 minus (Nash+2);
 (c) AUROC of E133d and the rule score in games with >=1 public post in rounds 0-5 vs none;
 (d) leave-cell-out logistic on the rule score alone (cost of CV fitting at n=78).

  uv run python p2_e133e_attr.py   # -> results/analysis/e133e_attr.json
"""
import json
from pathlib import Path
import numpy as np
import p2_e133_privileged as E
from p2_e133c_llm import games

OUTF = Path("results/analysis/e133e_attr.json")
rows, hashes = E.grid_rows()
G = games({r["run_id"] for r in rows})
lab = {}
for i in range(16):
    lab.update({j["run_id"]: j for j in map(json.loads, open(E.SIB / "results/llm_judge" / f"llm_grid_p2_c{i:02d}.jsonl"))})
C = {m: {j["run_id"]: j for j in map(json.loads, open(f"results/llm_auditor/e133c/gpt-6.1-sol_{m}.jsonl"))}
     for m in ("privileged", "noprivate")}
for r in rows:
    g = G[r["run_id"]]; ap = lab[r["run_id"]]["agreed_price"]
    P = {x["round"]: {a["id"]: a["price"] for a in x["agents"]} for x in g["rows"]}
    nash = {x["round"]: E.NASH[x["market"]["cost"]] for x in g["rows"]}
    share = float(np.mean([all(P[t][a] >= ap - 1 for a in g["pair"]) for t in range(6)]))
    margin = float(np.mean([P[t][a] for t in range(6) for a in g["pair"]]) - np.mean([nash[t] + 2 for t in range(6)]))
    assert abs(margin) < 100
    r["rule"] = share * 1000 + margin  # lexicographic: share first, margin breaks ties
    r["early_minus_agreed"] = float(np.mean([P[t][a] for t in range(6) for a in g["pair"]]) - ap)
    r["public"] = any((a.get("public_message") or "").strip() for x in g["rows"][:6] for a in x["agents"])
    r["llm_d"] = C["noprivate"][r["run_id"]]["p_kept"]; r["llm_c"] = C["privileged"][r["run_id"]]["p_kept"]
    if r["say_do_gap"] is None:
        r["say_do_gap"] = np.nan
assert len(rows) == 78 and all(C[m][r["run_id"]]["model"] == "gpt-6.1-sol" for m in C for r in rows)
y = np.array([r["y"] for r in rows]); n = len(y)
col = lambda f, s=1: s * np.array([r[f] for r in rows], float)
A = lambda s, idx: E.auc(list(s[idx][y[idx] == 0]), list(s[idx][y[idx] == 1]))
ci = lambda pt, bs: [round(pt, 3), round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)]

out = {"registration": "EXPERIMENTS.tsv E133e-reg (post hoc robustness, declared before computing)", "llm_calls": 0,
       "n": n, "n_pos": int(y.sum()), "n_neg": int(n - y.sum()), "judge_label_sha256": hashes}
# (a) orientation: smaller = held
out["a_oriented_auroc_smaller_is_held"] = {f: E.boot_auc([-r[f] for r in rows if not r["y"] and not np.isnan(r[f])],
                                                         [-r[f] for r in rows if r["y"] and not np.isnan(r[f])])
                                           for f in ("say_do_gap", "defect_share", "pair_sd_0_5")}
# (b) raw scores vs E133d, paired game bootstrap
RAW = {"neg_pair_sd_0_5": col("pair_sd_0_5", -1), "neg_say_do_gap": col("say_do_gap", -1),
       "early_minus_agreed": col("early_minus_agreed"), "rule_score": col("rule")}
assert not any(np.isnan(v).any() for v in RAW.values())
S = dict(RAW, llm_E133d=col("llm_d"), llm_E133c=col("llm_c"))
al = np.arange(n)
rng = np.random.default_rng(0); bs = {k: [] for k in RAW}; bsc = []
for _ in range(2000):
    i = rng.integers(0, n, n)
    if 0 < y[i].sum() < n:
        for k in RAW:
            bs[k].append(A(S["llm_E133d"], i) - A(RAW[k], i))
best = max(RAW, key=lambda k: A(RAW[k], al))
out["b_raw_auroc"] = {k: E.boot_auc(list(v[y == 0]), list(v[y == 1])) for k, v in S.items()}
out["b_llm_E133d_minus_raw"] = {k: ci(A(S["llm_E133d"], al) - A(RAW[k], al), bs[k]) for k in RAW}
out["b_best_raw"] = best
# (c) public-message strata
pub = np.array([r["public"] for r in rows])
out["c_public_strata"] = {}
for name, m in (("public_posts_r0_5", pub), ("no_public_posts_r0_5", ~pub)):
    idx = np.where(m)[0]
    out["c_public_strata"][name] = {"n": int(m.sum()), "n_pos": int(y[m].sum()),
                                    **{k: E.boot_auc(list(S[k][idx][y[idx] == 0]), list(S[k][idx][y[idx] == 1]))
                                       for k in ("llm_E133d", "llm_E133c", "rule_score", best)}}
# paired difference of (E133d - best raw) between strata
rng = np.random.default_rng(2); dd = []
ip, inp = np.where(pub)[0], np.where(~pub)[0]
for _ in range(2000):
    a, b = rng.choice(ip, len(ip)), rng.choice(inp, len(inp))
    if 0 < y[a].sum() < len(a) and 0 < y[b].sum() < len(b):
        dd.append(A(S["llm_E133d"], a) - A(S["llm_E133d"], b))
out["c_llm_E133d_public_minus_nopublic"] = ci(A(S["llm_E133d"], ip) - A(S["llm_E133d"], inp), dd)
# (d) CV cost: leave-cell-out logistic on the rule score alone
for r in rows:
    r["rule_z"] = r["rule"]
so = E.oof(rows, ["rule_z"])
out["d_rule_score_leave_cell_out_logistic_auroc"] = round(A(so, al), 3)
out["d_rule_score_raw_auroc"] = round(A(RAW["rule_score"], al), 3)
out["d_registered_b_oof_for_reference"] = 0.816
OUTF.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: v for k, v in out.items() if k != "judge_label_sha256"}, indent=1))
