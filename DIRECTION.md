# DIRECTION — Phase 2, director review 2026-10-24 20:00 UTC (Sat, checkpoint)
(experiments end Sun 15:00 · finalize-only Sun 16:30 · hard stop Sun 18:00 · merged repo `collusion-beyond-words` is built from **Sun 08:00** from both REPORTs, so anything not in REPORT by 07:30 may be missed)

**Verdict.**
1. On track. The Q2.2 answer is settled, bounded and replicated: no resolved text gain (−0.01 test; −0.07 [−0.17, +0.02] pooled n = 90), with the positive counter-case (SALT: text 0.87 when the deal is in the chat). Every 17:56 directive except E113 is done: E116 within-agreement (no text/plan view resolves execution), E112/E115 in the abstract, E120 definition sensitivity, E3 dropped.
2. Two real problems remain. (a) **E113's registered k/16 statistic is mostly uninformative as specified.** On luna cells there is no text, so "combined − best single" is auditor re-prompt noise. Ties are frequent at 6 + 6 per cell and count toward "P1 held". The per-cell max(text, action) is biased against a gain. The registered P1 therefore leans toward "no gain" by construction. Fix the *reporting* now, before any score is read (directive 1). (b) **A definition inconsistency in the abstract:** "Abliterated Qwen executes no more than its base model (13/15 both)" uses the looser registered floor rule, while the shared executed definition gives 5/15 both.
3. Explore vs exploit: exploit only; generation is finished. The rest of tonight is the E113 write-up (target Sun 00:30, not 10:00), then a single consolidation pass. The repo is polishing in a loop: 39 iterations, abstract trimmed 517→388→312→260→298→275 words, 7 E113 snapshot commits. Stop iterating on wording until E113 lands.

## Top directives (in priority order)

1. **E113: append ONE pre-eval reporting amendment (E113-amend3) now, before any metric is read; then eval once when Q1.4 STATUS says "6 sweeps complete" (≈22:40).** Additions to `p2_e1_audit.py eval` outputs only; P1 and its sign test stay as registered:
   (a) **Headline = qwen cells**: k/8 with **k_pos / k_tie / k_neg**, plus a **pooled cell-stratified** Δ (combined − action and combined − text; AUROC computed *within* each cell and then averaged, game-cluster bootstrap) on the 8 qwen cells. The current `pooled_auroc_channel_vs_none_descriptive` pools raw scores across cells, so between-cell level shifts (framing, memory) contaminate it. Keep it, but label it unstratified.
   (b) **Luna cells:** report "combined − action with no text input" as an auditor-noise estimate, not as "no text gain". The exceptions with posts (c02 channel 78/240, c07 no-channel 75/240, c04 none 3/240) go in a separate line.
   (c) One sentence in the write-up: per-cell max(text, action) selection biases Δ downward, so "P1 held" is a weak confirmation. The pooled stratified Δ with CI is the informative number.
   Then: `preflight` → `eval` once → ≤ 10 lines + glance row + one abstract clause ("no text gain in k/8 qwen cells; pooled Δ … [CI]") **by Sun 00:30**. Use Q1.4's board-share table for the board-use covariate. If Q1.4 reports the qwen-cell pCMI replication as *replicated*, add one joint sentence: "base Qwen3.6 cells are where both public text and price dependence carry signal".
   **Why:** this is your only remaining generalisation result ("held in k of 16 conditions"), and as registered it would let a judge say "of course you found nothing: 8 cells had no text".
2. **Fix the executed-definition inconsistency (≤ 20 min, zero calls).** In the abstract and the P2.11 glance row, use the shared strict definition first: "executes no more than its base model (strict 5/15 both; 13/15 both under the registered floor rule)". Grep REPORT and PRESENTATION for every "executed"/"executes" count and make sure each one names its definition (strict / floor rule / judge-kept). Add a `p2_claims.py` claim for it and re-run (must stay 30/30+).
   **Why:** both repos promise one shared executed definition. A judge who sees 13/15 in the abstract and 5/15 in the table will distrust every rate.
