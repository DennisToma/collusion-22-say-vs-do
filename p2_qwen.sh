#!/bin/bash
# Part C3 (E100): base vs abliterated Qwen3.8-27B sellers, lab prompt, matched private/none, 15 seeds each.
# Base via the shared Aqueduct gateway (keep <= 2 parallel calls here); abliterated on Modal (budget guard: QWEN_BUDGET.txt).
cd "$(dirname "$0")"
mkdir -p logs
( SIM_PAR=2 uv run python llm_market.py --ds llm_p2qwenb --framing lab --rounds 12 --matched private,none --matched-n 15 --seed 8100 --games-parallel 1 --seller-backend qwen --seller-model qwen-base > logs/partc_qwenb.log 2>&1; echo "qwenb done $(date -u)" >> logs/partc_qwen.log ) &
( if ! grep -q STOPPED ~/collusion/QWEN_BUDGET.txt; then SIM_PAR=2 uv run python llm_market.py --ds llm_p2qwena --framing lab --rounds 12 --matched private,none --matched-n 15 --seed 8100 --games-parallel 1 --seller-backend qwen --seller-model qwen-abliterated > logs/partc_qwena.log 2>&1; fi; echo "qwena done $(date -u)" >> logs/partc_qwen.log ) &
wait
