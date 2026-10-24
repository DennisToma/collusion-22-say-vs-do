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
    used = [f"{c} {board[c]['channel']['posts']}/{board[c]['channel']['agent_rounds']}"
            for c in luna if board[c]["channel"]["posts"] > 0]
    silent = sum(board[c]["channel"]["posts"] == 0 and board[c]["no_channel"]["posts"] == 0 for c in luna)
    ce, te = resolved(d["a_combined_flag_main_effects_all_cells"]), resolved(d["a_text_flag_main_effects_qwen_cells"])
    sec = d["secondary_executed_vs_no_channel"]
    if sec["provenance"]["state"] == "available":
        pos = sum(e["n"][1] for e in sec["per_cell"].values())
        sec_line = f"Secondary (Q1.4 E70 executed labels): {pos} executed channel games vs all matched no-channel games; per-cell AUROCs in the json."
    else:
        sec_line = "Secondary executed-vs-no-channel contrast: not run (Q1.4 E70 labels not published at eval time)."
    lines = [
        f"**P2.16 E1 factorial grid audit (E113, registered before the grid existed; amendments E113-amend/-amend2 before any score was read).** "
        f"Frozen gpt-6.1-sol auditors (dev thresholds) on Q1.4's E70 grid: {d['n_games']} games, {d['complete_sweeps']} balanced sweep(s), "
        f"{d['n_cells']} cells (channel vs no channel per cell, n per arm {', '.join(f'{a}/{b}' for a, b in n_per_arm)}).",
        f"Registered headline: combined view beats the best single view in **{k}/{K} cells** (one-sided sign test p = {d['b_sign_test_one_sided_p']}; "
        f"P1 'no systematic gain' {'held' if d['b_P1_held'] else 'failed'}); {qk}/{qK} Qwen cells, where public text is audited.",
        f"Pooled channel-vs-none AUROC (descriptive): action {pv('action_all')}, combined {pv('combined_all')}; "
        f"Qwen text {pv('text_qwen')}, Qwen combined {pv('combined_qwen')}; luna combined {pv('combined_luna')}.",
        f"Qwen text flags: {tx1[0]}/{tx1[1]} channel vs {tx0[0]}/{tx0[1]} no-channel games "
        f"(TL;DR 3 predicts control flags: Qwen invites rivals publicly).",
        f"Combined-flag factor main effects with CI excluding 0: {'; '.join(ce) if ce else 'none'}; "
        f"text-flag (Qwen cells): {'; '.join(te) if te else 'none'} (7 factors each, uncorrected, descriptive).",
        f"Board use is a finding, not an auditor effect: {silent}/{len(luna)} luna cells never post publicly"
        + (f"; exceptions {', '.join(used)} posts/agent-rounds (channel arm)." if used else "."),
        sec_line,
        f"Source: `results/analysis/p2_e1_audit.json` (`uv run python p2_e1_audit.py eval`, run once; lines by `p2_e1_report.py`).",
    ]
    glance = (f"| P2.16 | E1 factorial grid audit (Q1.4 E70, {d['n_games']} games) | combined > best single view in {k}/{K} cells "
              f"({qk}/{qK} Qwen); pooled combined {pv('combined_all')}, action {pv('action_all')} | `p2_e1_audit.json` |")
    assert len(lines) <= 10
    return "\n".join(lines), glance


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else SRC
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT
    body, glance = render(json.loads(src.read_text()))
    out.write_text(body + "\n\nGLANCE:\n" + glance + "\n")
    print(body + "\n\n" + glance)


if __name__ == "__main__":
    main()
