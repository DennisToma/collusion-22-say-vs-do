#!/bin/bash
# E112 (Part E2, registered): replacement generation, prefix/coverage check, then the registered evaluation once.
cd "$(dirname "$0")"
SIM_PAR=3 uv run python p2_replace.py gen --games-parallel 3 > logs/p2repl_gen.log 2>&1 || { echo "p2repl gen FAILED $(date -u)" >> logs/p2repl.log; exit 1; }
uv run python p2_replace.py check >> logs/p2repl.log 2>&1 && echo "p2repl gen done $(date -u)" >> logs/p2repl.log || exit 1
