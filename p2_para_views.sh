#!/bin/bash
# Phase 2 E94 (directive 3; registered 09:58 UTC before any output): frozen auditor views text/action/combined/action_stats
# (gpt-6.1-sol, unchanged prompts) on the wording-band datasets: llm_p2para2 (terse) first, then llm_p2para1 (control).
# One-shot (not a chain); workers 1 to keep total codex parallelism down.
cd "$(dirname "$0")"
for ds in llm_p2para2 llm_p2para1; do
  uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 1 && \
    uv run python p2_family_views.py --ds $ds && echo "$ds views done $(date -u)"
done
