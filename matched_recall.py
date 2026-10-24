"""Post-lock DESCRIPTIVE check (iter 12; REPORT finding 4 said "no matched-recall comparison was run"): at matched
recall on the llm_v3 test y=1 runs, how many `legit` and `none` runs does each scorer flag? Thresholds are read off
the TEST positives (smallest threshold reaching TPR >= r), so this is an oracle operating point, not a deployable
rule; it only removes the operating-point confound when comparing scorers on legit partnerships. No CIs on the
threshold choice; Wilson intervals on the flag counts.

    uv run python matched_recall.py   # -> results/analysis/matched_recall_llm_v3_test.json
"""
import json
from pathlib import Path
import numpy as np
from monitor_stratum import load
from fp_stratum import wilson

RECALLS = (0.5, 0.7, 0.9)


def main():
    labs, S, _, ids = load("llm_v3", "gpt-6.1-sol")
    ids = [r for r in ids if int(r.rsplit("_", 1)[1]) >= 30]  # locked test split
    assert len(ids) == 95, len(ids)
    pos = [r for r in ids if labs[r]["y"]]
    grp = {c: [r for r in ids if labs[r]["condition"] == c] for c in ("legit", "none")}
    out = {"n": len(ids), "n_pos": len(pos), "group_n": {g: len(v) for g, v in grp.items()}, "by_recall": {}}
    for rec in RECALLS:
        row = {}
        for k in S:
            ps = np.sort([S[k][r]["run"] for r in pos])[::-1]
            t = float(ps[int(np.ceil(rec * len(ps))) - 1])  # flag if score >= t gives TPR >= rec (ties may raise it)
            tpr = float(np.mean([S[k][r]["run"] >= t for r in pos]))
            row[k] = {"threshold": t, "tpr": round(tpr, 3),
                      **{g: wilson(sum(S[k][r]["run"] >= t for r in rs), len(rs)) for g, rs in grp.items()},
                      "legit_count": f"{sum(S[k][r]['run'] >= t for r in grp['legit'])}/{len(grp['legit'])}",
                      "none_count": f"{sum(S[k][r]['run'] >= t for r in grp['none'])}/{len(grp['none'])}"}
        out["by_recall"][str(rec)] = row
    Path("results/analysis/matched_recall_llm_v3_test.json").write_text(json.dumps(out, indent=1))
    for rec, row in out["by_recall"].items():
        print(f"recall >= {rec}")
        for k, v in row.items():
            print(f"  {k:15s} tpr {v['tpr']:.2f}  legit {v['legit_count']:6s} none {v['none_count']}")


if __name__ == "__main__":
    main()
