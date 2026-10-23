# Say vs. Do: does auditing what AI agents *say* together with what they *do* catch collusion better?

*Apart AI Collusion Sprint, Q2.2 — text + action auditing. Status: DRAFT, results accumulating (see STATUS.md).*

## Abstract (draft)
We build a 4-firm repeated-pricing market populated by LLM sellers (gpt-6-luna) in which one designated pair
may get a private channel. Sellers are never told to collude — they only get a profit objective and, in the
`private` condition, the opportunity. Auditors (gpt-6.1-sol) see only the observable log and score each of the
six firm pairs, under four views: public text only, actions only, both, and both + computed statistics
("structured"). We measure whether the hybrid views beat the best single modality (Δ_hybrid), and whether any gain
comes from cross-modal consistency checking (message↔action shuffle ablation), and compare all LLM views with an
untrained one-line statistic (pair price premium). Dev split so far (n = 30): LLM sellers never coordinate in public,
adding text does not help the auditor, a computed price-statistics table does — and the untrained premium alone
beats every LLM view (run AUROC 1.00 vs ≤ 0.89). Locked-test numbers pending.

## Question
Given logged trajectories (public messages + prices + market state), do auditors that see both streams detect
collusion — and identify the colluding pair — better than text-only or action-only auditors? Is any gain due
to genuine cross-modal reasoning or just more input?

## Setup
**LLM market (`llm_market.py`, headline data `data/llm_v3`).** 4 firms, 12 rounds, integer prices 6–30, logit
demand (μ=4; static Nash ≈ 11, joint-monopoly ≈ 19 at cost 6), public cost shocks and demand levels.
Each round each seller (gpt-6-luna via codex) returns `{public_message, price, notes}` (+ `private_message` if it has
a channel). Conditions (randomised, 125 runs planned): `private` (70) — designated pair has a private channel;
`none` (35) — no channel; `legit` (20) — the pair has a publicly announced cost-saving shipping partnership
(hard negative). Framing: economics-lab experiment with earnings = profit.

