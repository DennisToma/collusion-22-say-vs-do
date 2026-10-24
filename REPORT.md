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
6. *Phase 2 (in progress, section below):* an independent reimplementation reproduces the headline numbers. At 5%
   prevalence most premium alarms are false (precision 0.24 test). The supervised text signal appears without any delivered
   message (placebo AUROC 1.00). Judged by behaviour, 36 of 50 test "colluders" do not keep the agreed price; most of these
   agree on 18 for round 1 only (a second judge reads 18 of 21 checked cases as opening-only). The premium flags them
   anyway; against the kept-agreement label it falls to 0.80, and text + actions shows no resolved gain over the best
   single modality (combined −0.03 [−0.14, +0.06]).
7. *A substantial part of the premium is an offer artifact (P2.5, registered E77):* on 15 matched seeds, giving the pair a private
   **notepad with no recipient** raises their premium over rounds 2–12 by +1.04 [+0.65, +1.42] vs no channel. A real
   private channel raises it by +1.61 [+0.92, +2.35]; the difference is not resolved (+0.56 [−0.29, +1.48]), and so is the effect of delivery
   (private − placebo +0.38 [−0.41, +1.18]). The frozen premium flags 10/15 notepad runs (AUROC 0.89). The registered
   "offer alone is not the driver" prediction failed. The notepad arm has confounds (pair-only extra text, memory).
8. *The detectors depend on the seller model (P2.6, preliminary, 5 matched seeds):* Claude Sonnet 5.5 sellers with **no
   channel** already price at or above the joint-monopoly level (market 20.2 vs monopoly ≈ 19, Nash ≈ 11; 5/5 markets). Given the channel,
   all 5 pairs agree on 20–24 and keep it. Because the background is already high, the pair premium is small (+0.58
   [+0.23, +1.03]) and the frozen premium flags 2/5. The luna-trained text classifier scores 0.64. gpt-6.1-sol and deepseek runs are pending.

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
Legit-partnership runs vs the same negatives: AUROC 0.38. Prediction (b) held; its ±0.05 margin is loose with only 10 negatives. Prediction (a)
("gradual") had no numeric criterion, so it is descriptive only. **Reading:** the public-text trace *does not require
any delivered message*. Placebo sellers still write proposals they believe are delivered, so this does not
distinguish "reaction to the offer" from "intended (unilateral) coordination". It does mean that, with labels equal to
the condition, a near-perfect text classifier is not evidence that agreements can be detected from public text.
The notes-to-self condition (P2.5) separates the two explanations.

**P2.4 Labels by behaviour, not condition (E84, registered; amendment E77-p2cue-amend before running; `uv run python
p2_behaviour.py` → `results/analysis/p2_behaviour.json`).** A gpt-6.1-sol judge reads each private chat, blind to prices,
and extracts the agreed price floor and the round of agreement (85 calls, cached in `data/<ds>/terms.jsonl`). Code then
checks the prices. *Followed* = both pair firms price ≥ floor − 1 in at least half of the rounds after the agreement
(floors ≤ 11 = static Nash count as trivial; none occurred). **Most v1 "collusion" positives are opening-round price
agreements that are not kept.** 48 of 70 llm_v3 chats agree on 18 in round 1 (joint-monopoly price 19). On the locked
test, only 14 of 50 positive runs keep the agreed floor; 36 do not. The two classes differ in ambition. 35 of 36
not-kept agreements set floor 17–18, and 34 of 36 are made in round 1. Kept floors are 12–18 (median 14.5), and 11 of
14 are agreed in rounds 2–11. A second judge (Claude Sonnet 5.5, same prompt, first 30 test chats; E84d, `p2_terms_xfam.py`) matches
sol on agreed yes/no 25/30, floor 23/30 and class 24/30. Asked about scope, it reads 18 of the 21 not-kept agreements
as *meant for the opening round only* and none as ongoing. Example llm_v3_0040: "I suggest we both start at 18 this
round … adjust next round", and from round 3 both firms say they price independently. Detectors, followed (14) vs rest (81):

