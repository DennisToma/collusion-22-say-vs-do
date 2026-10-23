#!/bin/bash
# Iter 9: run finalize_test.sh (the ONE locked test analysis) as soon as its inputs are complete AND current, so the
# headline does not wait for the next manager iteration. Gate (codex review_iter9 P1): llm_v3 generator gone + marker,
# >=125 runs and labels, and `auditors.py --verify` (read-only: exactly one audit per labelled run per view, prompt hash
# current, no duplicates) passing twice 3 min apart with no llm_v3 labeller / orig auditor process running.
# finalize_test.sh holds the run-once lock/stamp; a preflight failure exits BEFORE the lock (fix, then rerun
# ./finalize_test.sh by hand). Never runs when a stamp exists (STARTED or HEADLINE_DONE). Exit status is propagated.
cd "$(dirname "$0")"
mkdir -p logs/final
until grep -q "llm_v3 generation done" logs/after_gen.log 2>/dev/null && ! pgrep -f "llm_market.py --ds llm_v3 " >/dev/null; do
  sleep 60; done
[ "$(wc -l < data/llm_v3/ground_truth.jsonl)" -ge 125 ] || { echo "$(date -u +%H:%M) generator ended with <125 runs; NOT finalizing"; exit 2; }
# pipeline.sh runs `auditors.py --ds llm_v3 --workers 2` and `label_llm.py --ds llm_v3` (llm_v3fp/v3mon/shuffle/Claude
# runs write other files and do not match these patterns)
auditing() { pgrep -f "auditors.py --ds llm_v3 --workers" >/dev/null || pgrep -f "label_llm.py --ds llm_v3( |$)" >/dev/null; }
ready() { [ "$(wc -l < data/llm_v3/labels.jsonl)" -ge 125 ] && ! auditing \
          && uv run python auditors.py --ds llm_v3 --verify > logs/final/verify_last.txt 2>&1; }
while true; do
  if ready; then sleep 180; ready && ! auditing && break; fi
  sleep 60
done
cat logs/final/verify_last.txt
if [ -e logs/final/RUN_ONCE.stamp ]; then echo "$(date -u +%H:%M) stamp exists; finalize already started -> not auto-running"; exit 0; fi
echo "$(date -u +%H:%M) inputs complete + current; running finalize_test.sh"
./finalize_test.sh; rc=$?
echo "$(date -u +%H:%M) AUTO_FINALIZE_EXIT $rc"; exit $rc
