# Say vs. Do — appendix (v1 exploration strata and Appendices A–D)

*Moved verbatim from REPORT.md on 2026-10-24 (Phase 2, director directive: keep the main report short). Text and
numbers unchanged; references to "Appendix A–D" in REPORT.md point here.*

## v1 exploration strata (from §Results)

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



## P2-detail — full P2.5 and P2.6 text (moved from REPORT.md 2026-10-24 ~10:30 UTC for length; text unchanged, interim numbers as of 09:57 UTC)

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
memory (last 8 own notes vs 6 rounds of price history). A control is running (E92, registered with an amendment before any outcome): the same notepad structure, but
the entry must be invented weather, which is irrelevant to prices (`llm_p2logbook`, 15 matched seeds). Caveats: 15 seeds, with percentile bootstrap CIs that may be narrow at this n;
the equivalence check uses 95% CIs (conservative vs TOST); one seller model (paraphrase band and other families pending).
Label judge (gpt-6.1-sol, price-blind): explicit agreement in 14/15 private, 14/15 neutral and 15/15 random-partner
chats; all 15 placebo runs contain unilateral proposals from both firms. The notepad entries we inspected (2 runs) contain no
coordination language (e.g. llm_p2cue_0002: "Test a high-margin price while leaving room to adjust"). **Supervised text classifier** (P2.3 model, fit on llm_v3; each arm scored against the same 10 fresh llm_v3rep `none` runs; `p2_textlr.py`): private 1.00,
neutral 1.00, random partner 1.00, placebo 0.96 [0.87, 1.00], **notes 0.86 [0.70, 0.98]**, and this dataset's own `none` arm 0.40. It puts the
notepad pair on top in 14/15 runs. The public-text trace therefore also appears when the firms have no one to talk to.

**Wording band (E78, registered; `uv run python p2_band.py` → `results/analysis/p2_band.json`).** Three wordings of the
same seller prompt (same facts), on the same 10 matched seeds, private − none pair premium over rounds 2–12: original
+1.75 [+0.91, +2.66]; paraphrase 1 +1.79 [+1.20, +2.43]; **paraphrase 2 (terse, list-like) +0.24 [−0.32, +0.81]**.
Paraphrase 2 minus original: −1.51 [−2.33, −0.68]. Frozen premium flags, private vs none: 9/10 vs 2/10; 9/10 vs 0/10; 4/10 vs 2/10. The registered
prediction (premium survives both paraphrases) **failed** for paraphrase 2. Two things change. (i) *Agreement content:* the
judge labels all 10 paraphrase-2 chats "explicit", but this does not establish unchanged mutual agreements (some
evidence combines conflicting proposals, e.g. 0004: 18 vs 12, or matching plans qualified by "choose independently"). Also the highest price named in the pair's round-1
messages is ≥ 17 in 7/10 pairs (original 10/10, paraphrase 1 9/10; json key `opening_proposal_per_pair`). By our reading
of the judge's evidence quotes (`data/llm_p2para2/labels.jsonl`), 5/10 agreements are on ~12, close to static Nash
(11), e.g. llm_p2para2_0008 "Let's start at 12". (ii) *Others' prices:* non-pair firms price higher (rounds 2–12: 14.0 vs 13.4),
and no-channel markets sit at 13.2 vs 12.1. The pair's round-1 price is 15.3 vs 17.1, and the round-1 premium is +1.9 [+0.1, +3.9]
vs +5.1 [+4.2, +5.9] (json key `pair_vs_others_price`). **Reading:** prompt wording changes the size of the premium,
through the pair's prices, the other firms' prices and the no-channel baseline all at once. With n = 10 and uncertain
agreement labels we cannot attribute the drop specifically to weaker follow-through on agreements. But the binary judge
label stays at 10/10 while the price contrast shrinks, so "agreement in chat" and "premium" measure different things.



**P2.6 Other seller families (E79 + amendments, registered before generation; E90 descriptive; `uv run python p2_cue.py
--ds llm_p2claude && uv run python p2_family.py` → `results/analysis/p2_cue_llm_p2claude.json`, `p2_family.json`).
Pilot: Claude Sonnet 5.5 is done (5 matched seeds × private/none). gpt-6.1-sol (same vendor as luna, so not
cross-family) and deepseek-v4.1-flash (Go) are still running.** At the costs used, static Nash ≈ 11 and joint monopoly ≈ 19.

| sellers (seeds) | market price r2–12, `none` | market price r2–12, private | pair premium private − none (r2–12) | frozen premium flags private / none | premium run AUROC |
|---|---|---|---|---|---|
| gpt-6-luna (llm_p2cue, 15) | 11.94 [11.56, 12.31] | 13.96 [13.39, 14.54] | +1.61 [+0.92, +2.35] | 14/15 / 2/15 | 0.91 [0.79, 1.00] |
| gpt-6-luna, same 5 seeds as Claude | — | — | — | 4/5 / 2/5 | — |
| Claude Sonnet 5.5 (llm_p2claude, 5) | 20.19 [19.66, 20.63] | 21.64 [20.72, 22.57] | +0.58 [+0.23, +1.03] | 2/5 / 0/5 | 0.70 [0.32, 1.00] |
| deepseek-v4.1-flash (llm_p2ds, **interim** 10 of 15) | 17.04 [16.27, 17.78] | 19.91 [19.11, 20.59] | +2.05 [+0.81, +3.26] | 7/10 / 4/10 | 0.75 [0.46, 1.00] |
| gpt-6.1-sol (llm_p2sol, **interim** 4 of 7) | 15.25 [14.52, 15.98] | 15.50 [14.69, 16.31] | −0.14 [−0.58, +0.19] | 2/4 / 1/4 (placebo 2/4) | 0.63 [0.19, 1.00] |

