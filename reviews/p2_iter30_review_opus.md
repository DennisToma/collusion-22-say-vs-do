# Adversarial review, iter30 (Opus): Abstract, TL;DR, glance table, P2.7, P2.14, P2.15
Reviewer: Opus subagent, read-only. `uv run python p2_claims.py` → 27 claims: 27 OK, 0 MISMATCH. Every abstract number matches
its JSON key (`claims_denominators.md` C01–C25). The problems are about framing and internal consistency, not arithmetic.

## P1 (wrong or overclaimed; must fix)
**P1-1. E112 conclusion goes beyond the design (abstract l.17–19; mirrored at P2.15 l.351–353).**
Quote: "under strong framing the high price is a property of the market prompt, not of the incumbent pair."
Evidence: only one of four firms is replaced. Its pair partner and both rivals keep their memory and plans. The newcomer sees the full
public price history from rounds 1–20 (high prices) and the board (P2.15 l.348). The partner "often re-proposes" (l.353), and the
newcomer writes first in only 10/20. The ledger's own E112 hypothesis says "market prompt/**state**" (EXPERIMENTS.tsv E112-registered
and E112-result). The design cannot separate prompt from inherited price history or the three incumbents. The incumbent pair is
also only half replaced.
Replacement: "Swapping one seller for a fresh luna at round 21 leaves the market level (+0.20 [−0.08, +0.62]) and re-agreement
(16/20 vs 15/20) without resolved change: with three incumbents and the price history intact, the level does not depend on one
firm's memory." Also drop "property of the market prompt" from P2.15's Reading.

**P1-2. TL;DR 5 contradicts the E116 table (l.37–38).** Quote: "Within channel pairs (13 vs 7, E116) no view resolves execution".
Evidence: `p2_within_agree_llm_p2strongF.json` gives market_excess_nash 0.78 [0.536, 0.958] and action_stats 0.181 [0.0, 0.418].
Both CIs exclude 0.5. P2.7 l.184 states the claim correctly ("No text **or plan** view resolves").
Replacement: "Within channel pairs (13 vs 7, E116, exploratory) no text or plan view resolves execution (plan 0.69 [0.44, 0.91]);
market excess separates partly by construction (0.78 [0.54, 0.96]) and action_stats inverts (0.18 [0.00, 0.42])."

**P1-3. "Luna talks only in private" is contradicted by P2.7 (abstract l.12–13; TL;DR 3 l.29; glance P2.6 l.63).**
Evidence: P2.7 l.195–198 says that under strong framing luna's public board has hold-price calls in 1362/3200 no-channel
messages (43%), and that inverts the public-text view (0.25). The "private only" finding comes from base framing (P2.6; Q1.4 E70
0/960). The abstract uses both framings without saying which claim belongs to which.
Replacement (abstract): "luna proposes coordination only in private at base framing". Add to TL;DR 3: "(under strong framing,
43% of luna's no-channel public messages are hold-price calls; P2.7, post hoc)".

## P2 (misleading framing, missing CI or denominator, unlabeled exploration)
**P2-1. The E116 sentence (abstract l.16–17) is technically correct but reads as a finding. This is question (b).**
"neither private plans (0.69 [0.44, 0.91]) nor public text resolvably predicts execution": the plan CI includes 0.5, so "not
resolvably" is correct. Problems: (i) n = 7 negatives, so the CI is compatible with a strong detector (upper bound 0.91). This is
absence of evidence, and the text should say "low power". (ii) "public text" has no number. It is 0.61 [0.37, 0.85]; add it or
drop it. (iii) The say-vs-do framing at P2.7 l.186 ("what pairs plan does not resolvably predict what they do") implies that doing
is legible. The action views do no better (premium 0.35, action 0.33, action_stats inverted), so say that. (iv) E116 was
registered at 17:58 after per-class flag counts were visible: E116-reg says "Expected from flags: weak or reversed". P2.7 l.183
says "registered before computing". Change it to "registered before computing AUROCs; per-class flag counts had been seen".
(v) 2 of the 7 "non-executed" have no judged agreement (`n_nonexec_agreed` 5). "Within channel pairs" is right. "Within-agreement"
(the ledger's term) is not.

**P2-2. CUSUM 0/30 needs its threshold (abstract l.18; P2.15 l.351).** The threshold `level_cusum_h_from_originals` = 38.5 is the
max over the original continuations, so the originals alarm 0 by construction (ledger E112-result). Over the full game, replaced
games alarm 1/20 + 2/10 (`O7a_level_cusum_any_alarm_repl`). Add: "(threshold = max over original continuations; any-round alarms
3/30)". Or cut CUSUM from the abstract, as in the rewrite below.

**P2-3. Abliterated Qwen, "no detectable increase in agreement" (l.19).** Agreement is 15/15 in both arms (a ceiling), so the
agreement test is uninformative. The premium difference −1.24 carries a bf16-vs-FP8 serving confound that is disclosed in the
glance (l.68) but not in the abstract. Replacement: "executes no more than its base model (13/15 both; agreement at ceiling) with a
smaller channel premium (−1.24 [−2.41, −0.03]; serving precision differs)".

