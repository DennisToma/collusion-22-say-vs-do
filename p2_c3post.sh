#!/bin/bash
# E100 post-processing (registered analysis): per qwen dataset after its generator exits -> judge labels, frozen auditor
# views (text, action, combined, action_stats; gpt-6.1-sol, codex workers 2), p2_strong (min-floor 12, late 2), p2_strong_eval.
cd "$(dirname "$0")"
for ds in llm_p2qwena llm_p2qwenb; do
  sleep 120
  while pgrep -f -- "--ds $ds " > /dev/null; do sleep 60; done
  uv run python p2_label.py --ds $ds && \
  uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 2 && \
  uv run python p2_strong_eval.py --ds $ds --min-floor 12 --late 2 > logs/c3_eval_$ds.log 2>&1 && echo "$ds post done $(date -u)"
done
uv run python p2_strong.py --ds llm_p2qwenb llm_p2qwena --min-floor 12 --late 2 --out results/analysis/p2_qwen.json > logs/c3_strong.log 2>&1 && echo "c3 strong done $(date -u)"
