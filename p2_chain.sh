#!/bin/bash
# Phase 2 generation chain (codex/gpt-6-luna sellers): gap 1 cue conditions -> wording paraphrases -> gap 4 replication.
cd "$(dirname "$0")"; export SIM_PAR=4
G="uv run python llm_market.py --rounds 12 --framing lab --games-parallel 2"
$G --ds llm_p2cue --matched private,neutral,notes,randpartner,placebo,none --matched-n 15 --seed 8100 && echo "p2cue done $(date -u)"
$G --ds llm_p2para1 --sysvar 1 --matched private,none --matched-n 10 --seed 8100 && echo "p2para1 done $(date -u)"
$G --ds llm_p2para2 --sysvar 2 --matched private,none --matched-n 10 --seed 8100 && echo "p2para2 done $(date -u)"
$G --ds llm_p2rep --plan private:30,none:20,legit:10 --seed 9500 && echo "p2rep done $(date -u)"
