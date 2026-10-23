The interim results support **a benefit from structured inputs for this auditor**, not yet a benefit from cross-modal reasoning.

**1. The decomposition is necessary but insufficient.**

`structured` adds both action statistics and a computed stated-versus-actual table; `action_stats` removes both public text and that table. Their difference therefore mixes text, supplied cross-modal computation, and length ([auditors.py:94](/home/factory/collusion/collusion-22-say-vs-do/auditors.py:94)).

Add `combined + statistics, without consistency table`; compare it with `action_stats` to isolate text, and with `structured` to isolate the table. `combined + consistency table, without statistics` completes the planned feature-removal control ([PLAN.md:41](/home/factory/collusion/collusion-22-say-vs-do/PLAN.md:41)). Also compare against dev-calibrated late fusion of unimodal scores: complementary independent cues can improve performance without relational reasoning.

Shuffle degradation alone does not establish the claim in [PLAN.md:39](/home/factory/collusion/collusion-22-say-vs-do/PLAN.md:39). Current donors match label, condition, and trajectory length, but not cost/demand histories or price regimes. Shuffling can create conspicuous impossibilities. Use several frozen permutations, context matching, and a paired intact-minus-shuffled contrast; verify text-only performance remains stable.

Padding matches approximate **characters**, not tokens, information, or evidence placement; repeated filler also changes attention ([auditors.py:206](/home/factory/collusion/collusion-22-say-vs-do/auditors.py:206)). It tests sensitivity to filler length, not whether gains reflect “more information.”

**2. Metric code: sound foundations, consequential gaps.**

- **Pair AUROC:** construction is correct for “assigned pair with verified communication”; bootstrapping whole runs preserves pair dependence ([analyze_llm.py:43](/home/factory/collusion/collusion-22-say-vs-do/analyze_llm.py:43)). But pooled AUROC mixes between-market discrimination with within-market localization. Add positive-run within-market AUROC. The independent sample is 36 games, not 216 pairs.

- **Paired Δ:** sharing bootstrap samples and recomputing the best single modality per draw is appropriate. However, `p_le_0` is bootstrap tail mass, not a calibrated hypothesis-test p-value. NaN differences become `False` under `db <= 0`, understating that fraction; filter finite draws or stratify resampling ([analyze_llm.py:64](/home/factory/collusion/collusion-22-say-vs-do/analyze_llm.py:64)). Interim peeking and multiple comparisons also weaken significance claims.

- **Ties:** fractional credit in `analyze_llm.py` is correct. Baselines use first-index `argmax`, creating pair-order bias ([baselines.py:138](/home/factory/collusion/collusion-22-say-vs-do/baselines.py:138)). Cross-family agreement compares deterministic `top_pair`; two flat scorers can appear perfectly concordant ([cross_family.py:44](/home/factory/collusion/collusion-22-say-vs-do/cross_family.py:44)).

- **Shuffle:** singleton strata crash the LLM implementation ([auditors.py:151](/home/factory/collusion/collusion-22-say-vs-do/auditors.py:151)). Baselines instead relax condition matching or leave inputs intact, and fail to rewrite firm references inside donor messages ([baselines.py:44](/home/factory/collusion/collusion-22-say-vs-do/baselines.py:44)). More seriously, growing the donor pool changes previously assigned inputs while cached outputs remain: I verified **15/36 changed** when expanding to 39 runs. Persist donor IDs, seeds, and prompt hashes. Label-conditioned shuffling is an oracle diagnostic, not directly an input leak.

- **Splits/comparisons:** the `<30` predicate correctly separates the frozen IDs ([analyze_llm.py:99](/home/factory/collusion/collusion-22-say-vs-do/analyze_llm.py:99)); it lacks dataset/range validation. Optional view files silently change the common cohort. The planned shuffle omits `action` ([STATUS.md:15](/home/factory/collusion/collusion-22-say-vs-do/STATUS.md:15)), so analysis cannot produce Δ unless unchanged action scores are explicitly reused. No paired cross-variant contrast exists.

- **Hard-set bug:** once a cache exists, an unchecked run’s fallback records only its first round; I reproduced missed explicit language in round two ([analyze_llm.py:27](/home/factory/collusion/collusion-22-say-vs-do/analyze_llm.py:27)). Failed LLM checks are cached as nonexplicit ([hardset.py:43](/home/factory/collusion/collusion-22-say-vs-do/hardset.py:43)).

- **Actual input omission:** seven of eight currently labelled `legit` runs lack partnership metadata. Rendering silently omits it ([auditors.py:185](/home/factory/collusion/collusion-22-say-vs-do/auditors.py:185)); metadata generation occurs after all games finish ([llm_market.py:238](/home/factory/collusion/collusion-22-say-vs-do/llm_market.py:238)). Existing caches will preserve those incomplete prompts.

**3. Label ≈ condition limits the scientific claim.**

You can claim discrimination/localization of **private agreement or information exchange under this generator**. You cannot yet claim detection of realized supra-competitive collusion, separation from opportunity/framing effects, or generalization across sellers. The report’s communication-only target differs from the plan’s agreement-plus-conduct definition ([REPORT.md:32](/home/factory/collusion/collusion-22-say-vs-do/REPORT.md:32), [PLAN.md:78](/home/factory/collusion/collusion-22-say-vs-do/PLAN.md:78)). Unassigned pairs and no-channel runs are not verified negatives for every broader coordination definition.

The +0.086 structured gain and negative combined pair gain specifically leave the statistical-summary explanation open ([REPORT.md:90](/home/factory/collusion/collusion-22-say-vs-do/REPORT.md:90)). The all-run interim already includes test observations; preserve remaining unseen data for confirmation rather than calling repeated all-run analyses “locked” ([data/SPLITS.md:6](/home/factory/collusion/collusion-22-say-vs-do/data/SPLITS.md:6)).

**4. Ranked actions for ten hours.**

1. **Repair inputs and provenance:** complete partnership metadata, fix hard-set aggregation, invalidate affected caches, freeze cohorts and donor mappings.
2. **Resolve the mechanism:** finish `action_stats`; add combined-plus-statistics without consistency; bootstrap direct differences on identical runs.
3. **Run controlled shuffles:** frozen context-matched donors, multiple seeds, unchanged action comparator, paired degradation intervals.
4. **Challenge the label confound:** prioritize private-channel nonagreement cases and agreement-without-conduct cases; manually verify a stratified label sample.
5. **Freeze and report:** confirm on unseen runs, finish Claude replication, correct ties, and include concrete evidence-checked successes/failures. Defer cosmetic figures and broad padding sweeps.
