#!/bin/bash
# Part C3c (E109): Qwen3.5-9B abliterated vs base, both Modal L4 FP8 (identical serving). Usage: ./p2_qwen9.sh pilot|full
cd "$(dirname "$0")"
mkdir -p logs
stage=${1:-pilot}
if [ "$stage" = pilot ]; then sfx=p; n=2; seed=8700; else sfx=""; n=15; seed=8100; fi
grep -q STOPPED ~/collusion/QWEN_BUDGET.txt && { echo "qwen9 $stage skipped: budget STOPPED $(date -u)" >> logs/partc_qwen9.log; exit 0; }
for m in b a; do
  model=$([ $m = b ] && echo qwen9-base || echo qwen9-abliterated)
  ( SIM_PAR=4 uv run python llm_market.py --ds llm_p2q9${sfx}${m} --framing lab --rounds 12 --matched private,none --matched-n $n \
      --seed $seed --games-parallel 2 --seller-backend qwen --seller-model $model > logs/partc_q9${sfx}${m}.log 2>&1
    echo "qwen9 $stage $model done rc=$? $(date -u)" >> logs/partc_qwen9.log ) &
done
wait
