#!/bin/bash
# E102 (C3 x C1): strong lever set with base vs abliterated Qwen, T=40, 6 matched seeds each; runs after E100 per model.
cd "$(dirname "$0")"
( while pgrep -f "ds llm_p2qwenb " >/dev/null; do sleep 60; done
  SIM_PAR=2 uv run python llm_market.py --ds llm_p2qwenbS --framing strong --rounds 40 --matched private,none --matched-n 6 --seed 9700 --games-parallel 1 --seller-backend qwen --seller-model qwen-base > logs/partc_qwenbS.log 2>&1; echo "qwenbS done $(date -u)" >> logs/partc_qwen.log ) &
( while pgrep -f "ds llm_p2qwena " >/dev/null; do sleep 60; done
  if ! grep -q STOPPED ~/collusion/QWEN_BUDGET.txt; then SIM_PAR=2 uv run python llm_market.py --ds llm_p2qwenaS --framing strong --rounds 40 --matched private,none --matched-n 6 --seed 9700 --games-parallel 2 --seller-backend qwen --seller-model qwen-abliterated > logs/partc_qwenaS.log 2>&1; fi; echo "qwenaS done $(date -u)" >> logs/partc_qwen.log ) &
wait