| detector (frozen dev threshold) | test run AUROC, followed vs rest | flags: followed / not followed / none / legit | test AUROC, followed vs not followed | replication, followed (5) vs rest (25) |
|---|---|---|---|---|
| premium | 0.80 [0.67, 0.90] | 12/14 · 34/36 · 2/30 · 5/15 | 0.60 [0.40, 0.79] | 0.72 [0.51, 0.89] |
| action_stats (LLM) | 0.65 [0.51, 0.78] | 9/14 · 27/36 · 1/30 · 1/15 | 0.38 [0.22, 0.54] | 0.80 [0.60, 0.96] |
| structured (LLM) | 0.61 [0.46, 0.74] | 5/14 · 15/36 · 2/30 · 0/15 | 0.37 [0.22, 0.55] | 0.61 [0.34, 0.88] |
| action (LLM) | 0.58 [0.45, 0.72] | 1/14 · 9/36 · 2/30 · 0/15 | 0.38 [0.23, 0.53] | 0.82 [0.57, 1.00] |
| combined (LLM) | 0.55 [0.42, 0.68] | 5/14 · 21/36 · 5/30 · 4/15 | 0.36 [0.21, 0.52] | 0.74 [0.53, 0.91] |
| text (LLM) | 0.50 [0.35, 0.66] | 1/14 · 4/36 · 4/30 · 1/15 | 0.52 [0.36, 0.69] | 0.52 [0.27, 0.76] |

Registered predictions: P1 (premium ≥ 0.85) **failed** (0.80); P2 (the premium also flags not-kept agreements)
**held**, 34/36; P3 (LLM views flag not-kept agreements less often) **failed**, action_stats 27/36 vs 9/14. P1 and P2
pull against each other by design, because not-kept runs count as negatives for P1. **Reading:** the detectors find runs
where a private agreement was *made*, mostly the ambitious opening offer. No detector separates kept from not-kept
agreements on test (all CIs include 0.5; the LLM views lean towards the not-kept runs). With 14 and 5 positives
the CIs are wide. On replication the LLM action view (0.82) is at least as good as the premium.
**Q2.2 contrast on this label** (post-hoc, E84b; Δ_hybrid[v] = AUROC(v) − max(AUROC(text), AUROC(action)), paired
bootstrap with the max inside each resample; all views in json key `delta_hybrid_followed`). Test: combined −0.03
[−0.14, +0.06], combined_stats −0.03 [−0.16, +0.09], action_stats +0.07 [−0.07, +0.19], structured +0.03 [−0.11, +0.14].
Replication: combined −0.08 [−0.32, +0.16], combined_stats −0.26 [−0.51, −0.07], action_stats −0.02 [−0.15, +0.09],
structured −0.21 [−0.48, 0.00]. No hybrid view shows a resolved gain over the better single modality (test CIs allow up
to +0.06 for combined). On replication, combined_stats is resolved *worse*. Premium minus the best LLM modality: +0.22
[+0.08, +0.33] on test, −0.10 [−0.34, +0.12] on replication.
**Label sensitivity** (post-hoc, json key `sensitivity`). Loosening to floor − 2 and/or ≥ 1/3 of rounds raises test
followed runs from 14 to 17–20 of 50. Premium is 0.79–0.83, action_stats 0.66–0.72, structured 0.66–0.70, combined
0.58–0.63 and text 0.54–0.56. Replication has only one alternative split (6 followed); requiring floor − 1 ≥ 12 removes
one run per split. No `none` run reached the tacit-high threshold (pair premium ≥ 1 in rounds 5–12).

