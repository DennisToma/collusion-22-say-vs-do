#!/bin/bash
# Background loop: label newly finished LLM runs, then audit them (orig variant, all views).
# Stops when generation is finished and everything is labelled + audited.
cd "$(dirname "$0")"
DS=${1:-llm_v3}
while true; do
  uv run python label_llm.py --ds $DS
  uv run python auditors.py --ds $DS --workers 2
  if ! pgrep -f "llm_market.py --ds $DS" >/dev/null; then
    uv run python label_llm.py --ds $DS; uv run python auditors.py --ds $DS --workers 2; break
  fi
  sleep 240
done
echo PIPELINE_DONE
