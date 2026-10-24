# P2 iter13 — Opus adversarial review of Abstract / TL;DR / glance / P2.11 / P2.12 (2026-10-24 ~14:05 UTC)

Reviewer: Opus subagent, read-only. Every checked number matched its json; issues were framing/overclaims. All 14 items applied
(script /var/tmp/fix13.py, not kept; diff in git):

1. SALT 62% is per episode (1 − 0.385), not per run (run-level onset 0.762); "because the act happens in the chat" was untested
   causation and verdict words leak (no-verdict AUROC 0.75 [0.66, 0.84]) → reworded, "plausibly", 0.75 added.
2. "No resolved gain" holds for the primary `combined` view; `structured` gains on test run-AUROC +0.083 [+0.001, +0.169]
   (from the statistics table: combined_stats − action_stats −0.06 [−0.14, +0.01]) → scoped in abstract + TL;DR 1.
   (Note: combined_stats − action_stats within-market is +0.036 [+0.008, +0.072] on test; v1 table already shows it.)
3. Premium 0.94/0.95 lacked "post-hoc selected" and the legitimate-asymmetry confound → added (abstract, TL;DR 2, glance P2.8).
4. Abliteration: agreement at ceiling; strict execution 5/15 both; premium diff opposite sign; bf16 vs FP8 → glance P2.11 + text.
5. TL;DR 3 heading "text helps only where the family speaks" contradicted below-chance text AUROCs → rewritten.
6. TL;DR 5 "model matters more than the channel" → descriptive, across-family wording.
7. TL;DR 4 mixed test/pooled → both given.
8. Abstract 255 words, answer in sentence 3 → 242 words, answer in sentence 1.
9. SALT luna/terra are gpt-5.6, same-model main condition (kept in P2.12 body; TL;DR now omits the luna/terra clause).
10. "60 fresh seeds" → runs with composition; round-1 premium reproduces (0.90), not "moves", the AUROC.
11. Terse paraphrase given with same-seed comparator +1.75.
12. P2.11 tacit-high defined for T = 12 (rounds 2–12); text flags 15/15 in both arms; causal "so" removed.
13. SALT P2 "held" → point estimate only, no paired CI.
14. Phase 2 experiment range E77–E105.
