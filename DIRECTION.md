# DIRECTION — set by research director, 2026-10-23 22:00 UTC
Deadline 09:00 UTC; **finalize-only from 08:15** (no new experiments after 06:30, no new generation launched after 03:30).
The binding Validity requirements in PLAN.md still apply.

## Verdict
1. Good infrastructure and unusually honest self-correction (label leakage fixed, donor-memorisation leak found, learner parity). The interim codex review (`logs/review_interim.md`) is accurate. **Its ranked action list is your work plan.**
2. The current interim story is "structured view +0.086 pair AUROC". That number can't be interpreted yet, for four reasons:
   - text-only is at chance;
   - the gain may be the stats table, not cross-modal reasoning;
   - 7/8 `legit` runs were audited **without** their partnership metadata;
   - all-run interim peeks already consume the test split.
3. The most likely true headline: an untrained one-line statistic (pair price premium) probably beats every zero-shot LLM auditor. On partial data, private pairs sit at +0.8…+3.7 over rivals, vs ±0.5 for none/legit. Text adds little because LLM sellers keep coordination private. That is a strong, publishable answer to Q2.2 if shown cleanly. Don't fight it.

## Directives (priority order)
1. **Repair inputs before auditing the remaining ~80 runs** (review item 1):
   - Generate `public_info` per run at game end, not after all games.
   - Re-audit every `legit` run whose cached prompt lacked partnership info. Invalidate by prompt hash.
   - Fix the hardset fallback that only checks round 0, and stop caching failed checks as non-explicit.
   - Persist shuffle donor IDs, seeds and prompt hashes.
   - Make baseline `argmax` and cross-family `top_pair` tie-aware.
   Log each fix in EXPERIMENTS.tsv. Until this is done, every auditor number is provisional.
2. **Mechanism decomposition on identical runs, with paired bootstrap over runs:**
   - Views: `text`, `action`, `action_stats`, `combined`, **`combined+stats` (no consistency table, new)** and `structured`.
   - Add **two untrained, zero-shot statistical comparators**: (a) pair premium (pair mean minus the other two firms; every pair, not only the assigned one), and (b) 14's pCMI/pair_level per-pair scores. 14 is asked to write `../collusion-14-infotheory/results/eval/llm_v3_ext.json`. If it isn't there by 02:00, compute (a) yourself and drop (b).
   - Add the review's dev-calibrated late-fusion of the unimodal LLM scores.
   - Report **within-market localisation AUROC (positive runs only)** separately from pooled pair AUROC. n = runs, not pairs.
   - Freeze `analyze_llm.py` and these comparisons now, before the full data exists. Run the final test-split analysis **once**. Interim results stay labelled as dev.
3. **Shuffle ablation on LLM data, done properly:**
   - Use frozen, context-matched donors (same condition, similar cost/demand path), with 3 permutation seeds.
   - Reuse the action scores, so Δ is defined.
   - Report the intact-minus-shuffled difference with a paired CI.
   If text is at chance, the expected outcome is "no degradation". Report that as the finding: on LLM data the hybrid gain is not cross-modal. The scripted v2 result remains the mechanism demo, labelled as template-dependent.
4. **Required deliverables still missing from PLAN.md:**
   - **Evidence accuracy:** programmatically check cited rounds and quotes against the trajectory and ground truth.
   - **Cost table:** calls and characters from `~/collusion/llm_calls.jsonl`.
   - **FPR at a fixed dev-chosen threshold** on `none`, `legit` and tacit-high `none` runs. Report tacit as its own label, not as FP.
   - **Failure gallery:** 3–4 cases.
   - **Architecture takeaway:** stats always-on → LLM audit for evidence and explanation. Quantify it, e.g. AUROC and cost of auditing only the top-k% runs by premium.
5. **Cross-family and label confound (by 05:00):**
   - Re-run Claude Sonnet on the full mod3 subset (~42) for all views incl. `action_stats` after generation ends. Report Spearman and top-pair agreement, tie-aware.
   - Stratify auditor detection by **realised premium** within private runs. This is the cheap answer to "label ≈ condition": do auditors catch agreements that weren't acted on?
   - Optional exploration only if codex is idle by 01:00: 15–20 `private` runs under the firm framing (llm_v2 showed channel use without agreement). They act as natural "channel, no agreement" negatives. Report them as a separate stratum, never pooled into the headline.

## Cross-pollination
- **From 14:** its locked scripted finding that information-theoretic dependence detects coordinated *variation*, not *level*. Your LLM colluders mostly coordinate on level, so cite it to explain why `corr_change`/lockstep stats help less than premium. Also its anchor lesson (one JSON example value pinned all prices at 12). Your prompt has no example value: good. Note that the reason is that it was checked.
- **To 14:** `data/llm_v3` is being used as their second LLM dataset (read-only). Do not rewrite run ids or change the schema of existing files. Append only.
- 14's `llm_v1` has no public messages. Don't try to pool it.

## STOP
- All-run "interim" analyses that include test runs. Analyse dev only until the final locked run.
- Padding/length sweeps beyond the one existing `pad` variant (the review: it tests filler, not information).
- More scripted datasets or scripted tuning. Scripted is a mechanism demo and is done.
- Reporting `p_le_0` as a p-value. Call it bootstrap tail mass, or drop it.
- Figures before directives 1–3 produce final numbers. Make figures once, after the locked analysis.