**Interim: deepseek and gpt-6.1-sol (E93, post-hoc, descriptive, no decisions; `uv run python p2_interim.py --ds llm_p2ds
llm_p2sol` → `results/analysis/interim/`; complete matched seeds only, final numbers replace these when generation ends).**
These descriptive interim samples pose opposite problems for luna-calibrated detectors; transfer performance is unresolved. *deepseek sellers invite coordination openly in both arms.* Every
private chat (10/10) proposes joint pricing ("let's cooperate: both price at 22 … I'll avoid undercutting if you do").
A regex screen also finds such invitations in 479/480 *public* messages of no-channel markets (480/480 with the channel;
Claude 240/240; luna 7/720, mostly non-invitations such as "We welcome steady business from everyone"). No-channel
markets already price at 17.0 (luna `none` on the same 10 seeds: 12.1). The channel still adds a pair premium (+2.05)
and raises the market price (+2.9). But the luna-calibrated threshold flags 4/10 no-channel markets: the run score is
the max premium over all 6 firm pairs (a plausible but untested mechanism: deepseek firm prices are more spread out); run AUROC 0.75 [0.46, 1.00].
*In the four completed gpt-6.1-sol private runs, no explicit joint-pricing proposal was observed.* sol pairs send a private message every round (96/96), but the
content is about pricing independently ("I will assess demand and customer response this round"). Regex: 0/96 joint-pricing
phrases; a 1–2 digit number appears in 4/96, e.g. disclosing an opening price; public invitations 0/576. The premium estimate is
−0.14 [−0.58, +0.19]; this small sample neither establishes a zero effect nor validates channel presence as a collusion label. Regex screens are descriptive; the sol
judge labels and frozen auditor views (E91-ext, registered) come with the final run. **Reading:** whether there is
collusion to detect, and whether a no-channel market is a clean negative, depend on the seller model. For 2 of 4
families the control arm's public messages already contain open invitations to coordinate (auditors so far run on
Claude only, where every message-reading view flags all 10 markets).

**Reading (n = 5 pairs, descriptive).** Claude sellers price at or above the joint-monopoly level from round 1, even
with no channel: round-1 no-channel prices are 18–22, set before any rival price has been seen, and the market mean over rounds 2–12 is 20.2
(luna `none` markets: 11.9, 0/15 at ≥ 19). This is *above* the industry profit-maximising price. All four firms at 19 earn
850 in total, at 22 they earn 755. It also leaves a large unilateral gain unused (best reply to rivals at 20 is 14, earning 352 vs 208). We therefore read it
as mainly a high-price disposition of this model, not learned tacit collusion. But the no-channel Claude markets are not clean
negatives either. Their *public* messages openly urge rivals not to undercut (llm_p2claude_0003, round 6, all four firms: "Let's keep avoiding
undercutting"). In some markets one firm undercuts in the final round (0003: A drops 20 → 15), and some drift down to 18 by round 12. With the channel, all 5 pairs state a price of 20–24 in round 1–2 and stay within 1 of it in ≥ 90% of later rounds.
Applying the same floor to the matched no-channel pair gives 0.0, 0.0, 0.0 and 0.27 of rounds for four seeds and 0.91 for one (floor 20). So in 4 of 5 seeds the chat moved the pair above
what the same model does unprompted. Because the other two firms also price high, the pair premium is small (+0.58; markup private − none
+1.46 [+0.49, +2.42]) and the frozen premium flags 2/5. The luna-trained public-text classifier scores the Claude private runs at 0.64 [0.24, 1.00] vs Claude `none`
(1.00 on luna's own arms). **With n = 5 we find no evidence that either detector transfers to Claude sellers (both CIs include chance).** On the same 5 seeds, luna's premium flags 4/5 vs 2/5. That gap is not resolved at this n. Absolute price levels
would flag every Claude market, including all 5 no-channel ones (cf. Q1.4 P2.3: absolute statistics need model-matched references).
**Frozen LLM auditors on the Claude markets (E91, registered; 60 gpt-6.1-sol calls, unchanged prompts; `uv run python
p2_family_views.py` → `results/analysis/p2_family_views.json`).** Flags private / none at the frozen dev thresholds: text 5/5 / 5/5,
combined 5/5 / 5/5, combined_stats 5/5 / 5/5, structured 5/5 / 5/5, action_stats 3/5 / 3/5, action 2/5 / 2/5. Every view that reads messages
flags every Claude market with score ≈ 96–98, because the public messages contain the invitations quoted above. Run AUROC private vs none: action_stats 0.70 [0.30, 1.00],
action 0.52, text 0.22. On this family the text-vs-action question turns on the label. If public invitations to
avoid undercutting count as collusion, the text auditor is right on all 10 markets. Under our condition label (channel or not), no view
separates the arms. Registered prediction (action views flag the kept 20–24 agreements more often than the premium, 2/5): **held weakly**, action_stats 3/5, but it flags 3/5 no-channel markets too.
Prediction "text view near chance" **failed**: it flags everything.

