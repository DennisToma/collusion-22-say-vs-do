# STATUS

## Current state (2026-10-24 05:03 UTC, iteration 25)
- LOCKED TEST DONE (00:03), REPLICATION DONE (02:07); never rerun; detection estimates unchanged.
- Test: premium run AUROC .95; action_stats .86; combined-minus-best-unimodal -.013 [-.091,+.064].
- Replication (n=30): premium .92 vs action_stats .80; 4/4 registered rules held (not equivalence).
- Placebo premium flags 14/15 with/without delivery; channel/condition confound remains.
- E69: 57/2,925 evidence items have parsed leading price transitions; 54 adjacent + 3 earlier endpoints match.
- Grammar omits joint/simultaneous wording; 52+17 further numeric-span items exposed without validation labels.
- Endpoint agreement is not explanation accuracy; the proposed explanation role remains unvalidated.
- Codex + Opus critiques applied; final Codex diagnostic recheck has no consequential findings.
- 47 tests / 412 hashes pass; clean export write-free; 2,213 prompts still 1,903 hashes + 310 length-only.
- Refreshed report: 26 pages / 8 figures; talk unchanged at 7 slides; scientific artifact bytes unchanged.
## Next steps (no new generation after 03:30; no new experiments after 06:30; FINALIZE 08:15)
1. Keep detection results frozen; present PRESENTATION.pdf or PRESENTATION.html. Send REPORT.pdf for detail.
2. Read-only: python3 -S verify_artifacts.py; uv run python check_audit_inputs.py; python3 -S check_price_transitions.py --check.
3. If REPORT.md changes, regenerate handoff exports and update the post-hoc manifest (README instructions).

## Log
- 04:40 iter 23: read-only integrity re-check (E67): verifier, handoff/presentation checks, audit-input check, 27 unittests all PASS. No changes to results; remaining open items (evasion, second seller model) need new generation, barred after 03:30.
- 04:05 iter 18: Figure 1 summary figure (E62) inserted after abstract; reproduce line added.
- 03:56 iter 17: repro check (E60); final codex+Opus claims audit applied (E61); abstract shortened; appendix D/E.
- 03:39 iter 16: applied codex + Opus reviews of placebo section (E59).
- 03:33 iter 16: placebo stratum E58 (generator condition placebo, placebo.py, 90 audits, REPORT); codex review launched.
- 02:37 iter 15: codex review_iter15_hint applied (E57).
- 02:32 iter 15: action_stats_hint exploration (E56, 155 gpt-6.1-sol calls), hint_view.py, REPORT section + abstract sentence; codex review launched.
- 02:21 iter 14: REPORT restructure (flag-rate tables, other test results -> Appendix C; numbers unchanged).
- 02:20 iter 14: applied e2e reviews (E55).
- 02:16 iter 14: evidence_rounds.py (E54) -> REPORT exploration; e2e reviews launched.
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

- 03:58 iter 19: E63 offline handoff: discovered original run-once locks are gitignored; added portable completion receipt + guards (test/all and replication smoke variants, fail closed on corrupted/deleted receipt/result). Added standard-library read-only verifier, post-hoc manifest, README and 9 isolation tests. Independent Codex review fixes applied; summary caption now discloses test exposure, duplicate figure numbering fixed, panel-b causal wording softened; no scientific estimates changed. Protected dev/test hashes match original replication record. VM date -u used for this entry; inherited iter17/18 timestamps retained unchanged.
- 03:59 iter 19 verification: Git-index-only export passes offline verifier and completion guard without logs/final/; all exported file hashes unchanged. Initial export assertion incorrectly expected no logs/ directory (six review files are tracked); corrected to check missing evaluation locks and unchanged inventory. No product failure or metric rerun.

- 04:07 iter 20: E64 presentation-only handoff: build_presentation.py renders seven offline HTML slides plus speaker notes and SHA-256 source hashes from existing JSON; --check is write-free. REPORT/README link it; verifier and post-hoc manifest cover freshness (396 hashes). Independent Codex reviewer found no blocking issues; all 3 minor caveats applied. Chromium checked navigation, JavaScript-disabled reading, zero external requests, local links, desktop/mobile layout and 7-page print. All 11 tests pass via uv (initial system-Python invocation lacked sklearn, so evaluator-import assertions failed before any metrics). All pre-existing scientific data/results/figures/receipts/analysis hashes unchanged. No generation, LLM audit calls, metrics, bootstrap or threshold refitting. Review: reviews/iteration20_presentation.md.

