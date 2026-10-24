# Splits (frozen 2026-10-23 21:45 UTC, iteration 3)

## llm_v3 (headline LLM-market data, 125 runs planned, ids llm_v3_0000 … llm_v3_0124)
- **dev** = llm_v3_0000 … llm_v3_0029 (30 runs). Any auditor-prompt / feature / threshold iteration may only
  look at metrics on these runs. The preliminary numbers seen in iteration 2 (n=14) were all from dev.
- **test (locked)** = llm_v3_0030 … llm_v3_0124. Metrics on test are computed once, with the frozen config.
- Frozen auditor config: `auditors.py` TASK/WHAT/render as of commit 5f2d8a0 (gpt-6.1-sol, max_tokens 600).
  The auditor prompt was written before any LLM-market data existed and has NOT been tuned:
  **tuning attempts on llm_v3 = 0** (update this line if that changes).
- ~~Headline = all runs~~ (superseded 22:15 UTC per DIRECTION 22:00): `final_analysis.py` calibrates two
  things on dev (late-fusion weight; Youden run-score thresholds for FPR), so **headline = test split only**
  (llm_v3_0030 … 0124), computed ONCE with `uv run python final_analysis.py --split test` after generation and
  audits finish. Dev results are labelled dev.
- Disclosure 2: at 22:20 a smoke test of `shuffle_analysis.py` (fake shuffle = copy of intact audits) printed intact
  Δ_hybrid on 24 test runs (0030–0057). Analysis code was already frozen; nothing was changed in response.
- Disclosure: iteration-3 interim analyses (n = 36–40, all runs) included test runs 0030–0039 before this rule;
  nothing was tuned on them (auditor prompt unchanged; analysis code frozen before the full test set exists).
- Analysis config frozen: `final_analysis.py` + `evidence.py` as of the iteration-4 commit after the codex review
  `logs/review_final_analysis.md` (fixes: cohort assertion, conservative Youden incl. +inf, class-stratified
  bootstrap, endpoint naming, high-markup proxy, stricter evidence checks, triage). Fusion weight objective = mean
  of dev run AUROC and within-market AUROC.

- Iter 5 (22:23): added an EXTERNAL comparator block to `final_analysis.py` (sibling's per-pair pcmi/mi/te/pearson
  and pair_level scores), checked on dev only. No existing scorer, threshold or metric changed. Separate block, so
  partial coverage of the sibling's file never affects the frozen cohort.
- Iter 5 (22:31, after codex review `logs/review_fp.md`): safeguards only — final_analysis now also requires the
  exact frozen id set llm_v3_0000–0124 to be labelled; `finalize_test.sh` (pipefail) refuses to run twice
  (`logs/final/RUN_ONCE.stamp`). No scorer, threshold rule or metric changed.

## scripted_v1 / scripted_v2 (mechanism demo only)
5-fold CV grouped by run_id (GroupKFold); no tuning beyond the learner choice (LR primary, GBM secondary).
- Iter 6 (22:35): pre-registered before these scorers were evaluated on test — (a) `baselines.py --split test` (LR, 5-fold grouped CV inside
  test only; dev version run for development); (b) NEW untrained scorer `textsim.py` (public-text lexical convergence
  of each pair; TF-IDF fit on DEV public messages only, no labels (the earlier all-run fit was replaced after the iter-6 codex review); nothing tuned; motivated by dev-only LR n-gram
  inspection); (c) `report_tables.py` renders REPORT tables from the json. All added to `finalize_test.sh`, which now
  runs a metrics-free preflight (`final_analysis.py --check-only`) and all dev steps first, then takes an atomic mkdir lock + STARTED stamp before the test step (a failed-and-rerun test analysis must be disclosed here).
- Iter 6 (23:00): additive output `triage.*.cascade_*` in final_analysis (end-to-end recall/FPR of premium screen →
  LLM flag at dev threshold), checked on dev only; no existing scorer/threshold/metric changed.
