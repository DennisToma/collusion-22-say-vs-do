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