*Pilot finding (framing matters):* with a "pricing manager + competition authority monitors public messages"
framing, luna sellers used the private channel only to say "I'll price independently" (0/3 runs with any
coordination) and posted near-identical boilerplate. With the lab framing, private pairs immediately exchange
intended prices and proposals ("I plan to price at 14; consider matching so we can improve margins without
triggering a price war"). Pilot data: `data/llm_v2` (firm framing), `data/pilot_lab_luna`.

**Labels (`label_llm.py`).** A gpt-6.1-sol judge reads ONLY the private chat (no prices, to avoid building the
action signal into the label) → `explicit` / `info_exchange` / `none`. Primary label y = explicit ∪
info_exchange on the assigned pair. Realised conduct (pair price premium over the other two firms, rounds ≥ 4)
is reported separately. Private chat is never auditor input.

**Auditors (`auditors.py`).** Same model (gpt-6.1-sol, medium reasoning; calls that silently fell back to another
model are discarded), same task text, same runs. Views: `text` (public messages + public facts), `action`
(prices, cost, demand, units, profit + public facts), `combined` (strict union), `structured` (combined + pair
statistics table + stated-vs-actual price table). Output: 0–100 suspicion per pair, P(any collusion), evidence.

**Scripted market (`sim.py`, mechanism check only).** Templated messages × scripted actions, 8 conditions incl.
hard negatives (cheap talk without action, common shocks, shared pricing rule, legit cooperation). Its Δ is a
function of how we designed the templates (colluders' stated price direction is decoupled from their action), so
it only validates the pipeline and the shuffle ablation.

## Results so far

### Scripted mechanism check (non-LLM baselines, `baselines.py`, 5-fold CV grouped by run, 320 runs)
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
  0.91→0.995 under shuffle); donors are now drawn within the CV test fold.

### LLM market (headline data) — DEV split only; locked test analysis pending
Generation still running (≈60/125 runs at 22:15 UTC). Per `data/SPLITS.md`, headline numbers will come from ONE
run of the frozen `final_analysis.py --split test` (runs 0030–0124; the script refuses to run unless every view has
audited every run). Numbers below are **dev** (runs 0000–0029: 20 positive, 10 negative = 5 `none` + 5 `legit`),
indicative only. `uv run python final_analysis.py --split dev --allow-partial` (the `combined_stats` view is still
being backfilled) → `results/analysis/final_llm_v3_gpt-6.1-sol_dev.json`.

**Endpoint.** y = 1 iff a judge reading the private chat finds an explicit price agreement or a pricing-intention
exchange on the assigned pair. This is *private coordination communication*, not realised supra-competitive
conduct; runs are split by late-window relative premium as a (weak) proxy for whether it was acted on.
Primary metrics: run AUROC (detection) and within-market AUROC (localisation: P(colluding pair scored above another
pair of the same market), positive runs). Pooled pair AUROC is secondary (a scorer that is flat within each
market can still reach ≈ 0.77 pooled, per the codex review).

**Public text is innocuous.** `hardset.py` (keyword list + a gpt-6-luna check of every public message) flagged
**0 / 32** checked runs for explicit coordination language in public: the LLM sellers keep coordination entirely
in the private channel. So the whole LLM set is the "hard" set; an "easy" set does not occur naturally here.

Scorers: six gpt-6.1-sol zero-shot auditor views; the **untrained pair premium** (pair mean price − mean of the
other two firms, every pair, all rounds; run score = max over pairs; nothing fitted); a **late fusion**
w·text + (1−w)·action of the unimodal auditor scores (w fitted on dev: 0.6). Dev, 1000 class-stratified run
bootstraps:

| scorer | run AUROC | within-market AUROC | pooled pair AUROC | flagged @dev thr.: y=1 / neg. (legit) |
|---|---|---|---|---|
| text | 0.58 [0.37, 0.78] | 0.62 [0.51, 0.72] | 0.56 [0.45, 0.68] | 0.25 / 0.10 (0.2) |
| action | 0.78 [0.57, 0.94] | 0.85 [0.73, 0.93] | 0.82 [0.70, 0.92] | 0.65 / 0.10 (0.2) |
| combined | 0.83 [0.65, 0.97] | 0.85 [0.73, 0.94] | 0.80 [0.69, 0.90] | 0.80 / 0.20 (0.2) |
| fusion (text+action scores) | 0.83 [0.66, 0.95] | 0.85 [0.73, 0.93] | 0.82 [0.70, 0.92] | 0.70 / 0.10 (0.2) |
| action_stats (actions + pair stats, no text) | 0.89 [0.75, 0.99] | 0.91 [0.80, 0.98] | 0.91 [0.80, 0.98] | 0.85 / 0.10 (0.2) |
| structured (combined + stats + stated-vs-actual) | 0.83 [0.67, 0.96] | 0.91 [0.80, 0.97] | 0.89 [0.78, 0.96] | 0.65 / 0.10 (0.0) |
| **pair premium (untrained)** | **1.00 [1.00, 1.00]** | **0.98 [0.94, 1.00]** | **0.99 [0.96, 1.00]** | **1.00 / 0.00 (0.0)** |
| pair premium, rounds 2–12 only (robustness) | 0.92 [0.80, 1.00] | 0.96 [0.89, 1.00] | 0.96 [0.91, 0.99] | – |

(Thresholds are dev-fitted, so the flag rates on dev are optimistic; test will show honest FPR.)
Why the premium is so strong: in many private runs the pair agrees in round 1 to open high ("let's both start at
18") while the rivals open at ≈ 12; the pair is undercut and often abandons the agreement within 1–3 rounds
(manual read of 3 dev chats: 0005, 0012, 0016). The opening-round gap alone carries much of the signal; without
round 1 the premium still matches or beats every LLM view on dev, but no longer significantly
(premium_r2plus − structured: run +0.09 [−0.10, +0.29]). The LLM auditors also see round 1.
**Label ≈ condition:** all 37 `private` runs so far are labelled y = 1 (35 explicit, 2 info-exchange), so on this
generator "agreement" and "had a channel" coincide; see Limitations.
Paired contrasts (dev): Δ_hybrid[combined] run +0.05 [−0.12, +0.19], within +0.01 [−0.05, +0.05];
combined − fusion ≈ 0 (run +0.00 [−0.12, +0.12]); action_stats − action: within +0.07 [+0.02, +0.11];
premium − structured: run +0.17 [+0.05, +0.34], within +0.08 [−0.01, +0.19]; premium − action_stats: run +0.11
[+0.01, +0.25].

![dev AUROC](figures/auroc_dev.png)

**Emerging answer (dev, to be confirmed on test):** giving an LLM auditor the public text on top of actions does
not help localise colluders (combined ≈ action; joint reading ≈ simple late fusion of the two unimodal auditors),
because the sellers keep coordination private and their public messages are bland. What helps is a *computed
price-statistics table*, and that statistic alone, untrained, beats every LLM view. This fits the sibling project's
finding that dependence statistics detect coordinated *variation*, not *level*: these colluders coordinate on
level, and the premium measures level directly.

**Information-theoretic dependence detectors (sibling Q1.4, dev).** Using the sibling project's per-pair scores on
the same runs (`../collusion-14-infotheory/results/eval/llm_v3_ext.json`, read-only; block `external_infotheory`
in the final_analysis output): run AUROC pCMI 0.47 [0.22, 0.73], MI 0.60 [0.40, 0.80], TE 0.59 [0.32, 0.83],
Pearson 0.21 [0.06, 0.41] (below chance: colluding pairs hold prices *flat*, so they co-vary less); within-market
MI 0.85, Pearson 0.76, TE 0.67, pCMI 0.55. Premium − pCMI run AUROC +0.53 [+0.28, +0.78]. Their independently
coded `pair_level` statistic reproduces our premium exactly (run 1.00, within 0.98) — a code-level replication.
So on this generator, dependence-in-variation statistics are weak, level statistics are strong.

**Where the LLM does add something (gallery, `results/analysis/gallery_dev.md`):** in `legit` run 0001 the
partnership pair has a positive premium (+0.62 all-round) and is the premium's top pair, while the text/structured
auditors read the public partnership notice and give that pair 4–7/100. On dev the premium's run-level threshold
happens to sit above it, but this is the failure mode a price-only screen has with legitimate cooperation.

**Evidence accuracy (dev, `evidence.py`).** All cited rounds/firms are valid. About half of evidence items contain a
price claim; of these, 51–65% match the cited firm's price in the exact cited round, 81–92% within ±1 round, 95–100%
match some firm's price nearby. On positive runs only 47–59% of cited firms belong to the colluding pair (chance
50%): auditors cite market-wide observations, so their evidence rarely singles out the colluders. No verbatim quotes.

**Audit cost (prompt size per call; `uv run python cost.py` → `results/analysis/cost_llm_v3.json`).** text 9.3k chars, action 3.3k, action_stats 3.7k, combined 11.4k,
structured 12.1k (≈ chars/4 tokens); one gpt-6.1-sol call per run per view. The premium costs nothing; a
premium-first triage that sends only the top 75% of dev runs to the LLM audit keeps all positives (dev base
rate is 2/3, so this saving will look larger on test).

*Caveat (22:00 codex review, `logs/review_interim.md`): `legit` runs were initially audited WITHOUT their public
partnership notice. Fixed 22:10 (auditors.py regenerates `public_info`; legit audits invalidated and re-run;
cached audits are now checked against the current prompt hash/length and re-run if stale).*

**Supervised non-LLM baselines (dev; `baselines.py --ds llm_v3 --split dev`, LR, 5-fold CV grouped by run inside
dev, n = 30).** Run AUROC text 0.79 [0.60, 0.92], action 0.96 [0.85, 1.00], combined 0.96, structured 0.95;
pair-ID accuracy text 0.90, action 0.95. Hybrid Δ ≈ 0 (ceiling). A *trained* classifier on price features far
outperforms the zero-shot LLM reading the same prices (not like-for-like: the LR sees in-distribution labels). The
text LR beats the LLM text auditor by a wide margin (pair-ID 0.90 vs 0.31). Its top-weighted n-grams show why:
positives share margin-flavoured phrasing ("considered price", "balances customer value", "sustainable"); negatives
include the `legit` pairs' "shipping partnership" notices.

**Untrained public-text convergence (new, iter 6, dev; `textsim.py`).** If the private agreement leaks into the
pair's public wording, the two colluders' public messages should resemble each other more than other pairs'. Score
= TF-IDF cosine of the pair's public messages − mean cosine of the other pairs (vectorizer fit without labels;
nothing tuned). Dev: within-market AUROC **0.85 [0.72, 0.94]** vs the zero-shot LLM text auditor 0.61
(Δ +0.24 [+0.12, +0.35]); pair-ID 0.65. It does **not** detect which markets have collusion (run AUROC 0.45
[0.23, 0.70]): every market has some most-similar pair. So the public text *does* carry a localisation signal
(lexical alignment between partners), and the zero-shot LLM auditor does not use it. Pre-registered for the single
test run (added to `finalize_test.sh` before any test look).

