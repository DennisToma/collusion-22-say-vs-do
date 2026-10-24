# STATUS

## Current state (2026-10-24 18:13 UTC from date -u, Phase 2 iteration 29)
- Main claim unchanged: combined Δ −0.01 [−0.09, +0.06] locked test; −0.07 [−0.17, +0.02] pooled fresh n=90 (post hoc).
- **Iter 29 (DIRECTION 17:56 dir 4):** abstract 388 → 312 words. The plan-vs-tacit detail (0.76/0.82/0 agreement words/0.25) moved to TL;DR 5;
  the abstract now leads with the de-confounded E116 result ("among channel pairs, 13 vs 7, neither private plans (0.69 [0.44, 0.91]) nor public text
  resolvably predicts execution"). p2_claims snippets repointed: **27/27 OK**. REPORT 699 lines.
- Dir 1 (E116 within-agreement) was already done in iter 27. Second stratum not run (no frozen-view scores, no new calls allowed).
- Tests: test_audit_inputs (5), test_handoff (5) and test_mechanism_sources (1) FAIL on inventory/manifest staleness, as before this edit
  (checked against the pre-edit REPORT). Expected until the Sun 16:30 manifest rebuild; the other 3 test files pass.
- **E115** (sol newcomer) 9/30 complete at 18:12, generator alive; ETA ~20:00–21:00.
- **E113:** snapshot 48 games / 16 cells (sibling 438fa0973f). Cached audit done (28 new calls); coverage 16/16 cells complete, 0 unparsed; no scores read.
  Q1.4 E70 = 6 sweeps (ETA ~21:30–22:00); final `eval` ONCE when their STATUS says "6 sweeps complete" (or Sun 08:00).

## Next steps
1. 19:30: one Opus review of abstract + TL;DR + glance + P2.7 + P2.14 + P2.15 (DIRECTION dir 4); apply. Abstract 312 words: cut more only if the review says so.
2. E115: when "p2replS gen done": `P2REPL_ARM=sol uv run python p2_replace_eval.py` ONCE → S1–S4 into P2.15; adjust the replacement sentence; claim C26.
3. E113: rerun `snapshot` + `audit` (cached) as sweeps land; FINAL `eval` ONCE at 6 sweeps.
- Risk: .git is 88 MB (cap 100 MB). Don't commit raw caches; check `du -sh .git` before adding large data.

## Log
- 18:13 P2 iter29: abstract 388→312 words (E116 within-channel result now carries the plan sentence; plan-vs-tacit detail → TL;DR 5); p2_claims 27/27; E113 snapshot 48 games + cached audit started.
- 18:09 P2 iter28: E112 sentence → abstract/TL;DR; abstract 517→388 words; REPORT 724→701 lines (evidence checks → appendix); C25; E115 raw-cache stash incident fixed + disclosed.
- 18:00 P2 iter27: E116 within-channel contrast (p2_within_agree.py) → REPORT P2.7/abstract/TL;DR/glance; C24 claim; E3 dropped.
- 17:58 P2 iter26: Opus checkpoint review (reviews/p2_iter26_checkpoint_opus.md) applied to abstract/TL;DR/glance/P2.15/header; p2_claims +C04c/C22/C23 → 25/25 OK; E1 snapshot 36 games/16 cells, coverage OK.
- 17:51 P2 iter25: P2.11 three-pair abliteration line (Q1.4 E61, E69 + ours) + glance; p2_claims 22/22 OK; REPORT 711 lines.
- 17:48 P2 iter25: E113 E1-audit pipeline p2_e1_audit.py + snapshot (24 games/12 cells); E113-amend (luna posts no public messages in grid) registered pre-audit; shakedown 60 calls, coverage OK (no scores read).
- 17:35 P2 iter24: E112 final (P1–P4 held) → P2.15 + glance; E115 auto-launched 17:28; REPORT trimmed (limitations / next) to 711 lines.
- 16:42 P2 iter24: E115 sol-newcomer arm registered + queued (p2_replace_sol.sh); E112 9/30; STATUS iter23 stamp (16:35) was ahead of the clock (actual ≤ 16:27).
- 16:35 P2 iter23: E102 result (p2_qwen_strong.json) into P2.11/glance; P2.4 detail → appendix (REPORT 710 lines); fixed iter22 timestamps.
- 16:22 P2 iter22 (was mis-stamped 16:45): E114 claims×denominators (p2_claims.py), abstract C04 error fixed, denominators added (n = 60, 50/50, 15 + 15), header refreshed.
- 16:18 P2 iter21: E113 E1-audit plan registered (no grid data exist yet).
- 16:16 P2 iter21: E112 replacement registered, smoke-tested (0 calls for replayed prefix), launched; p2_replace_eval.py committed pre-outcome.
- 16:12 P2 iter21: E111 plan-view keyword baseline (p2_plan_keyword.py); abstract/TL;DR/P2.7 plan claim rescoped; E66 line; joint sentence 2 rescoped.
- 16:09 P2 iter20: E110 German result (P2.14 + glance); codex review of E99 write-up applied.
- 15:40 P2 iter20: E99 strongF final → P2.7/abstract/TL;DR/glance; p2_strongF_public.py; E110 German market registered + launched (llm_market --lang de, p2_de.py).
- 15:14 P2 iter19: C3c E109 registered, pilot run, dropped by registered price rule (base 9B prices below Nash); qwen9 max_tokens fix; REPORT P2.11 line.
- 14:16 P2 iter16: p2_strongF_fig.py (Part C class-path figure, pilot smoke test); no new experiments, waiting on E99 gen 24/40.
- 14:35 P2 iter15: REPORT consolidation (v1 summary + v1 limitations -> appendix; Phase-2 Limitations/What-next), 770 -> 692 lines.
- 14:12 P2 iter14: p2_strongF_report.py formatter (pilot smoke test); P2.4 circularity caveat, E44 cite in P2.7, merger sentence 1.
- 14:10 P2 iter13: Opus adversarial review (directive 4) applied to abstract/TL;DR/glance/P2.11/P2.12 (14 items, no number changes).
- 14:03 P2 iter12: E99-x exploratory strict-executed vs tacit-high contrast registered + added to p2_strong_eval.py (pilot smoke test: old keys unchanged).
- 14:01 P2 iter12: E100 C3 result (P2.11), E98 C2 final, abstract/TL;DR/glance consolidation, P2.1-3 -> appendix.
- 13:55 P2 iter11: E105 result (sol text AUROC 0.87 on SALT, tacit 0.81), TF-IDF condition-grouped 0.91; P2.12 + abstract + takeaway.
- 13:30 P2 iter11: Part D1 SALT external say-vs-do: E104 result (all 3 predictions held), E105 sol text auditor launched, salt_d1.py, REPORT P2.12.
- 13:25 P2 iter10: P2.6 final (E95 3-way, all predictions held), P2.7 compressed, C3 post chain unblocked, p2_qwen_cmp.py.
- 12:36 P2 iter9: Opus review of P2.7/P2.9/P2.10 applied (p2_asym_nash.py competitive benchmark, E45 replication, prediction list).
- 12:31 P2 iter9: E86 p2aware result (P2.9; labels 20 calls), abstract sentence; asym renumbered P2.10.
- 12:27 P2 iter9: codex review applied to abstract/TL;DR/P2.4-P2.9; p2_strong_eval enforces n<3 descriptive rule.
- 12:20 P2 iter9: E87 asym result (P2.9; cost-adj P2 failed); E99-amend + E103 plan view registered, pilot calibration; strongF post chain w/ prefetch; p2coded killed; codex review launched.
- 12:10 P2 iter8: p2rep computed once (E80/E89 held; P2.8), E84 on p2rep, pooled E101; chain6 0-call bug -> chain6b; C3 qwen E100 + E102 launched; strong pilot final.
- 11:39 P2 iter7: luna pilot final 2/3 executed (strict 2/3); seed 2 executed floor 18 but matched no-channel market also 18.0 -> executed adds ~0 over tacit. g56sol started.
- 11:17 P2 iter7: E97 interim pilot (luna 1/2 executed, market-wide high prices, sol 0/1); E99 full arm registered+launched; REPORT P2.7.
- 10:31 P2 iter7: part C launched (E97 C1 strong pilot, E98 C2 older sellers registered first); p2_strong.py; REPORT P2.7 stub.
- 09:57 P2 iter5: codex review of E78+E93 applied (agreement labels qualified, say-vs-do attribution withdrawn, sol wording softened).
- 09:28 P2 iter5: E78 para2 result (band failed, p2_band.py); E93 review applied, refreshed to 10 ds seeds; E91-ext chain6 launched.
- 09:25 NOTE: earlier iterations stamped STATUS/EXPERIMENTS times ahead of the VM clock (e.g. E92 amend "09:58" was committed 09:20). Always use `date -u`.
- 09:22 P2 iter5: E93 interim family snapshot (p2_interim.py); REPORT P2.6/TL;DR 8/takeaways; Opus review launched.
- 09:58 P2 iter4: codex pre-outcome review of E92 applied as amendment (direction-aware/strict verdicts, completeness asserts).
- 09:40 P2 iter4: E92 logbook control registered + launched; p2_logbook.py; Phase 2 takeaways block in REPORT.
- 09:15 P2 iter3: E78 paraphrase 1 interim (+1.79 vs +1.75 orig, same seeds) in P2.5.
- 09:11 P2 iter3: Opus review of P2.6 applied; E91 frozen auditor views on Claude markets (text views flag 10/10 incl. none: public invitations).
- 08:58 P2 iter3: P2.6 Claude family result (E79-p2claude, E90 p2_family.py), REPORT P2.6 + TL;DR 8.
- 08:44 P2 iter2: P2.5 cue result (E77, H3 failed: notepad gives ~65% of premium), text LR on cue arms (E82b), Opus reviews E84e + P2.5 applied; chain4 for families.
- 07:58 P2 iter2: seller families sol/Claude/deepseek launched (E79 amendments); E84b/c/d; E89 registered + chain3; REPORT appendix split.
- 07:10 P2 iter1: E84 behaviour labels (P2.4); gaps 5/7/8 generator + E86-E88 registered, chain2 queued; TL;DR item 6.
- 06:53 P2 iter1: Opus design review (E85) applied: registration amendment, script fixes, REPORT wording.
- 06:43 P2 iter1: generator conds + matched seeds; E77-E83 registered; E81/E82/E83 done; generation launched (codex + Go).
- 06:20 iter 30: TL;DR block in REPORT (E75); handoff exports + manifest rebuilt; all verifiers/tests PASS. No new experiments from here.
- 06:10 iter 29: E74 cross-family label re-judge (label_xfam.py, 115 Sonnet calls), REPORT, exports, manifest; codex review logs/review_iter29_xfam_label.md.
- 05:50 iter 28: final claims audit (E73), codex + Opus; framing fixes in REPORT; exports/manifest rebuilt; test phrase updated.
- 05:35 iter 27: E71 level-column ablation (action_stats_nolevel, 155 audits, nolevel_view.py); checker/verifier counts 44->46 caches, 2,213->2,368 audits; codex review applied; REPORT/exports/manifest refreshed.
- 05:40 iter 26: E70 markup_baseline.py (comparison-free markup vs premium; own-cost variant after Codex review logs/review_iter26_markup.md); REPORT, exports, manifest updated.
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


- 2026-10-24 06:18 UTC iter 31: E76 summary/handoff finalization. Independent Codex and Opus reviews applied to TL;DR, abstract, README and talk: remove unsupported causal explanations, distinguish run detection from within-market localisation and test from replication, clarify raw-action/statistics views and non-equivalence. Added six source-linked presenter Q&As, E74 label robustness on slide 2 and uniform-stratum caveat in notes; repaired stale monitor judge caveat. Browser QA exposed a pre-existing focus/keyboard bug (Present retained focus; ArrowRight was ignored); fixed while preserving native Space activation, reproduced before/after, and asserted all seven slide transitions. Actual all-slide QA found and fixed slide 3 overflow at 1024x768. Five desktop layouts, mobile, no-JS reading and offline checks pass. Exports preserve 28 report / 7 talk pages, 341 cells, 477 report + 102 slide fragments and 8 figures. All 47 tests, 424 hashes, 2,368 audit-input checks and source/export freshness pass. Every scientific input/cache/result/figure/analysis/receipt unchanged; 417/424 previous manifested files identical. Review: reviews/iteration31_summary_handoff.md. No experiments, model audits, label judging, AUROC/bootstrap or threshold recomputation. Inherited log timestamps are retained unchanged; this entry uses date -u.

### 2026-10-24 10:03 UTC (P2 iter6)
- Directive 1 done: new Abstract/TL;DR (Phase 2 answer), P2.5/P2.6 condensed, appendix §P2-detail. Fixed sol public-invitation cell to the none arm (0/192; was all arms 0/576); luna none 7/720 verified.
- Directive 2: chain3 restarted with p2rep before p2cue. Directive 3: E94 registered 09:58 + launched. Directive 4: E95 registered 10:02 + p2_family3way.py. Ledger correction row (6 rows stamped after their commit).
- 10:09 E92 result landed (C_strict); codex review E96 applied to Abstract/TL;DR/takeaways/P2.2/P2.4-P2.6; reimpl corrected to 30/32.

- 14:33 P2 iter17 (fallback Codex manager): E99 completion/provenance hardening and reviewed handoff, no new experiment. Added exact registered seed/condition/model/round/firm checks, raw decision coverage + saved-plan/public-price equality; same-model finite-score/current-prompt coverage on all frozen views; atomic immutable class publication before remaining audits; saved-result/local run-once guards; E103 secondary threshold 58 flags. Existing scalar scorers/class rules/primary thresholds and prior pilot outputs unchanged. Switched only the idle old post wrapper/sleep to the amended flock-protected existing script; generator stayed running.
- 14:33 iter17 verification: 17 synthetic tests PASS (`uv run python -W ignore::ResourceWarning -m unittest discover -s tests -p test_strongf_completion.py -v`), 7 existing boundaries PASS (`PYTHONPATH=tests uv run python -W ignore::ResourceWarning -m unittest test_audit_inputs.PromptInputTests -v`), bash syntax PASS, disposable pilot old keys/values identical. Live check-only rejected 27/40; no class/result was created. `check_audit_inputs.py` fails at frozen inventory check because Phase 2 added caches, alongside the already-known stale manifest; no handoff artifacts rebuilt.
- 14:33 iter17 interpretation adjustment to director 1(ii), justified by the code and independent review: strict requires pair excess >=+2 after agreement; tacit-high requires market excess >=+2 in rounds 11–40. Different selections do not guarantee equal price distributions or price AUROC=0.5. Preserved E99-x prediction, but formatter now lists action controls separately and warns that text/plan separation alone does not establish incremental gain. REPORT replacements only (692 lines); no results changed. Review: reviews/p2_iter17_codex_review.md; objective cache-recovery procedure: data/SPLITS.md.

- 14:34 iter17 director steering: DIRECTION.md changed during verification (Dennis 14:30 Part E). Read the new diff and queued its E1–E5 instructions for after in-flight Part C, which is still generating; this supersedes the earlier blanket "no new registered experiments" for those directed designs. Did not start a second research chunk. Director edits will be included intact in the milestone commit.

- 2026-10-24 14:52 UTC P2 iter18 (fallback Codex manager): completed Part E4 zero-new-games anomaly hunt, E108a–e. Registered sampling before reading, then disclosed all five specific follow-ups as post-hoc after transcript review/preliminary helper counts. Sampled committed snapshots (24 eligible datasets per repo, 1038 eligible games; 20 datasets per repo selected), archived portable gzip + source hashes, and reviewed all 40 public/private transcripts / 841 rounds with two read-only Codex helpers. No live strongF/Qwen-strong data in the sample, no seller/auditor calls or headline evaluation. Scheduling rationale: E99 is still generating, so this independent zero-call work uses the wait without taking backend capacity; no new generation arm started.
- iter18 results: q14 strong_luna_C001 band compliance37/40 vs exact target1/40, equal prices8/40, persistent unequal12/13 for28 rounds (opening promises may be one-round only); q14 g56l/para disclaimers21/27 with equal pairs12/18 and13/15 thereafter, not proof of coordination/intent. q22 p2rep0048 A18 all12 rounds and strictly lowest relative profit each round (A1147.47, B2144.49, C2214.21, D2034.52), not a counterfactual harm result. Mixed q22 endings10/20 games any drop,21/80 firms (same state3/8,3/32); Claude withdraws21->19, GLM precommits/keeps20. Narrow numeric declarations143 (72 private,71 public),0 mismatches across10 games: same-response consistency only.
- iter18 verification/review: all40 archived transcripts and selected source blob hashes equal recorded git objects, including private chats; horizon/contiguity/unique firm/ID checks pass. Byte-identical analysis regeneration and freeze refusal verified. Independent q14 reviewer reproduced8 tolerance +2 disclaimer rows; q22 counts match separate transcript review. All five framing corrections applied; reviews/p2_iter18_serendipity.md. Corrected REPORT's false equivalence of Q1.4 +/-1 and Q2.2 lower-bound execution compliance; registered rules/results untouched, E66 adapter checked and already mirrors ours. Existing17 strongF tests and read-only transition-source checker pass. Case plot generated and visually inspected; old transition detail moved unchanged to appendix, REPORT692->689 lines. No handoff export/manifest rebuild.
- iter18 director steering: DIRECTION gained the separate Serendipity Explorer at runtime; read its HITS.md (none yet). Decision: no registered confirmation warranted without a hit; do not duplicate its pilots. E4 is now done; C3c and other Part E generation designs stay queued behind in-flight C.
