#!/bin/bash
# Iter 5 chain: wait for llm_v3 generation to finish, then start the post-generation jobs so no time is lost
# between manager iterations. Parallelism: fp generation (1 game, <=4 luna) + Claude subset (1) + llm_v3 pipeline
# audits (2 sol); the shuffle ablation (2 sol) only starts after pipeline.sh is done -> <=7 concurrent calls.
cd "$(dirname "$0")"
while pgrep -f "llm_market.py --ds llm_v3 " >/dev/null; do sleep 60; done
echo "$(date -u +%H:%M) llm_v3 generation done"
# exploration stratum: firm framing, private channel -> natural "channel, no agreement" negatives (never pooled)
( uv run python llm_market.py --ds llm_v3fp --plan private:16 --rounds 12 --framing firm --games-parallel 1 --seed 5000 \
    > logs/gen_v3fp.log 2>&1 && ./pipeline.sh llm_v3fp > logs/pipeline_v3fp.log 2>&1; echo "$(date -u +%H:%M) v3fp done" ) &
# cross-family subset (Claude Sonnet, all 6 views, runs with index % 3 == 0)
( uv run python auditors.py --ds llm_v3 --auditor claude-sonnet-5-5 --subset mod3 --workers 1 > logs/claude_mod3.log 2>&1;
  echo "$(date -u +%H:%M) claude subset done" ) &
# shuffle ablation on TEST runs after the orig audits finish (text view skipped: donors share label+condition, and
# the text-only view sees messages only, so text-shuffle is uninformative about cross-modal use)
while pgrep -f "pipeline.sh llm_v3$" >/dev/null || pgrep -f "auditors.py --ds llm_v3 --workers" >/dev/null; do sleep 60; done
echo "$(date -u +%H:%M) llm_v3 orig audits done"
for s in 0 1 2; do
  uv run python auditors.py --ds llm_v3 --variant shuffle --shuffle-seed $s --only-test --views combined,structured --workers 2 \
    >> logs/shuffle.log 2>&1
done
echo "$(date -u +%H:%M) shuffle done"
wait
echo AFTER_GEN_DONE
