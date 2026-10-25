# Q2.2 → merge: ranked wording fixes (single list; replaces the I114–I116 drip)

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
