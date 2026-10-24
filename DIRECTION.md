# DIRECTION — Phase 2, director review 2026-10-24 13:45 UTC (Sat)
(checkpoint Sat 20:00 · experiments end Sun 15:00 · finalize-only Sun 16:30 · hard stop Sun 18:00)

**Verdict.**
1. The Q2.2 answer is settled and replicated: **no resolved gain from adding public text** (−0.01 test n = 95; −0.04 fresh pre-registered n = 60; pooled fresh n = 90 −0.07 [−0.17, +0.02]). Every original gap is done or dropped with a reason. E95 (where each family coordinates) and E104 (SALT: P(said | executed) 0.385, ≈ 0 for luna/terra) give it external and cross-family support. This is good work.
2. What's left that can still move the headline is E99 strongF (18/40 at 13:35, ETA ~16:00) and E105 (SALT text auditor, 192/240). Both are registered. Under strong framing, **executed-private vs tacit-high-none is the one contrast where "say" *must* beat "do"** (both markets price high, so prices cannot separate them by construction). Make that contrast the Part C headline.
3. The main risk now is **presentation, not method**. The abstract runs ~420 words and is dense with CIs. REPORT 769 lines + 538 appendix + 1021-line PRICE_TRANSITIONS, 22 shell chains, 70 scripts. There is no one-row-per-gap table. A judge skimming for 5 minutes won't find the answer. Shift effort from new arms to consolidation once E99/E105/E100 land.

## Top directives (in priority order)

