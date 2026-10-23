1. **P1 — Retry failures disappear.** [finalize_test.sh:34](/home/factory/collusion/collusion-22-say-vs-do/finalize_test.sh:34): child `bash -c` shells lack `pipefail`; Python can fail while `tee` returns zero, bypassing `FAILED_STEPS.txt`. Confirmed with a synthetic shell pipeline. **Fix:** use `bash -o pipefail -c` for every retry pipeline.

2. **P1 — STARTED is mistaken for completion.** [finalize_test.sh:25](/home/factory/collusion/collusion-22-say-vs-do/finalize_test.sh:25): interruption between stamping and invocation consumes the headline attempt. On resume, any existing JSON—including a stale or truncated artifact—permits silently skipping it. **Fix:** distinguish STARTED/DONE, write JSON atomically, and require DONE plus validated output; interrupted attempts require explicit investigation/disclosure.

3. **P2 — Schema protection still permits headline crashes.** [final_analysis.py:278](/home/factory/collusion/collusion-22-say-vs-do/final_analysis.py:278): top-level `[]` crashes at `.get`; records containing `score: null` or strings pass validation but crash at `np.isfinite`, after primary metrics were computed. **Fix:** validate the root mapping and numeric score types before processing sibling data.

4. **P2 — Floating arithmetic breaks exact rank-sum ties.** [incremental.py:55](/home/factory/collusion/collusion-22-say-vs-do/incremental.py:55): dividing before addition gives unequal floats for mathematically equal sums. Synthetic denominator 180: ranks `(1,4)` and `(2,3)` differ. Exact metric comparisons then award arbitrary wins. **Fix:** sum integer doubled midranks before normalization.

5. **P2 — Bootstrap freezes a sample-dependent transformation.** [incremental.py:60](/home/factory/collusion/collusion-22-say-vs-do/incremental.py:60): resampling fixed `C` omits uncertainty from pooled percentile estimation. **Fix:** recompute ranks and combinations within each bootstrap multiset, preserving duplicate multiplicities.

6. **P2 — Complementarity assumes independent tie breaks.** [incremental.py:75](/home/factory/collusion/collusion-22-say-vs-do/incremental.py:75): identical two-way ties produce 0.25 “view-only-right” per run despite identical information. **Fix:** explicitly label independent-randomization expectations or report top-set overlap and uniquely correct counts.

Read-only review; no test-split commands executed.
