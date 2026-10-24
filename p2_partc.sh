#!/bin/bash
# Part C generation (E97 C1 pilot, E98 C2 older sellers). Logs -> logs/partc_*.log
cd "$(dirname "$0")"
mkdir -p logs
( SIM_PAR=2 uv run python llm_market.py --ds llm_p2strong_luna --framing strong --rounds 40 --matched private,none --matched-n 3 --seed 9700 --games-parallel 2 > logs/partc_luna.log 2>&1
  SIM_PAR=2 uv run python llm_market.py --ds llm_p2g56sol --framing lab --rounds 12 --matched private,none --matched-n 7 --seed 8100 --games-parallel 2 --seller-model gpt-5.6-sol > logs/partc_g56sol.log 2>&1 ) &
( SIM_PAR=2 uv run python llm_market.py --ds llm_p2strong_sol --framing strong --rounds 40 --matched private,none --matched-n 2 --seed 9700 --games-parallel 2 --seller-model gpt-6.1-sol > logs/partc_sol.log 2>&1 ) &
( uv run python llm_market.py --ds llm_p2mimo --framing lab --rounds 12 --matched private,none --matched-n 7 --seed 8100 --games-parallel 1 --seller-backend go --seller-model mimo-v2.5 > logs/partc_mimo.log 2>&1 ) &
wait