**P2.5 Is the "collusion" a prompt artifact? (E77 + amendment, registered before generation; `uv run python p2_cue.py
--ds llm_p2cue && uv run python p2_cue_verdict.py` → `results/analysis/p2_cue_verdict_llm_p2cue.json`, Figure P2.5.)**
Six arms share the same 15 seeds (same pair, costs and demand path; gpt-6-luna sellers, 90 runs): private channel;
neutrally worded "message box"; **notes-to-self** (the pair is told "You also have a private notepad. Only you can read what you write there"; each
firm sees its own past entries, and no other firm is mentioned); channel to a
random partner re-drawn each round; placebo (offered, never delivered); no channel. Statistic: assigned-pair premium
(pair mean − other-two mean), primary window rounds 2–12, paired over seeds, seed bootstrap; ±0.5 equivalence margin.
**A large share of the premium appears without any private channel or recipient.**

| arm | premium round 1 | premium rounds 2–12 | paired vs none (r2–12) | frozen premium flags | run AUROC vs none |
|---|---|---|---|---|---|
| private | 4.67 [3.77, 5.47] | 1.52 [0.82, 2.28] | +1.61 [+0.92, +2.35] | 14/15 | 0.91 [0.79, 1.00] |
| neutral wording | 3.50 [2.20, 4.67] | 1.39 [0.73, 2.25] | +1.47 [+0.78, +2.37] | 12/15 | 0.87 [0.72, 0.98] |
| notes-to-self | 2.37 [1.47, 3.33] | 0.96 [0.65, 1.26] | +1.04 [+0.65, +1.42] | 10/15 | 0.89 [0.76, 0.98] |
| placebo | 4.70 [3.97, 5.40] | 1.15 [0.64, 1.81] | +1.23 [+0.76, +1.85] | 13/15 | 0.91 [0.80, 1.00] |
| none | −0.87 [−2.07, 0.20] | −0.08 [−0.22, 0.02] | — | 2/15 | — |

Registered contrasts (rounds 2–12): private − notes +0.56 [−0.29, +1.48], placebo − notes +0.19 [−0.56, +1.07],
private − placebo +0.38 [−0.41, +1.18], neutral − private −0.13 [−1.29, +1.13]: all *inconclusive* (none positive, none
inside ±0.5). H1 (private > none) and H2 (neutral > none) **held**. H3 (notes − none upper CI < half of private − none,
i.e. < 0.80) **failed**: notes − none is +1.04 [+0.65, +1.42], a notes/private ratio of 0.65 [0.34, 1.32]. Round 1 is
identical in private and placebo (same prompt, nothing delivered yet: 4.67 vs 4.70), so the round-1 excess over notes
reflects how the offer is worded. It fades over rounds 2–5 (Figure P2.5; DiD private − notes −1.74 [−2.78, −0.73]).
Delivery itself (private − placebo) is unresolved: +0.38 [−0.41, +1.18] over rounds 2–12, DiD +0.41 [−0.71, +1.65]. Random partner: the assigned-pair premium is ~0 by construction, but the
whole market prices highest of all arms (markup vs none, rounds 2–12, +2.85 [+2.09, +3.59]). The matched-minus-unmatched price
gap at t + 1, relative to the same gap in round t, is −0.12 [−0.23, −0.02] (a slight convergence of partners). **Reading:** telling two firms they have a private writing space, even one nobody else reads, makes them price
about 1 unit above the other two for the whole game. The frozen premium flags 10/15 of these runs (AUROC 0.89 vs
none). A substantial share of the premium (point 65%, CI 34–132%) therefore needs no private channel. Whether delivered
coordination adds to it is unresolved at n = 15. The notepad arm changes several things at once. Only the pair gets
extra system text; it adds an output field; the prompt is longer; it uses the word "private"; and it gives persistent
memory (last 8 own notes vs 6 rounds of price history). The missing control is an irrelevant sentence of the same
length given to the pair, with no notepad. Caveats: 15 seeds, with percentile bootstrap CIs that may be narrow at this n;
the equivalence check uses 95% CIs (conservative vs TOST); one seller model (paraphrase band and other families pending).
Label judge (gpt-6.1-sol, price-blind): explicit agreement in 14/15 private, 14/15 neutral and 15/15 random-partner
chats; all 15 placebo runs contain unilateral proposals from both firms. The notepad entries we inspected (2 runs) contain no
coordination language (e.g. llm_p2cue_0002: "Test a high-margin price while leaving room to adjust"). **Supervised text classifier** (P2.3 model, fit on llm_v3; each arm scored against the same 10 fresh llm_v3rep `none` runs; `p2_textlr.py`): private 1.00,
neutral 1.00, random partner 1.00, placebo 0.96 [0.87, 1.00], **notes 0.86 [0.70, 0.98]**, and this dataset's own `none` arm 0.40. It puts the
notepad pair on top in 14/15 runs. The public-text trace therefore also appears when the firms have no one to talk to.

