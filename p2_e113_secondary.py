"""E113-secondary (registered with E113 16:16 / amend2 18:29; computed 2026-10-25 after the primary was read).

Executed-label contrast on Q1.4's E70 grid, 0 LLM calls: reads the FROZEN cached gpt-6.1-sol audit scores
(results/llm_auditor/ext_llm_grid_p2/) and Q1.4's per-game `executed` field (their E70 rule, distinct from our strict
rule; REPORT P2.7). Sealed E113 outputs (p2_e1_audit.json, lock, snapshot) are not touched.

  uv run python p2_e113_secondary.py snapshot   # copy Q1.4 results/eval/e70_grid.json -> data/ext_llm_grid_p2_e70/ (+sha, commit)
  uv run python p2_e113_secondary.py            # -> results/analysis/e113_secondary.json
"""
import hashlib, json, subprocess, sys
from pathlib import Path
from p2_cue import auc, boot_auc
from p2_e1_audit import SIB, VIEWS, load, cells, stratified_delta

SNAP = Path("data/ext_llm_grid_p2_e70")
OUTF = Path("results/analysis/e113_secondary.json")


def snapshot():
    src = SIB / "results/eval/e70_grid.json"
    raw = src.read_bytes()
    SNAP.mkdir(parents=True, exist_ok=True)
    (SNAP / "e70_grid.json").write_bytes(raw)
    commit = subprocess.run(["git", "-C", str(SIB), "log", "-1", "--format=%H", "--", "results/eval/e70_grid.json"],
                            capture_output=True, text=True).stdout.strip()
    (SNAP / "SOURCE.json").write_text(json.dumps({"source": str(src), "sha256": hashlib.sha256(raw).hexdigest(),
                                                  "sibling_commit_of_file": commit}, indent=1) + "\n")


def main():
    src = json.loads((SNAP / "SOURCE.json").read_text())
    raw = (SNAP / "e70_grid.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == src["sha256"]
    games = {g["run_id"]: g for g in json.loads(raw)["games"]}
    labs, S = load()
    C = cells()
    rows = []
    for r, l in labs.items():
        g = games[r]
        assert (g["cell"], g["sweep"], bool(g["channel"])) == (l["cell"], l["sweep"], bool(l["channel"])), r
        model = C[l["cell"]]["levels"]["model"]
        x = {"run_id": r, "cell": l["cell"], "y": int(l["channel"]), "model": model,
             "executed": bool(g["executed"]) if l["channel"] else None}
        for v in VIEWS:
            if v == "text" and not model.startswith("qwen"):
                continue  # registered text scope (E113-amend)
            if r in S[v] and S[v][r].get("collusion_present") is not None:
                x[v] = float(S[v][r]["collusion_present"])
        rows.append(x)
    qids = sorted(c for c in C if C[c]["levels"]["model"].startswith("qwen"))
    lids = sorted(c for c in C if c not in qids)
    res = {"source": src, "definition": "Q1.4 E70 executed rule (games[].executed; not Q2.2 strict)",
           "note": "computed after the E113 primary was read; registered secondary + DIRECTION 00:10 additions",
           "executed_counts": {}, "pooled": {}, "stratified": {}, "per_cell": {}}
    for name, ids in (("qwen", qids), ("luna", lids), ("all", qids + lids)):
        ch = [x for x in rows if x["cell"] in ids and x["y"]]
        res["executed_counts"][name] = [sum(x["executed"] for x in ch), len(ch)]
    subsets = {"executed_vs_A": lambda x: not x["y"] or x["executed"],
               "nonexecuted_vs_A": lambda x: not x["y"] or not x["executed"],
               "executed_vs_nonexecuted": lambda x: x["y"]}
    for sname, keep in subsets.items():
        lab = (lambda x: x["executed"]) if sname == "executed_vs_nonexecuted" else (lambda x: x["y"])
        for grp, ids in (("qwen", qids), ("luna", lids)):
            sub = [x for x in rows if x["cell"] in ids and keep(x)]
            for v in VIEWS:
                neg = [x[v] for x in sub if not lab(x) and v in x]; pos = [x[v] for x in sub if lab(x) and v in x]
                if len(neg) >= 3 and len(pos) >= 3:
                    res["pooled"][f"{sname}|{v}_{grp}"] = boot_auc(neg, pos) + [len(neg), len(pos)]
        if sname == "executed_vs_nonexecuted":
            continue
        sub = [x for x in rows if keep(x)]
        st = res["stratified"].setdefault(sname, {})
        st["qwen_combined_minus_action"] = stratified_delta(sub, qids, "combined", "action")
        st["qwen_combined_minus_text"] = stratified_delta(sub, qids, "combined", "text")
        st["luna_combined_minus_action"] = stratified_delta(sub, lids, "combined", "action")
        # post hoc, descriptive: luna cells with/without public posts (posting list from sealed E113 amend3)
        post = json.loads(Path("results/analysis/p2_e1_audit.json").read_text())["amend3"]["luna_posting_cells"]
        st["luna_posting_combined_minus_action_posthoc"] = stratified_delta(sub, post, "combined", "action")
        st["luna_silent_combined_minus_action_posthoc"] = stratified_delta(sub, [c for c in lids if c not in post], "combined", "action")
    for cid in sorted(C):  # registered per-cell form: executed channel vs all matched no-channel
        sub = [x for x in rows if x["cell"] == cid and (not x["y"] or x["executed"])]
        e = {"n": [sum(not x["y"] for x in sub), sum(x["y"] for x in sub)]}
        for v in VIEWS:
            e[f"auroc_{v}"] = auc([x[v] for x in sub if not x["y"] and v in x], [x[v] for x in sub if x["y"] and v in x])
        res["per_cell"][cid] = e
    OUTF.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "per_cell"}, indent=1))


if __name__ == "__main__":
    snapshot() if sys.argv[1:] == ["snapshot"] else main()
