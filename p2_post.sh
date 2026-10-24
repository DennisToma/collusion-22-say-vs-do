#!/bin/bash
# Phase 2: label + analyse each matched dataset as soon as its generation finishes (markers in logs/p2/chain.log).
cd "$(dirname "$0")"; export LABEL_PAR=1
for ds in p2cue p2para1 p2para2; do
  until grep -q "^$ds done" logs/p2/chain.log; do sleep 60; done
  uv run python p2_label.py --ds llm_$ds && uv run python p2_cue.py --ds llm_$ds > /dev/null && echo "llm_$ds analysed $(date -u)"
done