- Iter 7 (23:15): pre-registered before any test look — `incremental.py` (untrained, label-free percentile-rank
  average of premium and each LLM view vs premium alone; paired run bootstrap; pair-ID complementarity counts).
  Added to `finalize_test.sh` (dev in preflight, test after lock) and `report_tables.py`. Checked on dev only.
  No existing scorer/threshold/metric changed.
- Iter 7 (23:25, after Opus review): safeguards only — finalize_test.sh: only `final_analysis --split test` is
  run-once; later test steps are deterministic re-renderings and retryable (failures logged to
  logs/final/FAILED_STEPS.txt); preflight runs `hardset.py` on all runs and final_analysis asserts full hard-set
  coverage + valid labels (unparsed judge output would have become y=0); external block reports coverage and
  tolerates sibling schema changes; textsim cohort assert moved before metrics. No scorer/threshold/metric changed.
- Disclosure: `cross_family.py` (mod-3 subset, dev + test runs pooled, used for auditor agreement only) has been run
  on partial data during development (iters 4–7); it is not a held-out metric and no scorer was tuned on it.
- Iter 7 (23:40, after codex review `logs/review_iter7.md`): retry steps use pipefail; RUN_ONCE.stamp distinguishes
  STARTED from HEADLINE_DONE (a resumed finalize requires HEADLINE_DONE + a valid 95-run test json, else stop and
  disclose); headline json written atomically; stricter sibling schema check; incremental.py uses exact midrank sums
  recomputed inside every bootstrap resample (dev point estimates unchanged). Dev only.
- Disclosure 3 (iter 8, 23:11): the **pair-premium scorer** was not designed blind. The research director proposed it
  (DIRECTION.md, 22:00) after looking at per-condition pair-premium summaries on the partial data at that time (≈ runs
  0000–0060, i.e. including ~30 test runs). Its definition was fixed before the locked test analysis and is untrained
  (one line, no parameters), but its *selection* as the headline comparator used test-split exposure. REPORT says so.
  Robustness variant `premium_r2plus` was added for the same reason.
- Iter 8 (23:11): exploration stratum `data/llm_v3mon` (lab framing + publicly known price monitor that halves flagged
  pairs' earnings; private:14, none:6, seed 7000), analysed by `monitor_stratum.py` (written before any llm_v3mon data
  existed; frozen llm_v3 dev thresholds; comparator = llm_v3 dev only). Never pooled into the headline.
- Iter 9 (23:40): `auto_finalize.sh` runs `finalize_test.sh` automatically once llm_v3 generation is done, 125 runs are
  labelled and `auditors.py --verify` (read-only: one current-prompt-hash audit per labelled run per view, no
  duplicates) passes twice with no llm_v3 labeller/auditor running; `finalize_test.sh` preflight also runs `--verify`.
  `fig_mechanism.py` (descriptive price paths) refuses `--split test/all` before HEADLINE_DONE. No scorer changed.
- **Locked test run (iter 9).** `auto_finalize.sh` started `finalize_test.sh` at 23:45; its PREFLIGHT failed (before the
  lock, no test metric computed) because the hard-set LLM check of run 0106 returned empty text (deepseek-v4.1-flash
  at max_tokens=200). `hardset.py` now retries with a larger token budget (200 → 1000 → 3000); 0106 then checked
  (not flagged; 0/125 flagged overall). `finalize_test.sh` was then run once by hand: STARTED 23:59, HEADLINE_DONE
  00:03 UTC, no failed steps. This is the single headline run. Hard-set checker model: gpt-6-luna 94 runs,
  deepseek-v4.1-flash 31 runs (cheap-tier backend auto-order).

## llm_v3rep (fresh replication split, iter 12, PRE-REGISTERED 2026-10-24 01:10 UTC before generation)
- Purpose: the premium statistic was chosen after seeing partial llm_v3 data incl. test runs (REPORT disclosure), so
  the llm_v3 test split is not fully held-out for it. llm_v3rep is generated AFTER all analysis code and thresholds
  were frozen: same generator (`llm_market.py`, sim llm-0.3, lab framing, 12 rounds, gpt-6-luna), new seed 9000,
  plan private:15, none:10, legit:5 (30 runs). Labelled + audited by the unchanged `pipeline.sh`.