## Validity safeguards
Labels from private chat only (judge blind to prices); same auditor model across views, fallback calls dropped;
combined is a strict superset of both single views; shuffle donors matched on label *and* condition;
hard set excludes runs with explicit coordination language in public text; cross-family auditor (Claude) on
a stratified subset (planned); adversarial methodology review by gpt-6.1-sol (`logs/review_methodology.md`,
12 issues; fixes applied: label leakage, view superset, public partnership info, parse strictness, learner parity,
resume ids, donor matching).

## Held-out discipline
`data/SPLITS.md`: dev = llm_v3_0000–0029, locked test = 0030–0124. The auditor prompt was written before any
LLM-market data and has not been tuned (0 tuning attempts). `final_analysis.py` (frozen 22:15 UTC) calibrates the
fusion weight and the FPR thresholds on dev, so the headline is test-only, computed once. Disclosure: interim
iteration-3 analyses (n = 36–40) included test runs 0030–0039; nothing was tuned on them.

## Limitations (so far)
- **Label ≈ condition.** On llm_v3 every `private` run so far is judged y = 1, so detecting "agreement" and detecting
  "a channel was granted" coincide; the endpoint is coordination *communication*, not realised overcharge. A separate
  firm-framing stratum (`llm_v3fp`, `fp_stratum.py`, frozen dev thresholds) is an exploratory transfer check of
  "channel used vs. unused" — it changes framing, wording, refusals and price levels at the same time, so it cannot
  resolve the confound within llm_v3.