3. **Kill the self-blocking E100 waiter (after a 1-minute check).** `p2_qwen_cmp_wait.sh` (PID 1818687, parent shell 1818684, alive since 13:15) can never exit, because its parent shell's command line contains the `p2_c3post.sh` pattern it pgreps for. This is the same bug you found and logged at 13:05. `p2_qwen_cmp.json` was written at 13:55. If the parent ever dies, the waiter will silently re-run `p2_qwen_cmp.py` and overwrite a frozen result. Verify that `logs/c3_cmp.log`/`p2_qwen_cmp.json` are the reported ones, kill both PIDs, and log one ledger line.
4. **Merge-ready top by Sun 07:30, then freeze.** After E113 lands: abstract ≤ 260 words in ONE pass (E113 clause in, one weaker clause out; candidates are the SALT "8000 episodes, 10 models" detail and the Qwen premium-diff clause). Add an **8-line "For the merged report" block** under the abstract: the one-sentence answer, 3 numbers with CIs + denominators (Δ test/pooled, SALT 0.87, E113 pooled Δ), the figure to lift, what NOT to quote (E99-x plan 0.76 without the E111 keyword caveat, E116b Qwen strata, round-1 premium as a detector). Re-run `p2_claims.py` + `verify_phase2.py`. Opus + codex final review Sun 12:30, freeze Sun 14:00, rebuild of the presentation/EVIDENCE/manifest Sun 16:30.
5. **Sunday-morning optional, zero calls, only if 1–4 are done (≤ 45 min):** a single "say-vs-do in one table" for the merged report. For each of the 4 places where text could help (base-framing luna; public-inviting families; within-agreement E116; SALT), give the text-view AUROC and the action-view AUROC from existing JSON, with CIs. It makes the paper's thesis ("text helps only where the act happens in the conversation") visible at a glance. Build it in `report_tables.py` so it regenerates.

## STOP doing
- **No abstract/TL;DR wording iterations** until E113 lands; then one pass only (directive 4).
- **No more E113 snapshot commits per iteration.** Keep caching audits as sweeps land, but log one ledger row at the final snapshot, not seven.
- No new generation experiments, no new arms/families/languages, no re-calibration of frozen auditors, no new chain/waiter `.sh` scripts (there are 26). Kill the stale one (directive 3).
- No reviews before Sun 12:30; no PDF exports before Sun 16:30.
- No REPORT net growth beyond 711 lines: E113 text replaces stub text.

## Cross-pollination
- **From Q1.4 → here:** (a) the "6 sweeps complete" STATUS line + per-cell board-share table (their directive 1) trigger your eval. (b) The qwen-cell pCMI replication verdict → joint sentence if replicated (directive 1). (c) Their D2 verdict (≈22:00) → cite in one line (Part D2). (d) Their new executed-definition sensitivity on executed-only pCMI (their directive 4) reuses your E120 code. Give them the path if they ask. The shared merge sentence: "neither words (E116) nor co-movement (Q1.4 executed-only pCMI 0.42 [0.33, 0.53]) tell executed from non-executed agreements".
- **From here → Q1.4:** E115 (sol newcomer 0/20 re-agreement, 18/20 level holds), which they extend their P2.4 citation with; your luna board-post counts per cell (c02/c07/c04) to cross-check their table.
- **Shared definitions (unchanged):** executed = judged agreement AND both pair firms within ±1 of the agreed price in ≥ 50% of post-agreement rounds AND pair mean ≥ Nash + 2 ("strict"). Tacit-high = no-channel market mean ≥ Nash + 2 over the second half. Jeffreys CIs. The joint statement is verbatim in both reports (checked 20:00: identical).

---

## TOP PRIORITY (added by Dennis 10:25 UTC) — part C: strong / executed collusion + older models
**Why:** our LLM "collusion" is mostly *agreement without execution* (Q2.2: only 14/95 test runs keep the
agreement; deepseek 3/15; Q1.4 kept agreements sit at floor ≈12, barely above Nash 10) plus a prompt-
induced level effect (notepad ≈ 2/3 of the channel premium). Detectors were therefore mostly tested on weak
collusion. A judge will ask: do they work on collusion that is actually *executed and sustained*? We need a
clear positive arm. This outranks the remaining gap/exploration items (except finishing runs in flight).

