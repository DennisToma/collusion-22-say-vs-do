#!/bin/bash
# The ONE locked-test analysis (data/SPLITS.md). Run after every llm_v3 run is labelled and audited by all 6 views.
# Order: hard-set check + metrics-free preflight + all dev steps FIRST; then the run-once guard on the headline step
# (final_analysis --split test), taken atomically. Historical retry logic remains below, but a completed
# evaluation's committed receipt now refuses the whole script even without local logs/ locks. Invoke individual
# deterministic renderers to refresh tables/figures. Any rerun of the headline step requires disclosure in
# data/SPLITS.md and an explicit change to the committed completion protection.
set -o pipefail
cd "$(dirname "$0")"
# The original logs/ locks do not survive git clone. Respect the committed completion
# receipt before any preflight, calibration or writes; use individual renderers if needed.
python3 evaluation_guard.py headline || exit $?
mkdir -p logs/final
step() { echo "== $*"; "$@" || echo "!! STEP FAILED: $*" | tee -a logs/final/FAILED_STEPS.txt; }
if [ ! -e logs/final/RUN_ONCE.stamp ]; then
  set -e
  # --- preflight (no test metrics) ---
  uv run python hardset.py --ds llm_v3 | tail -3
  uv run python auditors.py --ds llm_v3 --verify | tee logs/final/verify_preflight.txt   # current-hash, 1 audit/run/view
  uv run python final_analysis.py --split test --check-only | tee logs/final/preflight.txt
  uv run python final_analysis.py --split dev  | tee logs/final/final_dev.txt
  uv run python baselines.py --ds llm_v3 --split dev  | tee logs/final/baselines_dev.txt
  uv run python textsim.py --split dev         | tee logs/final/textsim_dev.txt
  uv run python incremental.py --split dev     | tee logs/final/incremental_dev.txt
  uv run python report_tables.py --split dev   > /dev/null
  uv run python make_figures.py --split dev    | tee logs/final/figures_dev.txt
  # --- run-once guard (mkdir is atomic) ---
  mkdir logs/final/RUN_ONCE.lock || { echo "another finalize run holds the lock; refusing"; exit 1; }
  date -u +"%Y-%m-%dT%H:%M test analysis STARTED (any rerun of final_analysis --split test must be disclosed in data/SPLITS.md)" >> logs/final/RUN_ONCE.stamp
  # --- the single headline look ---
  uv run python final_analysis.py --split test | tee logs/final/final_test.txt
  date -u +"%Y-%m-%dT%H:%M HEADLINE_DONE" >> logs/final/RUN_ONCE.stamp
  set +e
else
  echo "headline step already run ($(head -1 logs/final/RUN_ONCE.stamp)); re-running only the retryable test steps"
  grep -q HEADLINE_DONE logs/final/RUN_ONCE.stamp && uv run python -c "import json; d=json.load(open('results/analysis/final_llm_v3_gpt-6.1-sol_test.json')); assert d['split']=='test' and d['n_runs']==95" \
    || { echo "headline step STARTED but not completed/valid: investigate + disclose in data/SPLITS.md before any rerun"; exit 1; }
fi
step bash -o pipefail -c "uv run python evidence.py --split test       | tee logs/final/evidence_test.txt"
step bash -o pipefail -c "uv run python gallery.py --split test        | tee logs/final/gallery_test.txt"
step bash -o pipefail -c "uv run python baselines.py --ds llm_v3 --split test | tee logs/final/baselines_test.txt"
step bash -o pipefail -c "uv run python textsim.py --split test        | tee logs/final/textsim_test.txt"
step bash -o pipefail -c "uv run python incremental.py --split test    | tee logs/final/incremental_test.txt"
step bash -o pipefail -c "uv run python cost.py --ds llm_v3            | tee logs/final/cost.txt"
step bash -o pipefail -c "uv run python report_tables.py --split test  | tee logs/final/report_tables_test.txt"
step bash -o pipefail -c "uv run python make_figures.py --split test   | tee logs/final/figures_test.txt"
date -u +"%Y-%m-%dT%H:%M retryable test steps finished (failures: logs/final/FAILED_STEPS.txt)" >> logs/final/RUN_ONCE.stamp
# these depend on jobs that may finish later; run them separately when their inputs are complete:
#   uv run python shuffle_analysis.py --views combined,structured     (after 3 shuffle seeds)
#   uv run python cross_family.py                                     (after Claude mod3 subset)
#   uv run python fp_stratum.py --ds llm_v3fp                         (after llm_v3fp labelled+audited)
#   then re-run: uv run python report_tables.py --split test          (picks up shuffle / cross-family / fp)
