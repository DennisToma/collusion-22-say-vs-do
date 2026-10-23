#!/bin/bash
# Iter 8 exploration chain: after llm_v3 and llm_v3fp generation, generate the monitored stratum llm_v3mon
# (lab framing + ANNOUNCED public price monitor; private:14, none:6), label + audit it, then run monitor_stratum.py.
# Respects DIRECTION: no new generation launched after 03:30 UTC. Serial after v3fp keeps LLM parallelism <= ~7.
# Sequencing via explicit markers (codex review_iter8 P2): after_gen.log "llm_v3 generation done", then the v3fp
# generator must have been seen and be gone (or 15 min without it appearing).
set -uo pipefail
cd "$(dirname "$0")"
gen_running() { pgrep -f "llm_market.py --ds $1( |$)" >/dev/null; }
until grep -q "llm_v3 generation done" logs/after_gen.log 2>/dev/null; do sleep 60; done
for i in $(seq 15); do gen_running llm_v3fp && break; sleep 60; done
while gen_running llm_v3fp; do sleep 60; done
echo "$(date -u +%H:%M) v3fp generation finished ($(wc -l < data/llm_v3fp/ground_truth.jsonl 2>/dev/null || echo 0) runs)"
if [ "$(date -u +%H%M)" -gt 0330 ] && [ "$(date -u +%H%M)" -lt 1200 ]; then echo "$(date -u +%H:%M) past 03:30 cutoff; not launching"; exit 0; fi
echo "$(date -u +%H:%M) llm_v3mon generation start"
uv run python llm_market.py --ds llm_v3mon --plan private:14,none:6 --rounds 12 --framing lab_monitored --games-parallel 1 --seed 7000 \
  > logs/gen_v3mon.log 2>&1 || { echo "!! v3mon generation FAILED"; exit 1; }
./pipeline.sh llm_v3mon > logs/pipeline_v3mon.log 2>&1 || { echo "!! v3mon pipeline FAILED"; exit 1; }
echo "$(date -u +%H:%M) llm_v3mon labelled+audited"
uv run python monitor_stratum.py --ds llm_v3mon 2>&1 | tee logs/monitor_stratum.txt || { echo "!! monitor_stratum FAILED"; exit 1; }
echo MON_CHAIN_DONE
