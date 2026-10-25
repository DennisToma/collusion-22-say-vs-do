"""E133 sensitivity (post hoc, zero LLM calls): cell-cluster bootstrap for the E133/E133c/E133d deltas.

Critics (codex + Opus review, 2026-10-25 03:1x) noted that the game bootstrap ignores within-cell correlation
(16 cells, CV already holds out whole cells). Same out-of-fold scores and cached LLM p_kept as the original
scripts; only the resampling unit changes (cells with replacement). Writes results/analysis/e133_cluster.json.
Run: uv run python p2_e133_cluster.py
"""
import json
from pathlib import Path
import numpy as np
import p2_e133_privileged as E

rows, _ = E.grid_rows()
C = {m: {j["run_id"]: j for j in map(json.loads, open(f"results/llm_auditor/e133c/gpt-6.1-sol_{m}.jsonl"))}
     for m in ("privileged", "noprivate")}
for r in rows:
    if r["say_do_gap"] is None:
        r["say_do_gap"] = np.nan
y = np.array([r["y"] for r in rows]); cell = np.array([r["cell"] for r in rows])
S = {"b": E.oof(rows, E.B_FEATS), "ab": E.oof(rows, E.B_FEATS + E.A_FEATS),
     "c": np.array([C["privileged"][r["run_id"]]["p_kept"] for r in rows], float),
     "d": np.array([C["noprivate"][r["run_id"]]["p_kept"] for r in rows], float)}


def A(s, idx):
    return E.auc(list(s[idx][y[idx] == 0]), list(s[idx][y[idx] == 1]))


PAIRS = {"E133_ab_minus_b": ("ab", "b"), "E133c_c_minus_b": ("c", "b"),
         "E133d_d_minus_b": ("d", "b"), "E133cd_c_minus_d": ("c", "d")}
cells = sorted(set(cell)); by = {c: np.where(cell == c)[0] for c in cells}
rng = np.random.default_rng(0); bs = {k: [] for k in PAIRS}; B = 2000
for _ in range(B):
    idx = np.concatenate([by[c] for c in rng.choice(cells, len(cells))])
    if 0 < y[idx].sum() < len(idx):
        for k, (p, q) in PAIRS.items():
            bs[k].append(A(S[p], idx) - A(S[q], idx))
al = np.arange(len(y))
out = {"note": "post hoc sensitivity: cell-cluster bootstrap (16 cells resampled with replacement), same scores as E133/E133c/E133d",
       "n": len(y), "n_cells": len(cells), "B": B,
       "cluster_ci": {k: [round(A(S[p], al) - A(S[q], al), 3), round(float(np.percentile(bs[k], 2.5)), 3),
                          round(float(np.percentile(bs[k], 97.5)), 3)] for k, (p, q) in PAIRS.items()}}
Path("results/analysis/e133_cluster.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
