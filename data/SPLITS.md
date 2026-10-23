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

## scripted_v1 / scripted_v2 (mechanism demo only)
5-fold CV grouped by run_id (GroupKFold); no tuning beyond the learner choice (LR primary, GBM secondary).
