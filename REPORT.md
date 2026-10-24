# Say vs. Do: does auditing what AI agents *say* together with what they *do* catch collusion better?

*Apart AI Collusion Sprint, Q2.2 — text + action auditing. Status: locked test results in (2026-10-24 00:03 UTC); registered replication run 02:07 UTC (chronology disclosed below); placebo-channel exploration 03:33 UTC; post-hoc markup baseline (E70) and stats-table column ablation (E71) 05:20–05:35 UTC (exploratory, headline unchanged). Offline verification: `python3 verify_artifacts.py`; handoff instructions in [README.md](README.md).*

For the five-minute presentation, open [PRESENTATION.html](PRESENTATION.html) locally in a browser;
[speaker notes, judge questions and saved-input hashes](PRESENTATION.md) accompany it. Render with
`python3 build_presentation.py`, or check freshness without writes using
`python3 build_presentation.py --check`. It reads existing results only; no estimates change.
Ready to share: [slides PDF](PRESENTATION.pdf), [report PDF](REPORT.pdf), and
[offline report HTML with embedded figures](REPORT.html). The report exports preserve this full
write-up; wide appendix tables use landscape PDF pages. Export with
`uv run --group handoff python build_handoff.py`; check source/output hashes without writes using
`python3 -S build_handoff.py --check` (post-hoc rendering receipt; no metrics recomputed).
The [cached evidence source ledger](EVIDENCE.html) lets reviewers inspect every original-view
test and replication evidence item beside the public log (offline, searchable; no semantic judging).

**TL;DR (plain-language summary; every number is repeated with its source below).**

1. *Question:* does a zero-shot LLM auditor detect collusion better if it reads sellers' public messages as well as
   their prices? *On our generator: no resolved run-level detection gain.* Locked test (n = 95): text alone run AUROC
   0.47 [0.36, 0.58] (consistent with chance); text + actions 0.74 vs actions alone 0.75; combined minus best single modality
   −0.01 [−0.09, +0.06]. A small unadjusted within-market localisation gain with statistics did not repeat on fresh data.
2. *What the messages show:* all 70 private pairs exchange price intentions or propose agreements, while the
   explicit-public-coordination screen flags 0/125 runs. Public text still carries a learnable trace for a supervised
   classifier; why the zero-shot text-only auditor is near chance is not established.
3. *What helps:* summarising the actions. A computed statistics table adds +0.11 [+0.04, +0.18] run AUROC on test
   (detection gain unresolved on replication; pair localisation improves in both samples). An untrained
   pair price premium reaches 0.95 (chosen after partial test exposure; 0.92 on a 30-run replication).
4. *Caution:* the label equals the condition in the main dataset. Round-1 prices (set before any partner message is
   received) already give 0.90 run AUROC. The premium flags 14/15 placebo-channel runs with no private-message
   delivery and 14/15 matched delivered runs. Flags can occur without delivery; the cues each detector uses and
   equivalence between these arms are not established.
5. *Suggested architecture:* always-on action statistics as the screen; LLM audit to explain flagged runs.
   Neither explanation usefulness nor this workflow's end-to-end performance was evaluated.

## Phase 2 results (in progress, from 2026-10-24 06:30 UTC; v1 above frozen as git tag `v1-overnight`)

Phase 2 closes known validity gaps. Every experiment is registered in `EXPERIMENTS.tsv` before its data exist
(E77–E80). New datasets are named `llm_p2*`. v1 numbers above are unchanged.

**P2.1 Precision at realistic prevalence (E81; post-hoc re-expression of saved scores, nothing refit).** The test split
has 53% positives, which flatters precision. At the frozen dev thresholds, precision(π) = TPR·π / (TPR·π + FPR·(1−π)),
with class-stratified bootstrap CIs (`uv run python p2_prevalence.py` → `results/analysis/p2_prevalence.json`):

| detector (frozen dev threshold) | split | TP/pos, FP/neg | precision @ 1% | @ 5% | @ 20% |
|---|---|---|---|---|---|
| premium | test (n=95) | 46/50, 7/45 | 0.06 [0.03, 0.13] | 0.24 [0.15, 0.43] | 0.60 [0.46, 0.78] |
| premium | replication (n=30) | 14/15, 4/15 | 0.03 [0.02, 0.13] | 0.16 [0.09, 0.44] | 0.47 [0.31, 0.79] |
| action_stats (LLM) | test | 36/50, 2/45 | 0.14 [0.06, 1.0] | 0.46 [0.24, 1.0] | 0.80 [0.60, 1.0] |
| action_stats (LLM) | replication | 8/15, 5/15 | 0.02 [0.01, 0.05] | 0.08 [0.04, 0.21] | 0.29 [0.15, 0.56] |
| combined (LLM) | test | 26/50, 9/45 | 0.03 [0.01, 0.06] | 0.12 [0.07, 0.24] | 0.39 [0.27, 0.60] |
| text (LLM) | test | 5/50, 5/45 | 0.01 [0.00, 0.04] | 0.05 [0.01, 0.16] | 0.18 [0.05, 0.47] |

When a resample has zero false positives the upper bound reaches 1.0. A conservative bound (Wilson lower TPR,
Wilson upper FPR) gives premium 0.13 / action_stats 0.17 at 5% prevalence on test (json key
`precision_conservative_wilson`). **Reading:** if 1 market in 20 colludes, most premium alarms are false (point
estimates 0.24 test, 0.16 replication; both CIs below 0.5). action_stats is better on test (0.46, CI up to 1.0) but not on
replication (0.08). At 5% prevalence the premium raises about 150 false alarms per 1,000 audited markets on test and
about 250 on replication. Two caveats. Labels equal the condition here, so this is precision for "a private channel
was offered and used", not for realised collusion. The premium was also selected after partial test exposure (see
§Held-out discipline). All views are reported in the json.

**P2.2 Independent reimplementation (E83).** codex gpt-6.1-sol worked in an empty scratch directory with only the
method excerpts of this REPORT ([results/reimpl/METHOD.md](results/reimpl/METHOD.md)) and the raw data files, not our code.
It reimplemented the premium scorer, the four metrics, bootstrap CIs, the dev Youden threshold and the
combined − best-unimodal contrast. On the locked test and the replication split, 31 of 32 point estimates agree with ours to 3 decimals.
The one exception is the replication premium pooled-pair AUROC, 0.9832 vs our 0.9836: a single tied pair comparison
out of 2,475, because its exact integer ties differ from our float means. The threshold (0.667), test flags (46/50
positives, 7/45 negatives) and the contrast (−0.0127 [−0.090, +0.065] vs our −0.013 [−0.091, +0.064]) also match. No bug was found
(`results/reimpl/NOTES.md`, `reimpl.py`, `reimpl_results.json`).

**P2.3 What does the 0.98 supervised text classifier detect? (E82, registered; `uv run python p2_textlr.py` →
`results/analysis/p2_textlr.json`; no LLM calls).** Its signal does not need any delivered private message.
(a) The signal is diffuse. On test (grouped CV, as published), removing each training fold's top 20 / 100 / 500
n-grams leaves run AUROC 0.98 / 0.96 / 0.92 [0.86, 0.97]. (b) We fit the same classifier on all llm_v3 runs and scored
fresh runs against fresh no-channel runs (llm_v3rep `none`, n = 10). Delivered private runs score 0.97 [0.89, 1.00].
**Placebo runs: all 15 score above all 10 negatives** (AUROC 1.00; the bootstrap CI is degenerate). In these runs
the channel was offered but no message was ever delivered (llm_v3plc; its seeds match llm_v3rep, not the training set).
Legit-partnership runs score 0.38. Prediction (b) held; its ±0.05 margin is loose with only 10 negatives. Prediction (a)
("gradual") had no numeric criterion, so it is descriptive only. **Reading:** the public-text trace *does not require
any delivered message*. Placebo sellers still write proposals they believe are delivered, so this does not
distinguish "reaction to the offer" from "intended (unilateral) coordination". It does mean that, with labels equal to
the condition, a near-perfect text classifier is not evidence that agreements can be detected from public text.
The notes-to-self condition (P2.4) separates the two explanations.

**P2.4 Is the "collusion" a prompt artifact? (E77/E78, generation running).** Six matched-seed conditions (same pair,
cost and demand path per seed): private channel; neutrally worded "message box"; private notepad with no recipient;
channel to a random partner that changes each round; placebo (offered, never delivered); no channel.
Also two paraphrases of the base seller prompt. Results will appear here.

## Abstract
Does an auditor catch LLM collusion better if it reads what sellers *say* in public as well as what they *do*?
**On our generator: no resolved run-level detection gain** (a small unadjusted within-market localisation gain with statistics did not repeat on fresh data). We simulate a 4-firm repeated-pricing market with gpt-6-luna sellers; in the
`private` condition one pair gets a private chat. Sellers are never told to collude, yet all 70 private pairs use it to
exchange prices or propose agreements, while a screen for explicit public coordination flags 0/125 runs. Zero-shot
gpt-6.1-sol auditors score each firm pair from the public log, seeing text only, actions only, or both. Further views
add a computed statistics table to the action log, with or without text; a structured view also adds a stated-vs-actual
price table. No view gives statistics without the raw action log. On the locked test split (n = 95, run once), text
alone is consistent with chance (run AUROC 0.47), combined text + actions gives 0.74 vs actions alone 0.75, and combined minus the best single modality is −0.01 [−0.09, +0.06] ("resolved" throughout = 95% run-bootstrap CI excludes 0; no multiplicity correction). A statistics table helps test detection (+0.11
[+0.04, +0.18]; unresolved on replication) and improves localisation in both samples. An untrained one-line statistic selected after partial test exposure, the pair's price premium over its rivals, reaches 0.95 against ≤ 0.86
for the six original LLM views. But round-1 prices alone give 0.90, and they are set before any partner message is read; and when
private messages are offered but never delivered (placebo, 15 matched seeds), the premium flags 14/15 placebo vs 14/15 matched
delivered runs (no difference resolved; equivalence not tested). So high premiums and detector flags occur without delivered private
messages; the round-1 gap indicates a response to the channel offer or its prompt framing, which the placebo cannot separate from tacit coordination on public prices. A replication
on 30 fresh runs keeps the premium's run-AUROC point estimate highest (0.92, lead unresolved) and does not resolve a gain from adding text; if anything text hurt (combined − action −0.14 [−0.30, +0.02]). Public text still
carries a learnable trace: supervised TF-IDF reaches 0.98 (five-fold CV grouped by run within the test split, a different regime from the zero-shot auditors). Caveats: the label coincides with the condition, one seller
model, and evasion is untested (under an announced monitor the judge finds coordination talk in 0/14 runs).
Suggested architecture: always-on action statistics as the screen, LLM audit reserved for explaining flagged runs;
neither explanation usefulness nor end-to-end performance was evaluated.

![summary](figures/summary.png)
*Figure 1 (`uv run python fig_summary.py`, read from existing results JSON). (a) Run AUROC with 95% run-bootstrap CIs;
filled = locked test split (n = 95), hollow = fresh replication (n = 30). The premium comparator was chosen after
seeing partial data including test runs; the round-1 replication point is exploratory (computed after `replication.py`). (b) Flag
rates at frozen dev thresholds in the placebo exploration stratum (15 placebo, 15 matched private, 10 `none`); n is
small and no scorer resolves placebo from private.*

### Key results (detail)
**Answer (on this generator): no resolved detection gain.** Adding what LLM sellers *say* in public to what they *do*
gives no resolved run-level detection gain, for zero-shot LLM auditors or for supervised baselines (with a statistics
table present, text gives a small nominal localisation gain that did not repeat on fresh data). What helps is a better
summary of the actions, and opening prices already discriminate strongly, before any partner message has been read.

