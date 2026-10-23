#!/bin/bash
# Iter 9: run finalize_test.sh (the ONE locked test analysis) as soon as its inputs are complete, so the headline does
# not wait for the next manager iteration. Waits for: llm_v3 generation done, 125 labels, 125 rows in all 6 orig view
# files. finalize_test.sh itself holds the run-once lock/stamp; a preflight failure exits BEFORE the lock (safe to fix +
# rerun by hand). Output: logs/final/auto_finalize.log.
cd "$(dirname "$0")"
mkdir -p logs/final
until grep -q "llm_v3 generation done" logs/after_gen.log 2>/dev/null; do sleep 60; done
done6() { for v in text action combined combined_stats action_stats structured; do
            [ "$(wc -l < results/llm_auditor/llm_v3/gpt-6.1-sol/${v}_orig.jsonl 2>/dev/null || echo 0)" -ge 125 ] || return 1; done; }
until [ "$(wc -l < data/llm_v3/labels.jsonl)" -ge 125 ] && done6; do sleep 60; done
sleep 120   # let pipeline.sh finish its current loop (writes are per-row, but be safe)
if [ -e logs/final/RUN_ONCE.stamp ]; then echo "$(date -u +%H:%M) stamp exists; finalize already run -> not auto-running"; exit 0; fi
echo "$(date -u +%H:%M) inputs complete; running finalize_test.sh"
./finalize_test.sh
echo "$(date -u +%H:%M) AUTO_FINALIZE_EXIT $?"
