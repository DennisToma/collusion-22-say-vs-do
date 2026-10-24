#!/bin/bash
# Phase 2 E91-ext (registered 09:24 UTC before any ds/sol auditor output): frozen auditor views text, action, combined,
# action_stats (gpt-6.1-sol, unchanged prompts) on llm_p2sol and llm_p2ds after each generator exits.
# Waits for chain3's llm_p2cue audit so our codex auditor parallelism stays at 2.
cd "$(dirname "$0")"
for ds in llm_p2sol llm_p2ds; do
  while pgrep -f -- "--ds $ds " > /dev/null; do sleep 60; done
  while pgrep -f -- "auditors.py --ds llm_p2cue" > /dev/null; do sleep 60; done
  uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 2 && \
    uv run python p2_family_views.py --ds $ds && echo "$ds views done $(date -u)"
done