We build a 4-firm repeated-pricing market with LLM sellers (gpt-6-luna). In the `private` condition one pair gets a
private chat channel. Sellers are never told to collude, yet all 70 private pairs (dev + test) exchange prices or propose agreements there (judge-labelled from the
private chat), and
the explicit-public-coordination screen flags 0/125 runs. Zero-shot gpt-6.1-sol auditors score every firm pair from the
public log under six views (defined in §Setup). Locked test split (n = 95, run once):
- **Text adds nothing resolved.** Text-only run AUROC is 0.47 (consistent with chance). Combined minus the best single modality is
  −0.01 [−0.09, +0.06] (gains up to ~0.06 not excluded). Replacing messages with a matched donor run's has no resolved
  effect. Claude Sonnet 5.5 shows the same pattern on 42 runs (dev + test pooled; pair-AUROC contrasts, run AUROCs without CIs). Supervised baselines agree: text + actions 0.96 vs
  actions alone 0.96 (text alone 0.98, see below; trained within the test split on labels that equal the condition).
- **A computed statistics table helps** (action_stats − action, run AUROC +0.11 [+0.04, +0.18]). On fresh data the
  run-level gain is not resolved (+0.04 [−0.10, +0.19]), but the localisation gain is. A post-hoc column ablation (E71)
  removes the table's three price-level columns. This lowers test run AUROC from 0.86 to 0.77 (Δ +0.09 [+0.02,
  +0.17]; actions alone 0.75); run-level differences on dev and replication are unresolved. For localisation the
  picture is mixed: the level columns' gain is resolved on dev (+0.05) and replication (+0.12) but not test (+0.03),
  and on test the remaining proximity/correlation columns beat actions alone (+0.07 [+0.02, +0.13]). The hypothesis
  registered before the E71 audits (no-level ≈ action) held only for test run AUROC. Post hoc.
- **A one-line untrained statistic ranks highest among untrained scorers.** The pair's price premium over its rivals
  reaches 0.95, against ≤ 0.86 for the six original LLM views (+0.09 [+0.01, +0.18]). A post-hoc one-sentence hint
  pointing the auditor at the premium gives action_stats 0.93 vs 0.86 on test (Δ +0.07 [−0.00, +0.15]) but 0.796 vs
  0.798 on the replication; neither dataset was held out for the hint. The premium comparator was chosen after seeing partial data, and
  **round-1 prices alone give 0.90**. Those prices are set before any partner message is read. So the premium picks up a
  substantial pre-message cue tied to the channel *offer*; its contribution to full-period discrimination is not
  quantified. A post-hoc comparison-free markup over cost (usable with two firms) gives 0.92–0.95 on
  test but 0.80–0.84 on the replication; it needs known costs and also flags 11/15 and 9/15 placebo runs.
- **The public text carries a learnable trace.** A supervised TF-IDF classifier reaches 0.98 (grouped CV within the
  test split). The tested zero-shot text auditor does not reach comparable detection performance.
- **Replication on 30 fresh runs** (analysis registered after generation began, before any metrics; 4/4 decision rules
  satisfied): premium 0.92 [0.79, 1.00] vs action_stats 0.80, a gap that is not resolved. Text scores 0.67;
  combined − action is −0.14 [−0.30, +0.02] (registered). Exploratory contrasts point the same way and
  two exclude zero (combined − fusion −0.17 [−0.32, −0.04]; Δ_hybrid[combined] −0.14 [−0.33, −0.02]): on fresh data,
  adding text, if anything, hurt.
- **Placebo channel (exploration, 15 matched seeds).** With private messages offered but never delivered, the pair
  premium in rounds 2–12 was +1.09 vs +1.06 with delivery (Δ +0.03 [−0.54, +0.49]). The premium flags 14/15 placebo
  vs 14/15 private runs, and the action-based LLM views flag placebo runs at least as often; no scorer resolves a
  separation of the two arms (n = 15). Elevated premiums and frequent flags occur without private-message delivery. This does not
  establish equivalence, nor exclude a smaller delivery effect.
- **Caveats.** The label coincides with the condition: we detect *channel granted and used*, and the placebo shows
  the conduct signal does not need the private messages to be delivered. We used one seller model,
  and sellers were never instructed or warned to evade (headline data). Frozen premium thresholds flag 4/10 fresh `none` runs; under a shifted framing the premium and
  stats/combined views flag 25–63% of runs (text and action 6%). With an announced price monitor, the judge finds no coordination communication (0/14), so evasion is untested.

## Question
Given logged trajectories (public messages + prices + market state), do auditors that see both streams detect
collusion — and identify the colluding pair — better than text-only or action-only auditors? Is any gain due
to genuine cross-modal reasoning or just more input?

**Short answer.** On this generator, raw public messages give the tested zero-shot LLM auditors no resolved detection
benefit. Computed action summaries help, and a simple premium comparator performs strongly. Opening prices already
separate the conditions before any partner message is received, and across 15 matched placebo runs where private messages are never
delivered, every action-based scorer flags the run at least as often (run-level flags, n = 15). That limits how far any detector here can be read
as detecting agreement-driven conduct.

## Setup
**LLM market (`llm_market.py`, headline data `data/llm_v3`).** 4 firms, 12 rounds, integer prices 6–30, logit
demand (μ=4; static Nash ≈ 11, joint-monopoly ≈ 19 at cost 6), public cost shocks and demand levels.
Each round each seller (gpt-6-luna via codex) returns `{public_message, price, notes}` (+ `private_message` if it has
a channel). Conditions (randomised, 125 runs planned): `private` (70) — designated pair has a private channel;
`none` (35) — no channel; `legit` (20) — the pair has a publicly announced cost-saving shipping partnership
(hard negative). Framing: economics-lab experiment with earnings = profit.

