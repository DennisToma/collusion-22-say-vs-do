#!/bin/bash
# E99 + E99-amend + E103 post-processing (registered before outputs): after llm_p2strongF generation exits ->
# judge labels, frozen auditor views (text, action, combined, action_stats), E103 plan view, p2_strong + p2_strong_eval
# (min-floor 13, late 11; behaviour classes -> results/analysis/p2_strong_classes_llm_p2strongF.json). Each runs ONCE.
cd "$(dirname "$0")"
ds=llm_p2strongF
# prefetch (cache only, nothing evaluated): audit completed games every ~40 min at parallelism 1 while generation runs
until grep -q "strongF gen done" logs/partc_chain.log 2>/dev/null; do
  LABEL_PAR=1 uv run python p2_label.py --ds $ds > /dev/null 2>&1
  uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 1 > /dev/null 2>&1
  uv run python p2_plan_view.py --ds $ds --workers 1 > /dev/null 2>&1
  sleep 2400
done
uv run python p2_label.py --ds $ds && \
uv run python auditors.py --ds $ds --views text,action,combined,action_stats --workers 2 && \
uv run python p2_plan_view.py --ds $ds --workers 2 && \
uv run python p2_strong.py --ds $ds --min-floor 13 --late 11 --out results/analysis/p2_strongF.json > logs/strongF_strong.log 2>&1 && \
uv run python p2_strong_eval.py --ds $ds --min-floor 13 --late 11 > logs/strongF_eval.log 2>&1 && echo "strongF post done $(date -u)" >> logs/partc_chain.log
