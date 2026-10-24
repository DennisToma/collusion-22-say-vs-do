#!/bin/bash
# E115 (registered second arm of E112): waits for E112 generation, then the same replacement design with a gpt-6.1-sol newcomer.
cd "$(dirname "$0")"
until grep -q "p2repl gen done\|p2repl gen FAILED" logs/p2repl.log 2>/dev/null; do sleep 60; done
grep -q "p2repl gen FAILED" logs/p2repl.log && { echo "p2replS skipped: E112 failed $(date -u)" >> logs/p2repl.log; exit 1; }
P2REPL_ARM=sol SIM_PAR=3 uv run python p2_replace.py gen --games-parallel 3 > logs/p2replS_gen.log 2>&1 || { echo "p2replS gen FAILED $(date -u)" >> logs/p2repl.log; exit 1; }
P2REPL_ARM=sol uv run python p2_replace.py check >> logs/p2repl.log 2>&1 && echo "p2replS gen done $(date -u)" >> logs/p2repl.log
