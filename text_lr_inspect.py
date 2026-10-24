"""Post-headline exploration (after HEADLINE_DONE): what does the supervised public-text LR key on?
Fits the same TF-IDF(1-2gram)+LR as baselines.py on ALL llm_v3 pair records (descriptive, not an evaluation) and
lists the top n-grams, then counts how often the top positive n-grams occur in colluding-pair vs other-pair messages.
    uv run python text_lr_inspect.py  -> results/analysis/text_lr_inspect.json
"""
import json, re
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from features import load, load_gt, pair_features, PAIRS
d = Path("data/llm_v3")
labs = {json.loads(l)["run_id"]: json.loads(l) for l in open(d / "labels.jsonl")}
runs, gt = load(d / "trajectories.jsonl"), load_gt(d / "ground_truth.jsonl")
recs = []
for rid in sorted(r for r in runs if r in labs):
    f = pair_features(runs[rid]); y = labs[rid]["agreement"] in ("explicit", "info_exchange")
    for pr in PAIRS:
        recs.append({"run_id": rid, "pair": pr, "text": f[pr]["text"], "cond": gt[rid]["condition"],
                     "y": int(y and pr == "".join(gt[rid]["assigned_pair"]))})
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
X = vec.fit_transform([r["text"] for r in recs]); y = np.array([r["y"] for r in recs])
m = LogisticRegression(C=1.0, max_iter=5000).fit(X, y)
voc = np.array(vec.get_feature_names_out()); w = m.coef_[0]; o = np.argsort(w)
top_pos = [(voc[i], round(float(w[i]), 2)) for i in o[::-1][:25]]; top_neg = [(voc[i], round(float(w[i]), 2)) for i in o[:15]]
def rate(term, sel):
    rs = [r for r in recs if sel(r)]
    return round(sum(bool(re.search(r"\b" + re.escape(term) + r"\b", r["text"].lower())) for r in rs) / len(rs), 3), len(rs)
groups = {"colluding_pair": lambda r: r["y"] == 1, "other_pairs_private_runs": lambda r: r["cond"] == "private" and r["y"] == 0,
          "pairs_none_runs": lambda r: r["cond"] == "none", "pairs_legit_runs": lambda r: r["cond"] == "legit"}
occ = {t: {g: rate(t, f) for g, f in groups.items()} for t, _ in top_pos[:12]}
out = {"note": "descriptive fit on all 125 runs after the locked headline; not an evaluation", "top_positive": top_pos,
       "top_negative": top_neg, "occurrence_rate_of_top_positive_ngrams": occ}
Path("results/analysis/text_lr_inspect.json").write_text(json.dumps(out, indent=1))
print("TOP +", top_pos); print("TOP -", top_neg)
for t, v in occ.items(): print(f"{t!r:30} " + "  ".join(f"{g}={r}" for g, (r, n) in v.items()))