**P2-4. The 65% ratio has no CI or n (l.11).** The ratio comes from +1.04 [+0.65, +1.42] / +1.61 with n = 15 seeds per arm (C06),
and it is derived. Either add "(+1.04 [+0.65, +1.42] vs +1.61)" or keep the glance pointer. It is acceptable only because P2.5
gives the CI.

**P2-5. TL;DR 1, "fresh 0.45" (l.25), sits next to "pooled fresh n = 90" but is llm_p2rep only (n = 60, 0.451).** The pooled n = 90
text AUROC is 0.52 [0.41, 0.63] (`p2_pool_rep.json` condition_label.run_auroc.text). Write "(test 0.47; p2rep 0.45, n = 60)".

**P2-6. The premium AUROC 0.94 includes legitimate runs among the negatives (group_n private 30 / none 20 / legit 10).** "n = 60
fresh" is right. TL;DR 2 gives the split. Fine as is, provided the split stays in TL;DR 2.

## P3 (wording and housekeeping)
- l.4: the header says E113 is "awaiting Q1.4 sweeps", but commit 96d9f85 audited 48 snapshot games. Update it.
- l.52: "Phase 2 experiments and checks are E77–E115". E116 exists, so change it to E77–E116.
- l.172: column header "both with channel". Add "(5/7 non-executed agreed)" so readers do not read it as within-agreement.
- P2.14 l.343: "language changed what sellers say more clearly than what they do" is supported (Jeffreys CIs 0.09–0.61 vs
  0.62–0.99 do not overlap, while the premium difference is unresolved). Add "(n = 10 seeds)" once in that sentence. Judge validity
  on German rests on a 7-chat spot check; say who did the spot check.
- Joint statement l.45–46 (Q1.4: abliterated channel +2.13) sits next to abstract l.20 (P2.11: smaller premium, −1.24). They come
  from different markets and T. The disclaimer exists, but add to the abstract or P2.11 "(Q1.4's T = 40 arm differs; P2.11)".
- P2.15 l.350: "re-agrees with its partner" should be "a new agreement is judged (newcomer first in 10/20)". The original agreement
  is not literally "intact" (abstract l.18).

## Internal-consistency check (question d)
Abstract, TL;DR, glance and section numbers agree everywhere I checked (13/20, 19/20, −0.44 [−1.84, +1.00], 0.76, 0.82, 0.69,
16/20, 0/30, +0.91, 3/10). There are three inconsistencies: P1-2 ("no view" vs table), P1-3 (luna private-only vs 43% public
hold-price calls) and P2-1(iv) (registration timing wording).

## Proposed abstract (261 whitespace tokens incl. CI fragments; every number is verbatim from the current REPORT text)
Adding LLM sellers' public messages to their prices gives **no resolved gain** for detecting collusion: combined minus the better
single view is −0.01 [−0.09, +0.06] run-AUROC on the locked test (n = 95) and −0.07 [−0.17, +0.02] on two fresh replications pooled
post hoc (n = 90), excluding gains above +0.06 and +0.02. Setup: a 4-firm pricing market of gpt-6-luna sellers (one pair may chat
privately); zero-shot gpt-6.1-sol auditors read public text, actions, or both. (1) Actions are partly a prompt effect: the
post-hoc-selected pair price premium (AUROC 0.94 [0.87, 0.99], n = 60 fresh) responds to an unread pricing notepad (65% of the channel
premium), wording and legitimate cost/quality edges. (2) Families differ in where they talk: luna (base framing) proposes only in
private; Claude, deepseek and Qwen also invite rivals publicly, so text auditors flag every control market (50/50). When the deal is
struck in chat (SALT-NLP), text predicts execution (AUROC 0.87 [0.83, 0.91]). (3) Labels disagree: only 14/50 test "colluders" keep
their agreement. Under memory + profit framing (levers combined), 13/20 channel pairs strictly execute, yet 19/20 no-channel markets
also price ≥ Nash + 2. Exploratory: within channel pairs (13 executed vs 7 not), no text or plan view resolves execution (private
plans 0.69 [0.44, 0.91]; low power). Swapping one seller for a fresh luna at round 21 leaves the market level (+0.20 [−0.08, +0.62])
and re-agreement (16/20 vs 15/20) without resolved change. Abliterated Qwen3.8-27B executes no more than its base model (13/15 both;
agreement at ceiling) with a smaller channel premium (−1.24 [−2.41, −0.03]; serving precision differs).
Every abstract number with its denominator and source key: `results/analysis/claims_denominators.md` (`p2_claims.py`).

Notes on the rewrite: the CUSUM (0/30) and the 19/20 post-replacement level are dropped for length. The paired difference carries
the claim. If they are kept, add the threshold caveat (P2-2). Cost/quality flags 7/10, 9/10 stay in TL;DR 6.
