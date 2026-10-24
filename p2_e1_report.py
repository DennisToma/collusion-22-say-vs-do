"""E113 formatter: turn the sealed p2_e1_audit.json into <= 10 REPORT lines + one glance row.

Pure formatting, 0 LLM calls, no recomputation: every number is read from the eval JSON.
Usage: uv run python p2_e1_report.py [results/analysis/p2_e1_audit.json] [out.md]
Written and tested on synthetic fixtures (tests/test_e1_completion.py) before the real eval exists.
"""
import json
import sys
from pathlib import Path

SRC = Path("results/analysis/p2_e1_audit.json")
OUT = Path("results/analysis/p2_e1_report.md")


def ci(x):
    return f"{x[0]:.2f} [{x[1]:.2f}, {x[2]:.2f}]"


def diff(x):
    if x == "not_estimable":
        return "n/e"
    d = x["diff"]
    return f"{d[0]:+.2f} [{d[1]:+.2f}, {d[2]:+.2f}]"


def resolved(effects):
    """Factors whose game-bootstrap CI excludes 0 (descriptive; 7 factors, no multiplicity correction)."""
    return [f"{f} {diff(x)}" for f, x in effects.items()
            if x != "not_estimable" and (x["diff"][1] > 0 or x["diff"][2] < 0)]


def render(d):
    k, K = d["b_cells_combined_gt_best_single"]
    qk, qK = d["b_qwen_cells_combined_gt_best_single"]
    per = d["c_per_cell_appendix"]
    n_per_arm = sorted({tuple(e["n"]) for e in per.values()})
    pooled = d["pooled_auroc_channel_vs_none_descriptive"]
    pv = lambda key: ci(pooled[key]) if key in pooled else "n/a"
    tx = d["a_text_flag_rate_by_arm_qwen"]
    tx0, tx1 = tx.get("0", tx.get(0)), tx.get("1", tx.get(1))
    board = d["board_usage_per_cell_arm"]
    luna = [c for c, e in per.items() if not e["model"].startswith("qwen")]
    used = [f"{c} channel {board[c]['channel']['posts']}/{board[c]['channel']['agent_rounds']}, "
            f"no-channel {board[c]['no_channel']['posts']}/{board[c]['no_channel']['agent_rounds']}"
            for c in luna if any(board[c][a]["posts"] > 0 for a in ("channel", "no_channel"))]
    silent = sum(board[c]["channel"]["posts"] == 0 and board[c]["no_channel"]["posts"] == 0 for c in luna)
    ce, te = resolved(d["a_combined_flag_main_effects_all_cells"]), resolved(d["a_text_flag_main_effects_qwen_cells"])
    sec = d["secondary_executed_vs_no_channel"]
    if sec["provenance"]["state"] == "available":
        pos = sum(e["n"][1] for e in sec["per_cell"].values())
        sec_line = f"Secondary (Q1.4 E70 executed labels): {pos} executed channel games vs all matched no-channel games; per-cell AUROCs in the json."
    else:
        sec_line = "Secondary executed-vs-no-channel contrast: not run (Q1.4 E70 labels not published at eval time)."
    m = d["amend3"]
    sd = lambda x: f"{x['delta']:+.2f} [{x['ci'][0]:+.2f}, {x['ci'][1]:+.2f}] ({x['n_cells']} cells)" if x else "n/a"
    qs, al = m["qwen_sign_counts"], m["all_sign_counts"]
    qca, qct = m["qwen_stratified_combined_minus_action"], m["qwen_stratified_combined_minus_text"]
    p1 = ("held: a weak confirmation" if d["b_P1_held"] else "failed")
    lines = [
        f"**P2.16 E1 factorial grid audit (E113, registered before the grid existed; amendments E113-amend/-amend2/-amend3 before any score was read).** "
        f"Frozen gpt-6.1-sol auditors (dev thresholds) on Q1.4's E70 grid: {d['n_games']} games, {d['complete_sweeps']} balanced sweep(s), "
        f"{d['n_cells']} cells (channel vs no channel per cell, n per arm {', '.join(f'{a}/{b}' for a, b in n_per_arm)}).",
        f"Headline (8 Qwen cells, where public text exists; amend3): combined beats the best single view in **{qs['pos']}/{qK} cells** "
        f"({qs['tie']} ties, {qs['neg']} worse); cell-stratified pooled Δ combined − action {sd(qca)}, combined − text {sd(qct)}.",
        f"Registered P1 over 16 cells: {k}/{K} positive ({al['tie']} ties, {al['neg']} negative; one-sided sign test p = {d['b_sign_test_one_sided_p']}), "
        f"P1 'no systematic gain' {p1}. Per-cell max(text, action) selection biases Δ downward and ties count toward P1; the stratified Δ is the informative number.",
        f"Luna combined − action {sd(m['luna_stratified_combined_minus_action_noise'])}; no separate text audit was registered. "
        + (f"Posting cells (posts/agent-rounds): {'; '.join(used)}; posting-cell Δ "
           f"{sd(m['luna_posting_stratified_combined_minus_action'])}; " if m["luna_posting_cells"] else "")
        + f"silent-cell Δ {sd(m['luna_silent_stratified_combined_minus_action'])} estimates auditor re-prompt noise with no text input.",
        f"Unstratified pooled channel-vs-none AUROC (raw scores pooled across cells; descriptive): action {pv('action_all')}, combined {pv('combined_all')}; "
        f"Qwen text {pv('text_qwen')}. Qwen text flags: {tx1[0]}/{tx1[1]} channel vs {tx0[0]}/{tx0[1]} no-channel games (TL;DR 3 predicts control flags: Qwen invites rivals publicly).",
        f"Combined-flag factor main effects with CI excluding 0: {'; '.join(ce) if ce else 'none'}; "
        f"text-flag (Qwen cells): {'; '.join(te) if te else 'none'} (7 factors each, uncorrected, descriptive). "
        f"{silent}/{len(luna)} luna cells never post publicly (a finding about the sellers, not the auditor).",
        sec_line,
        f"Source: `results/analysis/p2_e1_audit.json` (`uv run python p2_e1_audit.py eval`, run once; lines by `p2_e1_report.py`).",
    ]
    glance = (f"| P2.16 | E1 factorial grid audit (Q1.4 E70, {d['n_games']} games) | Qwen cells: combined > best single in {qs['pos']}/{qK} "
              f"({qs['tie']} ties); stratified Δ combined − action {sd(qca)}; silent luna re-prompt noise {sd(m['luna_silent_stratified_combined_minus_action'])} | `p2_e1_audit.json` |")
    clause = (f"combined exceeds the best single view in {qs['pos']}/{qK} Qwen cells of Q1.4's 16-cell grid "
              f"({qs['tie']} ties); cell-stratified Δ combined − action {sd(qca)}")
    assert len(lines) <= 10
    return "\n".join(lines), glance, clause


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else SRC
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT
    body, glance, clause = render(json.loads(src.read_text()))
    out.write_text(body + "\n\nGLANCE:\n" + glance + "\n\nABSTRACT CLAUSE:\n" + clause + "\n")
    print(body + "\n\n" + glance + "\n\n" + clause)


if __name__ == "__main__":
    main()
