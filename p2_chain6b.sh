#!/bin/bash
# Re-run of p2_chain6.sh (E91-ext, same registration): the 10:13 run made 0 audit calls because labels.jsonl for
# llm_p2sol/llm_p2ds did not exist yet (chain4 wrote them 10:20). No auditor output had been produced; nothing changed.
cd "$(dirname "$0")"
for ds in llm_p2ds llm_p2sol; do
  uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 2 && \
    uv run python p2_family_views.py --ds $ds && echo "$ds views done $(date -u)"
done
uv run python p2_family3way.py && echo "family3way done $(date -u)"
