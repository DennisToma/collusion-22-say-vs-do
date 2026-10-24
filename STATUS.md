# STATUS

## Current state (2026-10-24 00:35 UTC, iteration 10)
- LOCKED TEST DONE (00:03; do NOT rerun final_analysis --split test). REPORT restructured for judges: abstract rewritten,
  headline test → Exploration strata → Validity/Held-out/Limitations/Next steps/Reproduce → App. A dev, App. B scripted.
- Final REPORT reviews DONE (codex logs/review_report_codex.md + Opus subagent): all tables match sources; overclaims
  fixed (null≠equivalence, 'tied'→unresolved, legit = operating-point effect, label = condition, multiplicity 25×3).
- Cross-family full (42 runs): text null + no text gain replicate for Claude; stats views best for Claude.
- Firm-level text cue: colluders DROP competitive wording ("keeping" 67/140 vs rivals 133/140) → text LR pair-ID 1.00.
- llm_v3fp (firm framing): 16/16 channel-unused; frozen thresholds FP: premium .44, action_stats .50, structured .25,
  text/action .06 → stats scorers don't transfer across framing (in REPORT Exploration).
- New fig: figures/roc_test.png (fig_roc.py).
- Shuffle (test, 3 seeds): no degradation (combined run Δ −.011 [−.10,+.08]) → in REPORT + abstract (E43).
- Running: llm_v3mon generation (mon_chain → pipeline → monitor_stratum).
## Next steps
1. (done) shuffle.
2. mon_chain done → monitor_stratum result into REPORT Exploration (cutoff: no new experiments after 06:30).
3. Final pass: codex quick re-check of new Exploration paragraphs; keep abstract in sync; FINALIZE from 08:15.
- Risks: v3mon may not finish (20 runs × 12 rounds serial); then report as not completed.

## Log
- 00:40 iter 10: shuffle ablation on test (E43, null). cross-family full (E39), firm-level text cue (E40), fp stratum (E41), final REPORT reviews applied
  (E42), REPORT restructure + abstract + next steps, fig_roc.
- 00:09 iter 9: LOCKED TEST RUN (E36) after preflight caught 1 hardset failure (E37 fix); REPORT headline/abstract;
  text_lr_inspect (E38); mechanism figs dev/test/all.
- 23:40 iter 9: codex review_iter9 applied (E35): auditors.py --verify gate in auto_finalize + finalize preflight;
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
