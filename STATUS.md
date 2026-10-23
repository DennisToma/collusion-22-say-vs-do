# STATUS

## Current state (2026-10-23 22:30 UTC, end of iteration 5)
- **Generation** llm_v3 at 70/125 (ETA ~00:00); `pipeline.sh llm_v3` keeps audits in step (63 runs × 5 views; combined_stats backfilling).
- **`after_gen.sh` running (logs/after_gen.log)**: when llm_v3 generation ends it auto-starts (a) llm_v3fp firm-framing
  private:16 generation → `pipeline.sh llm_v3fp`; (b) Claude Sonnet mod3 subset (all 6 views); (c) after orig audits
  finish: shuffle seeds 0,1,2 on TEST runs, views combined,structured (logs/shuffle.log). No manual launch needed.
- Frozen `final_analysis.py` + new external block: sibling's info-theory per-pair scores. Dev: run AUROC pCMI .47,
  MI .60, TE .59, Pearson .21 (colluders hold prices flat); premium−pCMI +.53 [+.28,+.78]; 14's pair_level == our premium.
- Dev (n=30): premium run 1.00 / within .98 > action_stats .89/.91 > structured .83/.91 ≈ combined ≈ fusion > action .78 > text .58.
- New: `cost.py` (cost table), `fp_stratum.py` (frozen dev thresholds applied to llm_v3fp; smoke-tested on dev),
  `finalize_test.sh` (THE one test run: dev → test final_analysis, evidence, gallery, figures, cost).
## Next steps
1. When all 125 runs × 6 views are audited (check `wc -l results/llm_auditor/llm_v3/gpt-6.1-sol/*_orig.jsonl` = 125):
   `./finalize_test.sh` ONCE. Then write test headline into REPORT (replace dev table; keep dev as appendix), codex REPORT review.
2. After shuffle seeds: `uv run python shuffle_analysis.py --views combined,structured`. After Claude: `cross_family.py`.
   After llm_v3fp: `fp_stratum.py --ds llm_v3fp` (needs final dev json from step 1 for combined_stats threshold).
3. Read `logs/review_fp.md` (codex critique of fp stratum/new code, launched 22:28) and apply fixes before running fp_stratum.
4. Optional: baselines LR on llm_v3 test (recompute; the interim all-run numbers predate the split rule).
- Risks: ~7 concurrent LLM calls after 00:00 (slightly over the ≤6 guide); sol throughput ~5/min → shuffle done ~02:00.

## Log
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
