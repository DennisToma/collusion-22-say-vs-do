#!/bin/bash
# Phase 2 (E89, directive 3b): frozen auditor views (all 6, gpt-6.1-sol, unchanged prompts) on new data.
# Reordered 2026-10-24 10:01 UTC (director directive 2): p2rep (fresh headline test) BEFORE p2cue; the p2cue audit
# still waits for sol sellers to exit so codex parallelism stays <= 6.
cd "$(dirname "$0")"
until grep -q "^p2rep done" logs/p2/chain.log; do sleep 60; done
uv run python p2_label.py --ds llm_p2rep && echo "p2rep labelled $(date -u)"
uv run python auditors.py --ds llm_p2rep --workers 2 && echo "p2rep audited $(date -u)"
until grep -q "^llm_p2cue analysed" logs/p2/post.log; do sleep 60; done
while pgrep -f "ds llm_p2sol" > /dev/null; do sleep 60; done
uv run python auditors.py --ds llm_p2cue --conds private,placebo,notes,none --workers 2 && echo "p2cue audited $(date -u)"
