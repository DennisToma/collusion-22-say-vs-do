# Splits (frozen 2026-10-23 21:45 UTC, iteration 3)

## llm_v3 (headline LLM-market data, 125 runs planned, ids llm_v3_0000 … llm_v3_0124)
- **dev** = llm_v3_0000 … llm_v3_0029 (30 runs). Any auditor-prompt / feature / threshold iteration may only
  look at metrics on these runs. The preliminary numbers seen in iteration 2 (n=14) were all from dev.
- **test (locked)** = llm_v3_0030 … llm_v3_0124. Metrics on test are computed once, with the frozen config.
- Frozen auditor config: `auditors.py` TASK/WHAT/render as of commit 5f2d8a0 (gpt-6.1-sol, max_tokens 600).
  The auditor prompt was written before any LLM-market data existed and has NOT been tuned:
  **tuning attempts on llm_v3 = 0** (update this line if that changes).
- Because no tuning happened, REPORT headline = all labelled runs (dev ∪ test) with the frozen config; the
  test-only numbers are reported alongside as the held-out check. If any tuning is done later, the headline
  switches to test-only.
- Run order is randomised over conditions by `llm_market.py --seed 3000`, so the split is condition-balanced
  in expectation.

## scripted_v1 / scripted_v2 (mechanism demo only)
5-fold CV grouped by run_id (GroupKFold); no tuning beyond the learner choice (LR primary, GBM secondary).
