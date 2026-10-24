#!/bin/bash
# Runs the registered E100 comparison once, after p2_c3post.sh writes results/analysis/p2_qwen.json.
cd "$(dirname "$0")"
until [ -f results/analysis/p2_qwen.json ] && ! pgrep -f p2_c3post.sh >/dev/null; do sleep 60; done
uv run python p2_qwen_cmp.py > logs/c3_cmp.log 2>&1 && echo "c3 cmp done $(date -u)" >> logs/partc_qwen.log
