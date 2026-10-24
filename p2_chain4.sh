#!/bin/bash
# Phase 2 (E79 amendments): label + analyse each seller-family dataset when its generator exits.
cd "$(dirname "$0")"; export LABEL_PAR=1
for ds in llm_p2claude llm_p2sol llm_p2ds; do
  while pgrep -f -- "--ds $ds " > /dev/null; do sleep 60; done
  uv run python p2_label.py --ds $ds && uv run python p2_cue.py --ds $ds > /dev/null && echo "$ds analysed $(date -u)"
done
