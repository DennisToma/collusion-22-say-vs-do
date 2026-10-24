"""Phase 2 gap 6 (E82, registered before running): what does the supervised public-text LR (0.98 test run AUROC) key on?
Same learner as baselines.py (TF-IDF 1-2gram, min_df 2, sublinear tf; LR C=1), pair records = both firms' public
messages. No LLM calls.
 (a) llm_v3 test, grouped 5-fold CV (as published): fold-internal ablation — drop the train fold's top-k |coef|
     n-grams, refit, score the held-out fold. k in 0/20/50/100/200/500.
 (b) transfer: fit on all 125 llm_v3 runs; score fresh runs. Run score = max pair score. Run AUROC of each condition vs
     llm_v3rep `none` runs (fresh negatives): llm_v3rep private (delivered), llm_v3plc placebo (offered, never
     delivered), and every llm_p2cue condition if that dataset exists. If placebo ~ private the text signal is a
     response to the offer, not to coordination content.

    uv run python p2_textlr.py     # -> results/analysis/p2_textlr.json
"""
import json
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from features import load, load_gt, pair_features, PAIRS

KS = [0, 20, 50, 100, 200, 500]


def recs_of(ds):
    d = Path("data") / ds
    runs, gt = load(d / "trajectories.jsonl"), load_gt(d / "ground_truth.jsonl")
    labs = {l["run_id"]: l for l in map(json.loads, open(d / "labels.jsonl"))} if (d / "labels.jsonl").exists() else {}
    out = []
    for rid in sorted(runs):
        f = pair_features(runs[rid]); g = gt[rid]
        y = int(labs.get(rid, {}).get("agreement") in ("explicit", "info_exchange"))
        for pr in PAIRS:
            out.append({"run_id": rid, "pair": pr, "text": f[pr]["text"], "cond": g["condition"],
                        "y": int(y and pr == "".join(g["assigned_pair"]))})
    return out


def run_scores(recs, s):
    R = {}
    for r, v in zip(recs, s):
        R.setdefault(r["run_id"], []).append((v, r["y"], r["cond"]))
    return {k: (max(x[0] for x in v), int(any(x[1] for x in v)), v[0][2],
                np.mean([x[1] for x in v if x[0] == max(y[0] for y in v)])) for k, v in R.items()}


def auc(neg, pos):
    return float(np.mean([(p > q) + 0.5 * (p == q) for p in pos for q in neg])) if len(neg) and len(pos) else None


def auc_ci(neg, pos, n=2000, seed=0):
    rng = np.random.default_rng(seed); neg, pos = np.asarray(neg), np.asarray(pos)
    b = [auc(rng.choice(neg, len(neg)), rng.choice(pos, len(pos))) for _ in range(n)]
    return [round(auc(neg, pos), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]


def fit(texts, y, drop=()):
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(texts)
    if drop:
        voc = [t for t in vec.get_feature_names_out() if t not in drop]
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True, vocabulary=voc).fit(texts)
    return vec, LogisticRegression(C=1.0, max_iter=5000).fit(vec.transform(texts), y)


def main():
    out = {"note": "E82; same learner as baselines.py; transfer model fit on all llm_v3 (descriptive transfer, not tuning)"}
    allr = recs_of("llm_v3")
    test = [r for r in allr if int(r["run_id"].rsplit("_", 1)[1]) >= 30]
    y = np.array([r["y"] for r in test]); groups = [r["run_id"] for r in test]
    abl = {}
    for k in KS:
        s = np.zeros(len(test))
        for tr, te in GroupKFold(5).split(test, y, groups):
            T = [test[i]["text"] for i in tr]
            vec, m = fit(T, y[tr])
            if k:
                voc = vec.get_feature_names_out(); top = set(voc[np.argsort(-np.abs(m.coef_[0]))[:k]])
                vec, m = fit(T, y[tr], drop=top)
            s[te] = m.predict_proba(vec.transform([test[i]["text"] for i in te]))[:, 1]
        rs = run_scores(test, s)
        pos = [v[0] for v in rs.values() if v[1]]; neg = [v[0] for v in rs.values() if not v[1]]
        abl[k] = {"run_auroc": auc_ci(neg, pos), "pair_id_acc": round(float(np.mean([v[3] for v in rs.values() if v[1]])), 3)}
        print("ablate top", k, abl[k], flush=True)
    out["ablation_test_cv"] = abl
    vec, m = fit([r["text"] for r in allr], np.array([r["y"] for r in allr]))
    sc = lambda recs: run_scores(recs, m.predict_proba(vec.transform([r["text"] for r in recs]))[:, 1])
    rep = sc(recs_of("llm_v3rep"))
    neg = [v[0] for v in rep.values() if v[2] == "none"]
    tr = {"negatives": f"llm_v3rep none (n={len(neg)})",
          "llm_v3rep:private": auc_ci(neg, [v[0] for v in rep.values() if v[2] == "private"]),
          "llm_v3rep:legit": auc_ci(neg, [v[0] for v in rep.values() if v[2] == "legit"])}
    plc = sc(recs_of("llm_v3plc"))
    tr["llm_v3plc:placebo"] = auc_ci(neg, [v[0] for v in plc.values()])
    tr["pair_id_acc"] = {"llm_v3rep:private": round(float(np.mean([v[3] for v in rep.values() if v[2] == "private" and v[1]])), 3)}
    cue_gt = Path("data/llm_p2cue/ground_truth.jsonl")
    if cue_gt.exists() and sum(1 for _ in open(cue_gt)) == 90:  # only once generation is complete
        cue = recs_of("llm_p2cue")
        # placebo/notes/neutral runs carry y=0 or judge labels; localisation uses the assigned pair, so relabel by pair
        gt = load_gt(Path("data/llm_p2cue/ground_truth.jsonl"))
        cs = run_scores(cue, m.predict_proba(vec.transform([r["text"] for r in cue]))[:, 1])
        s_all = m.predict_proba(vec.transform([r["text"] for r in cue]))[:, 1]
        for c in sorted({v[2] for v in cs.values()}):
            tr[f"llm_p2cue:{c}"] = auc_ci(neg, [v[0] for v in cs.values() if v[2] == c])
            # assigned pair top-scored? (tie-aware) — localisation of the channel pair regardless of label
            hits = []
            for rid in {r["run_id"] for r in cue if r["cond"] == c}:
                ii = [i for i, r in enumerate(cue) if r["run_id"] == rid]; mx = max(s_all[i] for i in ii)
                hits.append(np.mean([cue[i]["pair"] == "".join(gt[rid]["assigned_pair"]) for i in ii if s_all[i] == mx]))
            tr.setdefault("assigned_pair_top_rate", {})[f"llm_p2cue:{c}"] = round(float(np.mean(hits)), 3)
        out["n_p2cue_runs"] = len(cs)
    out["transfer_run_auroc_vs_rep_none"] = tr
    Path("results/analysis/p2_textlr.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(tr, indent=1))


if __name__ == "__main__":
    main()
