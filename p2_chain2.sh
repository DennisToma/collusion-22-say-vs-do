#!/bin/bash
# Phase 2 generation chain 2: after p2_chain.sh finishes llm_p2rep, gaps 5 / 7 / 8 (matched to llm_p2cue seeds k<10).
cd "$(dirname "$0")"; export SIM_PAR=4
until grep -q "^p2rep done" logs/p2/chain.log; do sleep 60; done
G="uv run python llm_market.py --rounds 12 --framing lab --games-parallel 2 --seed 8100 --matched-n 10"
$G --ds llm_p2aware --matched aware,aware_all && echo "p2aware done $(date -u)"
$G --ds llm_p2asym --matched highcost,quality && echo "p2asym done $(date -u)"
$G --ds llm_p2coded --matched coded && echo "p2coded done $(date -u)"
