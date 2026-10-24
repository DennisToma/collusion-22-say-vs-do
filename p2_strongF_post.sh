#!/bin/bash
# E99/E99-amend/E99-x/E103: cache completed games while generating, publish complete classes first,
# then evaluate frozen detectors ONCE after exact coverage/provenance checks. No new experiment.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs/final
exec 9>logs/final/strongF_post.flock
flock -n 9 || { echo "strongF post already running"; exit 0; }
trap 'echo "strongF post FAILED $(date -u), line $LINENO" >> logs/partc_chain.log' ERR
ds=llm_p2strongF
until grep -q "strongF gen done" logs/partc_chain.log 2>/dev/null; do
  LABEL_PAR=1 uv run python p2_label.py --ds "$ds" >> logs/strongF_prefetch.log 2>&1 || echo "label prefetch failed; retry later" >> logs/strongF_prefetch.log
  uv run python auditors.py --ds "$ds" --views text,action,combined,action_stats --workers 1 >> logs/strongF_prefetch.log 2>&1 || echo "auditor prefetch failed; retry later" >> logs/strongF_prefetch.log
  uv run python p2_plan_view.py --ds "$ds" --workers 1 >> logs/strongF_prefetch.log 2>&1 || echo "plan prefetch failed; retry later" >> logs/strongF_prefetch.log
  # Keep ~40 min between prefetch batches, but notice generation completion within a minute.
  for ((poll=0; poll<40; poll++)); do
    grep -q "strongF gen done" logs/partc_chain.log 2>/dev/null && break
    sleep 60
  done
done
uv run python p2_strong_eval.py --ds "$ds" --check-only
# This may extract uncached price-blind terms, but reads no detector scores.
LABEL_PAR=1 uv run python p2_strong_eval.py --ds "$ds" --classes-only > logs/strongF_classes.log 2>&1
echo "strongF classes ready $(date -u)" >> logs/partc_chain.log
uv run python p2_strong.py --ds "$ds" --min-floor 13 --late 11 --out results/analysis/p2_strongF.json > logs/strongF_strong.log 2>&1
LABEL_PAR=1 uv run python p2_label.py --ds "$ds"
uv run python auditors.py --ds "$ds" --views text,action,combined,action_stats --workers 2
uv run python p2_plan_view.py --ds "$ds" --workers 2
uv run python p2_strong_eval.py --ds "$ds" --min-floor 13 --late 11 > logs/strongF_eval.log 2>&1
echo "strongF post done $(date -u)" >> logs/partc_chain.log