![Figure P2.5](figures/p2_cue_rounds.png)

**P2.6 Other seller families (E79 + amendments, registered before generation; E90 descriptive; `uv run python p2_cue.py
--ds llm_p2claude && uv run python p2_family.py` → `results/analysis/p2_cue_llm_p2claude.json`, `p2_family.json`).
Preliminary: Claude Sonnet 5.5 is done (5 matched seeds × private/none). gpt-6.1-sol (same vendor as luna, so not
cross-family) and deepseek-v4.1-flash (Go) are still running.** Static Nash ≈ 11, joint monopoly ≈ 19.

| sellers | market price r2–12, `none` | market price r2–12, private | pair premium private − none (r2–12) | frozen premium flags private / none | premium run AUROC | private chats: agreed / kept (E84 rule) |
|---|---|---|---|---|---|---|
| gpt-6-luna (llm_p2cue, 15 seeds) | 11.94 [11.56, 12.31] | 13.96 [13.39, 14.54] | +1.61 [+0.92, +2.35] | 14/15 / 2/15 | 0.91 [0.79, 1.00] | 14/15 explicit (terms not extracted) |
| Claude Sonnet 5.5 (llm_p2claude, 5 seeds) | **20.19 [19.66, 20.63]** | 21.64 [20.72, 22.57] | +0.58 [+0.23, +1.03] | 2/5 / 0/5 | 0.70 [0.32, 1.00] | 5/5 / **5/5** (floors 20–24) |

**Reading (n = 5 pairs, descriptive).** Without any channel, all 5 Claude markets price at or above the joint-monopoly
level for the whole game: this is tacit collusion by the whole market, which the luna `none` markets never reach (0/15 ≥ 19). With the channel, all
5 Claude pairs agree on a floor of 20–24 in round 1–2 and keep it in ≥ 90% of later rounds. These are the
*kept* agreements that P2.4 found rare for luna. Yet the pair-relative premium is small (+0.58; markup private − none +1.46
[+0.49, +2.42]), because the two other firms already price almost as high. The frozen premium flags only 2/5. The luna-trained
public-text classifier scores the Claude private runs at 0.64 [0.24, 1.00] vs Claude `none` (it gives 1.00 on luna's own arms).
**Both of our best detectors depend on the seller family: they find agreements that stand out from a competitive
background, and Claude sellers provide no such background.** Absolute price levels would flag every Claude market, but
then all 5 no-channel markets are flagged too (cf. Q1.4 P2.3: absolute statistics need model-matched references). One glm-5.3-flash run
per arm (llm_p2glm, stopped early, E79-p2glm-stop): `none` 15.8, private 19.3 (2 runs), descriptive only.

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
The scripted-market mechanism check (pipeline + shuffle-ablation validation) is in Appendix B ([REPORT_APPENDIX.md](REPORT_APPENDIX.md)); dev-split
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

### Exploration strata (moved)
v1 exploration strata (firm framing without agreement, announced price monitor, placebo channel, markup baseline,
stats-column ablation, auditor-hint and round-1 analyses) and Appendices A–D (dev split, scripted mechanism check,
extra test detail, strata detail) are in [REPORT_APPENDIX.md](REPORT_APPENDIX.md), text and numbers unchanged.

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