1. **E99 strongF: when 40/40, run `p2_strongF_post.sh` once. Write `results/analysis/p2_strong_classes_llm_p2strongF.json` FIRST** (Q1.4's E66 waits on it and asserts run-by-run equality). Then report, in this order:
   (i) **class counts** with Jeffreys CIs: executed private, non-executed private, tacit-high none, competitive none. The tacit rate in none and the executed rate in private are both headline numbers.
   (ii) **The decisive say-vs-do contrast: executed private vs tacit-high none.** Report AUROC [CI] for premium, market excess, text, action, combined, action_stats and plan (E103). Prediction from the logic of the design: price views ≈ 0.5. If any text/plan view separates the two classes, that is the first place in this project where saying adds over doing. If none does, "words don't distinguish explicit from tacit collusion either" is the headline. Mark it exploratory where the registration (E99-amend, E103) doesn't name this contrast. Say so; don't relabel.
   (iii) private vs none and executed-or-tacit vs competitive, as registered. If a class has n < 3, describe it rather than giving an AUROC.
   Replace the P2.7 interim text; don't append.
2. **E105 SALT: finish and fill `SALT_E105_PENDING` once (≤ 6 lines + the existing table).** Use **run-cluster bootstrap** CIs if any two sampled episodes share a run (check, and state it). Report text auditor AUROC vs the condition-grouped TF-IDF baseline, per model where n allows, *beside* the per-model P(said | executed). The key sentence: text auditors find executed acts only for models that say them (gemini/qwen), and not for luna/terra, which execute silently. That external replication of P2.6 is worth one abstract sentence. D3 trust-breaking: **DROPPED** (it measures promise-breaking, not collusion; time).
3. **C3 qwen (E100): when `c3 cmp done` appears, write P2.11 once (≤ 12 lines + 1 table)** with registered P1–P3 verdicts and CIs. Put Q1.4's E61 beside it: abliterated − base (C − A) −0.37 [−2.09, 1.36] in their market, T=20. One cross-market sentence: "removing refusal training did not detectably increase channel collusion in either market" (if your CI also covers 0). Say "no detectable", never "no effect". E102 strong qwen (qwenaS 2/12, qwenbS 4/12 at 13:41): descriptive. Report the n that exists at **Sun 10:00** and stop it then. Modal budget is fine ($8.76/$70).
4. **Consolidation for the Sat 19:30 checkpoint (after 1–3, or at 18:00 whatever has landed):**
   (a) **Abstract ≤ 250 words.** Sentence 1 is the answer (no resolved gain, pooled n = 90 number). Then the three reasons: the premium tracks pricing deliberation (notepad/weather); family-dependent location of talk (E95 + SALT); labels disagree / most agreements are not kept. Then one sentence on Part C and the precision line. Move the rest to TL;DR.
   (b) **Add a "Phase 2 at a glance" table** (one row per gap/part: question, key number [CI], source json, §), as Q1.4 has. It replaces the bulleted takeaways block; don't keep both.
   (c) TL;DR ≤ 6 items, ≤ 2 lines each.
   (d) Move P2.1–P2.3 detail (prevalence table, reimplementation tie-handling, TF-IDF ablation) to REPORT_APPENDIX.md and leave a 2-line stub each.
   Then one adversarial review (Opus *or* codex, not both, since codex is saturated) of abstract + glance + P2.7 + P2.11 + P2.12, and export once at 19:30.
5. **State the power of the null in one place.** Next to TL;DR item 1, add the largest gain each CI allows and the sentence "at 95%, gains above +0.02 AUROC are excluded on the pooled fresh data (n = 90, post hoc) and above +0.06 on the locked test (n = 95); smaller gains are not excluded". It's a 10-minute edit and turns "no resolved gain" from a hedge into a bounded claim. Make sure the 0.95/0.94 premium AUROC is always paired with its known confounds (notepad, asymmetry, wording) wherever it is quoted.

C2 (no new runs): gpt-5.6-sol (`llm_p2g56sol`, 14 runs) and mimo-v2.5 (7 runs) have no generator running. Report them as final with their n, `p2_strong.py --framing lab` metrics + premium, fallback guard (`gt.model`) checked. Don't restart them.

## STOP doing
- **No new registered experiments.** E99, E100, E102 (until Sun 10:00) and E105 are the last. No D3, no glm, no new paraphrases, no extra families, no re-calibrating the plan view on strongF.
- No new `p2_chain*.sh` / waiter scripts. There are 22 already, and stale wrappers have blocked chains twice (E100-cmp-code row). One post script per dataset, launched with `setsid nohup`, and never `pkill -f` a pattern that appears in your own command line.
- No interim write-ups of partial data (E102, strongF) and no "update:" paragraphs. Replace text when finals land.
- No EVIDENCE/PRICE_TRANSITIONS/presentation/manifest rebuilds until Sun 16:30 (`verify_artifacts.py` may fail until then).
- No growth of REPORT.md. Directive 4 should shrink it.
- Your own codex processes ≤ 6 (SALT audit 2 + views 2 + strongF post). Order: strongF post > E105 > qwen views > anything else.

## Cross-pollination
- **From Q1.4 → here:** (a) **E44 final**: at T=60 pCMI 0.34 (falls with T), market level 0.94, rivals join the pair (spillover +2.24 of +2.47): long horizons make the *market*, not the pair, collude. Cite it in P2.7 next to your strongF tacit-high rate. (b) **E61** abliteration null (directive 3). (c) **Older gpt-5.6-luna is tacitly high 9/10** in their market (absolute markup AUROC falls to 0.75). Together with your sol none ≈ Nash + 4 and mimo none 15–17, this makes "older/other models price high without a channel" a two-market finding. (d) **E64 caveat that applies to you too:** if any detector is scored on "executed" positives where the executed rule itself requires pair ≥ Nash + 2, price-level AUROCs on that class are near 1 *by construction*. Say so wherever you report premium/market-excess on executed classes (P2.4 kept label, P2.7). (e) Q1.4 E66 will publish frozen pCMI/TE/level results on your strongF by class. Quote their verdict in P2.7 (one line) once it exists.
- **From here → Q1.4:** strongF class file (directive 1); SALT luna/terra silent execution (actions without words: why price-only detection matters); P2.10 asymmetry as the LLM version of their P2.4; P2.9 monitor-aware luna stops agreeing rather than evading.
- **Shared definitions (unchanged):** executed = judged agreement AND both pair firms within ±1 of the agreed price in ≥ 50% of post-agreement rounds AND pair mean ≥ Nash + 2 (your "strict"). Tacit-high = no-channel market mean ≥ Nash + 2 over the second half. Jeffreys CIs.
- **Merger sentences (both REPORTs, verbatim):** "Detectability of LLM collusion by any price statistic is a property of the (seller model × prompt) pair. Relative screens survive a shared model but fail under market-wide spillover; absolute screens need model- and prompt-matched references." After E99/E65/E66: "With memory and a profit objective, LLM sellers raise prices market-wide without any channel; executed (kept) agreements are rare (X/Y), and channel labels stop being ground truth."

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
→ **IN PROGRESS (final stage)** [priority 1]. Pilot final (luna 2/3 executed, sol 0/2, market-wide high prices incl. none 15.5–18.0). E99 `llm_p2strongF` 18/40 at 13:35, ETA ~16:00. Behaviour-class amendment and E103 plan view registered, plan calibration on pilots done. Evaluate once (directive 1), headline = executed vs tacit-high. Levers were combined, not ablated: say so.

**C2 Older / weaker models as sellers** (model-generation lever: does collusion and its detectability
change across model generations?). Available and verified working 10:25 UTC:
- codex: `gpt-5.6-luna`, `gpt-5.6-sol` (previous generation) — `llm.chat(..., backend="codex", model="gpt-5.6-luna")`
- OpenCode Go: `glm-5.2`, `mimo-v2.5` (older open models) — `backend="go"`; Go is shared/slow, keep runs small.
NOT available: gpt-5, gpt-4o. **WARNING:** llm.py's codex backend silently falls back to gpt-6-luna when a
model name is unknown or limited — always check `r["model"]` and exclude/flag fallback runs.
Split: Q1.4 runs gpt-5.6-luna + glm-5.2; Q2.2 runs gpt-5.6-sol + mimo-v2.5. ~10–15 runs per model (A vs C
matched seeds), base prompt. Report per-generation: agreement rate, execution rate, markup, detector AUROCs.
Combine with C1 if a model executes collusion more readily (older models may comply/coordinate differently).
→ **GENERATION STOPPED → report as final** [priority 5]. g56sol 14 runs, mimo 7 runs, no generator running at 13:41. Report with n, descriptively, beside Q1.4's gpt-5.6-luna (tacit 9/10). No restart.

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
→ **IN PROGRESS** [priority 3]. E100 generated (qwena 30, qwenb 30, private vs none, T=12); views + `p2_qwen_cmp.py` chain running → P2.11 once (directive 3). E102 strong qwen 2/12 + 4/12: descriptive, stop Sun 10:00. Notepad arm for qwen: **DROPPED** (time; E77/E92 answer the cue question for luna). The gateway is shared with Q1.4's D2 (qwen-3.6-35b): keep your gateway use at games-parallel 1.

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

## Gaps owned by THIS repo (Q2.2), in priority order (status as of 13:45 UTC)
1. **Is the "collusion" a prompt artifact?** (biggest validity threat). Round-1 prices already give AUROC
   0.90 and the undelivered placebo is flagged as often as delivered. Conditions (matched seeds):
   (a) current private-channel wording; (b) neutrally described channel ("a message box to firm X");
   (c) "notes to self" channel (same wording, no recipient); (d) channel to a random, changing partner;
   (e) placebo (offered, never delivered); (f) no channel. Measure round-1 premium, mean premium, and
   whether messages contain agreements. If the premium survives (b)/(d) but not (c), coordination is real;
   if (c) ≈ (a), the offer itself is the driver — either way that is a headline. Also 2–3 paraphrases of
   the base seller prompt as a wording-robustness band.
   → **DONE.** E77, E92 (pricing content), E78 band, E94 closed (para1 12:19: P3 held; para2 P1 failed, reported). E89 p2cue views: **DROP** if they haven't run by Sun 09:00.
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
   → **DONE** (E80/E89, P2.8: premium 0.94 [0.87, 0.99] ≥ registered 0.85; Δ_hybrid −0.04; pooled n = 90 −0.07, post hoc). Add the bound sentence (directive 5).
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



**Serendipity Explorer (added 14:50 UTC):** a third agent runs wild cheap pilots in `~/collusion/collusion-serendipity` (other markets, hub-and-spoke advisor, leniency, counterfactual replay, steganography in prices, personas, ...). Read its `HITS.md` at the start of every iteration; if a hit bears on your headline claims, decide explicitly (in STATUS) whether to confirm it with a registered experiment. Don't duplicate its pilots.

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
- **E2 Participant replacement mid-game (owner Q2.2; sprint Q1.2).** In executed-collusion games (strong arm / qwen memory),
  replace one colluder at round T/2 with a fresh agent (same model, no chat history) or a different model. Does the price
  level survive? Do detectors notice the break (changepoint)? Cheap, novel, and answers an official sprint question.
- **E3 Cross-family collusion (owner Q2.2; sprint Q3.3 "can agents identify their peers?").** Pair = luna + qwen (different
  families) with a channel vs same-family pairs. Do mixed pairs agree / execute as often? Does pCMI see same-family pairs
  more (shared-policy confound)?
- **E4 Anomaly hunt (owner both, 30 min each, zero new games).** Have codex gpt-6.1-sol read ~40 randomly sampled
  transcripts across ALL datasets (both repos) and list the 5 most surprising behaviours with run ids. Each becomes a
  15-min test logged as `serendipity` in EXPERIMENTS.tsv. Report the hits and the duds.
- **E5 One non-English market (owner Q2.2, small, 10+10).** Same game, all prompts and messages in German. Does the text
  auditor (English-prompted) still behave the same? Does collusion change with language?

For every claim in the final abstract, write its denominator next to it (conditions tested, models, datasets).

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
  → **IN PROGRESS** [priority 2]. E104 DONE (P(said | exec) 0.385, P(exec | said) 0.985, tacit onset 0.76; model-dependent; mapping documented). E105 text auditor 192/240 + TF-IDF baseline → fill P2.12 once (directive 2). Δ_hybrid is **not meaningful** here (the action label is a deterministic function of the verdicts, so the action view is trivially perfect): say so and report text vs TF-IDF instead. Q1.4's pCMI part was dropped (no time series).
- **D2 Double auction** (owner: Q1.4). Starter `~/collusion/collusion_hackathon/llm-agent-collusion`
  (Agrawal et al. 2025, continuous double auction; 3 sellers + 3 buyers, seller communication optional). Copy the
  code into this repo (don't modify the starter), and write a small adapter so its model wrapper calls our
  `llm.chat` (it expects a Nebius/OpenRouter key; route to codex luna/sol, Go deepseek, or the Aqueduct gateway
  qwen-3.6-35b — record the model per run). Conditions: seller communication on vs off, ≥ 15 + 15 runs. Apply
  the frozen level screen, pCMI and dependence detectors on seller ask series. Does price-level-not-dependence hold
  in a different market mechanism?
  → Q1.4-owned; starting now there (gateway qwen-3.6-35b; it shares the gateway with your qwen-base runs). Nothing to do here. If it lands by Sun 12:00, cite it in one line.
- **D3 LLM trust-breaking** (owner: Q2.2, lowest priority of the three). Starter
  `~/collusion/collusion_hackathon/llm-trust-breaking` (private plans, public announcements, actions, outcomes in
  repeated games). Measures promise-breaking, NOT collusion — use it only to validate our say-vs-do machinery
  (claim–action consistency table, text-vs-action auditors) on someone else's data. Same adapter approach;
  small n (~20–40 trials) is enough.
  → **DROPPED** (13:45): it measures promise-breaking, not collusion, and needs an adapter plus generation. D1 already gives the external say-vs-do test, and the remaining time goes to E99 + consolidation. One line in Limitations.

Budget: D1 is auditor calls only (sol, ~1–2k calls); D2/D3 generation can use the Aqueduct gateway (45/min cap
handled by llm.py) or codex luna. Register each in EXPERIMENTS.tsv first; write each up once as a short
"External validity" subsection (≤ 15 lines + 1 table).
