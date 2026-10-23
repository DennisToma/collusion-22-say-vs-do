#!/bin/bash
# The ONE locked-test analysis (data/SPLITS.md). Run once, after every llm_v3 run is labelled and audited by all
# 6 views (final_analysis.py asserts this and exits non-zero otherwise -> nothing else runs).
# Dev outputs are regenerated first (complete dev cohort -> final dev thresholds used by fp_stratum.py).
set -eo pipefail
cd "$(dirname "$0")"
[ -e logs/final/RUN_ONCE.stamp ] && { echo "test analysis already run (logs/final/RUN_ONCE.stamp); refusing"; exit 1; }
mkdir -p logs/final
uv run python final_analysis.py --split dev  | tee logs/final/final_dev.txt
uv run python final_analysis.py --split test | tee logs/final/final_test.txt
uv run python evidence.py --split test       | tee logs/final/evidence_test.txt
uv run python gallery.py --split test        | tee logs/final/gallery_test.txt
uv run python make_figures.py --split test   | tee logs/final/figures_test.txt
uv run python cost.py --ds llm_v3            | tee logs/final/cost.txt
date -u +"%Y-%m-%dT%H:%M test analysis run" >> logs/final/RUN_ONCE.stamp
# these depend on jobs that may finish later; run them separately when their inputs are complete:
#   uv run python shuffle_analysis.py --views combined,structured     (after 3 shuffle seeds)
#   uv run python cross_family.py                                     (after Claude mod3 subset)
#   uv run python fp_stratum.py --ds llm_v3fp                         (after llm_v3fp labelled+audited)
