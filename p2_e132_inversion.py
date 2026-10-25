"""E132 (exploratory, post hoc; registered before computing): does the text-auditor inversion come from channel pairs
moving invitation talk off the public board? Zero LLM calls: saved transcripts + FROZEN cached gpt-6.1-sol text scores.

Per run: public messages (non-empty), hits of the frozen public-invitation regex (p2_family3way.RX), hit rate.
  (i)   arm means (channel vs no-channel);
  (ii)  Spearman(text score, invite count / rate), pooled over arms and within the no-channel arm alone;
  (iii) no-LLM baseline: AUROC of "fewer public invites => channel" vs the text auditor's AUROC on the same runs.
uv run python p2_e132_inversion.py -> results/analysis/e132_inversion.json
"""
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from p2_cue import boot_auc
from p2_family3way import RX

AUD = "results/llm_auditor/{}/gpt-6.1-sol/text_orig.jsonl"
SETS = {"Claude Sonnet": "llm_p2claude", "deepseek": "llm_p2ds", "Qwen3.8 base": "llm_p2qwenb",
        "Qwen3.8 abliterated": "llm_p2qwena", "Qwen3.6 E70 grid (8 cells)": "ext_llm_grid_p2"}


def arm(ds, row):
    if ds == "ext_llm_grid_p2":
        return int(row["channel"]) if row["condition"].startswith("qwen") else None
    return {"private": 1, "none": 0}.get(row["condition"])


def boot_spearman(x, y, B=2000):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rng = np.random.default_rng(0)
    b = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) > 0 and np.ptp(y[i]) > 0:
            b.append(spearmanr(x[i], y[i])[0])
    r = spearmanr(x, y)[0]
    return [round(float(r), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3), len(x)]


def one(ds):
    y = {}
    for l in open(f"data/{ds}/labels.jsonl"):
        r = json.loads(l); a = arm(ds, r)
        if a is not None:
            y[r["run_id"]] = a
    msgs, hits = defaultdict(int), defaultdict(int)
    for l in open(f"data/{ds}/trajectories.jsonl"):
        t = json.loads(l)
        if t["run_id"] not in y:
            continue
        for ag in t["agents"]:
            m = (ag.get("public_message") or "").strip()
            if m:
                msgs[t["run_id"]] += 1; hits[t["run_id"]] += bool(RX.search(m))
    S = {}
    for l in open(AUD.format(ds)):
        r = json.loads(l)
        if r["run_id"] in y and r.get("collusion_present") is not None:
            S[r["run_id"]] = float(r["collusion_present"])
    runs = sorted(r for r in y if r in S)
    rate = {r: hits[r] / msgs[r] if msgs[r] else 0.0 for r in runs}
    out = {"n_runs": [sum(y[r] == 0 for r in runs), sum(y[r] == 1 for r in runs)], "arms": {}}
    for a, name in ((0, "no_channel"), (1, "channel")):
        R = [r for r in runs if y[r] == a]
        out["arms"][name] = {"public_msgs_per_run": round(float(np.mean([msgs[r] for r in R])), 1),
                             "invite_hits_per_run": round(float(np.mean([hits[r] for r in R])), 1),
                             "invite_rate_pooled": round(sum(hits[r] for r in R) / max(1, sum(msgs[r] for r in R)), 3),
                             "mean_text_score": round(float(np.mean([S[r] for r in R])), 1)}
    A = [r for r in runs if y[r] == 0]
    for key, f in (("count", hits), ("rate", rate)):
        out[f"spearman_text_vs_invite_{key}_pooled"] = boot_spearman([S[r] for r in runs], [f[r] for r in runs])
        out[f"spearman_text_vs_invite_{key}_within_no_channel"] = (
            boot_spearman([S[r] for r in A], [f[r] for r in A]) if np.ptp([f[r] for r in A]) > 0 and np.ptp([S[r] for r in A]) > 0 else "constant")
    neg = lambda f: ([-f[r] for r in runs if y[r] == 0], [-f[r] for r in runs if y[r] == 1])
    out["auroc_fewer_invites_count"] = boot_auc(*neg(hits))
    out["auroc_fewer_invites_rate"] = boot_auc(*neg(rate))
    out["auroc_text_auditor_same_runs"] = boot_auc([S[r] for r in runs if y[r] == 0], [S[r] for r in runs if y[r] == 1])
    return out


def main():
    res = {"regex": RX.pattern, "note": "exploratory/post hoc (E132); E100 Qwen3.8 regex counts were seen before registration",
           "sets": {name: one(ds) for name, ds in SETS.items()}}
    Path("results/analysis/e132_inversion.json").write_text(json.dumps(res, indent=1) + "\n")
    for name, d in res["sets"].items():
        a0, a1 = d["arms"]["no_channel"], d["arms"]["channel"]
        print(f"{name}: n={d['n_runs']} invites/run A {a0['invite_hits_per_run']} vs C {a1['invite_hits_per_run']}; "
              f"rate A {a0['invite_rate_pooled']} vs C {a1['invite_rate_pooled']}; msgs/run A {a0['public_msgs_per_run']} C {a1['public_msgs_per_run']}; "
              f"rho pooled {d['spearman_text_vs_invite_count_pooled']} withinA {d['spearman_text_vs_invite_count_within_no_channel']}; "
              f"AUROC fewer-invites {d['auroc_fewer_invites_count']} rate {d['auroc_fewer_invites_rate']} text {d['auroc_text_auditor_same_runs']}")


if __name__ == "__main__":
    main()
