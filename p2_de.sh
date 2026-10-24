#!/bin/bash
# E110 (Part E5, registered): German market generation, then frozen labels + text/action/combined auditor views.
cd "$(dirname "$0")"
SIM_PAR=2 uv run python llm_market.py --ds llm_p2de --framing lab --lang de --rounds 12 --matched private,none --matched-n 10 \
  --seed 8100 --games-parallel 2 > logs/p2de_gen.log 2>&1 && echo "p2de gen done $(date -u)" >> logs/p2de.log || exit 1
LABEL_PAR=1 uv run python p2_label.py --ds llm_p2de >> logs/p2de.log 2>&1 && echo "p2de labelled $(date -u)" >> logs/p2de.log
uv run python auditors.py --ds llm_p2de --views text,action,combined --workers 1 >> logs/p2de.log 2>&1 && echo "p2de audited $(date -u)" >> logs/p2de.log
