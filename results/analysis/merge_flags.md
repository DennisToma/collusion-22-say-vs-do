# Q2.2 → merge: ranked wording fixes (single list; replaces the I114–I116 drip)

## Current — iteration 125, 2026-10-25 09:30 UTC, merge `37e7193` (clean tree)
**0 open.** Draft hashes: SUBMISSION.md sha256 `4ac51cd8…`, SLIDES.md `4ac573ec…`. `python3 -S check_merge_sources.py` PASS (16 groups, 69 checks, 21 hashes).

| id | status in `37e7193` |
|---|---|
| 121-1 | applied (SLIDES §6: "we detect no contemporaneous co-movement … small gains not excluded") |
| 121-2 | applied (SLIDES l.76: "a two-stage audit … is a proposal we did not evaluate"; SUBMISSION l.307–311 adds "our evidence does not support recommending a particular architecture") |
| 123-1 | applied (SUBMISSION l.236–237: "no gain could be credited to text (…)") |
| 123-2 | applied (SUBMISSION l.224–225: "post hoc, not interpreted in the Q2.2 report … need not involve an agreement"; SOURCES M30) |

New Q2.2 text checked, no P1: locked-test labels "48 explicit, 2 information exchange" (matches `data/llm_v3/labels.jsonl`, runs 0030–0124, condition private); "14/50 communication-positive private test runs"; strict-executed rule definition (E99-amend); logbook sentence carries the instruction-length and batch-timing caveats (REPORT P2.5/E92); SOURCES M31 luna posting/silent keys. Not posted (P2 style only): l.235–237 says "cannot be credited to text" twice in a row.

---

## Superseded — iteration 123, merge `f88618d` + working tree
Draft hashes: SUBMISSION.md sha256 `16303443…`, SLIDES.md `645defc9…`. `python3 -S check_merge_sources.py` PASS (16 groups, 69 saved-value checks, 21 hashes). All new Q2.2 numbers in the working tree match JSON (luna silent +0.12 [−0.08, +0.32] = `e113_secondary.json:stratified.executed_vs_A.luna_silent_combined_minus_action_posthoc`; sol text 0.17 [0.01, 0.41] = `p2_family3way.json:llm_p2sol.views.text.auroc_private_vs_none`, which **REPORT does not state**).

