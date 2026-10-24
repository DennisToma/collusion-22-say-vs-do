# Opus adversarial review — checkpoint, REPORT.md lines 1–348 (iteration 26, 2026-10-24 ~17:55 UTC)

Scope: Abstract, TL;DR, Phase 2 glance table, P2.1–P2.15. Read-only review; no new experiments proposed.

## Spot-checks (19 numbers, all match the JSON to the stated rounding)

| REPORT claim | JSON value | source |
|---|---|---|
| combined Δ test −0.01 [−0.09, +0.06], n = 95 | via claims C01 OK | `claims_denominators.md` |
| pooled Δ −0.07 [−0.17, +0.02], n = 90 | −0.0738 [−0.1704, 0.0153] | `p2_pool_rep.json` condition_label |
| text alone test 0.47 | 0.472 [0.365, 0.581] | `final_llm_v3_gpt-6.1-sol_test.json` point_ci.text.run_auroc |
| round-1-only premium 0.90 test | 0.9007 [0.829, 0.956] | `early_detection_llm_v3.json` results.test.r1-1 |
| premium precision 0.24 [0.15, 0.43] at 5% | 0.237 [0.154, 0.431] | `p2_prevalence.json` llm_v3_test |
| replication precision 0.16 | 0.156 [0.088, 0.441] | `p2_prevalence.json` llm_v3rep |
| 14/50 kept; premium 0.80 [0.67, 0.90] on kept label | 14 followed / 36 not; 0.795 [0.672, 0.900] | `p2_behaviour.json` |
| kept-label hybrid −0.03 [−0.14, +0.06] test | −0.031 [−0.142, 0.062] | `p2_behaviour.json` delta_hybrid_followed.combined |
| kept-label pooled premium 0.76 [0.64, 0.86]; hybrid −0.03 [−0.13, +0.06] | 0.755 [0.638, 0.864]; −0.034 [−0.132, 0.056] | `p2_pool_rep.json` followed_label |
| P2.7 text 0.25 [0.08, 0.46], combined 0.18, plan 0.76 [0.55, 0.93], plan p-v-n 0.70 | 0.249/0.178/0.755/0.696 | `p2_strong_eval_llm_p2strongF.json` |
| E111 partner count 0.82 [0.66, 0.96]; non-partner 0.42; 0/13, 0/19, 0/7 terms | matches | `p2_plan_keyword_llm_p2strongF.json` |
| P2.11 agreement 15/15, executed 13/15, diff 0 [−0.20/−0.26 …]; P3 −1.24 [−2.41, −0.03]; strict 5/15 both | matches | `p2_qwen_cmp.json`, `p2_strong_eval_llm_p2qwen{a,b}.json` |
| P2.11 Qwen text AUROC 0.21 / 0.15, flags none 15/15 | 0.213 / 0.147 | same |
| E102 strict 4/6 [0.29, 0.92] vs 3/6 [0.17, 0.83]; +3.42 / +2.97; excess 5.6/6.3, 3.8/2.9 | matches | `p2_qwen_strong.json` |
| P2.14 3/10 vs 9/10, +0.91 [+0.20, +1.58] vs +1.75; 0.56/0.78/0.75 vs 0.66/0.74/0.70; DE−EN −0.58 [−1.79, +0.51] | matches | `p2_de.json` |
| P2.15 +0.20 [−0.08, +0.62], +0.16 [−0.27, +0.57]; 19/20, 9/10; 16/20 vs 15/20; 15/20 vs 14/20; CUSUM 0/30 by r25 | matches | `p2_replace.json` |
| SALT P(said|exec) 0.385 [0.353, 0.416], 1989/5169 | matches | `salt_d1.json` |
| luna text vs action vs PRIV 0.64 vs 0.79 | 0.640 / 0.791 | `p2_family3way.json` |
| joint-statement Qwen +2.13 [1.28, 3.00]; 5/20 | Q1.4 E65 (sibling REPORT l. 812/832), not a Q2.2 json | sibling |

No numerical mismatches found. The issues are framing, omission and internal consistency.

---

## P1 — fix before the checkpoint