- Pre-registered analysis (`replication.py`, written before any llm_v3rep run exists, run ONCE on the full set):
  run AUROC and within-market AUROC (positive runs) for premium, premium_r2plus, and the 6 LLM views; FPR/TPR at the
  FROZEN llm_v3 dev thresholds (`results/analysis/final_llm_v3_gpt-6.1-sol_dev.json`); paired run-bootstrap CI for
  (premium − best LLM view) where "best" = the view with highest llm_v3 TEST run AUROC (action_stats? taken from
  final_llm_v3_gpt-6.1-sol_test.json, fixed before generation), and for (action_stats − action), (combined − action).
  Pre-registered predictions: P1 premium run AUROC ≥ 0.85; P2 text run AUROC CI includes 0.5; P3 premium − best
  view ≥ 0 (point estimate); P4 combined − action CI includes 0. n = 30 → wide CIs; this is a replication check,
  not a new headline. Reported as its own section; never pooled with llm_v3.
- Disclosure (codex review_iter12 P1): generation was launched ~01:00 in the same shell step that appended this
  section; the freeze commit 71eae06 (01:0x) therefore already contains partial raw seller output of runs 0000–0001.
  The manager looked only at the first two raw lines of run 0000 (a round-1 public and private message, to check
  progress); no label, audit, premium or metric of llm_v3rep was computed or viewed before the freeze. Seed not changed.
- Hardening after review (before any llm_v3rep metric): combined−action now also on within-market AUROC; exact id set
  llm_v3rep_0000–0029 and counts 15/10/5 asserted; finite scores asserted; sha256 of the frozen dev/test jsons recorded;
  run-once lock `logs/final/REPLICATION_ONCE.lock`; smoke runs write *_SMOKE.json. Only the three contrasts named above
  are registered; every other contrast in the output is exploratory.
