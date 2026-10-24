#!/bin/bash
# iter 16: placebo stratum chain: wait for generation -> labels (placebo => no_channel) -> 6 frozen auditor views -> placebo.py
cd "$(dirname "$0")"
while pgrep -f "python llm_market.py --ds llm_v3plc" | grep -qv $$; do sleep 30; done
echo "gen done $(date -u)"
uv run python label_llm.py --ds llm_v3plc
uv run python auditors.py --ds llm_v3plc --views text,action,combined,structured,action_stats,combined_stats --workers 2
uv run python auditors.py --ds llm_v3plc --verify && echo "verify ok"
uv run python placebo.py > logs/placebo.out && echo "placebo done $(date -u)"
