#!/bin/bash
# Iter 8 exploration chain: after llm_v3 and llm_v3fp generation, generate the monitored stratum llm_v3mon
# (lab framing + public price monitor; private:14, none:6), label + audit it, then run monitor_stratum.py.
# Respects DIRECTION: no new generation launched after 03:30 UTC. Serial after v3fp keeps LLM parallelism <= ~7.
cd "$(dirname "$0")"
while pgrep -f "llm_market.py --ds llm_v3 " >/dev/null; do sleep 60; done
sleep 120
while pgrep -f "llm_market.py --ds llm_v3fp " >/dev/null; do sleep 60; done
if [ "$(date -u +%H%M)" -gt 0330 ] && [ "$(date -u +%H%M)" -lt 1200 ]; then echo "$(date -u +%H:%M) past 03:30 cutoff; not launching"; exit 0; fi
echo "$(date -u +%H:%M) llm_v3mon generation start"
uv run python llm_market.py --ds llm_v3mon --plan private:14,none:6 --rounds 12 --framing lab_monitored --games-parallel 1 --seed 7000 \
  > logs/gen_v3mon.log 2>&1 && ./pipeline.sh llm_v3mon > logs/pipeline_v3mon.log 2>&1
echo "$(date -u +%H:%M) llm_v3mon labelled+audited"
uv run python monitor_stratum.py --ds llm_v3mon | tee logs/monitor_stratum.txt
echo MON_CHAIN_DONE
