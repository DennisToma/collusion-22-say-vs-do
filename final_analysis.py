"""FROZEN final analysis for llm_v3 (DIRECTION 22:00 directive 2). Frozen 2026-10-23 ~22:40 UTC, before the
full dataset exists. Run on dev while building; run on --split test ONCE for the headline.

Scorers (each gives 6 pair scores + 1 run score per run):
  LLM views (gpt-6.1-sol by default): text, action, combined, combined_stats, action_stats, structured
      pair score = auditor pair score; run score = collusion_present.
  premium   untrained statistic: pair mean price minus mean of the other two firms (all rounds, every pair);
            run score = max pair premium. No fitting at all.
  fusion    late fusion of the unimodal LLM auditors: w*text + (1-w)*action (pair scores and run scores),
            w chosen on DEV (grid 0..1 step .1, max dev pair AUROC). Tests "complementary cues without relational
            reasoning".
  ext_*     EXTERNAL (added 22:23 iter 5, before any test look): sibling Q1.4 per-pair information-theoretic scores
            (pcmi, mi, te, pearson; + pair_level = their reimplementation of premium) from ../collusion-14-infotheory/results/eval/<ds>_ext.json, used as-is (higher =
            more dependence). Separate block on the runs the file covers; paired premium-minus-ext contrast.
Metrics (bootstrap over runs, n = runs): pooled pair AUROC, within-market localisation AUROC (positive runs only),
run AUROC, pair-ID accuracy (tie-aware). Paired contrasts on identical runs.
FPR at a fixed DEV-chosen threshold (Youden J on dev run scores), reported per stratum on the eval split:
  private y=1 (TPR), none, legit, none tacit-high (mean markup over cost >= 7, i.e. >= 2 above static Nash ~5;
  tacit is its own label, not counted as FP in the headline FPR), private y=0.
Realised-premium stratification: detection rate among y=1 runs split by assigned-pair premium (labels.jsonl,
<= 0.5 'not acted on' vs > 0.5).

    uv run python final_analysis.py --split dev        # development (allowed any time)
    uv run python final_analysis.py --split test       # ONCE, frozen config -> headline
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import PAIRS, load_jsonl, auc, public_explicit

LLM_VIEWS = ["text", "action", "combined", "combined_stats", "action_stats", "structured"]
AG = ["A", "B", "C", "D"]
DEV_MAX = 30  # data/SPLITS.md: dev = llm_v3_0000..0029
N_FROZEN = 125  # llm_v3 plan private:70,none:35,legit:20


def idx(r):
    return int(r.rsplit("_", 1)[1])


def premium_scores(ds, start=0):
    """start = first round (0-based) included; start=1 drops the opening round (robustness: many private pairs
    open jointly high in round 1 and abandon the agreement after being undercut)."""
    P, C = {}, {}
    for l in open(Path("data") / ds / "trajectories.jsonl"):
        r = json.loads(l)
        P.setdefault(r["run_id"], []).append((r["round"], {x["id"]: x["price"] for x in r["agents"]}))
        C.setdefault(r["run_id"], []).append(r["market"]["cost"])
    out, markup = {}, {}
    for rid, rows in P.items():
        rows.sort(key=lambda t: t[0])
        pr = {a: np.array([d[a] for _, d in rows[start:]], float) for a in AG}
        sc = {}
        for p in PAIRS:
            o = [a for a in AG if a not in p]
            sc[p] = float(((pr[p[0]] + pr[p[1]]) / 2).mean() - np.mean([pr[a] for a in o], axis=0).mean())
        out[rid] = {"scores": sc, "run": max(sc.values())}
        markup[rid] = float(np.mean([pr[a].mean() for a in AG]) - np.mean(C[rid][start:]))
    return out, markup


def metrics(ids, S, labs):
    out = {}
    for k, R in S.items():
        py, ps, wm, pid = [], [], [], []
        for r in ids:
            ap, sc = "".join(labs[r]["assigned_pair"]), R[r]["scores"]
            for p in PAIRS:
                py.append(int(labs[r]["y"] and p == ap)); ps.append(sc[p])
            if labs[r]["y"]:
                wm.append(np.mean([(sc[ap] > sc[p]) + 0.5 * (sc[ap] == sc[p]) for p in PAIRS if p != ap]))
                top = [p for p in PAIRS if sc[p] == max(sc.values())]
                pid.append((ap in top) / len(top))
        out[k] = {"pair_auroc": auc(py, ps), "within_market_auroc": float(np.mean(wm)) if wm else np.nan,
                  "run_auroc": auc([labs[r]["y"] for r in ids], [R[r]["run"] for r in ids]),
                  "pair_id_acc": float(np.mean(pid)) if pid else np.nan}
    return out


def ci(a):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return [round(float(np.percentile(a, 2.5)), 4), round(float(np.percentile(a, 97.5)), 4)] if len(a) else [None, None]


def boot(ids, S, labs, n, seed=0):
    """Run-level bootstrap, stratified by class (keeps n_pos/n_neg fixed so AUROC is always defined)."""
    rng = np.random.default_rng(seed)
    pt = metrics(ids, S, labs)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    bs = [metrics(list(rng.choice(P, len(P))) + (list(rng.choice(N, len(N))) if N else []), S, labs) for _ in range(n)]
    out = {"point_ci": {k: {m: [round(pt[k][m], 4)] + ci([b[k][m] for b in bs]) for m in pt[k]} for k in pt},
           "n_boot_finite": {k: {m: int(np.isfinite([b[k][m] for b in bs]).sum()) for m in pt[k]} for k in pt},
           "note": "CIs condition on the dev-fitted fusion weight/thresholds; [1,1]-type intervals = boundary (perfect separation)"}
    M = ("pair_auroc", "within_market_auroc", "run_auroc")
    con = {}
    def contrast(name, f):
        for m in M:
            try:
                d0 = f(pt, m)
            except KeyError:
                return
            con[f"{name}:{m}"] = {"delta": round(d0, 4), "ci": ci([f(b, m) for b in bs])}
    best1 = lambda x, m: max(x["text"][m], x["action"][m])
    for h in ("combined", "combined_stats", "action_stats", "structured", "fusion"):
        contrast(f"delta_hybrid[{h}]", lambda x, m, h=h: x[h][m] - best1(x, m))
    for h1, h2 in (("action", "action_stats"), ("action_stats", "combined_stats"), ("combined_stats", "structured"),
                   ("combined", "combined_stats"), ("fusion", "combined"), ("fusion", "structured")):
        contrast(f"{h2}-{h1}", lambda x, m, h1=h1, h2=h2: x[h2][m] - x[h1][m])
    for h in [v for v in LLM_VIEWS + ["fusion"] if v in S]:
        contrast(f"premium-{h}", lambda x, m, h=h: x["premium"][m] - x[h][m])
        contrast(f"premium_r2plus-{h}", lambda x, m, h=h: x["premium_r2plus"][m] - x[h][m])
    out["contrasts"] = con
    return out


EXT_DETECTORS = ["pcmi", "mi", "te", "pearson", "pair_level"]  # info-theoretic (higher = more dependence);
# pair_level = sibling's INDEPENDENT reimplementation of our premium statistic (replication check, not a new comparator)


def _pd(ids, S, labs, k1, k2, m, n, seed=1):
    """paired (same resampled runs) difference k1 - k2 in metric m, class-stratified bootstrap."""
    rng = np.random.default_rng(seed)
    P, N = [r for r in ids if labs[r]["y"]], [r for r in ids if not labs[r]["y"]]
    f = lambda rs: (lambda M: M[k1][m] - M[k2][m])(metrics(rs, {k1: S[k1], k2: S[k2]}, labs))
    return {"delta": round(f(ids), 4), "ci": ci([f(list(rng.choice(P, len(P))) + (list(rng.choice(N, len(N))) if N else []))
                                                  for _ in range(n)])}


def youden(y, s):
    """Threshold maximising TPR-FPR on dev (flag if score >= t); candidates include +inf (flag nobody);
    ties -> the HIGHER threshold (conservative)."""
    y, s = np.asarray(y), np.asarray(s, float)
    if not (0 < y.sum() < len(y)):
        return None
    best = (-np.inf, None)
    for t in list(np.unique(s)) + [np.inf]:
        j = np.mean(s[y == 1] >= t) - np.mean(s[y == 0] >= t)
        if j >= best[0]:
            best = (j, float(t))
    return best[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--split", required=True, choices=["dev", "test", "all"])
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--allow-partial", action="store_true", help="development only: analyse runs that have all views so far")
    ap.add_argument("--check-only", action="store_true", help="preflight: assert the frozen cohort is complete, compute nothing")
    a = ap.parse_args()
    if a.ds == "llm_v3" and a.split in ("test", "all") and not a.check_only:
        from evaluation_guard import refuse_completed
        refuse_completed("headline")
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    S = {}
    for v in LLM_VIEWS:
        rows = load_jsonl(d / f"{v}_orig.jsonl")
        ids_v = [x["run_id"] for x in rows]
        assert len(ids_v) == len(set(ids_v)), f"duplicate audits in {v}"
        assert all(0 <= x["collusion_present"] <= 100 and all(0 <= x["scores"][p] <= 100 for p in PAIRS) for x in rows), v
        if rows or not a.allow_partial:
            S[v] = {x["run_id"]: {"scores": x["scores"], "run": x["collusion_present"]} for x in rows}
    S["premium"], markup = premium_scores(a.ds)
    S["premium_r2plus"], _ = premium_scores(a.ds, start=1)
    common = sorted(set(labs).intersection(*[set(R) for R in S.values()]))
    want_dev = sorted(r for r in labs if idx(r) < DEV_MAX)
    want = sorted(labs) if a.split == "all" else [r for r in sorted(labs) if (idx(r) < DEV_MAX) == (a.split == "dev")]
    incomplete = {v: len([r for r in set(want) | set(want_dev) if r not in R]) for v, R in S.items()}
    if not a.allow_partial:  # frozen cohort: every labelled run of the split (and all 30 dev runs) audited by every view
        assert len(want_dev) == DEV_MAX and not any(incomplete.values()), f"incomplete cohort: {incomplete}"
        if a.ds == "llm_v3":  # exact frozen id set (data/SPLITS.md): 0000-0124 all labelled, not just "available labels"
            exp = {f"llm_v3_{i:04d}" for i in range(N_FROZEN)}
            assert exp <= set(labs), f"missing labels: {sorted(exp - set(labs))[:5]}"
    if a.ds == "llm_v3" and not a.allow_partial:  # hard-set filter must be the LLM+keyword check on every run
        hs = {x["run_id"] for x in load_jsonl(Path("data") / a.ds / "public_explicit.jsonl")}
        assert set(labs) <= hs, f"hardset.py has not checked {len(set(labs) - hs)} runs; run `uv run python hardset.py`"
    bad = [r for r, L in labs.items() if L.get("agreement") not in ("explicit", "info_exchange", "none", "no_channel")
           or (L.get("agreement") == "no_channel") != (L.get("condition") != "private")]
    assert a.allow_partial or not bad, f"invalid/unparsed labels (would silently become y=0): {bad[:5]}"
    if a.check_only:
        print(f"preflight OK: split={a.split}, all views complete for {len(want)} runs (+{len(want_dev)} dev)"); return
    dev = [r for r in common if idx(r) < DEV_MAX]
    # late fusion weight from dev only
    def fuse(w):
        return {r: {"scores": {p: w * S["text"][r]["scores"][p] + (1 - w) * S["action"][r]["scores"][p] for p in PAIRS},
                    "run": w * S["text"][r]["run"] + (1 - w) * S["action"][r]["run"]} for r in common}
    grid = [round(0.1 * i, 1) for i in range(11)]
    def dev_obj(w):  # mean of the two primary endpoints on dev
        m = metrics(dev, {"f": fuse(w)}, labs)["f"]
        return float(np.mean([m["run_auroc"], m["within_market_auroc"]]))
    dev_auc = {w: dev_obj(w) for w in grid}
    w = max(grid, key=lambda g: (dev_auc[g], -abs(g - 0.5)))
    S["fusion"] = fuse(w)
    ids = common if a.split == "all" else [r for r in common if (idx(r) < DEV_MAX) == (a.split == "dev")]
    pe = public_explicit(a.ds)
    out = {"dataset": a.ds, "auditor": a.auditor, "split": a.split, "n_runs": len(ids),
           "n_pos": int(sum(labs[r]["y"] for r in ids)), "n_dev_for_calibration": len(dev),
           "fusion_w_text": w, "fusion_dev_objective_by_w": dev_auc, "missing_runs_by_view": incomplete,
           "endpoint": "y = verified private coordination COMMUNICATION on the assigned pair (judge on private chat: explicit "
                       "agreement or pricing-intention exchange); not realised supra-competitive conduct",
           "primary_metrics": ["run_auroc (detection)", "within_market_auroc (localisation, positive runs)"],
           "secondary_metrics": ["pair_auroc (pooled; mixes detection and localisation)", "pair_id_acc"],
           "views_missing": [v for v in LLM_VIEWS if v not in S], "n_public_explicit_in_split": int(sum(bool(pe.get(r)) for r in ids)),
           "models_seen": sorted({x["model"] for v in LLM_VIEWS if v in S for x in load_jsonl(d / f"{v}_orig.jsonl")})}
    out.update(boot(ids, S, labs, a.boot))
    hard = [r for r in ids if not pe.get(r)]
    out["hard_set"] = {"n": len(hard), "note": "identical to the full split" if len(hard) == len(ids) else "",
                       **({} if len(hard) == len(ids) or not hard else {"metrics": boot(hard, S, labs, a.boot)["point_ci"]})}
    # strata + fixed dev thresholds
    def stratum(r):
        L = labs[r]
        if L["y"]:
            return "private_y1"
        if L["condition"] == "none":
            return "none_highmarkup_proxy" if markup[r] >= 7 else "none_lowmarkup"
        return "legit" if L["condition"] == "legit" else "private_y0"
    th = {k: youden([labs[r]["y"] for r in dev], [S[k][r]["run"] for r in dev]) for k in S}
    out["threshold_calibration_counts"] = {"dev_pos": int(sum(labs[r]["y"] for r in dev)), "dev_neg": int(sum(1 - labs[r]["y"] for r in dev))}
    st = {}
    for r in ids:
        st.setdefault(stratum(r), []).append(r)
    out["thresholds_dev_youden"] = th
    st["none_all"] = [r for r in ids if labs[r]["condition"] == "none"]
    st["all_negatives"] = [r for r in ids if not labs[r]["y"]]
    def rate(k, rs):  # flag rate + Wilson 95% interval
        if th[k] is None or not rs:
            return None
        x, n = sum(S[k][r]["run"] >= th[k] for r in rs), len(rs)
        p, z = x / n, 1.96
        c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        return [round(p, 3), round(max(0, c - h), 3), round(min(1, c + h), 3)]
    out["flag_rate_by_stratum"] = {g: {"n": len(rs), **{k: rate(k, rs) for k in S}} for g, rs in sorted(st.items())}
    # y=1 runs split by LATE-WINDOW relative premium of the assigned pair (labels.jsonl, rounds >= 4). Low relative
    # premium != "not acted on" (all firms may have risen together); it is a proxy only.
    pos = [r for r in ids if labs[r]["y"]]
    for name, sel in (("late_rel_premium_le_0.5", lambda r: labs[r]["pair_premium"] <= 0.5), ("late_rel_premium_gt_0.5", lambda r: labs[r]["pair_premium"] > 0.5)):
        rs = [r for r in pos if sel(r)]
        out.setdefault("y1_by_late_relative_premium", {})[name] = {
            "n": len(rs), **{k: {"flag_rate": rate(k, rs),
                                 "pair_id_acc": round(metrics(rs, {k: S[k]}, labs)[k]["pair_id_acc"], 3) if rs else None}
                             for k in S}}
    # architecture takeaway: premium always on (free) -> LLM audit (structured view) only for the top-k% runs by premium
    order = sorted(ids, key=lambda r: -S["premium"][r]["run"])
    out["triage"] = {}
    for k in (0.25, 0.5, 0.75, 1.0):
        top_k = order[:int(np.ceil(k * len(ids)))]
        npos = sum(labs[r]["y"] for r in ids)
        out["triage"][f"top_{int(k * 100)}pct"] = {
            "llm_calls": len(top_k), "recall_of_positives": round(sum(labs[r]["y"] for r in top_k) / max(npos, 1), 3),
            "neg_audited": int(sum(1 - labs[r]["y"] for r in top_k)),
            "audited_negatives_flagged_by_structured": int(sum((not labs[r]["y"]) and th.get("structured") is not None
                                                             and "structured" in S and S["structured"][r]["run"] >= th["structured"] for r in top_k))}
        # cascade (added iter 6, before test): premium screen -> LLM view flags at its dev threshold. End-to-end
        # recall = y=1 runs both sent AND flagged / all y=1; FPR = negatives both sent AND flagged / all negatives;
        # pair-ID = LLM top pair (tie-aware) on y=1 runs that were sent and flagged, over all y=1 runs.
        nneg = len(ids) - npos
        for v in ("structured", "action_stats", "combined"):
            if v in S and th.get(v) is not None:
                fl = [r for r in top_k if S[v][r]["run"] >= th[v]]
                pid = 0.0
                for r in fl:
                    if labs[r]["y"]:
                        sc = S[v][r]["scores"]; top = [p for p in PAIRS if sc[p] == max(sc.values())]
                        pid += ("".join(labs[r]["assigned_pair"]) in top) / len(top)
                out["triage"][f"top_{int(k * 100)}pct"][f"cascade_{v}"] = {
                    "recall": round(sum(labs[r]["y"] for r in fl) / max(npos, 1), 3),
                    "fpr": round(sum(1 - labs[r]["y"] for r in fl) / max(nneg, 1), 3),
                    "recall_with_correct_pair": round(pid / max(npos, 1), 3)}
    # external comparator (DIRECTION directive 2b): sibling Q1.4 per-pair information-theoretic scores, read-only
    # (../collusion-14-infotheory/results/eval/<ds>_ext.json). Coverage may lag our cohort -> own block on the
    # intersection, paired against premium/structured on the same runs; never part of the frozen-cohort assert.
    ext_fn = Path("..") / "collusion-14-infotheory" / "results" / "eval" / f"{a.ds}_ext.json"
    if ext_fn.exists():
        try:
            X = json.loads(ext_fn.read_text())  # sibling may rewrite it concurrently
        except json.JSONDecodeError:
            X = {"per_pair_scores": [], "n_runs": "unreadable"}
        if not isinstance(X, dict) or not isinstance(X.get("per_pair_scores"), list) or not all(
                isinstance(x, dict) and {"detector", "run_id", "pair", "score"} <= set(x)
                and isinstance(x["score"], (int, float)) and not isinstance(x["score"], bool) for x in X["per_pair_scores"]):
            X = {"per_pair_scores": [], "n_runs": "unexpected schema"}  # never crash the frozen analysis on sibling data
        out["external_infotheory"] = {"source": str(ext_fn), "n_runs_in_file": X.get("n_runs")}
        for det in EXT_DETECTORS:
            E = {}
            for x in X["per_pair_scores"]:
                if x["detector"] == det and np.isfinite(x["score"]):
                    E.setdefault(x["run_id"], {})[x["pair"]] = float(x["score"])
            E = {r: {"scores": sc, "run": max(sc.values())} for r, sc in E.items() if set(sc) == set(PAIRS)}
            ix = [r for r in ids if r in E]
            out["external_infotheory"].setdefault("coverage", {})[det] = f"{len(ix)}/{len(ids)} runs of the split" + (
                "" if len(ix) == len(ids) else " (PARTIAL: sibling file lags our cohort)")
            if len(ix) < 4 or not (0 < sum(labs[r]["y"] for r in ix) < len(ix)):
                out["external_infotheory"][det] = {"n": len(ix), "note": "too few runs"}
                continue
            sub = {f"ext_{det}": E, "premium": S["premium"], **({"structured": S["structured"]} if "structured" in S else {})}
            b = boot(ix, sub, labs, a.boot)
            out["external_infotheory"][det] = {"n": len(ix), "n_pos": int(sum(labs[r]["y"] for r in ix)),
                                                "point_ci": b["point_ci"],
                                                "premium_minus_ext": {m: _pd(ix, sub, labs, "premium", f"ext_{det}", m, a.boot)
                                                                      for m in ("run_auroc", "within_market_auroc")}}
    out["markup_by_run"] = {r: round(markup[r], 3) for r in ids}
    Path("results/analysis").mkdir(parents=True, exist_ok=True)
    fn = Path("results/analysis") / f"final_{a.ds}_{a.auditor}_{a.split}.json"
    tmp = fn.with_suffix(".json.tmp"); tmp.write_text(json.dumps(out, indent=1)); tmp.replace(fn)  # atomic
    pc = out["point_ci"]
    print(f"split={a.split} n={out['n_runs']} pos={out['n_pos']} fusion w_text={w}")
    for k in pc:
        print(f"{k:15s} " + "  ".join(f"{m}={pc[k][m][0]:.3f}[{pc[k][m][1]},{pc[k][m][2]}]" for m in ("run_auroc", "within_market_auroc", "pair_auroc")))
    for c, v in out["contrasts"].items():
        if "run_auroc" in c or "within" in c:
            print(f"  {c:45s} {v['delta']:+.3f} {v['ci']}")
    print(json.dumps(out["flag_rate_by_stratum"], indent=0))
    for det, v in out.get("external_infotheory", {}).items():
        if isinstance(v, dict) and "point_ci" in v:
            e = v["point_ci"][f"ext_{det}"]
            print(f"ext {det:10s} n={v['n']} run={e['run_auroc'][0]:.3f}{e['run_auroc'][1:]} within={e['within_market_auroc'][0]:.3f}"
                  f"  premium-ext run {v['premium_minus_ext']['run_auroc']}")


if __name__ == "__main__":
    main()
