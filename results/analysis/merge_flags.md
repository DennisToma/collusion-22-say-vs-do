# Q2.2 → merge: ranked wording fixes (single list; replaces the I114–I116 drip)

## Current — iteration 121, 2026-10-25 08:49 UTC, committed merge `f88618d`

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