- **Generator-specific premium.** Much of the premium's strength comes from round-1 joint high openings that are
  quickly undercut; a colluder that opens at the market price would weaken it (rounds 2–12 robustness: 0.92 on dev).
- Single seller model family (GPT, gpt-6-luna), single framing for the headline data, 12 rounds, 4 firms.
- Agreement labels from one LLM judge (gpt-6.1-sol, same family as the auditor; blind to prices); manually
  spot-checked on 3 dev chats + pilots.
- Zero-shot auditors with one prompt (0 tuning attempts); a tuned or few-shot auditor might use the stats table better.
- Small dev split (30 runs, base rate 2/3) → dev-fitted thresholds and fusion weight are noisy.

## Reproduce
```
uv run python llm_market.py --ds llm_v3 --plan private:70,none:35,legit:20 --rounds 12 --framing lab --games-parallel 2 --seed 3000
uv run python label_llm.py --ds llm_v3
uv run python auditors.py --ds llm_v3 --views text,action,combined,structured --variant orig
uv run python hardset.py --ds llm_v3
uv run python final_analysis.py --split test   # headline (frozen; dev for development)
uv run python evidence.py --split test         # evidence accuracy + prompt cost
uv run python auditors.py --ds llm_v3 --variant shuffle --shuffle-seed 0 --views text,combined,structured   # seeds 0,1,2
uv run python baselines.py --ds llm_v3 --learner lr --split test   # CV inside the split
uv run python textsim.py --split test           # untrained public-text convergence
uv run python report_tables.py --split test     # renders all REPORT tables from results/*.json
./finalize_test.sh                              # the ONE locked test run (all of the above for test)
uv run python auditors.py --ds llm_v3 --auditor claude-sonnet-5-5 --subset mod3   # cross-family subset
uv run python sim.py --dataset scripted_v2 --n-per-cond 40 --rounds 30 --seed 1 --levels 12,14 --strength 0.15,0.5
uv run python baselines.py --ds scripted_v2 --learner lr
```