**P1-1. TL;DR 5 (line 36) says something the body explicitly rejects.**
"public text (0.25, inverted: *tacit markets coordinate on the public board*)" states public coordination as fact. P2.7 (ii) (lines 182–184) says the keyword rule "does not establish public agreement or explain the score difference" and that tacit-high "is the operational no-channel price class, not verified absence of public agreement". A judge reading both will see a contradiction.
Replace with:
> "…where prices (≈ 0.5) and public text did not (0.25 [0.08, 0.46], inverted; no-channel markets use more hold/keep-price phrases on the public board, 43% vs 28% of messages, post hoc and not shown to be agreement); a no-LLM partner-name count does as well (0.82 [0.66, 0.96])."

**P1-2. Abstract line 11 cites the action_stats gain on test without saying it did not replicate.**
"+0.11 [+0.04, +0.18]" is the locked-test value. On the fresh data the same contrast is +0.003 [−0.07, +0.07] (P2.8, line 209) and +0.005 [−0.06, +0.07] pooled (`p2_pool_rep.json` delta_hybrid[action_stats]). Quoting only the test gain overclaims the one positive hybrid result.
Replace line 11 with:
> "(A computed pair-statistics table added to the action view gains on test, +0.11 [+0.04, +0.18], but not on fresh data, +0.00 [−0.06, +0.07] pooled n = 90; adding text to it does not gain, −0.06 [−0.14, +0.01] test.)"
(Add a claims row C04c for the pooled value so p2_claims.py checks it.)

**P1-3. The abstract (line 16) and TL;DR 3 (line 30) use SALT only on the side that helps the thesis.**
Both quote the 62% "no explicit agreement" figure, but neither mentions that a text auditor still predicts execution well on SALT (0.87 [0.83, 0.91]; 0.81 on tacit cases). P2.12's own reading (lines 311–315) says this externally *contradicts* "text ≈ chance". An abstract that leaves this out reads as cherry-picking.
Replace the abstract sentence with:
> "On external SALT-NLP data (8000 episodes, 10 models) 62% of executed episodes have no explicit agreement in the chat, yet a text auditor still predicts execution (AUROC 0.87 [0.83, 0.91]; 0.81 on tacit cases) because the act there is negotiated in the chat itself."

Append to TL;DR 3:
> "SALT: P(said | executed) 0.385, but text auditor AUROC 0.87 there (P2.12): text helps when the decisive act happens in the conversation."

**P1-4. The P2.15 reading (lines 346–347) draws a conclusion the design cannot support.**
"not of the incumbent's memory" ignores that only one firm is replaced. In the private arm the other pair firm keeps its plan and the full chat history, and it writes first in 10/20 re-agreements (line 345). So what the data rule out is the replaced firm's memory, not memory in general. The claim also generalises from a single model (luna, n = 20 + 10).
Replace with:
> "**Reading:** in this luna arm (20 + 10 games), the high price and even the agreement survive replacing one firm's memory: a fresh seller that sees only public prices, the board and its own records re-joins the price level, and its partner, who keeps its memory, often re-proposes (newcomer writes first in 10/20). Replacing one participant is therefore no test for collusion here. Second arm (E115, gpt-6.1-sol newcomer) is still running."

---

## P2 — should fix

**P2-1. Lines 4, 45, 48: stale or inconsistent status text.**
- Line 4 is stamped "16:30 UTC" but reports E112 as final, and E112's result was logged at 17:33. It also calls E102 a "pilot", while P2.11 (line 277) calls it "registered descriptive, 6 seeds".
- Line 45 still says "(in progress …)".
- Line 48 says "Phase 2 experiments and checks are E77–E108", but E109–E115 are used in the text.

Replace line 4's sentence with:
> "Checkpoint text, 2026-10-24 18:00 UTC: P2.1–P2.15 final except the second P2.15 arm (E115, gpt-6.1-sol newcomer; generating). E102 (strong-framing Qwen, 6 seeds) is descriptive."

Line 45: "## Phase 2 results (from 2026-10-24 06:30 UTC; v1 below frozen as git tag `v1-overnight`)".

Line 48: "Phase 2 experiments and checks are E77–E115".

**P2-2. Line 13: "an unread pricing notepad gives 65% of the channel premium" is wrong and has no CI.**
The firm reads its own notepad, so "unread" is wrong; the intended meaning is "nobody else reads it". The ratio's CI [0.34, 1.32] includes 1, so "65%" sounds far more precise than it is.
Replace with:
> "(a private pricing notepad that no other firm reads gives 0.65 [0.34, 1.32] of the channel premium; an identical notepad for invented weather gives little, +0.22)"

