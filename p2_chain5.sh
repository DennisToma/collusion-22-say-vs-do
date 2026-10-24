#!/bin/bash
# Phase 2 E92: run the frozen p2_logbook.py analysis ONCE when the logbook generator exits with 15 runs.
cd "$(dirname "$0")"
while pgrep -f -- "--ds llm_p2logbook" > /dev/null; do sleep 60; done
[ "$(wc -l < data/llm_p2logbook/ground_truth.jsonl)" -eq 15 ] && uv run python p2_logbook.py > logs/p2/logbook_analysis.log 2>&1 && echo "logbook analysed $(date -u)"
