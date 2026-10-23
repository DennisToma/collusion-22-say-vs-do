# STATUS

## Current state (2026-10-23 22:40 UTC, iteration 6)
- **Generation** llm_v3 at 72/125 (ETA ~00:00); `pipeline.sh llm_v3` keeps audits in step (63 runs × 6 views).
- **`after_gen.sh` running**: when generation ends → llm_v3fp (private:16 firm framing) + Claude Sonnet mod3 subset +
  shuffle seeds 0,1,2 on TEST (combined,structured). No manual launch needed.
- Dev (n=30): premium run 1.00 / within .98 > action_stats .89/.91 > structured .83/.91 ≈ combined ≈ fusion > action
  .78 > text .58. External info-theory (pCMI .47, MI .60) weak: colluders coordinate on level.
- NEW iter 6: `textsim.py` untrained public-text convergence: dev within-market .85 vs LLM text .61 (Δ +.24 [+.12,+.35])
  but run AUROC .45 → public text carries a LOCALISATION signal the zero-shot LLM misses. Trained LR (dev split):
  text pair-ID .90, action run .96. Both pre-registered in `finalize_test.sh`; `report_tables.py` renders all REPORT
  tables from json (`results/analysis/report_tables_{dev,test}.md`).
- codex review of iter-6 code running → `logs/review_iter6.md` (apply fixes BEFORE finalize_test.sh).
## Next steps
1. Apply `logs/review_iter6.md` fixes (dev-only checks).
2. When 125×6 audits done (`wc -l results/llm_auditor/llm_v3/gpt-6.1-sol/*_orig.jsonl`): `./finalize_test.sh` ONCE;
   paste `results/analysis/report_tables_test.md` into REPORT (test = headline; dev → appendix); rewrite abstract.
3. Then shuffle_analysis / cross_family / fp_stratum as inputs complete; rerun `report_tables.py --split test`.
4. codex + Opus review of final REPORT claims.
- Risks: ~7 concurrent LLM calls after 00:00; sol ~5/min → shuffle done ~02:00.

## Log
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