- Run record (iter 13, 02:07 UTC): `replication.py` run ONCE (lock created), after `auditors.py --ds llm_v3rep --verify`
  OK (30/30 × 6 views current). Exposure before the run: label counts (15/15 private y=1) and three label_llm log lines
  showing per-run pair premiums of runs 0027–0029 (seen in a progress `tail`); no metric computed. pipeline.sh had
  to be killed after all audits were complete (its pgrep matched the parent shell's command line, so it never exited).
- Chronology clarification (codex review_iter13_rep): despite the "before generation" wording above and in the
  replication.py docstring, the registration commit followed the start of generation by ~2 min (see disclosure above);
  safeguards were added afterwards, before any llm_v3rep metric was computed.

## llm_v3plc (placebo-channel exploration stratum, iter 16, written ~03:05 UTC in the same shell step that launched generation)
- Purpose: E50/E52 showed the pair premium is already large in round 1 (before any partner message is read), so the
  premium may detect the *offer* of a channel rather than agreement. Placebo: the designated pair gets the identical
  private-channel prompt and writes private messages, but messages are never delivered (each seller sees only its own
  messages; the partner appears silent). One placebo run per llm_v3rep `private` run, same seed → same pair, cost and
  demand path (`llm_market.py --match-ds llm_v3rep`, lab framing, 12 rounds, gpt-6-luna). Never pooled into any headline.
- Analysis (`placebo.py`, descriptive, exploratory): matched per-run assigned-pair premium placebo vs private
  (round 1, rounds 2–12, all), paired bootstrap over the 15 matched seeds; plus none runs of llm_v3rep for reference.
- Predictions stated before data: (a) round-1 premium placebo ≈ private (identical prompt); (b) if the later premium is
  agreement-driven, rounds 2–12 placebo premium < private and decays toward `none`; if it is mostly offer-response,
  it stays near private. Either outcome is reported.
- Chronology (codex review_iter16_placebo P2): the "03:12" originally written here was wrong; this section was appended
  ~03:05 in the same shell command that started generation. The first commit (9113f4b, 03:07:52) already contained two
  finished placebo runs, and placebo.py had been smoke-run on them (output seen). Pre-generation registration is not
  independently established; treat E58 as exploratory. Post-review change: private-vs-placebo AUROC CIs resample the
  matched seed pairs jointly (bauc_paired).

## Portable completion protection (iteration 19, post-hoc)
`logs/` is gitignored, so the original run-once stamps/lock directories do not survive a clone.
`data/evaluation_receipt.json` now records the two completed output hashes and their completion
times (transcribed from local stamps / the records above). `finalize_test.sh`,
`final_analysis.py --split test/all` (except metrics-free `--check-only`), and `replication.py`
on `llm_v3rep` (including smoke flags) refuse to recompute these completed evaluations.
`python3 verify_artifacts.py` checks the saved artifacts without rerunning any metric.
The receipt and manifest are post-hoc handoff records, not new evidence about registration timing.
Only safeguards and the inaccurate replication docstring were changed; the protected result bytes,
scorers, thresholds, metric definitions and published numerical estimates are unchanged.

## Phase 2 datasets (registered 2026-10-24 06:31–06:52 UTC, EXPERIMENTS.tsv E77–E84, before any outcome was viewed)
- No tuning happens on any Phase 2 dataset. Every Phase 2 analysis uses frozen v1 scorers and the llm_v3 dev
  thresholds, and is computed on the whole dataset; there is no dev/test split inside these sets.
- `llm_p2cue` (seed 8100, k = 0..14, conditions private/neutral/notes/randpartner/placebo/none matched per seed,
  run index = 6k + condition index). `llm_p2para1` / `llm_p2para2` (sysvar 1/2, seed 8100, k = 0..9, private/none).
- `llm_p2glm` (glm-5.3-flash sellers via Go, seed 8100, k = 0..14, private/none). Uses whatever completes by Sun 15:00.
- `llm_p2rep` (gap 4, seed 9500, plan private:30,none:20,legit:10, llm_v3 settings): fully HELD-OUT second
  replication of the frozen premium statistic. Labels by p2_label.py (same JUDGE as label_llm.py for private
  runs). Premium run AUROC is computed ONCE after all 60 runs are labelled.
- `llm_p2aware` (aware/aware_all), `llm_p2asym` (highcost/quality), `llm_p2coded` (coded): seed 8100, k = 0..9,
  matched to llm_p2cue seeds (E86–E88); no tuning; whole set analysed once.
- `llm_p2sol` (gpt-6.1-sol sellers via codex, seed 8100, k = 0..6, private/none/placebo; registered E79-p2sol-reg 07:45). Same vendor as luna.
- `llm_p2claude` (claude-sonnet-5-5 sellers, seed 8100, k = 0..4, private/none; E79-p2claude-reg). Cross-family.
- `llm_p2ds` (deepseek-v4.1-flash, thinking disabled, Go; seed 8100 k = 0..14, private/none; E79-p2ds2-reg). Cross-family; best-effort.
- E89 (07:50, before llm_p2rep exists): frozen 6 auditor views on `llm_p2rep` (all 60, held-out; `replication.py --ds llm_p2rep`
  computed ONCE, lock `logs/final/P2REP_ONCE.lock`) and on `llm_p2cue` private/placebo/notes/none (descriptive).
- Part C (DIRECTION 10:25, registered E97/E98 at 10:4x UTC before generation): `llm_p2strong_luna` (gpt-6-luna, --framing strong,
  T=40, seed 9700, matched private/none k=0..2), `llm_p2strong_sol` (gpt-6.1-sol, same, k=0..1) = C1 pilot; the full C1 arm
  will be a NEW dataset with a new seed. `llm_p2g56sol` (gpt-5.6-sol), `llm_p2mimo` (mimo-v2.5, Go): lab, T=12, seed 8100,
  matched private/none k=0..6 (C2). No tuning; whole sets analysed once; fallback-model runs excluded.
