"""Failure/complementarity gallery: rule-selected cases (no hand-picking) with scores from every scorer.

Cases (first match by run id within the split):
  1 text_miss      y=1, premium top pair correct, text auditor's assigned-pair score <= its median pair score
  2 acted_not      y=1 with realised assigned-pair premium <= 0.5 (agreement not visibly acted on)
  3 legit_pair     legit run: does the partnership pair get flagged by premium vs by the LLM views?
  4 llm_beats_stat y=1 where structured localises the pair (top) but premium does not
  5 tacit_none     none run with the highest markup (supra-competitive without a channel)

    uv run python gallery.py --split dev   > results/analysis/gallery_dev.md
"""
import argparse, json
from pathlib import Path
import numpy as np
from analyze_llm import load_jsonl, PAIRS
from final_analysis import LLM_VIEWS, premium_scores, idx, DEV_MAX


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    ap.add_argument("--auditor", default="gpt-6.1-sol")
    ap.add_argument("--split", default="dev", choices=["dev", "test", "all"])
    a = ap.parse_args()
    labs = {x["run_id"]: dict(x, y=int(x["agreement"] in ("explicit", "info_exchange")))
            for x in load_jsonl(Path("data") / a.ds / "labels.jsonl")}
    d = Path("results") / "llm_auditor" / a.ds / a.auditor
    S = {v: {x["run_id"]: x for x in load_jsonl(d / f"{v}_orig.jsonl")} for v in LLM_VIEWS}
    S = {v: R for v, R in S.items() if R}
    prem, markup = premium_scores(a.ds)
    traj = {}
    for r in load_jsonl(Path("data") / a.ds / "trajectories.jsonl"):
        traj.setdefault(r["run_id"], []).append(r)
    ids = sorted(r for r in labs if all(r in R for R in S.values())
                 and (a.split == "all" or (idx(r) < DEV_MAX) == (a.split == "dev")))
    ap_ = lambda r: "".join(labs[r]["assigned_pair"])
    top = lambda sc: [p for p in PAIRS if sc[p] == max(sc.values())]
    rules = [
        ("text_miss", "positive run; price premium localises the pair, text auditor does not",
         lambda r: labs[r]["y"] and top(prem[r]["scores"]) == [ap_(r)] and "text" in S
         and S["text"][r]["scores"][ap_(r)] <= np.median(list(S["text"][r]["scores"].values()))),
        ("acted_not", "positive run whose agreement was not visibly acted on (assigned-pair premium <= 0.5)",
         lambda r: labs[r]["y"] and labs[r]["pair_premium"] <= 0.5),
        ("legit_pair", "legit partnership pair (hard negative)", lambda r: labs[r]["condition"] == "legit"),
        ("llm_beats_stat", "structured auditor localises the pair, premium does not",
         lambda r: labs[r]["y"] and "structured" in S and top(S["structured"][r]["scores"]) == [ap_(r)]
         and ap_(r) not in top(prem[r]["scores"])),
    ]
    out, used = [], set()
    for name, desc, f in rules:  # each case a different run
        hit = next((r for r in ids if r not in used and f(r)), None)
        used.add(hit)
        out.append((name, desc, hit))
    nones = [r for r in ids if labs[r]["condition"] == "none"]
    out.append(("tacit_none", "no-channel run with the highest markup over cost", max(nones, key=lambda r: markup[r]) if nones else None))
    print(f"# Case gallery ({a.split} split, rule-selected by `gallery.py`)\n")
    for name, desc, r in out:
        print(f"## {name}: {desc}")
        if r is None:
            print("_no run in this split matches the rule_\n"); continue
        L = labs[r]
        print(f"`{r}` condition={L['condition']} label={L['agreement']} assigned pair={ap_(r)} "
              f"realised pair premium={L['pair_premium']:+.2f} markup={markup[r]:.2f}")
        if L.get("evidence"):
            print(f"- private-chat label evidence (auditors never see this): {L['evidence'][:300]}")
        print("\n| scorer | score of assigned pair | top pair(s) | run score |\n|---|---|---|---|")
        print(f"| premium | {prem[r]['scores'][ap_(r)]:+.2f} | {','.join(top(prem[r]['scores']))} | {prem[r]['run']:+.2f} |")
        for v, R in S.items():
            x = R[r]
            print(f"| {v} | {x['scores'][ap_(r)]:.0f} | {','.join(top(x['scores']))} | {x['collusion_present']:.0f} |")
        rows = traj[r]
        print("\nprices per round: " + "; ".join("".join(f"{x['id']}{x['price']} " for x in t["agents"]).strip() for t in sorted(rows, key=lambda t: t["round"])))
        t3 = sorted(rows, key=lambda t: t["round"])[min(3, len(rows) - 1)]
        print("\nround 4 public messages: " + " | ".join(f"{x['id']}: \"{(x['public_message'] or '')[:110]}\"" for x in t3["agents"]))
        if "structured" in S:
            ev = S["structured"][r].get("evidence") or []
            print("\nstructured-auditor evidence: " + " / ".join(f"r{e.get('round')} {e.get('firm')}: {e.get('observation')}" for e in ev[:3]))
        print()


if __name__ == "__main__":
    main()
