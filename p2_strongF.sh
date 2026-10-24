#!/bin/bash
# E99 (registered before generation): C1 full arm, luna strong framing, T=40, 20 matched seeds x private/none.
cd "$(dirname "$0")"
SIM_PAR=3 uv run python llm_market.py --ds llm_p2strongF --framing strong --rounds 40 --matched private,none --matched-n 20 \
  --seed 9800 --games-parallel 3 > logs/partc_strongF.log 2>&1 && echo "strongF gen done $(date -u)" >> logs/partc_chain.log
