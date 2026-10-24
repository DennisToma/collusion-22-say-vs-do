# STATUS

## Current state (2026-10-24 02:15 UTC, iteration 13)
- LOCKED TEST DONE (00:03; never rerun). REPLICATION DONE (02:07, run once; lock logs/final/REPLICATION_ONCE.lock;
  never rerun). REPORT presentable; all reviews applied thru E53.
- Replication llm_v3rep (n=30, 15 y=1): 4/4 pre-registered predictions held, P3/P4 narrowly: premium run .92
  [.79,1.00] vs action_stats .80 (Δ +.12 [-.004,+.29]); text .67; combined-action -.14 [-.30,+.02]; frozen
  thresholds flag 40-60% of fresh none runs (operating points unstable).
- E50/E52: round-1 prices are set BEFORE any private message is read, yet channel holders open +4.6 (llm_v3) / +5.0
  (rep) above rivals → round-1-only premium test run AUROC .90: the premium is largely a treatment-response detector.
  In REPORT abstract caveats, §Exploration "When does the premium appear?", Limitations, Appendix A (corrected).
- pipeline.sh bug: its pgrep matches the parent shell cmdline → never exits; kill it manually once audits verify.
## Next steps (no new generation after 03:30, no new experiments after 06:30; FINALIZE from 08:15)
1. Opus-subagent + codex end-to-end review of REPORT for coherence now that all results are in (abstract is long;
   consider tightening to ~6 bullets with the round-1 finding prominent). Keep numbers traceable.
2. Optional exploration (no LLM generation): auditor evidence — do LLM auditors cite round 1 as evidence? (evidence.json)
3. Finalize: figures check, reproduce block, final codex review of REPORT claims.

## Log
- 02:15 iter 13: replication run once (E47 result: 4/4 held), round-1 replicates (E52), codex review_iter13_rep applied (E53).
- 02:05 iter 13: codex review_iter13 applied (E51).
- 01:50 iter 13: round-1 treatment-response finding (E50), early_detection.py, round1_effect.py, fig_early.py.
- 01:35 iter 12: codex review_iter12 applied (E49).
- 01:10 iter 12: llm_v3rep replication pre-registered + launched (E47); matched-recall legit (E48); codex review started.
- 01:25 iter 11: monitor_stratum FP (E46) + codex review fixes in REPORT.
- 01:00 iter 11: v3mon deterrence result (E45) → REPORT; codex review started.
- 00:50 iter 10: codex re-check (E44) applied.
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