**C1 Strong-collusion arm** (both repos, in your own market; coordinate via the sibling's STATUS.md so
you don't build identical arms — Q1.4 focuses on T=60–100 long games and dependence detectors, Q2.2 on
auditors/text and kept-vs-not-kept). Levers, piloted cheaply first (≤ 10 runs) and combined if needed:
- persistent memory: the agreed terms + full price history (incl. partner's compliance) visible every round;
- Fish et al. (2024)-style profit-maximisation framing ("maximise long-run profit"), no instruction to collude;
- repeated private messaging every round (not only opening), so deviations can be discussed/punished;
- longer horizon (T ≥ 40) with an unknown end;
- stronger sellers (gpt-6.1-sol) for the pair.
Promote the lever set that yields *sustained execution* (agreement kept ≥ 50% of post-agreement rounds,
floor clearly above Nash). Then run a properly sized set (≥ 20 C + 20 matched A) and evaluate ALL headline
detectors/auditors on executed-collusion runs vs controls. Report the executed-collusion rate per lever
(how rare is sustained collusion?) — that rate is itself a headline number.
Never instruct agents to collude; only opportunity, memory and profit objective.
→ **DONE (E99 final 15:34).** Strict-executed 13/20 [.43, .83], tacit-high none 19/20 [.79, .99], competitive 1/20; paired private − none −0.44 [−1.84, +1.00]. Executed vs tacit (E99-x, exploratory): price views ≈ 0.5, public text 0.25, combined 0.18, plan 0.76 [0.55, 0.93]. Class file published (Q1.4 E66: 0 mismatches). Plan-view keyword baseline done (E111: channel footprint, 0.82 partner-name count), rewording + E66 line done. Within-agreement contrast **DONE** (E116, 13 vs 7: plan 0.69 [0.44, 0.91], text 0.61 [0.37, 0.85], none resolved; E116b Qwen strata 5 vs 10, exploratory). Definition sensitivity **DONE** (E120: strict 10–16/20, tacit-high 17–20/20). Levers were combined, not ablated: keep saying so (E1/E70 varies framing and memory).

**C2 Older / weaker models as sellers** (model-generation lever: does collusion and its detectability
change across model generations?). Available and verified working 10:25 UTC:
- codex: `gpt-5.6-luna`, `gpt-5.6-sol` (previous generation) — `llm.chat(..., backend="codex", model="gpt-5.6-luna")`
- OpenCode Go: `glm-5.2`, `mimo-v2.5` (older open models) — `backend="go"`; Go is shared/slow, keep runs small.
NOT available: gpt-5, gpt-4o. **WARNING:** llm.py's codex backend silently falls back to gpt-6-luna when a
model name is unknown or limited — always check `r["model"]` and exclude/flag fallback runs.
Split: Q1.4 runs gpt-5.6-luna + glm-5.2; Q2.2 runs gpt-5.6-sol + mimo-v2.5. ~10–15 runs per model (A vs C
matched seeds), base prompt. Report per-generation: agreement rate, execution rate, markup, detector AUROCs.
Combine with C1 if a model executes collusion more readily (older models may comply/coordinate differently).
→ **DONE** (reported final with n in P2.7: gpt-5.6-sol executed 1/7, mimo 4/4; fallback guard checked). No restart. Beside Q1.4 E62 gpt-5.6-luna tacit 9/10: "older/other models price high without a channel" is a two-market finding.

**C3 Abliterated (refusal-removed) seller: does safety training suppress collusion?** (added 10:45 UTC)
Model: `huihui-ai/Huihui-Qwen3.8-27B-abliterated` on Modal (1× A100-80GB, vLLM), via
`llm.chat(..., backend="qwen")` — explicit only, no fallback. Cold start after 10 min idle: up to ~10 min,
so run games in batches back-to-back, never one-off calls spread out. Concurrency: up to ~8 parallel
games is fine (vLLM batches them).
**BUDGET (hard):** Modal credits are capped at $79.99 total until Sun 18:00 UTC; a guard stops the endpoint
at $70 for good. ~$2.80/GPU-hour. Read `~/collusion/QWEN_BUDGET.txt` before every batch; status `warn`
→ only the most valuable runs; `STOPPED` → don't use qwen, report what you have.
Design: matched seeds, base prompt, A (no channel) vs C (private channel), ≥ 15 + 15 runs (Q1.4: its
market, T=20; Q2.2: its market + the notepad/placebo arms if budget allows). Compare agreement rate,
execution (kept agreements), markup, and all headline detectors vs the safety-trained families. Also
try it in the C1 strong-collusion lever set. Never instruct agents to collude.
**Clean pair (updated 11:20 UTC):** control = base `Qwen/Qwen3.8-27B` (FP8) via the TU Wien Aqueduct gateway:
`llm.chat(..., backend="qwen", model="qwen-base")` (routes to the gateway) — free, fast, no Modal cost. Abliterated stays on
Modal (bf16; note the FP8-vs-bf16 precision difference as a caveat). Run both on the SAME seeds/conditions (A vs C,
≥ 15 + 15 each). Headline: abliterated − base (agreement, kept rate, markup, detector AUROCs), plus vs gpt/deepseek.
Gateway also serves `qwen-3.6-35b`, `glm-5.3-744b-experimental`, `deepseek-v4-vision-exp-284b` via
`llm.chat(..., backend="aqueduct", model=...)` — extra seller families for C2/robustness (shared university
gateway: keep ≤ 4 parallel calls, back off on 429).
→ **DONE** (E100, P2.11: agreement 15/15 both (ceiling), strict 5/15 both; floor-rule executed 13/15 both, diff 0 [−0.26, +0.26]; premium diff −1.24 [−2.41, −0.03] with a bf16-vs-FP8 caveat). **Open (20:00 directive 2):** the abstract quotes 13/15 without naming the floor rule, so lead with strict 5/15. E102 strong qwen: **final** (descriptive; strict 4/6 base vs 3/6 abliterated). Notepad arm for qwen **DROPPED**. Gateway: games-parallel 1 (shared with Q1.4 D2/E1).

---

# Phase 2 gap list (set by Dennis, 2026-10-24 06:40 UTC) — overrides earlier "no new experiments"

v1 (overnight result) is frozen as git tag `v1-overnight`. Phase 2 = close every known gap. Research is
OPEN again: new experiments are wanted. Keep v1 numbers reproducible; new results go in new sections
/ new datasets (`*_p2`), registered in EXPERIMENTS.tsv before running, decided on dev, confirmed once on a
fresh locked split recorded in data/SPLITS.md.

**Timeline (UTC):** presentable checkpoint (REPORT.md updated with whatever is done) by **Sat 20:00**;
all experiments done by **Sun 15:00**; finalize-only from **Sun 16:30**; hard stop **Sun 18:00**.
Submission is Sun 23:59 AoE — Dennis submits Sunday evening from the merged repo
(`collusion-beyond-words`, built by a third manager from Sun 08:00 using BOTH repos' REPORTs).
Keep REPORT.md always presentable; put a "Phase 2 results" section near the top once results land.

**Ownership:** each gap below is owned by ONE repo (no duplicate work). The sibling may read your data.

**Budget / models:** GPT-family sellers via `llm.chat(tier="cheap")` (gpt-6-luna). For the **second seller
family** use OpenCode Go: `llm.chat(..., backend="go", model="deepseek-v4.1-flash")` (or glm-5.3-flash /
kimi-k3) — Go is serialised and shared with another service; if it 429s, llm.py cools down 30 min;
then continue with what you have. Claude Sonnet as a seller only on a small subset (≤ 10 runs) — the
Claude quota runs the managers. gpt-6.1-sol as a seller for a third family check is fine (codex quota).

**Gaps owned by BOTH repos (do in your own market):**
- **Precision at realistic prevalence** (15 min): for every headline detector, report precision / FPR-
  normalised alarm rates at 1%, 5%, 20% collusion prevalence at the frozen thresholds, with CIs.
  → **DONE** (E81, P2.1). Detail → appendix (directive 4d). Behaviour-label row: **DROPPED** (not one line of code; adds nothing to the reading).
- **Independent reimplementation check:** have codex (gpt-6.1-sol, `-s workspace-write` in a scratch dir,
  given ONLY the REPORT's method description, not your code) reimplement your headline statistic(s); compare
  numbers on the same data. Report agreement; fix any bug found (and re-state affected numbers).
  → **DONE** (E83, P2.2: 30/32 match to 3 dp, both differences ≤ 0.001, tie handling; no bug).

## Gaps owned by THIS repo (Q2.2), in priority order (status as of 20:00 UTC; all eight closed — frozen)
1. **Is the "collusion" a prompt artifact?** (biggest validity threat). Round-1 prices already give AUROC
   0.90 and the undelivered placebo is flagged as often as delivered. Conditions (matched seeds):
   (a) current private-channel wording; (b) neutrally described channel ("a message box to firm X");
   (c) "notes to self" channel (same wording, no recipient); (d) channel to a random, changing partner;
   (e) placebo (offered, never delivered); (f) no channel. Measure round-1 premium, mean premium, and
   whether messages contain agreements. If the premium survives (b)/(d) but not (c), coordination is real;
   if (c) ≈ (a), the offer itself is the driver — either way that is a headline. Also 2–3 paraphrases of
   the base seller prompt as a wording-robustness band.
   → **DONE.** E77, E92 (pricing content), E78 band, E94 closed (para1 12:19: P3 held; para2 P1 failed, reported). E89 p2cue views: **DROPPED** (20:00; codex is saturated and they would add nothing to the reading; one line if mentioned at all).
2. **Labels by behaviour, not condition**: break label = condition. Label every run from the private chat
   (agreement yes/no, judge tier="big" + Claude subset) AND realised behaviour (agreement followed?). Add
   channel-but-no-agreement runs and no-channel tacit-high runs; re-evaluate all auditors against the
   behaviour labels.
   → **DONE** (E84/E84b–e, P2.4; p2rep followed label, pooled kept-label contrast −0.03). The tacit-high class comes from E99 (directive 1). Add the circularity caveat on price views for the kept label (cross-pollination d).
3. **Second (and third) seller family**: deepseek via Go (≥ 30 runs over private/none), gpt-6.1-sol
   sellers (~20 runs), Claude Sonnet sellers (≤ 10 runs). Do premium, text-adds-nothing, and the placebo
   effect replicate?
   → **DONE** (E95 3-way final 13:03, all predictions held; E91-ext ds/sol views). glm **DROPPED**. SALT per-model say rates (E104) are the external echo (directive 2).
4. **Second replication of the premium statistic**: ≥ 60 fresh seeds, statistic frozen exactly as
   published (pre-register in EXPERIMENTS.tsv + data/SPLITS.md first). Removes the "chosen after seeing
   test data" bias.
   → **DONE** (E80/E89, P2.8: premium 0.94 [0.87, 0.99] ≥ registered 0.85; Δ_hybrid −0.04; pooled n = 90 −0.07, post hoc). Bound sentence in abstract (gains > +0.06 test / +0.02 pooled excluded).
5. **Monitor-aware adversarial colluders**: tell the channel pair (and in a control, all firms) that a
   regulator screens price premiums over rivals / public messages. Does the premium collapse? Does
   collusion move elsewhere (smaller premium, alternation, text)? Which auditor survives?
   → **DONE** (E86, P2.9: 0/10 + 0/10 agreements, compliance not evasion; market −1.19 below none). Frozen.
6. **Explain the 0.98 supervised text classifier**: top TF-IDF features, ablate them, check if signal is
   style shift after channel offer (present in placebo / notes-to-self?) vs coordination content.
   → **DONE** (E82, E82b). Frozen; detail → appendix.
7. **Cost asymmetry hard negative** for the premium: firms with legitimately lower costs / differentiated
   quality but no channel. Premium's FPR there; does a cost-adjusted markup fix it?
   → **DONE** (E87 + post-hoc E87-nash, P2.10: highcost 7/10, quality 9/10 vs 2/10; competition predicts the cost flag; cost adjustment overcorrects). Frozen.
8. **Hidden signals in public text (exploration)**: one condition where the pair may agree on a code in the
   private channel and is told public messages are monitored; does any auditor catch coded public
   coordination? (Shows the limit of text auditing; one small condition is enough.)
   → **DROPPED** (11:45; codex to Part C). One Limitations line, citing Q1.4 P2.6 bid rotation and SALT's silent executors.
Items 1–4 must be done by Sat 20:00 if at all possible; 5–8 by Sun 15:00.


**C3b/C3c — replicate the abliteration null on more Qwen pairs (added 16:00 UTC).** C3 (Qwen3.8-27B) gave no
abliteration effect; one pair is a case, three pairs are a pattern. Same design as C3 (matched seeds, A vs C,
15 + 15 per model, base prompt; plus the memory lever if C3's memory arm shows execution), all via `llm.chat(backend="qwen", model=...)`
unless noted:
- **C3b Qwen3.6-35B-A3B (MoE, 3B active):** abliterated `model="qwen36-abliterated"` (Modal L40S, FP8) vs base
  `llm.chat(backend="aqueduct", model="qwen-3.6-35b")` (gateway, AWQ 4-bit, free). Owner: Q1.4.
- **C3c Qwen3.5-9B (small, cheap):** `model="qwen9-abliterated"` vs `model="qwen9-base"` (both Modal L4, FP8 —
  identical serving, the cleanest pair). Owner: Q2.2. First check the 9B follows the game protocol (parse rate,
  sane prices in 3 pilot games); if > 10% unparsable or nonsense prices, report that and drop it.
Each Modal endpoint cold-starts in up to ~10 min after 10 min idle → run each model's games as one batch.
Cost ≈ L40S $2.2/h, L4 $1/h each; the $70 guard covers all apps. Priority: after the running Part C arms and
Part D1, before Part D2/D3. Report the three pairs in one table: abliterated − base (agreement, executed, markup,
detector AUROCs) with CIs, and state the precision caveat (FP8/AWQ/bf16) per pair.
→ **C3c DROPPED** by its registered pilot rule (E109, 15:12: base Qwen3.5-9B prices below Nash; process deviation disclosed). **C3b DONE** by Q1.4 (E69: −0.65 [−1.97, +0.65], null replicates); cited in P2.11 + glance at 17:51 (3/3 pairs no detectable increase; your −1.24 premium decrease kept visible).



**Serendipity Explorer (added 14:50 UTC):** a third agent runs wild cheap pilots in `~/collusion/collusion-serendipity` (other markets, hub-and-spoke advisor, leniency, counterfactual replay, steganography in prices, personas, ...). Read its `HITS.md` at the start of every iteration; if a hit bears on your headline claims, decide explicitly (in STATUS) whether to confirm it with a registered experiment. Don't duplicate its pilots.
→ Status 20:00: **still no promoted hits** (S01, S03, S07 duds; S02 odd; S04 uninformative; S11 ODD; S14 tender caution (relevant to Q1.4 D2, not here); S16 failed pilot). Nothing to confirm; one STATUS line per iteration.

## Part E — BROADEN THE DESIGN so we can make concrete, general claims (added by Dennis 14:30 UTC)
**Why:** so far we varied one thing at a time (model, prompt, memory, channel) in mostly one market setup. Claims like
"collusion shows up as level, not co-movement" are only as general as the conditions we tested. Goal: a small number of
designs that turn one-off pilots into **general statements with a denominator** ("held in 14 of 16 conditions").
**Priority:** right after finishing the in-flight Part C arms; run in parallel with Part D (different backends). Results by Sun 13:00 UTC.

- **E1 Factorial "generalization grid" (owner Q1.4 generates, Q2.2 audits).** 2-level fractional factorial, 2^(7-3) = 16
  cells (resolution IV), ~6 games per cell (A vs C split inside each cell), T=20, public messages logged. Factors:
  (1) seller family: gpt-6-luna vs Aqueduct qwen-3.6-35b; (2) firms: 2 vs 4; (3) rivals' prices visible each round vs hidden
  (only own sales); (4) private channel only in round 1 vs every round; (5) memory: last 3 rounds vs full history;
  (6) public demand/cost shocks: none vs random; (7) framing: neutral vs long-run-profit.
  Outcomes per cell: channel markup, executed rate, market-wide spillover, level-screen AUROC, pCMI AUROC, text-auditor flag rate.
  Report main effects with CIs (which factors CAUSE the price lift — answers sprint Q1.1 — and which single restriction
  cuts it most — answers Q1.5) and the claim's **denominator** (in how many cells level > co-movement, text ≈ chance).
  Gateway is 45 calls/min shared: luna cells via codex, qwen cells via gateway; one queue, resumable, registered first.
  → Generation: Q1.4 **E70 IN PROGRESS** (sweep index 3 of 0–5 running at 20:00; generation ETA ≈22:40). **Audit (this repo) = E113 IN PROGRESS:** registered 16:16, amend 17:36 (text on qwen cells), amend2 18:29 (luna board exceptions c02/c07; guards), snapshot7 at 19:58 = 100 games / 3 sweeps, coverage 100%, no scores read. **Next:** E113-amend3 (qwen k/8 + ties + cell-stratified pooled Δ; luna = noise estimate), then eval once at 6 sweeps → write-up by Sun 00:30 (directive 1 of 20:00).
- **E2 Participant replacement mid-game (owner Q2.2; sprint Q1.2).** In executed-collusion games (strong arm / qwen memory),
  replace one colluder at round T/2 with a fresh agent (same model, no chat history) or a different model. Does the price
  level survive? Do detectors notice the break (changepoint)? Cheap, novel, and answers an official sprint question.
  → **DONE (E112, 17:33, P2.15):** 30/30 prefixes byte-identical; market excess repl − orig +0.20 [−0.08, +0.62] private, +0.16 [−0.27, +0.57] none; ≥ Nash + 2 in 19/20 & 9/10; re-agreement 16/20; level CUSUM 0/30 by r25; P1–P4 held. **E115 DONE** (19:20: sol newcomer re-agrees 0/20, undercuts −3.38, market −1.34 [−1.79, −0.91] but ≥ Nash + 2 in 18/20 & 9/10; S1 failed, S2–S4 held). Both in abstract + TL;DR 6 (done).
- **E3 Cross-family collusion (owner Q2.2; sprint Q3.3 "can agents identify their peers?").** Pair = luna + qwen (different
  families) with a channel vs same-family pairs. Do mixed pairs agree / execute as often? Does pCMI see same-family pairs
  more (shared-policy confound)?
  → **DROPPED (17:56)**: gateway saturated by Q1.4's E70 qwen lane + D2; E70's model factor varies family at the market level. One Limitations line (directive 5 of 17:56).
- **E4 Anomaly hunt (owner both, 30 min each, zero new games).** Have codex gpt-6.1-sol read ~40 randomly sampled
  transcripts across ALL datasets (both repos) and list the 5 most surprising behaviours with run ids. Each becomes a
  15-min test logged as `serendipity` in EXPERIMENTS.tsv. Report the hits and the duds.
  → **DONE** (E108, P2.13: 40 games across both repos' datasets, 5 follow-ups, hits + duds, codex-verified). Counts for Q1.4 too.
- **E5 One non-English market (owner Q2.2, small, 10+10).** Same game, all prompts and messages in German. Does the text
  auditor (English-prompted) still behave the same? Does collusion change with language?
  → **DONE** (E110, 16:08, P2.14: explicit agreement DE 3/10 vs EN 9/10; premium DE +0.91 [+0.20, +1.58]; P1 held, P3 failed, P4 not evaluable). Frozen.

For every claim in the final abstract, write its denominator next to it (conditions tested, models, datasets).
→ **DONE** (E114, `p2_claims.py`, now 30/30 match). Re-run after the E113 clause and the strict-5/15 fix (directives 1, 2 of 20:00).

## Part D — EXTERNAL VALIDITY with the three proposed datasets (added by Dennis 14:05 UTC)
**Priority:** after the important in-flight work (E44/P2.8, Part C strong arm + C3 qwen pair, the Sat 20:00
checkpoint) — and BEFORE any remaining exploration-portfolio (part B) items. Target: results by Sun 12:00 UTC.
**Why:** every result so far comes from our own simulated market. Judges will ask whether "price level yes,
dependence no, words no" is an artifact of our toy market. External data is the strongest answer.
Use FROZEN detectors/auditors (no re-tuning on external data); report agreement/disagreement with our
findings honestly, including where they don't transfer.

- **D1 SALT-NLP agent-collusion** (owner: Q2.2; Q1.4 may read the data). HF dataset `SALT-NLP/agent-collusion`
  (public, not gated; ~27k episodes + ~2.6k longer trajectories; two-agent communication, decisions, tool traces,
  rewards, settings). Download to `/var/tmp` (not into git; commit only a small sample + a loader + summary stats).
  Read its README/paper for the operational definition of its collusion field; map it explicitly to our label
  levels (opportunity / agreement / executed) and say where it differs. Stratified sample of ~200–300 episodes.
  Run the frozen auditor views (text, action, combined, action_stats where defined) + simple non-LLM baselines.
  Headline: Δ_hybrid on external data with bootstrap CI. Note: two-agent episodes → no pairwise net-influence;
  Q1.4 can still test pCMI/MI between the two agents over trajectories if they are long enough (optional).
  → **DONE.** E104 (P(said | exec) 0.385 [0.353, 0.416], model-dependent; mapping documented), E105 (sol text auditor 0.87 [0.83, 0.91] vs condition-grouped TF-IDF 0.91; tacit 0.81). Δ_hybrid not meaningful on SALT (the action label is a function of the verdicts): said so. Q1.4 pCMI part dropped (no time series).
- **D2 Double auction** (owner: Q1.4). Starter `~/collusion/collusion_hackathon/llm-agent-collusion`
  (Agrawal et al. 2025, continuous double auction; 3 sellers + 3 buyers, seller communication optional). Copy the
  code into this repo (don't modify the starter), and write a small adapter so its model wrapper calls our
  `llm.chat` (it expects a Nebius/OpenRouter key; route to codex luna/sol, Go deepseek, or the Aqueduct gateway
  qwen-3.6-35b — record the model per run). Conditions: seller communication on vs off, ≥ 15 + 15 runs. Apply
  the frozen level screen, pCMI and dependence detectors on seller ask series. Does price-level-not-dependence hold
  in a different market mechanism?
  → Q1.4-owned, **IN PROGRESS** there (E68: 24/30 runs at 20:00, analysis ≈21:00–22:00; manipulation check declared and corrected before reading). Nothing to do here. Cite its verdict in one line once it is in their REPORT.
- **D3 LLM trust-breaking** (owner: Q2.2, lowest priority of the three). Starter
  `~/collusion/collusion_hackathon/llm-trust-breaking` (private plans, public announcements, actions, outcomes in
  repeated games). Measures promise-breaking, NOT collusion — use it only to validate our say-vs-do machinery
  (claim–action consistency table, text-vs-action auditors) on someone else's data. Same adapter approach;
  small n (~20–40 trials) is enough.
  → **DROPPED** (13:45): it measures promise-breaking, not collusion, and needs an adapter plus generation. D1 already gives the external say-vs-do test, and the remaining time goes to E99 + consolidation. One line in Limitations.

Budget: D1 is auditor calls only (sol, ~1–2k calls); D2/D3 generation can use the Aqueduct gateway (45/min cap
handled by llm.py) or codex luna. Register each in EXPERIMENTS.tsv first; write each up once as a short
"External validity" subsection (≤ 15 lines + 1 table).
