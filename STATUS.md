# STATUS

## Current state (2026-10-23 23:30 UTC, iteration 9)
- **Generation** llm_v3 110/125 (ETA ~23:55); `pipeline.sh` audits in step; `after_gen.sh` then v3fp gen, Claude mod3,
  shuffle seeds 0–2 on TEST; `mon_chain.sh` then llm_v3mon (cutoff 03:30).
- NEW `auto_finalize.sh` (log `logs/final_auto.log`): waits for gen done + 125 labels + `auditors.py --verify` OK, then
  runs `finalize_test.sh` ONCE. **Do not run finalize by hand unless final_auto.log shows a preflight failure.**
- Dev (n=30): premium run 1.00 / within .98 > action_stats .89/.91 > structured .83/.91 ≈ combined ≈ fusion > action
  .78 > text .58. Mechanism fig (dev): private pair opens ~17.4 vs 12.5, late premium +0.90, >0 in 12/20 runs.
- REPORT now has a HEADLINE (test) slot above the dev section; dev section labelled as superseded.
## Next steps
1. When `logs/final/RUN_ONCE.stamp` has HEADLINE_DONE: paste `results/analysis/report_tables_test.md` into the REPORT
   headline slot; rewrite abstract from test numbers; move dev tables to an appendix; `fig_mechanism.py --split all`.
2. After inputs: shuffle_analysis.py --views combined,structured; cross_family.py; fp_stratum.py --ds llm_v3fp;
   monitor_stratum.py (mon_chain does it); report_tables --split test; make_figures --split test.
3. Remaining P2s of logs/review_iter9.md. Final codex + Opus review of REPORT claims.
- Risks: LLM concurrency ~7; finalize preflight needs hardset coverage of every run (it reruns hardset).

## Log
- 23:46 iter 9: codex review_iter9 applied (E35): auditors.py --verify gate in auto_finalize + finalize preflight;
  REPORT dev table now generated values, softened claims, full disclosure. Open P2s in logs/review_iter9.md (evidence
  scope, n-gram coefficient artifact, cascade 'explanation role' wording).
- 23:30 iter 9: auto_finalize.sh chain (E34); fig_mechanism.py dev figure (E33); REPORT test slot; codex review_iter9 started.
- 23:26 iter 8: codex review_iter8 applied (E32); mon_chain restarted with explicit sequencing.
- 23:13 iter 8: premium-selection disclosure (E30); llm_v3mon monitored stratum code + chain launched (E31).
- 23:25 iter 7: incremental.py (pre-registered); Opus pre-test review applied (logs in EXPERIMENTS E28); hardset.py
  on all runs started; codex review of iter-7 diff applied (E29).
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