| rank / id | where / status | current text | exact replacement | REPORT § / JSON key |
|---|---|---|---|---|
| P1 / 121-1 | `SLIDES.md` §6 / **applied** (working tree) | "…we detect no contemporaneous co-movement, and a zero-shot auditor gains nothing resolved from public messages (small gains not excluded)" | – | P2.0 / TL;DR 1 |
| P1 / 121-2 | `SLIDES.md` §6 "Practical reading" / **open** (SUBMISSION's hedged "could … serve … (not evaluated end to end)" is fine) | "Practical reading: a cheap level screen … as a first-stage *audit trigger*; expensive audits … only on flagged pairs. Not evaluated end to end." | "Price screens need model- and prompt-matched references; a two-stage audit (level screen, then private logs / dependence / provenance) is a proposal we did not evaluate." | TL;DR 7 / P2.7 / Limitations |
| P1 / 123-1 | `SUBMISSION.md` §5.3 E113 paragraph, new last sentence / open | "In these markets public text resolvedly hurt the auditor (Qwen) and nowhere resolvedly helped." | "In these markets public text resolvedly hurt the auditor (Qwen); no gain could be credited to text (the luna executed-game gain also appears in cells without public posts)." — REPORT says "cannot be credited to text", not that text never helped: the posting luna cells give +0.19 [+0.06, +0.33] (post hoc). | P2.16 E113-secondary; `e113_secondary.json:stratified.executed_vs_A.luna_posting_combined_minus_action_posthoc` |
| P1 / 123-2 | `SUBMISSION.md` §5.3 *Inversion* parenthesis / open | "(a gpt-6.1-sol seller arm with 0/7 private agreements is also inverted, 0.17 [0.01, 0.41], so inversion does not require an agreement)" | "(post hoc, not in the Q2.2 REPORT text: a gpt-6.1-sol seller arm with 0/7 private agreements also scores 0.17 [0.01, 0.41], 7 + 7 markets, so inversion need not involve an agreement)" — or drop it. The number is correct, but REPORT never interprets it; at n = 7 + 7 it supports "need not", not "does not require". Add the JSON key to SOURCES.md. | P2.6 table (sol row: text flags 3/21, location 0/0/21); `p2_family3way.json:llm_p2sol.views.text.auroc_private_vs_none` |

Other new Q2.2 text checked, no flag: abstract executed definition (48/149), glossary "Executed", slide invite rate 0.40 vs 0.88 (post hoc), placebo − private +0.03 [−0.54, +0.49], slide sample-size line, 1% prevalence "max 0.20" (Q1.4 number, not checked here).

---

## Superseded — iteration 121, 2026-10-25 08:49 UTC, committed merge `f88618d`

**All 7 original fixes are committed; 2 new P1s open in the newly added slides.** The previous working-tree risk is closed: P1-a and P2-b both landed in `f88618d`. [Pinned review receipt](merge_source_audit_i121.json) records full draft hashes, exact committed fix quotes, and the two new slide findings. `python3 -S check_merge_sources.py` PASS: 16 groups, 69 saved-value checks, 21 hashes; this checks frozen source values, not the latest draft automatically. Scientific results and the joint statement are unchanged.

### New P1s in new text only (recommendations; merge repo remains read-only)

| rank / id | where / status | current text | exact replacement | REPORT § / JSON key |
|---|---|---|---|---|
| P1 / 121-1 | `SLIDES.md` l.71 / open | Channel assignment (including its prompt cue) is visible as **how high** prices are — not **how they move together**, and not in **what is said publicly**. | Channel assignment (including its prompt cue) often changes price levels. Adding public text gives no resolved gain in the base market and replications; Qwen public text is informative but inverted for zero-shot auditors. | P2.0 / TL;DR 3 / P2.16; `results/analysis/p2_strong_eval_llm_p2qwenb.json:detectors.text.auroc_private_vs_none`; `results/analysis/p2_strong_eval_llm_p2qwena.json:detectors.text.auroc_private_vs_none` |
| P1 / 121-2 | `SLIDES.md` l.73 / open | Practical reading: a cheap level screen against a **model- and prompt-matched** reference as a first-stage *audit trigger*; expensive audits (private logs, dependence statistics, provenance) only on flagged pairs. Not evaluated end to end. | Price screens need model- and prompt-matched references. Our evidence does not support recommending a particular screening architecture; a two-stage audit remains a proposal for evaluation. | TL;DR 7 / P2.7 / Limitations (pair-relative screens); `results/analysis/p2_strongF_report_llm_p2strongF.json:markdown (premium flags strict-executed 2/13; descriptive frozen threshold)`; `results/analysis/p2_strongF_report_llm_p2strongF.json:E99_P3.paired_excess_private_minus_none` |

No new numerical estimates or P2 items. The sections below preserve the earlier review history; their working-tree notes are superseded by this committed check.

---


Checked against `collusion-beyond-words` HEAD `02ebfd2` (SUBMISSION.md sha256 `3c6ff0d2…`, clean tree), 2026-10-25 08:40 UTC.
P1 = merge text claims more than REPORT, or drops a caveat that changes meaning. P2 = style / partial.
All Q2.2 numbers in this draft were re-checked against REPORT/JSON: correct (incl. new paraphrase-1 CI +1.79 [+1.20, +2.43] = `p2_band.json:"sysvar1 (paraphrase 1)".private_minus_none_prem_r2_12`, which REPORT gives only as a point value).
No new items will be added unless they are P1 in newly written text.

## Update 2026-10-25 08:52 UTC — merge HEAD `e606cb7` + working tree (SUBMISSION.md sha256 `bba51050…`, uncommitted)
**All 7 fixes applied; 0 open.** P1-a (E133 caveat) and P2-b (Limitations placebo) are in the uncommitted working tree; P1-b (Fig. 5) and P2-a (abstract + §5.3 heading) are in HEAD `e606cb7`.
`check_merge_sources.py` PASS (16/16 groups, 69 checks, 21 hashes). New Q2.2 text in §5.3 ("a compliance rule that uses early prices *and* the privately judged agreed price") matches REPORT P2.17 E133e → no flag. The new Table 1 executed-only pair-level 0.87 is a Q1.4 number (not checked here).

## Formerly open (now applied)

| rank | id | where | status |
|---|---|---|---|
| P1-a | 114-4 | §5.3 l.247–249 E133 caveat appended verbatim (gpt-6.1-sol named) | applied (working tree, uncommitted) |
| P1-b | 116-2 | Fig. 5 caption l.275–276: "placebo − private over rounds 2–12 is +0.03 [−0.54, +0.49] (no resolved difference, not equivalence)" | applied (`e606cb7`) |
| P2-a | 114-2 | Abstract l.22 + §5.3 heading l.198: "no resolved gain" | applied (`e606cb7`) |
| P2-b | 114-3 | §7 Limitations l.325: "leaves delivery unresolved (private − placebo +0.38 [−0.41, +1.18])" | applied (working tree, uncommitted) |

## Applied (closed)

| id | what | where now |
|---|---|---|
| 115-5 | inversion range limited to resolved arms | Abstract l.24: Qwen "0.15–0.21, CI below 0.5" — matches Table 2 bold rows |
| 116-1 | "text helps only where the deal is the conversation" | Abstract l.25 now descriptive: "Text did work in an external negotiation dataset … (0.87 [0.83, 0.91])" |
| 114-1 | executed-only −0.30 names Q1.4 rule | §5.3 l.228 "executed under Q1.4's rule", rule defined in label table l.109 |

## I127 (09:50 UTC): Q2.2 source check of merge `reviews/codex_v2.md` (uncommitted, vs HEAD `37e7193`)
Merge HEAD unchanged; no new Q2.2 text, so no new flags from us. Each Q2.2 source key cited by the merge's codex_v2 review was checked against our JSON. **All are correct**, so its Q2.2 replacements can be applied as written:
| codex_v2 item | key | value in our JSON | verdict |
|---|---|---|---|
| P1 SLIDES l.65 "same premium" → no resolved difference, not equivalence | `placebo_llm_v3plc.json:windows.r2_12.placebo_minus_private_paired` | +0.03 [−0.54, +0.49] | supports the fix (same wording as our closed 116-2) |
| P2 SUBMISSION l.28 add window "rounds 11–40" | `p2_strong_classes_llm_p2strongF.json:n_tacit_high_none` | 19/20; `p2_strong_eval.py --late 11`, T = 40 → rounds 11–40 | correct |
| P2 SUBMISSION l.110 "for the strong-framing arm" | `…:n_strict_executed` | 13/20; floor 13 applies to strong framing only (REPORT label table) | correct |
| P2 SLIDES l.64 "≈ two thirds" vs no channel | `p2_cue_llm_p2cue.json:H3_notes_over_private_r2_12` | 0.65 [0.34, 1.32] = notes−none 1.04 / private−none 1.61 | correct |
The Q1.4 items (SLIDES l.68, SUBMISSION l.18) are not ours to check.

## I129 (10:05 UTC): merge HEAD `4e17126` (from `37e7193`; iter4 Opus final-claims fixes + iter5 check_sources.py)
check_merge_sources PASS (16/16 groups, 69 checks, 21 hashes). Merge working tree clean. Every new/changed Q2.2 number checked against our JSON — **all correct, no new P1, 0 open**:
| merge text | value | our source | verdict |
|---|---|---|---|
| SUBMISSION §5.3 inversion: "within the Qwen3.8-base no-channel arm, text score vs invite rate: Spearman −0.41 [−0.83, +0.18]" | −0.405 [−0.833, +0.178], n=15 | `e132_inversion.json:sets."Qwen3.8 base".spearman_text_vs_invite_rate_within_no_channel` (not stated in REPORT; REPORT cites the pooled 0.41–0.74, CI > 0) | number correct. P2 note only (not posted as an ask): the within-arm sign is opposite to the mechanism, and the pooled evidence REPORT cites (Qwen3.8 base 0.49 [0.17, 0.71]) is left out. Optional replacement: "(text score vs invite rate, both arms pooled: Spearman 0.49 [0.17, 0.71]; within the no-channel arm −0.41 [−0.83, +0.18], so the association comes from the arm difference)". The text is more cautious than REPORT, so not P1 |
| SUBMISSION Discussion: logbook pair premium +0.22 [+0.05, +0.40] vs +1.04 pricing notepad; caveats: longer instruction, later batch | +0.22 [+0.05, +0.40]; +1.04 [+0.65, +1.42] | REPORT P2.5 / `p2_logbook.json` | correct, caveats kept |
| Abstract: Qwen3.6 grid text 0.32 [0.24, 0.42], "CIs below 0.5" for both Qwen families | 0.32 [0.24, 0.42]; Qwen3.8 arms 0.15–0.21 CI < 0.5 | E113 / Table 2 | correct (closes the 115-5 scope: every listed range has CI < 0.5) |
| §5.3 SALT "in the full dataset (5169 executed episodes), 62% carry no explicit agreement" | 1 − 1989/5169 = 0.615 | `salt_d1.json`, REPORT P2.12 | correct |
| Glossary C − A: "Q2.2 contrasts use the designated-pair premium" | — | REPORT P2.5 / Table P2.5 | correct |
| Label table: strict-executed "for the strong-framing arm"; SLIDES placebo "no resolved difference … not equivalence"; "≈ ⅔ … vs no channel" | 13/20; +0.03 [−0.54, +0.49]; 0.65 [0.34, 1.32] | as in I127 | correct (codex_v2 items applied as checked in I127) |
