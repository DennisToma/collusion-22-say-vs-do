"""Claims x denominators table for the REPORT.md abstract (offline; stdlib only; no LLM calls).

For each numeric abstract claim: load the saved json, extract the value by an explicit key path, round as the
abstract does (half-up), assert it equals the number text hard-coded here, check that text also appears in the
REPORT.md Abstract/TL;DR, and record the denominator (units, split, registered vs exploratory). A claim whose json
or key is absent is recorded as NO_SOURCE (not a failure, never invented). Exit 1 on any MISMATCH.

    python3 p2_claims.py            # writes results/analysis/claims_denominators.{json,md}
"""
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
A = "results/analysis/"
OUT = ROOT / A / "claims_denominators"


def r(x, nd=2, sign=False):
    q = Decimal(str(round(float(x), 8))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    s = f"{q:+f}" if sign else f"{q:f}"
    return s.replace("-0.00", "+0.00" if sign else "0.00")


def ci(v, sign=True):
    return f"{r(v[0], 2, False if v[0] == 0 else sign)} [{r(v[1], 2, sign)}, {r(v[2], 2, sign)}]"


def dci(c):  # {"delta":..,"ci":[lo,hi]}
    return ci([c["delta"], *c["ci"]])


def pick(src, path):
    """Load json `src` (repo-relative) and follow `path` (tuple of keys/indices)."""
    obj = json.loads((ROOT / src).read_text())
    for k in path:
        obj = obj[k]
    return obj


def norm(t):
    return re.sub(r"\s+", " ", t.replace("−", "-"))


def abstract_text():
    t = (ROOT / "REPORT.md").read_text()
    return norm(t[t.index("## Abstract"):t.index("*Joint statement")])


CLAIMS = []


def claim(cid, text, expected, snippet, denom, status_note=""):
    def deco(fn):
        CLAIMS.append(dict(id=cid, claim=text, expected=expected, snippet=snippet, denominator=denom,
                           note=status_note, fn=fn))
        return fn
    return deco


FINAL = A + "final_llm_v3_gpt-6.1-sol_test.json"
POOL = A + "p2_pool_rep.json"
REPJ = A + "replication_llm_p2rep.json"
CUE = A + "p2_cue_llm_p2cue.json"
ASYM = A + "p2_asym.json"
FAM = A + "p2_family3way.json"
SALT = A + "salt_d1.json"
BEH = A + "p2_behaviour.json"
CLS = A + "p2_strong_classes_llm_p2strongF.json"
EVAL = A + "p2_strong_eval_llm_p2strongF.json"
KEY = A + "p2_plan_keyword_llm_p2strongF.json"
REPORTJ = A + "p2_strongF_report_llm_p2strongF.json"
QWEN = A + "p2_qwen_cmp.json"
QEVAL = A + "p2_strong_eval_llm_p2qwen{}.json"


@claim("C01", "combined minus better single view, run-AUROC, locked test", "-0.01 [-0.09, +0.06]",
       "-0.01 [-0.09, +0.06]", "n=95 runs (llm_v3 locked test split of 125 runs); registered primary contrast")
def _():
    k = ("contrasts", "delta_hybrid[combined]:run_auroc")
    d = pick(FINAL, ())
    assert d["n_runs"] == 95 and d["split"] == "test"
    return dci(pick(FINAL, k)), FINAL, "contrasts['delta_hybrid[combined]:run_auroc']{delta,ci}; n_runs"


@claim("C02", "same contrast, two fresh replications pooled", "-0.07 [-0.17, +0.02]", "-0.07 [-0.17, +0.02]",
       "n=90 runs (30 llm_v3rep + 60 llm_p2rep, label = channel condition); post hoc pooling of two registered splits")
def _():
    d = pick(POOL, ())
    assert d["n"] == 90 and d["n_by_ds"] == {"llm_v3rep": 30, "llm_p2rep": 60}
    return (dci(d["condition_label"]["contrasts"]["delta_hybrid[combined]"]), POOL,
            "condition_label.contrasts['delta_hybrid[combined]']{delta,ci}; n; n_by_ds")


@claim("C03", "gains above +0.06 (test) / +0.02 (pooled) excluded at 95% (upper CI limits)", "+0.06 / +0.02",
       "gains above +0.06 (test) and +0.02 (pooled)", "upper 95% CI limit of C01 (n=95) and C02 (n=90); pooled is post hoc")
def _():
    a = pick(FINAL, ("contrasts", "delta_hybrid[combined]:run_auroc", "ci", 1))
    b = pick(POOL, ("condition_label", "contrasts", "delta_hybrid[combined]", "ci", 1))
    return (f"{r(a, 2, True)} / {r(b, 2, True)}", FINAL + " + " + POOL,
            "contrasts[...run_auroc].ci[1]; condition_label.contrasts['delta_hybrid[combined]'].ci[1]")


@claim("C04", "a computed pair-statistics table added to the action view gains on test (action_stats minus action)",
       "+0.11 [+0.04, +0.18]", "+0.11 [+0.04, +0.18]",
       "n=95 runs, locked test; registered contrast family (delta_hybrid[action_stats] = action_stats - max(text, action)), "
       "not the primary endpoint. Corrected 2026-10-24 16:40: the abstract previously quoted structured (+0.08)")
def _():
    return (dci(pick(FINAL, ("contrasts", "action_stats-action:run_auroc"))), FINAL,
            "contrasts['action_stats-action:run_auroc']{delta,ci}")


@claim("C04b", "adding text to the pair-statistics view does not gain (combined_stats minus action_stats)",
       "-0.06 [-0.14, +0.01]", "-0.06 [-0.14, +0.01]", "n=95 runs, locked test; registered contrast family")
def _():
    return (dci(pick(FINAL, ("contrasts", "combined_stats-action_stats:run_auroc"))), FINAL,
            "contrasts['combined_stats-action_stats:run_auroc']{delta,ci}")


@claim("C04c", "same pair-statistics gain on fresh data (action_stats minus better single view), two replications pooled",
       "+0.00 [-0.06, +0.07]", "+0.00 [-0.06, +0.07] pooled n = 90",
       "n=90 runs (30 llm_v3rep + 60 llm_p2rep, label = channel condition); post hoc pooling; added 2026-10-24 17:57 (iter26 review: test gain did not replicate)")
def _():
    return (dci(pick(POOL, ("condition_label", "contrasts", "delta_hybrid[action_stats]"))), POOL,
            "condition_label.contrasts['delta_hybrid[action_stats]']{delta,ci}")


@claim("C05", "pair price premium AUROC, fresh replication", "0.94 [0.87, 0.99]", "0.94 [0.87, 0.99]",
       "n=60 runs (llm_p2rep: 30 private / 20 none / 10 legit); premium selected post hoc after v1; replication registered")
def _():
    d = pick(REPJ, ())
    assert d["n_runs"] == 60 and d["group_n"] == {"private_y1": 30, "private_y0": 0, "none": 20, "legit": 10}
    return ci(d["point_ci"]["premium"]["run_auroc"], False), REPJ, "point_ci.premium.run_auroc; n_runs; group_n"


@claim("C06", "unread pricing notepad premium as share of channel premium (rounds 2-12)", "65% (1.04/1.61)",
       "65% of the channel premium",
       "n=15 seeds per arm (llm_p2cue: notes vs none, private vs none, paired by seed); gpt-6-luna; registered arms, ratio is derived")
def _():
    n = pick(CUE, ("paired", "notes-none", "prem_r2_12", 0))
    p = pick(CUE, ("paired", "private-none", "prem_r2_12", 0))
    assert pick(CUE, ("paired", "notes-none", "n")) == pick(CUE, ("paired", "private-none", "n")) == 15
    return (f"{Decimal(str(round(100 * n / p, 6))).quantize(Decimal(1), rounding=ROUND_HALF_UP)}% "
            f"({r(n)}/{r(p)})", CUE, "paired['notes-none'].prem_r2_12[0] / paired['private-none'].prem_r2_12[0]; n")


@claim("C07", "legitimate cost / quality edges flagged by premium vs controls", "7/10, 9/10 vs 2/10",
       "flagged 7/10, 9/10 (controls 2/10)",
       "10 runs per condition (highcost, quality, plus 10 no-channel reference runs from llm_p2cue); gpt-6-luna; "
       "frozen dev threshold 0.667")
def _():
    c = pick(ASYM, ("conditions",))
    f = [c[k]["premium_flags"] for k in ("highcost", "quality", "none_ref_p2cue")]
    assert all(x[1] == 10 for x in f)
    return f"{f[0][0]}/10, {f[1][0]}/10 vs {f[2][0]}/10", ASYM, "conditions.{highcost,quality,none_ref_p2cue}.premium_flags"


@claim("C08", "text views flag every control (no-channel) market for Claude, deepseek, Qwen base+abliterated",
       "100% (5/5, 15/15, 15/15, 15/15)", "text auditors flag every control market",
       "control (condition=none) markets: Claude 5, deepseek 15, Qwen-base 15, Qwen-abliterated 15; text view; "
       "families differ by model so cross-family comparison is associative; registered predictions (E95) for Claude/deepseek")
def _():
    cl = pick(FAM, ("llm_p2claude", "views", "text", "flags_by_class", "PUB"))
    ds = pick(FAM, ("llm_p2ds", "views", "text", "flags_by_class", "PUB"))
    qa = pick(QEVAL.format("a"), ("detectors", "text", "flags", "none"))
    qb = pick(QEVAL.format("b"), ("detectors", "text", "flags", "none"))
    assert pick(FAM, ("llm_p2claude", "class_by_condition", "none", "PUB")) == 5
    assert pick(FAM, ("llm_p2ds", "class_by_condition", "none", "PUB")) == 15
    allf = [cl, ds, qa, qb]
    assert all(x[0] == x[1] for x in allf)
    return ("100% (" + ", ".join(f"{x[0]}/{x[1]}" for x in allf) + ")",
            f"{FAM} + {QEVAL.format('a')} + {QEVAL.format('b')}",
            "llm_p2{claude,ds}.views.text.flags_by_class.PUB; llm_p2qwen{a,b}.detectors.text.flags.none")


@claim("C09", "text-view run AUROC range across those control-flagging families (private vs none)", "0.15-0.36",
       None, "run AUROC private vs none, text view: Claude n=10, deepseek n=30, Qwen-base n=30, Qwen-abl n=30 runs; TL;DR claim (not in abstract text)")
def _():
    v = [pick(FAM, ("llm_p2claude", "views", "text", "auroc_private_vs_none", 0)),
         pick(FAM, ("llm_p2ds", "views", "text", "auroc_private_vs_none", 0)),
         pick(QEVAL.format("a"), ("detectors", "text", "auroc_private_vs_none", 0)),
         pick(QEVAL.format("b"), ("detectors", "text", "auroc_private_vs_none", 0))]
    return f"{r(min(v))}-{r(max(v))}", f"{FAM} + {QEVAL.format('{a,b}')}", "views.text.auroc_private_vs_none[0] (min,max over 4)"


@claim("C10", "SALT-NLP episodes", "8000", "8000 episodes",
       "episodes = 7998 with valid judge label + 2 invalid-judge episodes; 800 runs; external data (SALT-NLP)")
def _():
    d = pick(SALT, ("E104_sayvsdo",))
    assert d["n_episodes"] == 7998 and d["n_invalid_judge"] == 2 and sum(d["crosstab"].values()) == 7998
    return str(d["n_episodes"] + d["n_invalid_judge"]), SALT, "E104_sayvsdo.n_episodes + n_invalid_judge; crosstab sum"


@claim("C11", "SALT distinct models", "10", "10 models",
       "distinct model names parsed from per_condition ids (main__X and cross_model__A__B); 16 conditions x 500 episodes")
def _():
    pc = pick(SALT, ("E104_sayvsdo", "per_condition"))
    m = {x for c in pc for x in c["condition"].split("__")[1:]}
    return str(len(m)), SALT, "E104_sayvsdo.per_condition[*].condition (parsed)"


@claim("C12", "share of executed SALT episodes with no explicit agreement (1 - P(said|exec))", "62% (P(said|exec)=0.385)", "P(said | executed) 0.385",
       "executed episodes n=5169 (1989 said + 3180 not said), 7998 judged; Qwen judge label for 'said'; episodes are clustered in 800 runs (check CI method in salt script)")
def _():
    d = pick(SALT, ("E104_sayvsdo",))
    x = d["crosstab"]
    assert x["exec1_said0"] + x["exec1_said1"] == 5169
    e = d["P_said_given_exec"]
    return (f"{Decimal(str(round(100 * (1 - e['est']), 6))).quantize(Decimal(1), rounding=ROUND_HALF_UP)}% "
            f"(P(said|exec)={r(e['est'], 3)})", SALT, "E104_sayvsdo.P_said_given_exec.est; crosstab.exec1_*")


@claim("C13", "test 'colluders' that keep their agreement", "14/50", "14/50",
       "n=50 judged-agreement private runs among the 95 llm_v3 test runs (14 followed + 36 not followed); behaviour labels registered (E84)")
def _():
    c = pick(BEH, ("datasets", "llm_v3", "class_counts"))
    assert pick(BEH, ("datasets", "llm_v3", "n")) == 95
    return f"{c['followed']}/{c['followed'] + c['not_followed']}", BEH, "datasets.llm_v3.class_counts.{followed,not_followed}; n"


@claim("C14", "strict-executed channel pairs (memory + profit objective)", "13/20", "13/20",
       "20 channel markets (llm_p2strongF, seeds 9800000-9800019); strict rule fixed in registered amendment E99-amend; Jeffreys [0.43, 0.83]")
def _():
    v = pick(CLS, ("n_strict_executed",))
    return f"{v[0]}/{v[1]}", CLS, "n_strict_executed"


@claim("C15", "no-channel markets that price >= Nash + 2 (tacit-high)", "19/20", "19/20",
       "20 no-channel markets (paired seeds with C14); tacit-high rate >= 0.5 registered (E99amend); Jeffreys [0.79, 0.99]")
def _():
    v = pick(CLS, ("n_tacit_high_none",))
    return f"{v[0]}/{v[1]}", CLS, "n_tacit_high_none"


@claim("C16", "paired excess private - none (market price over cost-adjusted Nash)", "-0.44 [-1.84, +1.00]",
       "-0.44 [-1.84, +1.00]", "n=20 paired seeds; registered prediction E99_P3 (excess > 0) FAILED; unresolved")
def _():
    e = pick(REPORTJ, ("E99_P3",))
    assert e["n_pairs"] == 20
    return ci(e["paired_excess_private_minus_none"]), REPORTJ, "E99_P3.paired_excess_private_minus_none; n_pairs"


@claim("C17", "private-plan LLM monitor AUROC, strict-executed vs tacit-high", "0.76 [0.55, 0.93]", "(0.76 [0.55, 0.93])",
       "13 strict-executed vs 19 tacit-high markets; EXPLORATORY (E103 plan view registered before plan calls, but classes defined post hoc); "
       "CI [0.55, 0.93]")
def _():
    d = pick(EVAL, ("detectors", "plan", "auroc_strict_vs_tacit_high"))
    g = pick(EVAL, ("groups_n",))
    assert g["strict"] == 13 and g["tacit_high"] == 19
    assert d == pick(KEY, ("detectors", "plan_view", "auroc_strict_vs_tacit_high"))
    return r(d[0]) + f" [{r(d[1])}, {r(d[2])}]", EVAL, "detectors.plan.auroc_strict_vs_tacit_high (== keyword file detectors.plan_view...); groups_n"


@claim("C18", "no-LLM count of plans naming the chat partner, same contrast", "0.82 [0.66, 0.96]", "does comparably (0.82 [0.66, 0.96])",
       "13 vs 19 markets; EXPLORATORY post hoc keyword detector (E111) K_dir; CI [0.66, 0.96]")
def _():
    d = pick(KEY, ("detectors", "K_dir", "auroc_strict_vs_tacit_high"))
    assert pick(KEY, ("n_pos_strict",)) == 13 and pick(KEY, ("n_neg_tacit_high",)) == 19
    return r(d[0]) + f" [{r(d[1])}, {r(d[2])}]", KEY, "detectors.K_dir.auroc_strict_vs_tacit_high; n_pos_strict; n_neg_tacit_high"


@claim("C19", "no plan uses agreement words", "0/13 strict, 0/19 tacit-high",
       "no plan uses agreement words", "13 strict + 19 tacit-high (+7 non-executed) markets; keyword K_terms; exploratory")
def _():
    k = pick(KEY, ("runs_with_term_in_any_plan",))
    return f"{k['strict'][0]}/{k['strict'][1]} strict, {k['tacit_high'][0]}/{k['tacit_high'][1]} tacit-high", KEY, "runs_with_term_in_any_plan"


@claim("C20", "public-text view AUROC, strict-executed vs tacit-high (inverted)", "0.25 [0.08, 0.46]", "public text (0.25 [0.08, 0.46], inverted",
       "13 vs 19 markets; EXPLORATORY (E99-x, added after generation began, before detector scores); CI [0.08, 0.46]")
def _():
    d = pick(EVAL, ("detectors", "text", "auroc_strict_vs_tacit_high"))
    return r(d[0]) + f" [{r(d[1])}, {r(d[2])}]", EVAL, "detectors.text.auroc_strict_vs_tacit_high"


@claim("C21", "abliterated vs base Qwen: executed markets each arm; agreement at ceiling", "13/15; 13/15",
       "13/15 under the registered floor rule; agreement at ceiling)",
       "15 vs 15 private markets (llm_p2qwena vs llm_p2qwenb); execution diff 0.00 [-0.26, +0.26] Newcombe; agreement 15/15 both; registered (C3), predictions not supported")
def _():
    assert pick(QWEN, ("P1_agreement_rate", "base")) == [15, 15] == pick(QWEN, ("P1_agreement_rate", "abliterated"))
    a, b = pick(QWEN, ("P2_executed_rate", "abliterated")), pick(QWEN, ("P2_executed_rate", "base"))
    return f"{a[0]}/{a[1]}; {b[0]}/{b[1]}", QWEN, "P2_executed_rate.abliterated; P2_executed_rate.base; P1_agreement_rate"


@claim("C22", "SALT-NLP: gpt-6.1-sol text auditor AUROC for execution", "0.87 [0.83, 0.91]", "(AUROC 0.87 [0.83, 0.91])",
       "n=240 sampled SALT episodes (120 executed; 79 tacit) audited by gpt-6.1-sol (E105); external data")
def _():
    d = pick(SALT, ("E105_audit",))
    assert d["n"] == 240 and d["n_exec"] == 120
    return ci([d["auroc"]["est"], *d["auroc"]["ci"]], False), SALT, "E105_audit.auroc{est,ci}; n; n_exec"


@claim("C21b", "abliterated vs base Qwen: strict-executed (shared definition) each arm", "5/15; 5/15",
       "executes no more than its base model (strict 5/15 both",
       "15 private markets per model; shared strict executed rule (p2_strong_classes on llm_p2qwena / llm_p2qwenb)")
def _():
    a = json.loads((ROOT / A / "p2_strong_classes_llm_p2qwena.json").read_text())["n_strict_executed"]
    b = json.loads((ROOT / A / "p2_strong_classes_llm_p2qwenb.json").read_text())["n_strict_executed"]
    return f"{a[0]}/{a[1]}; {b[0]}/{b[1]}", A + "p2_strong_classes_llm_p2qwena.json", "n_strict_executed (qwena; qwenb)"


@claim("C23", "abliterated minus base Qwen: paired channel premium difference", "-1.24 [-2.41, -0.03]",
       "smaller channel premium (-1.24 [-2.41, -0.03]; serving precision differs)",
       "15 vs 15 private markets with matched none; bootstrap; registered P3 (abliterated >= base) not supported; bf16 vs FP8 serving confound")
def _():
    return ci(pick(QWEN, ("P3_paired_premium", "diff_boot95"))), QWEN, "P3_paired_premium.diff_boot95"


@claim("C24", "E116 within channel: plan view AUROC strict-executed vs non-executed", "0.69 [0.44, 0.91]",
       "(plans 0.69 [0.44, 0.91])",
       "13 strict vs 7 non-executed private markets (llm_p2strongF); exploratory, zero LLM calls, seed bootstrap")
def _():
    src = "results/analysis/p2_within_agree_llm_p2strongF.json"
    d = json.load(open(src))
    assert (d["n_strict"], d["n_nonexec"]) == (13, 7)
    return ci(d["views"]["plan"]["auroc_strict_vs_nonexec"], False), src, "views.plan.auroc_strict_vs_nonexec"


@claim("C27", "E116b within agreement, Qwen abliterated / base: public text AUROC strict vs non-executed", "0.73 [0.43, 0.99]; 0.51 [0.25, 0.70]",
       "public text 0.73 [0.43, 0.99] / 0.51 [0.25, 0.70]",
       "5 strict vs 10 non-executed private markets per model (llm_p2qwena, llm_p2qwenb; 15/15 judged agreement each); exploratory, not pooled")
def _():
    v = []
    for ds in ("llm_p2qwena", "llm_p2qwenb"):
        src = f"results/analysis/p2_within_agree_{ds}.json"
        d = json.load(open(src))
        assert (d["n_strict"], d["n_nonexec"], d["n_nonexec_agreed"]) == (5, 10, 10)
        v.append(ci(d["views"]["text"]["auroc_strict_vs_nonexec"], False))
    return "; ".join(v), "results/analysis/p2_within_agree_llm_p2qwen{a,b}.json", "views.text.auroc_strict_vs_nonexec"


@claim("C25", "E112 participant replacement (luna newcomer), private arm: market excess replaced - original; re-agreement replaced; originals",
       "+0.20 [-0.08, +0.62]; 16/20; 15/20", "level (+0.20 [-0.08, +0.62]) nor re-agreement (16/20 vs 15/20)",
       "20 paired private games replayed from llm_p2strongF, newcomer from round 21, rounds 21-40; registered E112, all 4 predictions held; none arm +0.16 [-0.27, +0.57] in P2.15")
def _():
    src = "results/analysis/p2_replace.json"
    a = json.load(open(src))["arms"]["private"]
    ra = a["O4_reagreement_floor_ge13"]
    v = f"{ci(a['O1_market_repl_minus_orig'])}; {ra['repl'][0]}/{ra['repl'][1]}; {ra['orig'][0]}/{ra['orig'][1]}"
    return v, src, "arms.private.O1_market_repl_minus_orig; arms.private.O4_reagreement_floor_ge13.{repl,orig}"


@claim("C28", "E115 participant replacement (gpt-6.1-sol newcomer), private arm: re-agreement replaced; markets >= Nash + 2 replaced",
       "0/20; 18/20", "re-agrees 0/20, yet 18/20 markets stay",
       "same 20 paired private games as E112, sol newcomer from round 21; registered E115, S1 failed, S2-S4 held; none arm 9/10 in P2.15")
def _():
    src = "results/analysis/p2_replace_sol.json"
    a = json.load(open(src))["arms"]["private"]
    ra, l = a["O4_reagreement_floor_ge13"]["repl"], a["O6_market_excess_ge2"]["repl"]
    return f"{ra[0]}/{ra[1]}; {l[0]}/{l[1]}", src, "arms.private.O4_reagreement_floor_ge13.repl; arms.private.O6_market_excess_ge2.repl"


@claim("C29", "E120 definition sensitivity (P2.7 body): strict-executed one-at-a-time range; full grid; tacit-high range", "10-16/20; 7-18/20; 17-20/20",
       None, "llm_p2strongF, frozen judge terms, 81 threshold combinations; exploratory, zero LLM calls; registered 13/20 reproduced")
def _():
    src = "results/analysis/p2_strict_sensitivity.json"
    d = json.load(open(src))["llm_p2strongF"]
    assert (d["registered"]["k"], d["registered"]["n"], d["n_cells"]) == (13, 20, 81)
    o, g, t = d["strict_range_one_at_a_time"], d["strict_range_all"], [x["k"] for x in d["tacit_high"]]
    return f"{o[0]}-{o[1]}/20; {g[0]}-{g[1]}/20; {min(t)}-{max(t)}/20", src, "strict_range_one_at_a_time; strict_range_all; tacit_high[].k"


def run():
    text = abstract_text()
    rows = []
    for c in CLAIMS:
        row = {k: c[k] for k in ("id", "claim", "expected", "denominator", "note")}
        try:
            value, src, path = c["fn"]()
            row.update(value=value, source=src, key_path=path)
            row["status"] = "OK" if norm(value) == norm(c["expected"]) else "MISMATCH"
            row["in_report_abstract"] = (c["snippet"] is None or norm(c["snippet"]) in text)
            if not row["in_report_abstract"]:
                row["status"] = "MISMATCH"
                row["note"] = f"text '{c['snippet']}' not found in REPORT.md abstract"
        except (OSError, KeyError, IndexError, TypeError) as exc:
            row.update(value=None, source=None, key_path=None, status="NO_SOURCE", in_report_abstract=None)
            row["note"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def write(rows):
    OUT.with_suffix(".json").write_text(json.dumps(rows, indent=1) + "\n")
    lines = ["| id | claim | value (abstract text) | status | denominator / registration | source : key path |",
             "|---|---|---|---|---|---|"]
    for x in rows:
        lines.append("| {id} | {claim} | {v} | {status} | {denominator} | `{s}` : `{k}` |".format(
            v=(x["value"] if x["value"] is not None else "-"), s=x["source"] or "-", k=x["key_path"] or "-", **x))
    OUT.with_suffix(".md").write_text("\n".join(lines) + "\n")


def check(root=ROOT, write_files=True):
    rows = run()
    if write_files:
        write(rows)
    bad = [x for x in rows if x["status"] == "MISMATCH"]
    for x in bad:
        print(f"MISMATCH {x['id']}: {x['claim']}: json gives {x['value']!r}, abstract says {x['expected']!r}; {x['note']}",
              file=sys.stderr)
    nos = [x["id"] for x in rows if x["status"] == "NO_SOURCE"]
    if nos:
        print("NO_SOURCE:", ", ".join(nos))
    return rows, bad


def main():
    rows, bad = check()
    print(f"{len(rows)} claims: {sum(x['status'] == 'OK' for x in rows)} OK, {len(bad)} MISMATCH")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
