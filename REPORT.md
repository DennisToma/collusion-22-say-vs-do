# Say vs. Do: does auditing what AI agents *say* together with what they *do* catch collusion better?

*Apart AI Collusion Sprint, Q2.2 — text + action auditing. Status: DRAFT, results accumulating (see STATUS.md).*

## Abstract (draft)
We build a 4-firm repeated-pricing market populated by LLM sellers (gpt-6-luna) in which one designated pair
may get a private channel. Sellers are never told to collude — they only get a profit objective and, in the
`private` condition, the opportunity. Auditors (gpt-6.1-sol) see only the observable log and score each of the
six firm pairs, under four views: public text only, actions only, both, and both + computed statistics
("structured"). We measure whether the hybrid views beat the best single modality (Δ_hybrid), and whether any gain
comes from cross-modal consistency checking (message↔action shuffle ablation). Final numbers: pending.

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

### LLM market (headline) — interim, n = 36 of 125 runs (NOT final; CIs wide)
Snapshot 21:50 UTC, `uv run python analyze_llm.py --ds llm_v3` → `results/analysis/llm_v3_gpt-6.1-sol_orig.json`
(24 positive runs: 23 explicit private agreements + 1 info-exchange; 12 negatives: 6 `none`, 6 `legit`).

**Public text is innocuous.** `hardset.py` (keyword list + a gpt-6-luna check of every public message) flags
**0 / 32** checked runs for explicit coordination language in public — the LLM sellers keep coordination entirely
in the private channel. So the whole LLM set is the "hard" set; an "easy" set does not occur naturally here.

**Actions carry the signal.** Assigned private pairs price on average +1.84 above the other two firms
(other pairs −0.37; `none`/`legit` assigned pairs ≈ 0), with more lockstep (51% equal-price rounds vs 34%).

LLM auditor (gpt-6.1-sol, zero-shot), run-level and pair-level AUROC [95% bootstrap CI, 500 resamples]:

| view | run AUROC | pair AUROC | pair-ID acc (positives) | mean prompt chars |
|---|---|---|---|---|
| text | 0.46 [0.30, 0.63] | 0.58 [0.48, 0.69] | 0.35 | 9.3k |
| action | 0.65 [0.43, 0.83] | 0.78 [0.66, 0.88] | 0.51 | 3.2k |
| combined | 0.74 [0.53, 0.91] | 0.76 [0.66, 0.85] | 0.50 | 11.4k |
| structured | 0.73 [0.54, 0.89] | 0.86 [0.77, 0.94] | 0.67 | 12.0k |

Δ_structured (pair) = +0.086 [+0.006, +0.171] (paired bootstrap, P(Δ≤0)=0.014); Δ_combined (pair) = −0.014
[−0.066, +0.034]; Δ_combined (run) = +0.094 [−0.018, +0.238]. Text-only is at chance.
Open question this raises: is the structured gain from *cross-modal* reasoning or simply from the computed
price statistics? → new ablation view `action_stats` (actions + pair statistics, no text) is being audited.

Supervised non-LLM baselines (`baselines.py --ds llm_v3 --learner lr`, 5-fold grouped CV, same 36 runs):
pair AUROC text 0.82 [0.77, 0.88], action 0.99 [0.97, 1.00], combined 0.99, structured 0.99; Δ ≈ 0 (ceiling).
A simple *trained* classifier on price statistics far outperforms the zero-shot LLM reading raw price tables
(not a like-for-like comparison: the LR sees in-distribution labels). The text LR beats chance while the LLM
text auditor does not; its top-weighted n-grams show why: negatives are partly the `legit` pairs announcing
their "shipping partnership", positives use margin-flavoured wording ("sustainable price", "considered price",
"margins", "balances") — a weak stylistic tell of the private agreement that a zero-shot auditor does not exploit.

## Validity safeguards
Labels from private chat only (judge blind to prices); same auditor model across views, fallback calls dropped;
combined is a strict superset of both single views; shuffle donors matched on label *and* condition;
hard set excludes runs with explicit coordination language in public text; cross-family auditor (Claude) on
a stratified subset (planned); adversarial methodology review by gpt-6.1-sol (`logs/review_methodology.md`,
12 issues; fixes applied: label leakage, view superset, public partnership info, parse strictness, learner parity,
resume ids, donor matching).

## Held-out discipline
`data/SPLITS.md`: dev = llm_v3_0000–0029, locked test = 0030–0124. The auditor prompt was written before any
LLM-market data and has not been tuned (0 tuning attempts), so headline = all runs; test-only reported alongside.

## Limitations (so far)
Single seller model family (GPT) and single framing for headline data; 12 rounds; agreement labels from one
LLM judge (spot-checked manually on pilots only).

## Reproduce
```
uv run python llm_market.py --ds llm_v3 --plan private:70,none:35,legit:20 --rounds 12 --framing lab --games-parallel 2 --seed 3000
uv run python label_llm.py --ds llm_v3
uv run python auditors.py --ds llm_v3 --views text,action,combined,structured --variant orig
uv run python hardset.py --ds llm_v3
uv run python analyze_llm.py --ds llm_v3            # --split dev|test, see data/SPLITS.md
uv run python baselines.py --ds llm_v3 --learner lr
uv run python auditors.py --ds llm_v3 --auditor claude-sonnet-5-5 --subset mod3   # cross-family subset
uv run python sim.py --dataset scripted_v2 --n-per-cond 40 --rounds 30 --seed 1 --levels 12,14 --strength 0.15,0.5
uv run python baselines.py --ds scripted_v2 --learner lr
```
