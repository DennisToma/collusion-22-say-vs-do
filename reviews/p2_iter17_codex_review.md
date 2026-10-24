# Iteration 17 — independent adversarial Codex review

Reviewed the uncommitted E99 completion safeguards against E99/E99-amend/E99-x/E103 and DIRECTION.md.
No full-arm data or partial scores inspected, no model calls, no files modified by the reviewer.

Verdict: no substantive change to frozen class definitions, thresholds, or detector contrasts. Expanded n<3 suppression
follows DIRECTION 1(iii). The reporting guard correctly rejects the assumption that selected price distributions must
match or that text separation alone establishes incremental value over actions.

Findings and resolution:

1. **P2: Raw E103 completeness unchecked.** Public completeness plus prompt reconstruction can accept silently truncated
   raw plans. Fixed: require all 160 raw round/firm keys per game; compare raw plans to saved private plans and raw prices
   to public trajectories. Legitimately empty model plans are allowed. Final input hashes include raw files and plan counts.
2. **P2: Old wrapper bypasses new flock.** Fixed operationally: checked old PID 662788 had only an idle sleep child;
   terminated that wrapper and the sleep explicitly, leaving generation alone, then relaunched the amended existing
   wrapper with setsid/nohup (PID 3033342). New wrappers take a nonblocking flock before prefetch or final work.
3. **P2: Invalid cached terms/audits require recovery.** Preserved fail-closed behavior; objective recovery procedure is
   documented in data/SPLITS.md. Archive invalid rows and retry identical prompts before any metric computation; never
   retry because of a negative label or low score. Plan parsing now retries missing/nonfinite/out-of-range probabilities.

Manager verification: synthetic completion/pipeline tests, existing prompt-boundary tests, and a disposable pilot smoke
run preserving every existing saved result key/value. No strongF aggregate was computed in this iteration.

Reviewer follow-up: all three findings resolved; no unresolved correctness issues. No real strongF data or scores inspected.