**P2-3. Line 21: the abliteration sentence leaves out the qualifiers that limit it.**
Agreement is at ceiling (15/15 both), so P1 could not detect an increase. Serving is confounded (bf16 vs FP8), and the premium difference is resolved in the *opposite* direction.
Replace with:
> "Abliterated vs base Qwen3.8-27B (15 + 15 markets; bf16 vs FP8 serving): agreement at ceiling in both (15/15), execution equal (13/15), and a smaller channel premium for abliterated (−1.24 [−2.41, −0.03]), so there is no detectable increase (also none in two Q1.4 Qwen pairs)."

**P2-4. Glance P2.11 (line 64): the CI is attached to the wrong count.**
"strict 5/15 both (diff 0 [−0.26, +0.26])" is misleading: the Newcombe CI is for *executed* 13/15 (`p2_qwen_cmp.json` P2_executed_rate), not for strict.
Replace with:
> "agreement 15/15 both (ceiling); executed 13/15 both (diff 0 [−0.26, +0.26]); strict 5/15 both"

**P2-5. Glance P2.6 (line 59): two counts are attributed to the wrong thing.**
"Claude/deepseek public too (719/720 invitations)" has two problems. 719/720 is deepseek-only (no-channel public messages). And these are regex *matches*, not judged invitations; regex precision is 17/20 for Claude and 20/20 for deepseek.
Replace with:
> "luna private only; Claude (5 seeds) / deepseek public too (deepseek 719/720 no-channel public messages match the invitation regex, precision 20/20); sol 0/7 agreements, Nash + 4"

**P2-6. Lines 19–20 (abstract): "does as well" and "channel footprint, not stated collusion" are stated too strongly.**
There is no paired test of 0.82 vs 0.76. The non-partner control was added after the partner count was seen (line 190). Everything rests on 13 vs 19 markets in one arm.
Replace with:
> "…a no-LLM count of plans naming the chat partner does comparably (0.82 [0.66, 0.96]; no paired test), and no plan uses agreement words; this is consistent with the plans carrying a channel footprint rather than stated collusion. Public text ranks the classes in reverse (0.25 [0.08, 0.46])."

Also add "[0.55, 0.93]" after "AUROC 0.76" on line 19, since every other abstract AUROC carries a CI.

**P2-7. Lines 41–43 (joint statement): the Qwen numbers come from the sibling, and "predicts" is too strong.**
"+2.13 [1.28, 3.00]; 5/20" is Q1.4 E65 (their market, T = 40). A reader will confuse it with this report's P2.11 Qwen numbers (+0.86, 13/15). "As the first sentence predicts" overstates what a non-falsifiable dependence statement can do. The quote is verbatim, so leave it unchanged and add a bracketed note after it:
> "(The Qwen numbers in the quote are Q1.4's E65 arm, their market, T = 40; this report's own Qwen comparison is P2.11. 'Predicts' means 'is consistent with': the first sentence allows any model-dependent result.)"

**P2-8. TL;DR 6 (line 38): "we recommend no screening architecture" is ambiguous.**
It can be read as "we recommend not screening".
Replace with:
> "Screens need model- and prompt-matched references; our evidence does not support recommending any particular screening architecture."

---

## P3 — nits

**P3-1. Line 30: "gpt-6.1-sol never proposes coordination" rests on 7 private markets.**
Replace with: "gpt-6.1-sol proposed coordination in 0/7 private markets".

**P3-2. Line 28 and glance line 54: two numbers lack CIs.**
- Round-1-only premium: write "0.90 [0.83, 0.96] test AUROC".
- Replication precision: write "0.16 [0.09, 0.44] replication".

**P3-3. Line 47: the blanket registration claim is too strong.**
"Generators are registered … analyses and audits before their outputs" does not cover E104 (registered after the crosstab was seen) or E99-x (registered after generation began), even though both are flagged in the body. Append:
> "; exceptions are marked where they occur (e.g. E104, E99-x)."

**P3-4. Glance P2.14 (line 67): the paired contrast is missing.**
Append ", paired German − English −0.58 [−1.79, +0.51]" so the reader sees that the halving is unresolved. Glance P2.15 (line 68): write "re-agreement 16/20 (originals 15/20)".

**P3-5. Lines 17 and 33: "with memory and a profit objective" undersells the strong framing.**
The arm combines five levers: profit priority, unknown end, full history, persistent plan, and T = 40. Write "with memory, a profit objective and other strong-framing levers (combined, not ablated)" at the first use in the abstract.
