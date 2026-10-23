# STATUS

## Current state (2026-10-23 23:10 UTC, iteration 7)
- **Generation** llm_v3 ~95/125 (ETA ~23:35); `pipeline.sh` audits in step; `after_gen.sh` then launches llm_v3fp,
  Claude mod3 subset, shuffle seeds 0–2 on TEST (combined,structured; ETA ~02:00). `hardset.py` on all runs running.
- Dev (n=30): premium run 1.00 / within .98 > action_stats .89/.91 > structured .83/.91 ≈ combined ≈ fusion > action
  .78 > text .58. textsim (public-text convergence) within .81 vs LLM text .61. Cascade: LLM = explanation not detection.
- NEW iter 7: `incremental.py` (untrained rank-average premium+view): no view adds over premium on dev (Δ ≤ 0; dev at
  ceiling) — pre-registered for test. Opus pre-test review: no headline-distorting bug; fixes applied
  (finalize: only headline step run-once, others retryable; label validity + full hard-set asserts; ext guard).
## Next steps
1. When 125×6 audits done (`wc -l results/llm_auditor/llm_v3/gpt-6.1-sol/*_orig.jsonl` all 125): `./finalize_test.sh`
   ONCE (if a later step fails: fix, rerun the script — it skips the headline step). Check logs/final/FAILED_STEPS.txt.
2. Replace REPORT dev tables with `results/analysis/report_tables_test.md` (test = headline; dev → appendix);
   rewrite abstract around: premium ≫ zero-shot LLM; text adds nothing to LLM; stats table helps; LLM = explanation.
3. After inputs: shuffle_analysis.py --views combined,structured; cross_family.py; fp_stratum.py --ds llm_v3fp;
   rerun report_tables --split test; figures. 4. codex + Opus review of final REPORT claims.
- Risks: codex review_iter7 pending (logs/review_iter7.md) — apply before finalize; LLM concurrency ~7 after 00:00.

## Log
- 23:25 iter 7: incremental.py (pre-registered); Opus pre-test review applied (logs in EXPERIMENTS E28); hardset.py
  on all runs started; codex review of iter-7 diff running → logs/review_iter7.md.
- 23:00 iter 6: applied codex review_iter6 (P1: textsim dev-only fit, figure CI crash, finalize preflight/lock;
  P2: report_tables labels, FP rendering, None CIs); cascade metrics in final_analysis triage (dev).
- 22:40 iter 6: baselines.py --split (dev run), textsim.py (new untrained scorer, dev), report_tables.py,
  finalize_test.sh extended + STARTED stamp; SPLITS pre-registration; REPORT dev baseline/textsim paragraphs.
- 22:31 iter 5: codex review of new code → safeguard fixes (exact id set, run-once stamp, pipefail, fp asserts);
  after_gen.sh restarted (waits on 125×6 audit completeness, not pipeline.sh, whose pgrep also matches llm_v3fp).
- 22:30 iter 5: external info-theory comparator block (dev), cost.py, fp_stratum.py, finalize_test.sh, after_gen.sh
  chain launched; codex review of fp stratum in background.
- 22:30 iter 4: input repairs (prompt hash check, frozen donor maps, ties); final_analysis.py frozen after codex
  review; evidence.py, gallery.py; dev results in REPORT (premium dominates; text adds nothing); SPLITS: headline=test once.
- 21:55 iter 3: SPLITS.md + EXPERIMENTS.tsv; hardset.py (0/32 flagged); baselines on llm_v3 (donor fallback for tiny
  folds, counted); analyze_llm --split + hardset flags; action_stats ablation view; Claude Sonnet subset launched;
  REPORT interim LLM section.
- 21:35 fold-local shuffle donors in baselines.py (fixes donor-memorisation leak); `--variant pad` length control
  added to auditors.py; Claude auditor call isolated (no tools, /var/tmp cwd) and tested OK on 1 run.
- 20:28 iter 2 start. Built llm_market.py, baselines.py, show_run.py, label_llm.py, auditors.py, analyze_llm.py, pipeline.sh.
- Pilots: firm+regulator framing → luna sellers refuse to coordinate (data/llm_v2, /var/tmp/llm_v1_pilot0);
  lab framing → private intention exchange + lockstep (data/pilot_lab_luna). Chose lab + luna for llm_v3.
- 20:41 launched llm_v3. codex methodology review → fixed label leakage (judge no longer sees prices; primary label
  = communication), combined/structured now strict superset (units+profit), public partnership info in
  `public_info.jsonl`, strict parse + failure log + no silent model fallback, exact-id resume, LR for all
  baseline feature sets (GBM optional), price-context number extraction, same-condition shuffle donors.
- 20:50 scripted_v2 generated (levels 12/14, strength .15–.5).