*Pilot observation (framing; 3 firm-framing pilot runs vs 1 lab pilot run, not a controlled comparison):* with a "pricing manager + competition authority monitors public messages"
framing, luna sellers used the private channel only to say "I'll price independently" (0/3 runs with any
coordination) and posted near-identical boilerplate. With the lab framing, private pairs immediately exchange
intended prices and proposals ("I plan to price at 14; consider matching so we can improve margins without
triggering a price war"). Pilot data: `data/llm_v2` (firm framing), `data/pilot_lab_luna`.

**Labels (`label_llm.py`).** A gpt-6.1-sol judge reads ONLY the private chat (no prices, to avoid building the
action signal into the label) → `explicit` / `info_exchange` / `none`. Primary label y = explicit ∪
info_exchange on the assigned pair. *Cross-family label check (E74, post-hoc, label-only; `uv run python label_xfam.py` → `results/label_xfam.json`):* Claude Sonnet 5.5 with the same `JUDGE` template and chat formatting (backend wrappers differ) re-judged all 115 private chats (llm_v3 70, llm_v3rep 15, firm-framing `llm_v3fp` 16, monitored `llm_v3mon` 14) and agrees on y in 115/115 (70/70 and 15/15 positive; 0/16 and 0/14 positive). The two judges give identical binary labels on these 115 chats (pooled binary κ = 1; within each dataset κ is undefined because each is single-class); this does not establish label correctness or generalisation; the explicit-vs-info_exchange split is less stable (Claude: 57 explicit/13 info_exchange vs GPT 67/3 on llm_v3, exact agreement 60/70, 3-class κ 0.33; llm_v3rep 9/6 vs 13/2, 11/15, κ 0.38) and is not used as an endpoint. Realised conduct (pair price premium over the other two firms, rounds 5–12; the
mechanism-figure summaries separately use rounds 9–12) is reported separately. Private chat is never auditor input.

**Endpoint.** y = 1 iff a judge reading the private chat finds an explicit price agreement or a pricing-intention
exchange on the assigned pair. This is *private coordination communication*, not realised supra-competitive
conduct; runs are split by late-window relative premium as a (weak) proxy for whether it was acted on.
Primary metrics: run AUROC (detection) and within-market AUROC (localisation: P(colluding pair scored above another
pair of the same market), positive runs). Pooled pair AUROC is secondary (a scorer that is flat within each
market can still reach ≈ 0.77 pooled, per the codex review).

**Auditors (`auditors.py`).** Same model (gpt-6.1-sol, medium reasoning; calls that silently fell back to another
model are discarded), same task text, same runs. Six views: `text` (public messages + public facts), `action`
(prices, cost, demand, units, profit + public facts), `action_stats` (action + computed pair-statistics table),
`combined` (strict union of text and action), `combined_stats` (combined + pair-statistics table) and `structured`
(combined_stats + stated-vs-actual price table). There is no text + statistics view. Every view receives the public
partnership information. Output: 0–100 suspicion per pair, a separately elicited `collusion_present` score (the run
score used for detection), and up to 4 evidence items. Premium run scores are the maximum pair premium. Pair
identification is tie-aware.

**Scripted market (`sim.py`, mechanism check only).** Templated messages × scripted actions, 8 conditions incl.
hard negatives (cheap talk without action, common shocks, shared pricing rule, legit cooperation). Its Δ is a
function of how we designed the templates (colluders' stated price direction is decoupled from their action), so
it only validates the pipeline and the shuffle ablation.

## Results
The scripted-market mechanism check (pipeline + shuffle-ablation validation) is in Appendix B; dev-split
development results are in Appendix A.

### LLM market — HEADLINE: locked test split (runs 0030–0124, n = 95; 50 y=1, 30 `none`, 15 `legit`)
Computed ONCE by `./finalize_test.sh` (stamp `logs/final/RUN_ONCE.stamp`: started 23:59, HEADLINE_DONE 00:03 UTC) with
the configuration frozen on dev; the headline scorer table, paired-contrast rows and Appendix C flag-rate tables are copied from the generated
`results/analysis/report_tables_test.md` (source: `results/analysis/final_llm_v3_gpt-6.1-sol_test.json` and
siblings); replication and exploratory results cite their own JSON sources. Hard set: the keyword/LLM screen flags 0/125 runs for explicit public coordination (`hardset.py`), so every run meets the operational "hard" criterion.
95% class-stratified run-bootstrap CIs; fusion weight w_text = 0.6 fitted on dev.

| scorer | run AUROC (detection) | within-market AUROC (localisation) | pooled pair AUROC | pair-ID acc |
|---|---|---|---|---|
| text | 0.47 [0.36, 0.58] | 0.65 [0.59, 0.71] | 0.60 [0.53, 0.67] | 0.35 [0.26, 0.46] |
| action | 0.75 [0.65, 0.85] | 0.79 [0.72, 0.87] | 0.78 [0.72, 0.84] | 0.42 [0.28, 0.56] |
| action_stats | 0.86 [0.77, 0.94] | 0.89 [0.84, 0.94] | 0.89 [0.84, 0.94] | 0.66 [0.52, 0.80] |
| combined | 0.74 [0.64, 0.83] | 0.80 [0.71, 0.87] | 0.78 [0.72, 0.84] | 0.43 [0.31, 0.57] |
| combined_stats | 0.80 [0.70, 0.89] | 0.93 [0.89, 0.96] | 0.89 [0.85, 0.93] | 0.73 [0.60, 0.84] |
| structured | 0.84 [0.75, 0.91] | 0.92 [0.89, 0.96] | 0.89 [0.85, 0.94] | 0.70 [0.57, 0.82] |
| fusion | 0.72 [0.62, 0.83] | 0.82 [0.74, 0.88] | 0.80 [0.74, 0.85] | 0.43 [0.30, 0.57] |
| premium | 0.95 [0.90, 0.98] | 0.96 [0.91, 0.99] | 0.96 [0.92, 0.99] | 0.89 [0.79, 0.97] |
| premium_r2plus | 0.90 [0.84, 0.95] | 0.93 [0.88, 0.98] | 0.92 [0.88, 0.96] | 0.84 [0.73, 0.93] |

![test AUROC](figures/auroc_test.png)
*Figure 2. Test detection (all 95 runs) and localisation (50 positive runs) AUROCs with 95% run-bootstrap CIs.*

![test ROC](figures/roc_test.png)
*Test ROC curves (`uv run python fig_roc.py`; descriptive, thresholds read from the locked json). Dots = dev-chosen
operating points with the number of `legit` runs flagged. The frozen operating points differ widely (FPR here is over all 45
negatives, not legit only) and the curves cross; at very low FPR (≈ 0.04) action_stats' curve sits above the premium's (TPR ≈ 0.82 vs ≈ 0.66),
so the premium's AUROC lead comes from the moderate-FPR region. Read off the curve, no CI.*

**Key paired contrasts** (same runs; Δ_hybrid[v] = v − max(text, action); rows selected from the generated file,
which lists all 25 contrast families specified before the locked analysis (after interim exposure, see Held-out discipline); no multiplicity correction):

| contrast | run AUROC | within-market AUROC | pooled pair AUROC |
|---|---|---|---|
| delta_hybrid[combined] | -0.013 [-0.091, +0.064] | +0.002 [-0.052, +0.050] | +0.004 [-0.039, +0.046] |
| delta_hybrid[action_stats] | +0.106 [+0.038, +0.180] | +0.100 [+0.036, +0.164] | +0.116 [+0.067, +0.164] |
| delta_hybrid[structured] | +0.083 [+0.001, +0.169] | +0.130 [+0.068, +0.194] | +0.116 [+0.066, +0.165] |
| delta_hybrid[fusion] | -0.028 [-0.073, +0.018] | +0.022 [+0.000, +0.052] | +0.017 [-0.007, +0.043] |
| action_stats-action | +0.106 [+0.038, +0.180] | +0.100 [+0.036, +0.164] | +0.116 [+0.067, +0.164] |
| combined_stats-action_stats | -0.061 [-0.138, +0.014] | +0.036 [+0.008, +0.072] | -0.005 [-0.044, +0.035] |
| combined-fusion | +0.016 [-0.064, +0.092] | -0.020 [-0.070, +0.022] | -0.013 [-0.053, +0.029] |
| premium-combined_stats | +0.150 [+0.056, +0.248] | +0.028 [-0.022, +0.080] | +0.069 [+0.015, +0.115] |
| premium-action_stats | +0.089 [+0.010, +0.182] | +0.064 [+0.006, +0.124] | +0.064 [+0.012, +0.118] |
| premium_r2plus-action_stats | +0.045 [-0.042, +0.139] | +0.038 [-0.022, +0.104] | +0.030 [-0.024, +0.079] |
| premium-structured | +0.112 [+0.026, +0.197] | +0.034 [-0.016, +0.078] | +0.065 [+0.013, +0.116] |
| premium_r2plus-structured | +0.068 [-0.029, +0.161] | +0.008 [-0.046, +0.058] | +0.030 [-0.024, +0.080] |

**Findings (test):**
1. **No resolved gain from adding raw public text to the LLM auditor.** The text-only auditor is consistent with
   chance for detection (run AUROC 0.47 [0.36, 0.58]) and weak but above chance at localisation (0.65 [0.59, 0.71]).
   Giving the auditor messages + actions together does not resolve a gain over actions alone (Δ_hybrid[combined] run
   −0.013 [−0.091, +0.064], within +0.002 [−0.052, +0.050]; the intervals still allow gains of ~0.05–0.06, no
   equivalence test), and joint reading is not resolved better than late fusion of the two unimodal auditors
   (combined − fusion within −0.020 [−0.070, +0.022]). The gain is also unresolved on dev. That colluders keep coordination in
   the private channel is a plausible explanation, not tested.
2. **A computed statistics table helps a lot.** action_stats − action: run +0.106 [+0.038, +0.180], within +0.100
   [+0.036, +0.164]. With the table present, adding text gives a small localisation gain (combined_stats −
   action_stats within +0.036 [+0.008, +0.072]; dev +0.020 [0.000, +0.050]) and no detection gain (run −0.061
   [−0.138, +0.014]). This is the only positive say+do signal for the zero-shot LLM auditors (the supervised baseline shows a negligible +0.003 pooled-pair gain): nominal, unadjusted (25 contrast families × 3 metrics are reported, no multiplicity correction), and small; dev's lower bound is 0.000. It **did not repeat on the fresh replication split**: combined_stats − action_stats within −0.007 [−0.040, +0.020] (`replication_llm_v3rep.json`; not a registered contrast).
3. **The untrained premium has the highest run AUROC among the zero-shot LLM views and untrained comparators.** (The supervised text baseline scores higher, 0.98, under within-split CV, a different regime.) Pair premium run AUROC 0.95
   [0.90, 0.98] vs best original LLM view 0.86 (action_stats; premium − action_stats +0.089 [+0.010, +0.182], premium −
   structured +0.112 [+0.026, +0.197]). For localisation the premium also has the highest point
   estimates (pair-ID 0.89 vs 0.73 combined_stats / 0.70 structured); its within-market advantage over structured
   (+0.034 [−0.016, +0.078]) and combined_stats (+0.028 [−0.022, +0.080]) is unresolved, over action_stats it
   nominally excludes zero (+0.064 [+0.006, +0.124]). The premium is a generator-specific price-level comparator (run
   score = max over pairs); the stats table itself contains a premium row, so the stats-table gain is "better action
   summary", not cross-modal reasoning.
   Without round 1 (premium_r2plus) the detection gap vs structured/action_stats is no longer resolved (+0.068
   [−0.029, +0.161], +0.045 [−0.042, +0.139]). Disclosure: the premium was proposed after a look at partial data
   that included test runs (see Held-out discipline), so this is not a blind discovery.
4. **Legitimate cooperation: no LLM advantage at matched recall.** At dev thresholds structured and action flag
   0/15 `legit` runs vs the premium's 5/15, but at far lower recall (0.40 / 0.20 vs 0.92). At a common minimum-recall
   target (post-lock, descriptive) the LLM views show no consistent advantage in clearing legit runs (target 0.9:
   premium 5/15, action_stats 9/15, structured 11/15). Detail in Appendix C.
5. **No tested rank-average combination gives a resolved improvement over the premium** (`incremental.py`, one fixed untrained label-free
   rank-average rule; other combination rules or conditional use were not tested): combo − premium run AUROC from −0.147 [−0.226, −0.078] (text) to +0.001 [−0.038, +0.043] (structured); never resolved positive.
6. **Label = condition check.** Among y=1 runs where the pair's late-window premium is ≤ 0.5 (n = 20; low relative
   premium does not establish that coordination ended), the premium still flags 0.80 [0.58, 0.92] and action_stats 0.65. Opening-round price
   differences may contribute (premium without round 1: 0.90 vs 0.95, no paired CI), but a low later relative
   premium does not show that coordination stopped (rivals may follow the pair), so this stratification does not
   settle whether agreements were sustained.

**Flag rates at the dev-chosen thresholds** (honest FPR on `none`/`legit`; detection by realised premium) are in
Appendix C. At those thresholds the premium flags 0.92 of y=1 runs and 0.07 of test `none` runs.

**Trained non-LLM baselines on test (caution):** a logistic regression on TF-IDF of the public messages, trained by
5-fold CV *within* the test split, reaches run AUROC 0.98 [0.95, 1.00] and pair-ID accuracy 1.00, while the zero-shot
LLM text auditor has run AUROC consistent with chance. Shuffling messages within label+condition does not hurt it (0.97). So the public text
*does* carry a strong condition-linked signal that no public message states explicitly (0/125 hard-set flags) and the
zero-shot LLM does not use. Post-headline inspection (descriptive, Appendix C) suggests the cue is mostly what colluders *stop* saying
(e.g. "keeping" in 67/140 colluding firms' messages vs 133/140 rivals and 139/140 `none` firms): an indirect trace that
a supervised in-distribution model learns but a zero-shot auditor reading for explicit coordination does not use
(interpretation, not tested; transfer untested).
The untrained text-convergence score (`textsim.py`) localises at 0.74 [0.66, 0.81] vs the LLM text auditor 0.65
(Δ +0.088 [−0.010, +0.176], not resolved).

**Other test results** (details in Appendix C): sibling information-theoretic detectors are weak (run AUROC
0.45–0.62); a premium-first cascade trades recall for fewer false positives; evidence items name a colluding firm
54–62% of the time (chance 50%). Cross-family: Claude Sonnet 5.5 on the 42 mod-3 runs reproduces the pattern (text
lowest, adding text to action unresolved, adding stats helps; Appendix C).
Message-shuffle ablation and exploration strata: see Exploration below.

![mechanism test](figures/mechanism_test.png)
*Descriptive test: late-window (rounds 9–12) pair-minus-rivals premium +1.02 (none -0.02, legit +0.08), positive in 44/50 private runs.*
The numerical sources for this figure and the dev figure are preserved in
`results/analysis/mechanism_sources.json`; reproduce them with `python3 -S check_mechanism_sources.py`,
or check them without writes using `python3 -S check_mechanism_sources.py --check`.
This post-hoc source record reconstructs the original per-round means and pointwise normal bands
(mean ± 1.96 sample SE across runs), plus the original caption summaries. The bands are not simultaneous
intervals, and these condition summaries do not establish agreement-driven price effects.

### Replication on a fresh split (`llm_v3rep`, pre-registered, run once 02:07 UTC)
Because the premium was chosen after a look at partial data including test runs, we generated 30 new runs with the
unchanged generator (seed 9000; 15 `private`, 10 `none`, 5 `legit`), using the existing llm_v3 scorers, thresholds
and fusion weight. The registration commit followed the start of generation, and analysis safeguards were added
afterwards but before any replication metric was computed. Analysis
(`uv run python replication.py` → `results/analysis/replication_llm_v3rep.json`; frozen llm_v3 dev thresholds and
fusion weight; best LLM view = action_stats, fixed from the llm_v3 test json; run-once lock
`logs/final/REPLICATION_ONCE.lock`) and four predictions were pre-registered in `data/SPLITS.md` (commit 71eae06;
generation had started ~2 min earlier and that commit includes partial raw output of runs 0000–0001, but no labels,
audits or scores existed; see the SPLITS.md disclosure). Before the run the manager saw the label counts and three
labeller log lines with per-run pair premiums (runs 0027–0029); no metric was computed. All 15 private runs are judged y = 1
(13 explicit, 2 info_exchange), so label = condition again. Run-bootstrap 95% CIs (2000 class-stratified); n = 30.

| scorer | run AUROC | within-market AUROC | flag rate at frozen dev threshold: private y=1 / none / legit |
|---|---|---|---|
| text | 0.67 [0.47, 0.86] | 0.69 [0.55, 0.82] | 0.07 / 0.20 / 0.00 |
| action | 0.76 [0.57, 0.91] | 0.81 [0.67, 0.93] | 0.33 / 0.10 / 0.00 |
| combined | 0.62 [0.40, 0.80] | 0.80 [0.66, 0.91] | 0.53 / 0.50 / 0.20 |
| action_stats | 0.80 [0.61, 0.94] | 0.99 [0.96, 1.00] | 0.53 / 0.50 / 0.00 |
| combined_stats | 0.66 [0.47, 0.85] | 0.98 [0.95, 1.00] | 0.73 / 0.60 / 0.20 |
| structured | 0.66 [0.45, 0.84] | 0.91 [0.82, 0.98] | 0.40 / 0.40 / 0.00 |
| fusion | 0.78 [0.60, 0.93] | 0.84 [0.71, 0.93] | 0.47 / 0.10 / 0.00 |
| premium | 0.92 [0.79, 1.00] | 0.99 [0.96, 1.00] | 0.93 / 0.40 / 0.00 |
| premium_r2plus | 0.90 [0.75, 1.00] | 0.95 [0.89, 1.00] | 1.00 / 0.20 / 0.20 |

**All four registered decision rules were satisfied**, two only narrowly, and n = 30 gives wide CIs. Two rules concern CI inclusion; satisfying them does not establish equivalence or a substantive replication of a null effect.
- P1 premium run AUROC ≥ 0.85: **0.92** [0.79, 1.00] — held (point estimate; the CI dips below 0.85).
- P2 text run AUROC CI includes 0.5: 0.67 [0.47, 0.86] — held, but the point estimate is higher than on test (0.47).
- P3 premium − best view (action_stats) ≥ 0, point: **+0.12** [−0.004, +0.29] — held; CI just includes 0
  (within-market: +0.00 [−0.04, +0.04]).
- P4 combined − action run AUROC CI includes 0: **−0.14** [−0.30, +0.02] — held narrowly. The exploratory
  Δ_hybrid[combined] CI is [−0.33, −0.02], but it subtracts max(text, action) within each bootstrap resample, so it
  is a different contrast. Neither contrast resolves a text gain.
- Registered action_stats − action: run +0.04 [−0.10, +0.19] (not resolved, vs +0.11 on test), within-market +0.17
  [+0.05, +0.32] (resolved, as on test).

**Reading.** The fresh sample preserves the premium's highest run-AUROC point estimate, but its advantage over the
fixed best LLM view is unresolved. No run-AUROC gain from adding text is resolved; P2 and P4 establish CI inclusion,
not equivalence. Exploratory: combined − fusion run −0.17 [−0.32, −0.04] and Δ_hybrid[combined] −0.14 [−0.33, −0.02]
exclude zero, so on fresh data text nominally hurt. action_stats and combined_stats reach within-market AUROCs of 0.99 and 0.98 on the 15 positive runs;
their run-AUROC point estimates are lower than on test. At the frozen dev thresholds several scorers flag 40–60% of
the 10 fresh `none` runs (test `none`: 3–17%; premium 0.40 vs 0.07), suggesting that the frozen operating points may
be unstable even under the same generator. With only 10 fresh `none` runs, uncertainty is substantial: Wilson 95% CIs
are [0.17, 0.69] for 4/10, [0.24, 0.76] for 5/10, and [0.31, 0.83] for 6/10. Exploratory contrasts (not
pre-registered) are all in the json.

### Exploration strata (never pooled into the headline; frozen dev thresholds, nothing fitted)
**Firm framing, channel offered, no agreement found (`llm_v3fp`, 16 runs; detail in Appendix D).** Under a
"pricing manager + competition authority" framing the judge finds no agreement in 16/16 private runs, yet at frozen
dev thresholds the premium flags 0.44 of runs and combined / action_stats / combined_stats 0.50–0.63 (structured 0.25; text and
action 0.06), vs
0.03–0.17 on lab `none` test runs. **Thresholds and stats-based scorers did not transfer to a framing shift.**

**Announced price monitor (`llm_v3mon`, 14 private + 6 none; detail in Appendix D).** The pre-registered evasion
question could not be tested: with a public note that prices are monitored, the judge finds an agreement in **0/14**
monitored private runs vs 70/70 unmonitored (Fisher p ≈ 3·10⁻¹⁶); 335/336 monitored private messages contain independence/refusal phrases. On these
all-negative runs the premium still flags 0.36 / 0.50 (private / none) and action_stats / combined / combined_stats 0.33–0.43.

**Message-shuffle ablation on test (pre-registered; `uv run python shuffle_analysis.py --seeds 0,1,2 --views
combined,structured` → `results/analysis/shuffle_llm_v3_gpt-6.1-sol_test.json`; 95 runs × 3 seeds × 2 views).**
Each run's public messages are replaced by those of a donor run with the same label and condition, sampled from the three closest
eligible runs by cost/demand-path distance; firm letters are remapped so the donor's designated pair lands on the
recipient's; prices are intact. The ablation tests whether disrupting run-specific message–price alignment reduces
discrimination. It does not:
intact − shuffled run AUROC combined −0.011 [−0.101, +0.078], structured −0.019 [−0.094, +0.061]; within-market
combined −0.046 [−0.098, −0.002] (shuffled nominally *better*), structured +0.020 [−0.008, +0.054]. No loss of run-level
discrimination is resolved under this shuffle, matching the null Δ_hybrid; this does not establish that the auditors
ignore text or rule out every form of cross-modal use. Caveat: because donors
share label + condition and the pair mapping, the shuffled text still carries condition- and role-level style
(e.g. colluders' missing competitive wording), so the ablation only removes run-specific message–price consistency.

**When does the premium appear? Round 1 is set before any partner message is seen (post-lock, descriptive; `uv run
python round1_effect.py --ds llm_v3` → `results/analysis/round1_effect_llm_v3.json`; `uv run python early_detection.py
--ds llm_v3 && uv run python fig_early.py` → `results/analysis/early_detection_llm_v3.json`).** In `llm_market.py` a
seller writes its round-1 price and its first private message in the same call, while its private history is still
empty, so round-1 prices cannot reflect any agreement. Yet in round 1 the channel holders already price at 17.5
[17.2, 17.7] vs 12.9 [12.6, 13.2] for their rivals (pair premium +4.56 [+4.19, +4.90], > 0 in 69/70 private runs;
`none` +0.17 [−0.54, +0.81], `legit` −0.45 [−1.23, +0.38]; run-bootstrap CIs of means). 98.6% of round-1 private
messages contain a digit (138/140; regex only, not a validated "names a price" measure; e.g. "I suggest we both start
at 15"). The channel-holding pair therefore opens higher on average before receiving any partner message, consistent
with anticipation of coordination. As a result the premium from **round 1 alone** gives run AUROC 0.90
[0.83, 0.96] and within-market AUROC 0.93 [0.89, 0.96] on the test runs (0.91 / 0.94 on all 125), close to the full
12-round premium (0.95 / 0.96) and above every original LLM view's run-AUROC point estimate (below the post-hoc hinted view, 0.93), though below combined_stats on
localisation (0.926 vs 0.930; no paired CIs for these comparisons). Dropping round 1, the premium over rounds 2..k has
test run AUROC 0.877 at k = 2, falls to 0.855 at k = 4, and reaches 0.904 at k = 12, so later prices also distinguish
the conditions. In exploratory analyses of `llm_v3rep` performed after `replication.py`, the round-1 private-pair premium is
+5.03 [+4.30, +5.80] (> 0 in 15/15; `none` −0.40, `legit` −1.40). Round 1 alone gives run AUROC 0.84 [0.69, 0.96]
across 30 runs and within-market AUROC 0.95 [0.91, 0.99] across the 15 positive runs. Strong discrimination is thus already present before sellers receive any partner message: the
round-1 score is a **treatment-response detector** (it reacts to the channel *offer*). These analyses do not quantify
how much of the full-period AUROC comes from that response, nor performance when no agreement develops. This tightens
the label = condition caveat. Round-1 prices support early ranking here; first-round alarm rates at a calibrated
threshold were not evaluated. Matching rivals' opening prices would remove this opening-round cue.

![early detection](figures/early_detection_llm_v3.png)
*Premium AUROC vs rounds observed (all 125 llm_v3 runs, descriptive; bands = 95% class-stratified run bootstrap).*

**Placebo channel: does delivering the partner's messages add anything? (`llm_v3plc`, E58; exploratory. The plan and
predictions were appended to `data/SPLITS.md` in the same shell step that launched generation; the first commit
followed after two placebo runs had finished and after a code smoke-run of `placebo.py` on them, so pre-generation
registration is not independently established by the repo history. `uv run python llm_market.py --ds llm_v3plc
--match-ds llm_v3rep --rounds 12 --framing lab`, labels + the six frozen auditor views as usual, then
`uv run python placebo.py` → `results/analysis/placebo_llm_v3plc.json`, `figures/placebo_premium.png`).** For each of
the 15 `private` replication runs we re-ran the same seed (same designated pair, cost and demand path) with the
*identical* channel prompt, but private messages are never delivered: each seller sees only its own private messages,
so the partner appears silent. This prevents coordination through delivered private messages; public messages and
prices remain visible. (All 15 comparison runs are judge-positive: 13 explicit agreements, 2 information exchanges.
Placebo runs are not judged; they are a separate stratum, not y = 0 headline negatives.) Placebo − private is a
paired bootstrap over the 15 seeds; `none` = the 10 `llm_v3rep` no-channel runs, resampled independently:
- **Designated-pair premium with and without delivery.** Round 1: placebo +5.30 vs private +5.03 (Δ +0.27
  [−0.47, +1.07]); rounds 2–12: +1.09 vs +1.06 (Δ +0.03 [−0.54, +0.49]); rounds 7–12: +0.82 vs +0.72; `none` +0.06
  (rounds 2–12). Pair markup over cost 7.91 vs 7.88 (Δ +0.03 [−0.66, +0.71]); rivals 6.46 vs 6.49 (`none` 6.26–6.28).
  The estimates are consistent with the offer-response prediction (b) written in `SPLITS.md`. They do not establish equivalence:
  delivery effects of up to about half a price unit either way are compatible with these intervals.
- **At frozen thresholds, every action-bearing scorer flags placebo runs at least as often as delivered runs (equivalence not established).** At the frozen dev thresholds the
  premium flags 14/15 placebo and 14/15 matched private runs (`none` 4/10) and ranks the designated pair first in
  13.5/15 (tie-aware) vs 14/15. The action-bearing LLM views flag placebo runs at least as often as private runs
  (action 7 vs 5, action_stats 12 vs 8, combined 11 vs 8, combined_stats 12 vs 11, structured 8 vs 6 of 15); text
  flags 1 vs 1. Private-vs-placebo run AUROC (seed pairs resampled jointly): premium 0.46 [0.25, 0.66]; action-bearing
  views 0.31–0.44 (point estimates favour placebo; e.g. combined 0.31 [0.12, 0.54]); text alone leans toward private,
  0.68 [0.49, 0.86]. Nothing is resolved at n = 15.
- **Interpretation.** Elevated premiums and frequent detector flags occur without private-message delivery in this
  sample; the experiment does not isolate channel-offer effects from coordination through public prices, nor establish
  which cues each scorer uses. It also does not show that what is detected is pure "offer
  response". In both arms sellers open with a unilateral "let's both start at ~18" (a focal point the shared prompt
  creates) and then see each other's high opening price on the public board; placebo sellers often read the partner's
  public price as a reply ("Your price of 18 left room…"). The delivered-message arm's relative premium also declines
  sharply after round 1 (agreement persistence was not systematically measured), so the experiment cannot separate offer-induced focal pricing from tacit
  coordination on public prices. Further caveats: one seed set, one seller model; placebo sellers can notice the
  partner's silence, and the prompt's private-history window (last 8 messages) holds 8 of the seller's own messages in
  placebo vs ~4 per side in private, which may anchor placebo sellers on their own proposals. In both arms the premium
  falls from about +5 in round 1 to about +1 from round 3 on (figure). A seller model that sustains a high agreed price
  could behave differently.

![placebo premium](figures/placebo_premium.png)
*Designated-pair premium by round: delivered channel vs placebo (same 15 seeds) vs no channel; bands = 95% run bootstrap.*

**Do auditors cite round 1? (descriptive; Appendix D).** Views without a stats table cite round 1 at or below the
uniform rate (4.5–6.8% of evidence items vs 8.3% uniform), although round 1 is where the pair premium is largest.

**Telling the auditor where to look (`action_stats_hint`, post-hoc E56; Appendix D).** One fixed sentence pointing
the auditor at pair premiums and round-1 prices lifts action_stats on test (run AUROC 0.86 → 0.93, Δ +0.07
[−0.00, +0.15]) but not on the replication (0.798 → 0.796); neither split is held out for this hint.

**Which table columns help? (`action_stats_nolevel`, post-hoc E71; `uv run python auditors.py --ds llm_v3 --views
action_stats_nolevel` (+ `--ds llm_v3rep`), then `uv run python nolevel_view.py` → `results/analysis/nolevel_view.json`).**
Same prompt as action_stats, but the pair table keeps only its price-proximity column (rounds within 1) and its
price-change correlation; the three level columns (pair mean, rivals' mean, premium) are removed. The raw action log is
unchanged (155 completed gpt-6.1-sol audits, one prompt, no tuning; hypothesis logged in EXPERIMENTS.tsv before any E71
audit ran). Paired, class-stratified bootstrap over runs (95% intervals, 2,000 resamples):

| split | run AUROC action / no-level / action_stats | full − no-level (run) | within-market action / no-level / action_stats | full − no-level (within) | no-level − action (within) |
|---|---|---|---|---|---|
| test (n = 95) | 0.75 / 0.77 / 0.86 | +0.09 [+0.02, +0.17] | 0.79 / 0.86 / 0.89 | +0.03 [−0.01, +0.08] | +0.07 [+0.02, +0.13] |
| replication (n = 30) | 0.76 / 0.71 / 0.80 | +0.09 [−0.04, +0.21] | 0.81 / 0.87 / 0.99 | +0.12 [+0.04, +0.25] | +0.05 [−0.11, +0.23] |
| dev (n = 30) | 0.78 / 0.78 / 0.89 | +0.11 [−0.04, +0.28] | 0.85 / 0.86 / 0.91 | +0.05 [+0.01, +0.09] | +0.015 [0.000, +0.040] |

Pair-ID accuracy (action / no-level / action_stats): test 0.42 / 0.55 / 0.66, replication 0.47 / 0.53 / 0.93.
Reading: removing the three level columns reduces test run AUROC by 0.09 [0.02, 0.17]; the corresponding run-level
differences on dev and replication are unresolved. No run-AUROC difference between the reduced table and actions
alone is resolved (test +0.01 [−0.06, +0.09], replication −0.04 [−0.20, +0.11]), which is not evidence of equivalence.
Adding the price-proximity and price-change-correlation columns to the action log improves test localisation (+0.07
[+0.02, +0.13]); on the replication, the within-market gap between the full and reduced tables is +0.12 [+0.04, +0.25].
Run-level results partly fit the level-vs-variation reading in Appendix A; the localisation results do not cleanly separate level from proximity columns. The test covers the three
level columns jointly and does not single out the premium, which is the difference of the two means. Post hoc, on splits whose results were
already known.

**Dropping the rival comparison: absolute markup over cost (post-hoc E70, `markup_baseline.py`).** The premium compares a
pair with its rivals, so it is undefined with two firms. Three untrained, comparison-free scores: `markup_pair` (max over
pairs of pair mean price minus mean common base cost; usable with two firms), `markup_pair_own` (same, with each firm's own
public unit cost, i.e. legit partners at cost − 1) and `markup_all` (all-firm mean price minus cost).
Run AUROC on test: premium 0.95 [0.90, 0.98], markup_pair 0.95 [0.90, 0.98] (Δ +0.00 [−0.05, +0.05]), markup_pair_own
0.92 [0.86, 0.97] (Δ +0.03 [−0.03, +0.08]), markup_all 0.91 [0.85, 0.96]. On the replication (n = 30): premium 0.92,
markup_pair 0.84 [0.68, 0.96] (Δ +0.08 [−0.04, +0.22]), markup_pair_own 0.80 [0.62, 0.94] (Δ +0.12 [−0.02, +0.28]),
markup_all 0.76 [0.57, 0.91]. At frozen dev Youden thresholds markup_pair / markup_pair_own flag 0.78 / 0.72 of test and
0.67 / 0.60 of replication y = 1 runs (premium 0.92 / 0.93); `none` 0.07 / 0.00 (test) and 0.30 / 0.10 (replication);
`legit` 0.07 / 0.20 and 0.20 / 0.20 (premium: `none` 0.07 / 0.40, `legit` 0.33 / 0.00). Placebo runs: 0.73 / 0.60
(premium 0.93). Within a four-firm run markup_pair ranks pairs exactly like the premium (premium = 2 × (pair markup − all-firm markup)), so its localisation is identical.
Reading: two-firm-compatible markup scores retain substantial discrimination here (at a lower flag rate on y = 1 runs);
the premium's AUROC advantages are statistically unresolved, but the point gaps on the replication (0.08–0.16) are not
small. Similar AUROCs do not show where the signal comes from, and real two-firm markets were not tested. Post hoc, on splits whose premium results were already known; it needs known
costs and a competitive benchmark; a uniform four-firm price rise remains untested (no such data).

## Validity safeguards
Labels from private chat only (judge blind to prices); same auditor model across views, fallback calls dropped;
combined is a strict superset of both single views; shuffle donors matched on label *and* condition;
the hard-set rule excludes runs flagged by the explicit-public-coordination screen; cross-family auditor (Claude Sonnet 5.5) on
the 42-run mod-3 subset, all six views (done; text ≈ chance and no text gain for both auditors); adversarial methodology review by gpt-6.1-sol (`logs/review_methodology.md`,
12 issues; fixes applied: label leakage, view superset, public partnership info, parse strictness, learner parity,
resume ids, donor matching).

**Post-hoc input check (iteration 22).** `uv run python check_audit_inputs.py` reconstructs all 2,368 cached
auditor prompts (46 files, incl. the post-hoc E71 view added in iteration 27): 2,058 match their recorded 64-bit prompt-hash prefix; 310 older rows match only the
recorded length (150 original-view dev, 120 original-view test and 40 cross-family rows), which cannot authenticate
their historical content. The check also validates public partnership
metadata, frozen shuffle mappings and unchanged recipient actions, and tests that the current renderer excludes
injected private fields and the withheld modality. `data/audit_input_receipt.json` preserves this check after the
experiments; it is not pre-registration evidence. No model calls, scores, CIs or thresholds are rerun.

**Evidence-check coverage (post-hoc, iteration 24).** `python3 -S check_evidence_sources.py` →
`results/analysis/evidence_sources.json` and [offline source ledger](EVIDENCE.html). Across the six
original GPT views, the test caches contain 2,229 evidence items and the replication 696. All have well-formed
firm/round anchors (firm A–D, integer round 1–12), but only 3 test items and 1 replication item contain quote-marked phrases; all four
phrases occur in the cited firm's message in the cited round (case/whitespace/Unicode normalization,
word-boundary substring, punctuation retained; short phrases included). These are coverage counts for
the saved outputs, not semantic accuracy estimates: marked phrases can be terminology rather than
source quotations, and literal presence does not validate the surrounding observation. All four are
text-view items; two quote the generic phrase "considered price", which occurs across multiple firms
and rounds in their respective runs. The remaining items contain no quote-marked span and were not
semantically classified. The historical
price regex check below cannot validate these inferences; its strict same-round check can fail
legitimate price-transition descriptions. The ledger exposes all public rounds and firms for manual
comparison, including modalities withheld from the particular auditor view. **The proposed LLM
explanation role remains unvalidated.** No headline result, cache, threshold or price-check estimate changed.

**Transition-source check (post-hoc, iteration 25).** `python3 -S check_price_transitions.py` →
`results/analysis/price_transitions.json` and [all parsed clauses with source prices](PRICE_TRANSITIONS.md).
A fixed, selective grammar recognizes leading transition clauses in 51/2,229 test items and 6/696 replication items
across the same six views. All 57 parsed clauses have matching source endpoints under a cited-round reading:
54 adjacent-round matches and 3 with an earlier, nonadjacent start; no numeric-direction conflicts.
For example, `llm_v3_0030`, action view, item 0 describes firm A cutting from 18 to 14 over three rounds;
the public prices are 18 → 16 → 14 (rounds 1–3). Requiring both endpoints to equal the single cited-round price
rejects this description; even the historical ±1-round check at round 3 misses the starting 18 in round 1.
This is an illustrative example, not a re-estimate of the historical dev/test regex rates.
The new check uses only public logs and cached observations, with explicit subjects overriding the cited firm
and omitted subjects binding to it. It checks endpoints only: intermediate paths, duration, market context,
other clauses and collusion inferences remain unchecked. Unparsed items remain in the coverage denominator;
these selective counts are **not an explanation-accuracy rate**, and no semantic judge was run. A source mismatch,
if found, would call for review rather than automatically establish hallucination. Historical evidence outputs
and all frozen detection results are unchanged. Items include repeated descriptions across views and are not
independent trajectories.
Selection is especially restrictive for coordination claims: adverbs such as *jointly/simultaneously* and verbs
such as *decrease/fall/rise* are outside the grammar. A lexical diagnostic added after the first census finds
52 further unparsed test items and 17 replication items containing numeric `from X to Y` spans anywhere in the
observation; these can describe costs, later clauses or quoted wording, rather than price transitions. They are
exposed without source-agreement labels, and the validation grammar was not widened. The 57 endpoint matches
give limited assurance about collusion-alleging evidence, which may use the excluded wording.

## Held-out discipline
`data/SPLITS.md`: dev = llm_v3_0000–0029, locked test = 0030–0124. The core auditor prompt was written before any
LLM-market data; the core task text of the six original views was never optimised (0 attempts), but views and comparators were developed adaptively after interim exposure (views
`action_stats`/`combined_stats` added, public-partnership info rendering fixed; all before the locked test run,
logged in EXPERIMENTS.tsv). `final_analysis.py` (frozen 22:15 UTC) calibrates the
fusion weight and the FPR thresholds on dev, so the headline is test-only, computed once. Disclosure: interim
iteration-3 analyses (n = 36–40) included test runs 0030–0039; no prompt was tuned on them, but they informed later analysis choices. Second disclosure: the pair-premium
comparator is untrained and its one-line definition was fixed before the locked test run, but it was *chosen* after
the research director looked at premium summaries on partial data that included ~30 test runs (data/SPLITS.md,
disclosure 3); its test number is therefore not a blind out-of-sample discovery. The rounds-2–12 variant is reported
as a robustness check for that reason. Further disclosed exposures (data/SPLITS.md): a 24-test-run shuffle smoke
test, an early all-run TF-IDF fit for textsim (since replaced by a dev-only fit), and cross-family agreement numbers
computed on the mod-3 subset incl. test runs. The test evaluation is locked and run once, but not fully blind.

## Limitations
- **Label = condition.** On llm_v3 all 70 `private` runs are judged y = 1 and `none`/`legit` runs are y = 0 by
  construction (no channel to judge), so y equals the condition in all 125 runs: the endpoint is effectively "channel
  granted and used", and detecting "agreement" and detecting "a channel was granted" coincide; the endpoint is coordination *communication*, not realised overcharge. A separate
  firm-framing stratum (`llm_v3fp`, `fp_stratum.py`, frozen dev thresholds) is an exploratory transfer check of
  "agreement vs. channel without agreement" — it changes framing, wording, refusals and price levels at the same time, so it cannot
  resolve the confound within llm_v3. The placebo stratum (`llm_v3plc`, same seeds and prompt, messages never
  delivered) addresses part of it within one generator: premium and auditor flags are no lower without message delivery, so
  in this sample, delivered private coordination was not required to produce the flags our conduct-based detectors raise (n = 15, exploratory;
  equivalence not shown; focal opening prices and tacit public-price coordination are not separated).
- **Evasion not tested.** Sellers in the headline data were never told prices are watched. In the exploration
  stratum `llm_v3mon`, with an announced price monitor the judge found no agreements (0/14), so no evasive
  colluders were produced; robustness of the premium to evasion remains open.
- **The premium requires comparison firms.** As specified it is undefined in a two-firm market and cannot detect a
  uniform price increase shared by all four firms. A comparison-free markup over cost keeps much of the signal here
  (post-hoc E70), but it needs known costs and a competitive benchmark, and it can flag high pricing without delivered private messages; a
  uniform all-firm cartel was not generated, so this case is untested.
- **Generator-specific premium.** Channel holders open higher before receiving any private message. Round 1 alone
  gives test run AUROC 0.90; rounds 2–12 give test 0.90 and dev 0.92. Removing observed round 1 does not estimate what
  would happen if sellers changed their opening strategy.
- Single seller model family (GPT, gpt-6-luna), single framing for the headline data, 12 rounds, 4 firms.
- Agreement labels from one LLM judge (gpt-6.1-sol, same family as the auditor; blind to prices); manually
  spot-checked on 3 dev chats + pilots. A Claude Sonnet 5.5 re-judge (E74) reproduces the binary label on all 115
  private chats, but the explicit vs info_exchange sub-label differs between these two judges.
- Zero-shot auditors with one prompt per view (0 tuning attempts on the six original views; the post-hoc hint view E56 is one data-informed revision); a tuned or few-shot auditor might use the stats table better.
- Small dev split (30 runs, base rate 2/3) → dev-fitted thresholds and fusion weight are noisy. Reported intervals resample saved runs and
  scores; they do not repeat model calls, refit supervised models, or account for adaptive analysis selection. The Youden rule breaks
  ties toward the higher threshold: conservative on FPR only — with perfect dev separation (premium) the cut sits at
  the lowest dev-positive score, which can cost test TPR.
- The sibling's information-theoretic detectors may have been developed while looking at llm_v3 runs that include our
  test runs; their test numbers are a comparator, not a locked held-out result.

## What to do next
1. **Evasion-aware colluders.** The premium already discriminates strongly before any partner message is read;
   robustness to sellers that conceal this opening-price cue remains untested. Under our `llm_v3mon`
   announcement (prices monitored, flagged pairs lose half their earnings) gpt-6-luna produced no judge-labelled
   agreements (0/14), so testing evasion needs a red-teamed or instructed colluder (or a less safety-tuned seller
   model), including colluders that coordinate on gradual drift; we expect the premium and stats-table views to
   degrade first.
2. **Make text matter.** Text should become necessary when conduct alone is ambiguous: legit cooperation that moves
   prices, or collusion signalled in public through innocuous-looking wording (a supervised text model already finds
   such a trace here). Train/transfer that text model across seller models and framings before trusting it.
3. **Label ≠ condition.** Include placebo-matched negatives and test whether public text or conduct distinguishes
   delivered private coordination from an offered but undelivered channel, across seller models and games where a
   delivered agreement actually changes prices. Add a one-sided placebo (offer to one seller only) to separate
   offer-induced focal pricing from tacit coordination on public prices.
4. **Auditor design.** The stats-table views already include the premium. A one-sentence premium hint was tested
   post hoc (§Exploration, E56: mixed). Test it prospectively on a fresh split, repeat the post-hoc level-column ablation (E71) prospectively, evaluate any
   stats-first → LLM cascade on fresh data, and test tuned/few-shot auditors on a fresh split.
5. **Breadth.** Other seller model families, more firms/rounds, and a second market type.

## Appendix A — LLM market, DEV split (runs 0000–0029; development only, superseded by the locked test above)
Headline numbers above come from the completed, single locked test analysis
(`final_analysis.py --split test` via `finalize_test.sh`, runs 0030–0124). The development results below are retained
for context. Numbers below are **dev** (runs 0000–0029: 20 positive, 10 negative = 5 `none` + 5 `legit`),
indicative only. `uv run python final_analysis.py --split dev` → `results/analysis/final_llm_v3_gpt-6.1-sol_dev.json`.

**No explicit public coordination was flagged.** `hardset.py` (keyword list + a cheap-tier LLM check of every run's public messages: gpt-6-luna for 94 runs,
deepseek-v4.1-flash via llm.py's backend auto-order for 31) flagged
**0 / 94** runs checked at that point (final: **0 / 125**, re-checked in the locked run) for explicit coordination
language in public. Within the limits of a keyword list + one LLM check, the sellers keep coordination in the private
channel, so the LLM set is effectively all "hard" set; an "easy" set does not occur naturally here.

Scorers: six gpt-6.1-sol zero-shot auditor views; the **untrained pair premium** (pair mean price − mean of the
other two firms, every pair, all rounds; run score = max over pairs; nothing fitted); a **late fusion**
w·text + (1−w)·action of the unimodal auditor scores (w fitted on dev: 0.6). Dev, 2000 class-stratified run
bootstraps; table copied verbatim from the generated `results/analysis/report_tables_dev.md`
(flag rates at dev thresholds: see the flag-rate table there; y=1 / all negatives: text .25/.10, action .65/.10,
action_stats .85/.10, combined .80/.20, combined_stats .90/.30, structured .65/.10, fusion .70/.10, premium 1.00/.00):

| scorer | run AUROC (detection) | within-market AUROC (localisation) | pooled pair AUROC | pair-ID acc |
|---|---|---|---|---|
| text | 0.57 [0.37, 0.78] | 0.61 [0.50, 0.72] | 0.56 [0.45, 0.68] | 0.31 [0.17, 0.45] |
| action | 0.78 [0.57, 0.93] | 0.84 [0.73, 0.93] | 0.82 [0.70, 0.92] | 0.52 [0.30, 0.72] |
| action_stats | 0.89 [0.75, 0.99] | 0.91 [0.80, 0.98] | 0.91 [0.80, 0.98] | 0.75 [0.55, 0.90] |
| combined | 0.83 [0.64, 0.97] | 0.85 [0.73, 0.94] | 0.80 [0.68, 0.90] | 0.55 [0.35, 0.75] |
| combined_stats | 0.81 [0.64, 0.95] | 0.93 [0.82, 1.00] | 0.89 [0.78, 0.97] | 0.85 [0.70, 1.00] |
| structured | 0.83 [0.67, 0.96] | 0.91 [0.80, 0.97] | 0.89 [0.78, 0.96] | 0.70 [0.50, 0.90] |
| fusion | 0.82 [0.66, 0.95] | 0.85 [0.73, 0.93] | 0.82 [0.70, 0.92] | 0.52 [0.30, 0.72] |
| premium | 1.00 [1.00, 1.00] | 0.98 [0.94, 1.00] | 0.99 [0.96, 1.00] | 0.95 [0.85, 1.00] |
| premium_r2plus | 0.92 [0.80, 1.00] | 0.95 [0.89, 1.00] | 0.96 [0.91, 0.99] | 0.90 [0.75, 1.00] |

(Thresholds are dev-fitted, so the flag rates on dev are optimistic; honest test FPR is in the headline section.)
Why the premium is so strong: private-channel sellers choose their opening price and first private message in the
same call, before reading a partner message (see §Exploration "When does the premium appear?"; earlier versions
wrongly said the pair "agrees in round 1"), while the rivals open at ≈ 12. In three inspected dev chats (0005, 0012,
0016), sellers lower their opening prices after rivals undercut them; this does not establish that coordination ends. The opening-round gap alone carries much of the signal; without
round 1 the premium still matches or beats every original LLM view on dev, but no longer significantly vs structured/action_stats
(premium_r2plus − structured: run +0.09 [−0.10, +0.29]; it still beats text, and action/combined on
localisation). The LLM auditors also see round 1.
![mechanism dev](figures/mechanism_dev.png)
*Descriptive dev: private pairs' mean opening price 17.35 vs 12.53 for rivals; late-window (rounds 9–12) pair-minus-rivals premium +0.90 (none -0.07, legit +0.15), positive in 12/20 private runs.*
Source: `results/analysis/mechanism_sources.json` (same saved-price reconstruction as the test caption).
The figure shows a large opening gap and a smaller late-window gap; 8/20 private pairs have a
non-positive average gap in rounds 9–12. This does not measure whether an agreement persisted.
**Label ≈ condition:** all 20 dev `private` runs are labelled y = 1 (19 explicit, 1 info-exchange), so on this
generator "agreement" and "had a channel" coincide; see Limitations.
Paired contrasts (dev, from the generated file): Δ_hybrid[combined] run +0.052 [−0.123, +0.210], within +0.005
[−0.050, +0.045]; Δ_hybrid[combined_stats] within +0.085 [+0.040, +0.135]; combined − fusion run +0.003
[−0.120, +0.120]; action_stats − action within +0.065 [+0.020, +0.110]; combined_stats − action_stats within +0.020
[+0.000, +0.050]; premium − structured run +0.168 [+0.043, +0.333], within +0.075 [−0.010, +0.185]; premium −
action_stats run +0.113 [+0.010, +0.250].

![dev AUROC](figures/auroc_dev.png)

**Development interpretation (compare the completed test and replication results above):** on dev, adding the public text to the actions shows no resolved
gain for the LLM auditor (combined − action within +0.005 [−0.05, +0.045]; joint reading ≈ late fusion of the two
unimodal auditors). A plausible reason, not tested causally, is that the sellers keep coordination private and their
public messages are bland. The views that include a *computed pair-statistics table* (action_stats, combined_stats,
structured) localise better than those without; separately, a single untrained statistic (the pair premium) beats
every original LLM view on dev. (A later post-hoc column ablation, E71 in §Exploration, finds that removing the table's three level columns lowers test run AUROC; dev and replication run-level differences are unresolved and within-market results are mixed.) This fits the sibling project's
finding that dependence statistics detect coordinated *variation*, not *level*: price levels discriminate strongly here and the premium
measures level directly (this does not establish agreement-driven pricing).

**Information-theoretic dependence detectors (sibling Q1.4, dev).** Using the sibling project's per-pair scores on
the same runs (`../collusion-14-infotheory/results/eval/llm_v3_ext.json`, read-only; block `external_infotheory`
in the final_analysis output): run AUROC pCMI 0.47 [0.22, 0.72], MI 0.60 [0.40, 0.80], TE 0.59 [0.32, 0.83],
Pearson 0.21 [0.06, 0.39] (below chance; hypothesis, not tested: colluding pairs hold prices flat, so co-vary less); within-market
MI 0.85, Pearson 0.76, TE 0.67, pCMI 0.55. Premium − pCMI run AUROC +0.53 [+0.27, +0.78]. Their independently
coded `pair_level` statistic matches our premium's aggregate metrics (run 1.00, within 0.98); per-pair equality not checked.
So on this generator, dependence-in-variation statistics are weak, level statistics are strong.

**Illustrative differences in pair scores (gallery, `results/analysis/gallery_dev.md`; both approaches clear this run
at their frozen thresholds, so this illustrates differing rationales, not better classification):** in `legit` run 0001 the
partnership pair has a positive premium (+0.62 all-round) and is the premium's top pair, while the text/structured
auditors read the public partnership notice and give that pair 4–7/100. On dev the premium's run-level threshold
happens to sit above it, but this is the failure mode a price-only screen has with legitimate cooperation.

**Evidence accuracy (dev, `evidence.py` → `results/analysis/evidence_llm_v3_gpt-6.1-sol_dev.json`; 5 views, combined_stats
not checked).** Syntactic checks only (cited round/firm exist; extracted price numbers vs the log), not whether the
evidence supports the claim. All cited rounds/firms are valid. In the four action-bearing views 45–55% of items
contain a price claim; of these, 51–65% match the cited firm's price in the exact cited round, 81–92% within ±1 round,
95–100% match some firm's price nearby (text view: only 3 price claims). On positive runs 47–59% of cited firms
belong to the colluding pair (chance 50%): auditors cite market-wide observations, so their evidence rarely singles
out the colluders. No verbatim quotes were cited.

**Audit cost (prompt size per call; `uv run python cost.py` → `results/analysis/cost_llm_v3.json`).** text 9.2k chars, action 3.3k, action_stats 3.7k, combined 11.4k,
combined_stats 11.8k, structured 12.0k (≈ chars/4 tokens); one gpt-6.1-sol call per run per view. The premium requires no LLM calls; a
premium-first triage that sends only the top 75% of dev runs to the LLM audit keeps all positives (dev base
rate is 2/3; test: auditing the top 50% / 75% sends 0.84 / 1.00 of y=1 runs, see `report_tables_test.md`). End to end (run sent by the premium screen AND flagged by
the LLM view at its dev threshold), the cascade cannot exceed its premium screen's recall but can cut false positives: dev, auditing all
runs, action_stats catches 0.85 of y=1 runs at FPR 0.10 and names the correct pair in 0.65; structured 0.65 / 0.10 /
0.55 (`triage.*.cascade_*` in the final json). A proposed architecture is premium screen → LLM audit for explanation/evidence and false-positive filtering
(explanation usefulness itself is not measured here).
**Does any LLM view add to the premium? (`incremental.py`, iter 7, dev.)** An untrained, label-free combination
(average percentile rank of premium and the view) never beats the premium alone on dev: combo − premium run AUROC
from −0.10 [−0.24, −0.005] (text) to −0.015 [−0.065, 0.00] (action_stats); within-market ≤ 0. On y=1 runs, every
view gets the colluding pair right while the premium gets it wrong in at most 1 of 20 runs. Dev is at the premium's
ceiling, so this can only show harm there; the completed test comparison is in Findings, item 5.

*Caveat (22:00 codex review, `logs/review_interim.md`): `legit` runs were initially audited WITHOUT their public
partnership notice. Fixed 22:10 (auditors.py regenerates `public_info`; legit audits invalidated and re-run;
cached audits are now checked against the current prompt hash/length and re-run if stale).*

**Supervised non-LLM baselines (dev; `baselines.py --ds llm_v3 --split dev`, LR, 5-fold CV grouped by run inside
dev, n = 30).** Run AUROC text 0.79 [0.61, 0.93], action 0.96 [0.86, 1.00], combined 0.96, structured 0.95;
pair-ID accuracy text 0.90, action 0.95 (action = computed price/outcome features; supervised CV inside dev, labels of
other dev runs). Hybrid Δ ≈ 0 (ceiling). A *trained* classifier on price features far
outperforms the zero-shot LLM reading the same prices (not like-for-like: the LR sees in-distribution labels). The
text LR beats the LLM text auditor by a wide margin (pair-ID 0.90 vs 0.31). An informal look at its top-weighted
n-grams during development (no saved artifact) suggested margin-flavoured phrasing for positives ("considered price",
"sustainable") and the `legit` pairs' "shipping partnership" notices for negatives.

**Untrained public-text convergence (new, iter 6, dev; `textsim.py`).** Hypothesis: if partners' private
coordination shapes their public wording, the two colluders' public messages should resemble each other more than
other pairs' do. Score = TF-IDF cosine of the pair's public messages − mean cosine of the other pairs (vectorizer fit
on dev text only, no labels; nothing tuned). Dev: within-market AUROC **0.81 [0.69, 0.91]** vs the zero-shot LLM
text auditor 0.61 (paired Δ +0.20 [+0.07, +0.31]); pair-ID 0.55. It showed no detection ability on dev (run AUROC
0.48 [0.24, 0.72], inconclusive). So the public text does contain a localisation cue that the zero-shot LLM text
auditor does not reflect in its pair scores. That the cue comes from the private agreement leaking into public
wording is a plausible mechanism, not shown (label ≈ condition here). Pre-registered before this scorer was
evaluated on test (earlier disclosed test exposures of other scorers still apply, `data/SPLITS.md`).

## Appendix B — Scripted mechanism check (non-LLM baselines, `baselines.py`, 5-fold CV grouped by run, 320 runs)
`uv run python baselines.py --ds scripted_v2 --learner lr` → `results/baselines/scripted_v2_lr.json`.
- scripted_v1 (strong collusion): action features alone reach AUROC 1.0 → Δ_hybrid = 0 by ceiling; uninformative.
- scripted_v2 (weak, low-markup collusion; hard set = 280 runs excl. explicit public talk), logistic regression on
  nested feature sets, run-level AUROC [95% bootstrap CI]:

  | view | intact | messages shuffled (same label+condition donor, same CV test fold) |
  |---|---|---|
  | text (TF-IDF) | 0.839 [0.788, 0.882] | 0.837 [0.787, 0.882] |
  | action stats | 0.951 [0.922, 0.973] | 0.951 (unchanged by construction) |
  | combined raw (text + action) | 0.961 [0.939, 0.979] | 0.961 [0.940, 0.979] |
  | structured (action + say-vs-do consistency) | 1.000 [1.000, 1.000] | 0.748 [0.680, 0.811] |

  Δ_structured = +0.049 [0.027, 0.079]; Δ_combined = +0.010 [0.004, 0.019]. Shuffling leaves both single
  modalities and the raw union untouched but collapses the structured model → its gain comes from the
  say-vs-do alignment features, i.e. the mechanism the templates were built to contain.
- Methodological cautions found on the way: (i) mixing learners (boosting for numeric, LR for text) produced an
  apparent shuffle collapse on scripted_v1 that vanished with identical learners; (ii) drawing shuffle donors from
  the whole dataset let a boosted text model recognise memorised training-fold text (text-only AUROC *rose*
  0.91→0.995 under shuffle; historical debugging value, EXPERIMENTS.tsv E05, configuration not retained); donors are now drawn within the CV test fold.

## Appendix C — Additional test-split detail (locked test split, n = 95; moved from §Results for length)

**Flag rates at the dev-chosen thresholds (test, honest FPR):**

| stratum | n | text | action | action_stats | combined | combined_stats | structured | fusion | premium | premium_r2plus |
|---|---|---|---|---|---|---|---|---|---|---|
| all_negatives | 45 | 0.11 [0.05, 0.23] | 0.04 [0.01, 0.15] | 0.04 [0.01, 0.15] | 0.20 [0.11, 0.34] | 0.18 [0.09, 0.31] | 0.04 [0.01, 0.15] | 0.09 [0.04, 0.21] | 0.16 [0.08, 0.29] | 0.20 [0.11, 0.34] |
| legit | 15 | 0.07 [0.01, 0.30] | 0.00 [0.00, 0.20] | 0.07 [0.01, 0.30] | 0.27 [0.11, 0.52] | 0.20 [0.07, 0.45] | 0.00 [0.00, 0.20] | 0.07 [0.01, 0.30] | 0.33 [0.15, 0.58] | 0.33 [0.15, 0.58] |
| none_all | 30 | 0.13 [0.05, 0.30] | 0.07 [0.02, 0.21] | 0.03 [0.01, 0.17] | 0.17 [0.07, 0.34] | 0.17 [0.07, 0.34] | 0.07 [0.02, 0.21] | 0.10 [0.04, 0.26] | 0.07 [0.02, 0.21] | 0.13 [0.05, 0.30] |
| none_highmarkup_proxy | 1 | 1.00 [0.21, 1.00] | 0.00 [0.00, 0.79] | 0.00 [0.00, 0.79] | 1.00 [0.21, 1.00] | 1.00 [0.21, 1.00] | 1.00 [0.21, 1.00] | 1.00 [0.21, 1.00] | 0.00 [0.00, 0.79] | 0.00 [0.00, 0.79] |
| none_lowmarkup | 29 | 0.10 [0.04, 0.26] | 0.07 [0.02, 0.22] | 0.03 [0.01, 0.17] | 0.14 [0.06, 0.31] | 0.14 [0.06, 0.31] | 0.03 [0.01, 0.17] | 0.07 [0.02, 0.22] | 0.07 [0.02, 0.22] | 0.14 [0.06, 0.31] |
| private_y1 | 50 | 0.10 [0.04, 0.21] | 0.20 [0.11, 0.33] | 0.72 [0.58, 0.82] | 0.52 [0.39, 0.65] | 0.68 [0.54, 0.79] | 0.40 [0.28, 0.54] | 0.28 [0.17, 0.42] | 0.92 [0.81, 0.97] | 0.84 [0.71, 0.92] |

**Label≈condition check**: detection (flag rate) among y=1 runs by realised late-window relative premium of the colluding pair:

| stratum | n | text | action | action_stats | combined | combined_stats | structured | fusion | premium | premium_r2plus |
|---|---|---|---|---|---|---|---|---|---|---|
| late_rel_premium_le_0.5 | 20 | 0.05 [0.01, 0.24] | 0.25 [0.11, 0.47] | 0.65 [0.43, 0.82] | 0.55 [0.34, 0.74] | 0.60 [0.39, 0.78] | 0.35 [0.18, 0.57] | 0.35 [0.18, 0.57] | 0.80 [0.58, 0.92] | 0.60 [0.39, 0.78] |
| late_rel_premium_gt_0.5 | 30 | 0.13 [0.05, 0.30] | 0.17 [0.07, 0.34] | 0.77 [0.59, 0.88] | 0.50 [0.33, 0.67] | 0.73 [0.56, 0.86] | 0.43 [0.27, 0.61] | 0.23 [0.12, 0.41] | 1.00 [0.89, 1.00] | 1.00 [0.89, 1.00] |

**Other test results** (all in `results/analysis/report_tables_test.md`): sibling information-theoretic detectors are
weak (run AUROC pCMI 0.54, MI 0.62, TE 0.45, Pearson 0.56; their `pair_level` = our premium, 0.95); premium-first
cascade end to end (premium sends top 50% of runs, LLM view must also flag): action_stats recall 0.60 / FPR 0.02 /
correct pair 0.44, structured 0.34 / 0.00 / 0.26 — relative to its upstream premium screen (top 50%: recall 0.84, FPR 6/45 = 0.13) the AND-gate trades recall for fewer false positives; which is better depends on the costs of misses, false alarms and audit calls;
evidence items name a colluding firm 54–62% of the time on y=1 runs (chance 50%); 81–93% of price claims pass a permissive regex check (numbers match the log within
±1 round; exact-round 49–63%; action-bearing views; reasoning itself not validated). Cross-family (Claude Sonnet 5.5 vs gpt-6.1-sol, all 42 mod-3
runs, 24 y=1, dev+test pooled; `cross_family.py` → `results/analysis/llm_v3_crossfamily_claude-sonnet-5-5.json`): the
**main pattern replicates across model families** — text lowest (run AUROC GPT 0.51 / Claude 0.58), action 0.76 / 0.80,
combined 0.74 / 0.74; stats views (action_stats 0.85 / 0.91, structured 0.79 / 0.90, combined_stats 0.76 / 0.92) are
highest for Claude, while for GPT only action_stats clearly is (point estimates, no CIs, n = 42, dev + test pooled). Adding text to action has no resolved effect for either auditor (Δ pair AUROC combined − best single: GPT +0.01
[−0.05, +0.08], Claude −0.01 [−0.10, +0.07]); adding stats does (action_stats: GPT +0.09 [+0.02, +0.16], Claude +0.09
[+0.00, +0.19]). Per-pair agreement between the two auditors is only moderate (Spearman 0.31 text … 0.59 structured;
top-pair agreement 0.38–0.71), so individual verdicts are model-dependent even though the tested aggregate comparisons agree.

**Finding 4 in full (legitimate cooperation at matched recall; moved from §Results):**
**Legitimate cooperation: no LLM advantage at matched recall.** At dev-chosen thresholds the premium flags 5/15
   (0.33) `legit` partnership runs, while structured and action flag 0/15 (Wilson CI [0, 0.20]); these views can read
   the public partnership notice (no notice-removal ablation was run). But they operate at much lower recall (0.40 and
   0.20 of y=1 runs vs the premium's 0.92), and the text-reading combined views flag legit runs about as often as the
   premium (combined 0.27, combined_stats 0.20). Comparing at a common *minimum recall target* (post-lock,
   descriptive; `uv run python matched_recall.py` → `results/analysis/matched_recall_llm_v3_test.json`; oracle
   thresholds read off the test positives; ties can push a scorer's recall above the target) gives mixed results at
   moderate recall and a premium advantage at high recall. Legit runs flagged: target 0.5 — premium 0/15 (TPR 0.50),
   structured 0/15 (0.54), action_stats 1/15 (0.50); target 0.7 — premium 2/15 (0.72), action_stats 1/15 (0.72),
   structured 3/15 (0.78); target 0.9 — premium 5/15 (0.90), action_stats 9/15 (0.92), structured 11/15 (0.92);
   `none` runs at target 0.9: 2/30 vs 20/30 and 19/30. At these recall targets the LLM views show no consistent
   advantage over the premium in clearing legitimate runs (n = 15 legit runs; no CIs). The contribution of the public
   partnership notice was not isolated. Numerical note: the frozen and oracle premium cuts both
   represent 2/3 but differ in floating-point rounding (premium scores of mathematically tied runs differ at ~1e-15),
   which explains a one-run recall difference (46/50 vs 45/50); it has no substantive meaning.

**Text-classifier inspection in full (moved from §Results):** Post-headline inspection (`uv run python text_lr_inspect.py` → `results/analysis/text_lr_inspect.json`;
descriptive all-data refit, not an evaluation; it does not show which features drive the out-of-fold performance):
top positive uni/bigrams are bland margin phrasing ("considered price", "supports reliable", "balances customer"),
top negative ones competitive phrasing ("price competitive", "your business", "keeping"). At the firm level (all
125 runs; each firm's concatenated public messages; role = colluding firm / rival firm in the same private run /
firm in a `none` run): "considered price" 25/140 colluders, 11/140 rivals, 0/140 `none` (0/80 `legit`) — so rivals
pick it up too (condition-level shift); but the **pair-specific cue is large**, and mostly it is what colluders
*stop* saying: "keeping" 67/140 vs 133/140 vs 139/140, "business" 6/140 vs 45/140 vs 56/140, while "adjusting our"
rises (51/140 vs 12/140 vs 21/140). This is consistent with the text LR's perfect pair-ID (1.00 vs premium 0.89).
The message shuffle (donors share label + condition) cannot remove a condition-level style signal, so its
shuffle-robust 0.97 is not evidence against it. Interpretation (not tested): public text carries an *indirect*
trace — colluders drop competitive language — that a supervised model trained in-distribution learns but a
zero-shot LLM auditor reading for explicit coordination does not use. Whether it reflects the channel prompt, the
communication or the conduct cannot be separated here (label = condition). Whether it transfers to other seller models or framings is untested.

## Appendix D — Exploration strata detail (moved from §Results for length; text unchanged)
**Firm framing, channel offered, no agreement found (`llm_v3fp`, 16 `private` runs, `uv run python fp_stratum.py --ds
llm_v3fp` → `results/analysis/fp_stratum_llm_v3fp.json`).** Under the "pricing manager + competition authority"
framing, the judge finds **no agreement in 16/16 runs**: sellers given a private channel declined to coordinate
(replicating the pilot). These are natural "channel, no agreement" negatives, so a scorer that tracks agreement
rather than framing should rarely flag them. Flag rates at the dev thresholds [Wilson 95%]: text 0.06 [0.01, 0.28],
action 0.06 [0.01, 0.28], structured 0.25 [0.10, 0.50], premium 0.44 [0.23, 0.67], combined 0.50, action_stats 0.50,
combined_stats 0.63 [0.39, 0.82] — vs 0.03–0.17 on lab-framing `none` test runs. Mean prices are close to the lab
`none` runs (13.2 in round 1, 12.5 in round 12, vs 12.9 / 12.0; `uv run python fp_prices.py` → `results/analysis/fp_prices.json`), but the source of the false alarms was not
established (pair-level price differences under the other framing are a guess, not analysed). **Thresholds and
stats-based scorers did not transfer to a framing shift**; the stats table, which helped on llm_v3, raised false
alarms here. With only y = 0 runs, no AUROC can be computed. Exploratory (n = 16, one framing change that also
changes wording and refusals).

**Announced price monitor (`llm_v3mon`, lab framing + public announcement that prices are monitored; 14 private,
6 none; the note says an automated monitor reviews prices + public board, cannot see private messages, and halves
the earnings of flagged pairs — announced only, no monitor is run). `uv run python deterrence.py` →
`results/analysis/deterrence.json`.** The pre-registered question (does the premium survive colluders who know prices
are watched?) **could not be tested: the monitored sample contains no judge-labelled coordination communication.** The
judge finds an agreement in **0/14** monitored private runs [Wilson 0.00, 0.22] vs **70/70** unmonitored lab private
runs [0.95, 1.00] (Fisher p ≈ 3·10⁻¹⁶). The cohorts are unpaired (seeds 3000000–3000124 vs 7000000–7000019; 70 vs 14
private, 35 vs 6 `none` runs); same seller model (gpt-6-luna), 12 rounds, and system prompts that differ only by the
monitor note. Lexical indicators (regexes, not validated measures): digit matches in 0/336 monitored private messages
vs 1488/1680 (88.6%) on llm_v3; independence/refusal phrases (e.g. "I can't coordinate prices") in 335/336 (99.7%) vs
613/1680 (36.5%). Mean markup over cost in monitored private runs is 6.16 vs 6.27 in monitored `none` runs (llm_v3:
private 7.66, none 5.84); assigned-pair premium +0.23 (llm_v3 private +1.65); premium > 1 in 1/14 runs (llm_v3 61%)
— close to no-channel levels, though not shown equivalent. So on this sample, announcing a monitor coincides with no
coordination talk rather than with hidden coordination. Caveats: n = 14, one seller model; the later E74 Claude
re-judge agrees on all 14 negative private-chat labels, but correctness on refusal-style chats remains unvalidated.
We cannot distinguish safety-triggered refusal from
strategic deterrence, nor exclude tacit coordination, and it says nothing about how a model that does try to evade
would look. **False alarms on this stratum** (all 20 runs are y = 0; frozen dev thresholds; `uv run python
monitor_stratum.py --ds llm_v3mon` → `results/analysis/monitor_stratum_llm_v3mon.json`), flag rate on the 14
private-no-agreement / 6 `none` runs [Wilson 95%]: text 0.00 [0.00, 0.22] / 0.00 [0.00, 0.39], action 0.21 / 0.50,
structured 0.21 / 0.17, premium 0.36 [0.16, 0.61] / 0.50 [0.19, 0.81], action_stats 0.43 / 0.33, combined 0.43 / 0.33,
combined_stats 0.36 / 0.33 — vs 0.03–0.17 on lab `none` test runs. Like the firm-framing stratum, a prompt change
after which no agreements are found leaves the premium and the stats/combined views flagging a third to a half of runs:
the premium's run score is the largest premium over all six pairs, and in 8/20 monitored runs it reaches the frozen
cut of 0.67 price units (max 2.29), more often than in lab `none` test runs (why was not analysed). Exploratory, n = 20.

**Round-1 citations by the LLM auditors (post-lock, descriptive; `uv run python evidence_rounds.py --ds llm_v3
--split test` → `results/analysis/evidence_rounds_llm_v3_test.json`; `--ds llm_v3rep --split all` for the
replication).** Each audit cites up to 4 evidence items, each tied to a round. On the 95 test runs, round 1 accounts for
4.5–10% of cited items depending on the view (text 6.8%, action 4.5%, combined 5.0%, combined_stats 8.5%,
action_stats 10.1% [7.7, 12.7], structured 9.0%). Uniformly cited rounds would give 8.3%. Among audits of y = 1 runs,
round 1 is cited at all in 16–24% of text/action/combined audits and 42–48% of the stats-table views (11–31% of y = 0
audits). In the replication, round 1 accounts for 5.8–11.8% of cited items. The views without a stats table cite
round 1 at or below the uniform rate, although round 1 is where the pair premium is already large. The headline run
score (`collusion_present`) correlates with both the round-1 and the rounds-2..12 premium (test Spearman: action_stats
0.52 vs 0.58; combined 0.42 vs 0.40). These are citation frequencies and descriptive associations. They do not show
which rounds drove a verdict, nor do they explain the stats-table benefit.

**Telling the auditor where to look (`action_stats_hint`; post-lock exploration E56; `uv run python auditors.py --ds
llm_v3 --views action_stats_hint` (+ `--ds llm_v3rep`), then `uv run python hint_view.py` →
`results/analysis/hint_view.json`).** This view is `action_stats` plus one fixed sentence. The sentence says that
colluding pairs typically price above the other two firms, often from round 1, and asks the auditor to check each
pair's premium and round-1 prices. We wrote it once, after the locked test and the replication, using what those
analyses had shown. No further prompt search followed this data-informed revision. Because the hint encodes knowledge taken from the test and replication data,
neither split is held out for it. Paired, class-stratified bootstrap over runs:
- **Test (n = 95).** Run AUROC rises from 0.86 to 0.93 (Δ +0.07 [−0.00, +0.15]). Within-market AUROC rises from 0.89 to 0.96
  (Δ +0.06 [+0.02, +0.11]). Pair-ID rises from 0.66 to 0.83. The remaining gap to the premium is +0.02 [−0.02, +0.07]
  (run) and +0.00 [−0.03, +0.03] (within-market).
- **Replication (n = 30).** No resolved run-level gain: 0.796 vs 0.798, Δ −0.002 [−0.18, +0.16]. Within-market AUROC is
  0.99 for both, near ceiling. The premium's point estimate remains higher at 0.92 (Δ +0.12 [−0.03, +0.28]).
- **Dev (n = 30).** Run AUROC 0.93 vs 0.89; within-market 0.98 vs 0.91. Neither change is resolved.

The hint makes the run score track the premium more closely: Spearman with the max-pair premium rises from 0.60 to 0.87
on test and from 0.65 to 0.75 on the replication. Pointing the auditor at the premium can therefore recover much of
the premium's ranking on test, but the gain does not show on the 30 replication runs (where action_stats' pair scores
already localised near ceiling).
The test gaps to the premium are unresolved; this establishes neither equivalence nor superiority. A cheaper design is to
compute the statistic and ask the LLM only for explanation (proposed; explanation quality untested).

## Appendix E — Reproduce
The experiments are complete. For a read-only offline check of the shipped artifacts, run
`python3 verify_artifacts.py` (standard library only; no LLM calls, metric recomputation, or writes).
For a separate read-only reconstruction of cached auditor inputs, run
`uv run python check_audit_inputs.py` (requires NumPy; recorded-hash and length-only matches reported separately).
For a read-only freshness check of the cached evidence source ledger, run
`python3 -S check_evidence_sources.py --check` (standard library only; literal source locations, no semantic judge).
For a separate read-only check of leading price-transition endpoints, run
`python3 -S check_price_transitions.py --check` (standard library only; selective grammar, no semantic judge).
For a read-only reconstruction of the existing mechanism figure's numerical sources and captions, run
`python3 -S check_mechanism_sources.py --check` (standard library only; descriptive public-price means and normal bands).
The post-hoc manifest and completion receipt were added in iteration 19 to preserve the handoff;
they are not pre-registration evidence. See [README.md](README.md) for artifact locations and
safe rendering commands. The generation/audit commands below document how the existing results
were produced; the two completed run-once entry points now refuse to rerun even in a fresh clone.

```
uv run python llm_market.py --ds llm_v3 --plan private:70,none:35,legit:20 --rounds 12 --framing lab --games-parallel 2 --seed 3000
uv run python label_llm.py --ds llm_v3
uv run python label_xfam.py                    # E74 cross-family (Claude Sonnet) label re-judge, label-only
uv run python auditors.py --ds llm_v3 --variant orig   # default = all six views
uv run python hardset.py --ds llm_v3
uv run python final_analysis.py --split dev    # development only; the test headline runs ONLY via finalize_test.sh
uv run python evidence.py --split test         # evidence accuracy + prompt cost
uv run python auditors.py --ds llm_v3 --variant shuffle --shuffle-seed 0 --views text,combined,structured   # seeds 0,1,2
uv run python baselines.py --ds llm_v3 --learner lr --split test   # CV inside the split
uv run python textsim.py --split test           # untrained public-text convergence
uv run python report_tables.py --split test     # renders all REPORT tables from results/*.json
uv run python fig_mechanism.py --split all      # descriptive price paths by condition (no metric)
python3 -S check_mechanism_sources.py           # preserve existing figure/caption sources; no figure or detection rerun
uv run python fig_roc.py                        # test ROC + dev operating points (descriptive)
uv run python fig_summary.py                    # Figure 1 summary (reads existing results JSON only)
uv run python text_lr_inspect.py                # n-gram / firm-level text cue inspection (descriptive)
uv run python incremental.py --split test       # premium + LLM view rank-average (run by finalize_test.sh)
uv run python fp_stratum.py --ds llm_v3fp       # firm-framing exploration stratum
uv run python fp_prices.py                      # firm-framing vs lab none mean prices (descriptive)
uv run python monitor_stratum.py --ds llm_v3mon # announced-monitor stratum (frozen thresholds)
uv run python deterrence.py                     # agreement / message / markup comparison llm_v3 vs llm_v3mon
uv run python markup_baseline.py                # E70 post-hoc: comparison-free markup vs premium (test, rep, placebo)
uv run python matched_recall.py                 # legit/none flags at matched recall (post-lock, descriptive)
uv run python round1_effect.py --ds llm_v3      # round-1 (pre-message) prices by role (descriptive)
uv run python early_detection.py --ds llm_v3 && uv run python fig_early.py   # premium AUROC vs rounds observed
uv run python evidence_rounds.py --ds llm_v3 --split test   # do auditors cite round 1? (descriptive)
uv run python auditors.py --ds llm_v3 --views action_stats_hint && uv run python auditors.py --ds llm_v3rep --views action_stats_hint
uv run python hint_view.py                      # premium-hint auditor exploration (E56, post-lock)
uv run python auditors.py --ds llm_v3 --views action_stats_nolevel && uv run python auditors.py --ds llm_v3rep --views action_stats_nolevel
uv run python nolevel_view.py                   # level-column ablation of the stats table (E71, post-lock)
uv run python llm_market.py --ds llm_v3plc --match-ds llm_v3rep --rounds 12 --framing lab   # placebo channel (E58)
uv run python label_llm.py --ds llm_v3plc && uv run python auditors.py --ds llm_v3plc && uv run python placebo.py
uv run python replication.py                    # historical run-once command; now guarded by committed completion receipt
./finalize_test.sh                              # historical locked-test command; now guarded by committed completion receipt
uv run python auditors.py --ds llm_v3 --auditor claude-sonnet-5-5 --subset mod3   # cross-family subset
uv run python cross_family.py --ds llm_v3 --other claude-sonnet-5-5               # cross-family comparison
uv run python sim.py --dataset scripted_v2 --n-per-cond 40 --rounds 30 --seed 1 --levels 12,14 --strength 0.15,0.5
uv run python baselines.py --ds scripted_v2 --learner lr
```