- 2026-10-24 04:20 UTC iter 21: E65 portable handoff: saved-result slides PDF, full report PDF and standalone HTML with embedded figures; build_handoff.py + optional locked renderer dependencies and post-hoc source/output receipt. Independent Codex review found absolute VM paths in PDF links; fixed to GitHub links before printing. Checks preserve all 18 headings, 317 cells, 441 report text fragments (including reproduction code), 100 visible slide fragments and 8 figures; 7 slide pages, 25 report pages (2 landscape appendix tables). PDFs have no machine paths or clipped text; relocated standalone HTML works offline without JavaScript at mobile/desktop widths. 401 hashes and 14 isolation tests pass; clean Git-index export verified without locks or writes. Every original scientific data/result/figure/receipt/analysis hash unchanged. No generation, audit calls, metrics, bootstrap or threshold refitting. Review: reviews/iteration21_portable_exports.md.

- 2026-10-24 04:32 UTC iter 22: E66 cached-input provenance: new read-only checker imports the frozen renderer without entering the historical auditor CLI (whose --verify path regenerates metadata). All 44 caches / 2,213 audits reconstruct: 1,903 recorded 64-bit prompt-hash prefixes match; 310 legacy rows have only matching lengths (150 original dev, 120 original test, 40 cross-family). Added public-info/setup checks, frozen donor/context/pair checks, independently checked shuffled recipient actions, injected-private-field and withheld-modality controls, and positive controls for retained observables. Post-hoc receipt freezes individual hash eligibility and all 68 sources; stdlib verifier validates receipt freshness. Codex + Opus critiques applied (complete source/count coverage, hash-vs-length wording, alternate-root identity, missing/stale receipt refusal); final Codex recheck found no consequential issues. All 27 tests and 404 hashes pass; clean Git-index export preserves all file hashes/mtimes/inventory and refuses completed evaluation without local locks. REPORT/README updated; regenerated 25-page report/7-page talk exports preserve 442 report fragments, 317 cells and 8 figures. Every scientific input/cache/result/figure/analysis/evaluation-receipt hash unchanged. No generation, audit calls, AUROC/bootstrap or threshold refitting. Review: reviews/iteration22_audit_inputs.md.

- 2026-10-24 04:47 UTC iter 24: E68 evidence-source coverage and offline ledger: six original GPT views on 95 test + 30 replication runs, 750 audits / 2,925 evidence items (2,229 test, 696 replication), all well-formed anchors; only four quote-marked phrases, all text-view and literally present in cited firm/round (two generic repeated phrases). This does not validate semantic accuracy; REPORT/README now make the untested explanation role explicit. New standard-library renderer/checker hashes all 16 public-data/cache inputs plus its source, preserves every cached observation, exposes all 1,500 public rounds / 6,000 firm observations and ties prose counts to JSON. Codex + Opus reviews applied; final Codex recheck found no consequential issues. Numeric/multiline quotes, malformed anchors, missing semantic support, private-field exclusion, corruption detection and no-JS navigation addressed. All 36 tests, 408 manifest hashes, original prompt checks and browser checks pass; clean Git-index export is write-free without evaluation locks. Refreshed report 26 pages / 443 text fragments / 317 cells / 8 figures; talk remains 7 pages. Every original scientific input/cache/result/figure/analysis/evaluation/provenance receipt hash unchanged. No generation, label judging, auditor calls, AUROC/bootstrap or threshold refitting. Review: reviews/iteration24_evidence_sources.md.

- 2026-10-24 05:03 UTC iter 25: E69 selective price-transition source census: 51/2,229 test + 6/696 replication items, six original GPT views. All parsed endpoint pairs match public logs (54 adjacent, 3 earlier starts); this is not semantic accuracy. Concrete 18→16→14 example demonstrates failure of historical same-round and ±1-round number proxies; historical outputs untouched. Codex + Opus reviews confirmed counts; Opus identified grammar bias against jointly/simultaneously wording. Kept validation grammar fixed, disclosed omissions and absent advance commit/registration, and added a separately labelled lexical diagnostic exposing 52+17 unparsed numeric-span items (can describe costs/later clauses; never counted as endpoint successes). Stronger REPORT/README count guards, missing-private-files checks, multi-firm/invalid-anchor/negative controls and historical-regex counterexample tests. Final Codex rechecks found no consequential issues. 47 tests / 412 hashes pass; 403 pre-existing manifested artifacts unchanged, including every scientific input/cache/result/figure/analysis/evaluation/provenance receipt. Refreshed 26-page report preserves 444 text fragments, 317 cells and 8 figures; talk remains 7 pages. Clean Git-index export passes all six read-only checkers and completed-evaluation refusal without locks; hashes/mtimes/inventory unchanged. No seller generation, label judging, new scientific audit calls, AUROC/bootstrap or threshold refitting. Review: reviews/iteration25_price_transitions.md.
