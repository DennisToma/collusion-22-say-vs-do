# Q2.2 → merge: ranked wording fixes (single list; replaces the I114–I116 drip)

Checked against `collusion-beyond-words` HEAD `02ebfd2` (SUBMISSION.md sha256 `3c6ff0d2…`, clean tree), 2026-10-25 08:40 UTC.
P1 = merge text claims more than REPORT, or drops a caveat that changes meaning. P2 = style / partial.
All Q2.2 numbers in this draft were re-checked against REPORT/JSON: correct (incl. new paraphrase-1 CI +1.79 [+1.20, +2.43] = `p2_band.json:"sysvar1 (paraphrase 1)".private_minus_none_prem_r2_12`, which REPORT gives only as a point value).
No new items will be added unless they are P1 in newly written text.

## Open

| rank | id | SUBMISSION line | current text | exact replacement | REPORT § | JSON key | status |
|---|---|---|---|---|---|---|---|
| P1-a | 114-4 | §5.3 l.236–240 (E133 paragraph) | "…beats the best raw early-price rule (0.94 vs 0.885, Δ +0.06 [+0.02, +0.10], post hoc), with no evidence that its edge comes from public messages." | append: "This is the third analysis of the same 78 games; the rule score was fixed after E133c/d were seen, the LLM prompt states the label rule, and the same model (sol) is Q1.4's label judge and extracted the agreed price." | P2.17 (E133e paragraph, "Post-hoc caveat") | `e133e_attr.json:b_llm_E133d_minus_raw.rule_score` | open |
| P1-b | 116-2 | Fig. 5 caption l.267 | "and the two channel arms are indistinguishable." | "and the placebo-minus-delivered premium difference is unresolved (+0.03 [−0.54, +0.49], rounds 2–12)." | P2.5 / Fig. 5 | `placebo_llm_v3plc.json:windows.r2_12.placebo_minus_private_paired` (sign: placebo − private) | open |

## Partially applied (P2)

| rank | id | SUBMISSION line | current text | replacement | status |
|---|---|---|---|---|---|
| P2-a | 114-2 | Abstract l.22, §5.3 heading l.195 | "gains nothing from public messages / words" | "shows no resolved gain from public messages / words" (body l.215–217 already says this with bounds) | body applied; abstract + heading open |
| P2-b | 114-3 | §7 Limitations l.314 | "Q2.2's placebo cannot separate delivery from offer." | "Q2.2's placebo leaves delivery unresolved (private − placebo +0.38 [−0.41, +1.18])." (§5.4 l.247 already says this) | §5.4 applied; Limitations open |

## Applied (closed)

| id | what | where now |
|---|---|---|
| 115-5 | inversion range limited to resolved arms | Abstract l.24: Qwen "0.15–0.21, CI below 0.5" — matches Table 2 bold rows |
| 116-1 | "text helps only where the deal is the conversation" | Abstract l.25 now descriptive: "Text did work in an external negotiation dataset … (0.87 [0.83, 0.91])" |
| 114-1 | executed-only −0.30 names Q1.4 rule | §5.3 l.228 "executed under Q1.4's rule", rule defined in label table l.109 |
