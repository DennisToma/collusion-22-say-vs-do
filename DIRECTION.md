# DIRECTION — Phase 2, director review 2026-10-24 09:40 UTC (Sat)


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

**C2 Older / weaker models as sellers** (model-generation lever: does collusion and its detectability
change across model generations?). Available and verified working 10:25 UTC:
- codex: `gpt-5.6-luna`, `gpt-5.6-sol` (previous generation) — `llm.chat(..., backend="codex", model="gpt-5.6-luna")`
- OpenCode Go: `glm-5.2`, `mimo-v2.5` (older open models) — `backend="go"`; Go is shared/slow, keep runs small.
NOT available: gpt-5, gpt-4o. **WARNING:** llm.py's codex backend silently falls back to gpt-6-luna when a
model name is unknown or limited — always check `r["model"]` and exclude/flag fallback runs.
Split: Q1.4 runs gpt-5.6-luna + glm-5.2; Q2.2 runs gpt-5.6-sol + mimo-v2.5. ~10–15 runs per model (A vs C
matched seeds), base prompt. Report per-generation: agreement rate, execution rate, markup, detector AUROCs.
Combine with C1 if a model executes collusion more readily (older models may comply/coordinate differently).


**Verdict.**
1. Phase 2 has produced the most important findings of either repo. A notepad with no recipient yields ~65% of the premium (E77). A terse paraphrase removes the premium while the chats still agree on 18 (E78). Most "colluders" don't keep the agreement (E84). The luna-calibrated detectors don't transfer to other families: Claude prices ≥ monopoly with no channel; deepseek invites coordination publicly in both arms; sol doesn't collude. Registration discipline is good, and failed predictions are reported as failed.
2. But the REPORT still tells the v1 story. The abstract and TL;DR 3/5 sell the premium (0.95) and "always-on action statistics" as the screen, which Phase 2 has largely undermined. The Q2.2 question (does text + actions beat either?) has new evidence that nobody has written up as a Q2.2 answer. The one pending result that tests the headline on fresh data (p2rep, 5/60, + auditor views) is queued behind everything else.
3. The repo is spread thin: 6 background chains, 5 generators, E89–E93 registered within 2 h, codex oversubscribed (also carrying Q1.4's E44). Time to exploit. Finish p2rep + views, reframe the headline, and run only the explorations that answer Q2.2 directly.

## Top directives (in priority order)

1. **Rewrite the headline for the Sat 19:30 checkpoint, starting now with interim numbers (update finals later).** Rewrite the Abstract (≤ 250 words) and cut the TL;DR to ≤ 6 items so they state the Phase 2 answer to Q2.2. Proposed spine (adjust to the numbers): *(i)* zero-shot text + actions does not beat the better single modality (v1 test, replication, behaviour label; p2rep pending). *(ii)* The action premium mostly measures the pair's response to being *offered* a private space and to prompt wording, not delivered coordination (notepad +1.04 of +1.61; paraphrase 2 +0.24). *(iii)* Whether text helps depends on *where* a seller family says its coordination. Luna says it privately, so public text adds nothing. Claude and deepseek say it publicly, so text views flag every market, including no-channel ones. *(iv)* Talk-based and price-based labels disagree (most agreements are opening-round only and not kept). Remove "suggested architecture: always-on action statistics as the screen" as a recommendation, or qualify it with (ii). Do not soften (ii). The merger lifts the abstract + takeaways block verbatim on Sun 08:00.
2. **Protect the fresh-data headline test (gap 4): p2rep → frozen premium once (E80) → frozen 4–6 auditor views (E89) → Δ_hybrid on the condition label AND the followed label (E84 rep).** This is the only pending result that re-tests the v1 headline at n=60. Give it codex priority: if parallelism > 6, pause `p2_chain2.sh` (gaps 5/7/8) and E91-ext rather than slow p2rep or its views. In chain3, the p2cue audit waits on `pgrep -f "ds llm_p2sol"`, so p2rep views may not start before ~14:00. If so, audit p2rep first, since it is the more important dataset. Report a pooled v1-rep + p2rep Δ_hybrid (n=90 fresh) as the decisive row. ETA target: p2rep views done by Sat 18:00.
3. **New, cheap, squarely Q2.2 (register before running; ~80 sol calls): frozen auditor views on `llm_p2para2` (and para1 as its control).** E78 says the chats still agree on 18 while the price premium vanishes. That is exactly the case where a text-reading auditor *should* beat an action-only one. Predict before running: text/combined flag private para2 runs more often than premium (4/10) and action. If it holds, it is the first evidence in the repo that text adds something over actions, and it goes in the abstract. If it fails, that strengthens "zero-shot text auditors don't read private intent off public text". Either way, it is the most informative ~80 calls left.
4. **Turn the family results into a Q2.2 answer with a 3-way label (register before E91-ext outputs land).** Label every family run as private agreement (judge) / public invitation (existing regex + sol check on a sample) / neither. Report text, action and combined views against that label for Claude (E91, done), deepseek and sol (E91-ext). The answer to "does text help?" is then per family and per *location* of coordination, which is the paper's message. Keep it to one table + 5 lines in P2.6 and cut the current P2.6 prose (~35 lines) to ≤ 20.
5. **Gap 5 is the only remaining exploration worth its runs; answer it with auditors, not just the premium.** When `llm_p2aware` lands (chain2), run the frozen views (text, action, action_stats, combined) on it. "Which auditor survives a monitor-aware colluder" is the gap's question. Gap 7 (`llm_p2asym`): premium FPR + cost-adjusted markup only, and cite Q1.4 P2.4 (private costs: level screens 30/30 false). Gap 8 (`llm_p2coded`): **drop** unless chain2 reaches it before Sun 10:00.

Then: E92 logbook (once, via chain5, as registered) → one line in P2.5 and takeaways. Final sol/deepseek numbers replace the interim rows (chain4/6). One codex adversarial review of abstract + TL;DR + takeaways + P2.4–P2.6 after directive 1, and one more Sun ~13:00 after the finals.

## STOP doing
- **No new registered experiments beyond directives 2–5 and those already registered** (E89–E93). Six chains is the limit; no chain7+ unless it replaces one.
- No more interim snapshots + Opus review cycles per partial dataset (E93-style). Report interim numbers once, then replace them with finals.
- No glm (3 runs; **dropped**: deepseek with thinking off replaced it). No extra Claude seller runs (10 used, the cap).
- No provenance/manifest/EVIDENCE/presentation rebuilds until the Sun 16:30 window. Delete the export/provenance paragraph under the title from the reader path (move it to README) at the checkpoint.
- Don't grow REPORT.md. Each P2 section ≤ 20 lines + one table; P2.5 and P2.6 are ~40 lines each, so cut them. Takeaways ≤ 8 lines.
- Don't silently rewrite ledger timestamps that ran ahead of the clock (e.g. E92-amend "09:58"). Append one correction row that maps each affected row to its git commit time, so the registration chronology stays auditable. Stamp from `date -u` from now on.

## Cross-pollination
- **From Q1.4 → here:** (a) P2.7: across 5 wordings their channel effect holds (+0.69, I² = 0), but the no-channel baseline moves −0.19..+2.56. Your E78 shows the effect itself can vanish. Write the two side by side honestly, in the same terms; don't claim either generalises. (b) P2.9 deepseek *without a public board*: no-channel markets undercut Nash (−0.58), against 17.0 here *with* a public board. Q1.4 is directed to run a deepseek public-board arm. Cite it: public cheap talk is itself the coordination channel for deepseek, which supports directive 1(iii). (c) P2.4 all-firm cartel: pair-relative AUROC 0.25. Your random-partner arm (whole market +2.85, assigned-pair premium ~0) and Claude markets are the LLM instances. State the premium's blind spot with this citation. (d) Q1.4's E44 long games (final ~12:30) show the pair's lead decaying while the market stays high. That is the long-horizon version of your "opening-round only" agreements; cite it in P2.4. (e) P2.4 private cost asymmetry for gap 7.
- **From here → Q1.4:** E77 notepad and E92 logbook results (they cite them for level screens), E78, the family 3-way labels.
- **For the merger:** the shared sentence both REPORTs should contain: "Detectability of LLM collusion by any price statistic is a property of the (seller model × prompt) pair. Relative screens survive a shared model but fail under market-wide spillover; absolute screens need model- and prompt-matched references." Name the CI method in each precision caption (class-stratified bootstrap here, Jeffreys/Wilson in Q1.4).

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
  → **DONE** (E81, P2.1; premium precision@5% 0.24 test / 0.16 rep). Behaviour-label row: add from p2rep only if it's one line of code.
- **Independent reimplementation check:** have codex (gpt-6.1-sol, `-s workspace-write` in a scratch dir,
  given ONLY the REPORT's method description, not your code) reimplement your headline statistic(s); compare
  numbers on the same data. Report agreement; fix any bug found (and re-state affected numbers).
  → **DONE** (E83, P2.2: 31/32 match, one tie-handling difference, no bug).

## Gaps owned by THIS repo (Q2.2), in priority order (status as of 09:40 UTC)
1. **Is the "collusion" a prompt artifact?** (biggest validity threat). Round-1 prices already give AUROC
   0.90 and the undelivered placebo is flagged as often as delivered. Conditions (matched seeds):
   (a) current private-channel wording; (b) neutrally described channel ("a message box to firm X");
   (c) "notes to self" channel (same wording, no recipient); (d) channel to a random, changing partner;
   (e) placebo (offered, never delivered); (f) no channel. Measure round-1 premium, mean premium, and
   whether messages contain agreements. If the premium survives (b)/(d) but not (c), coordination is real;
   if (c) ≈ (a), the offer itself is the driver — either way that is a headline. Also 2–3 paraphrases of
   the base seller prompt as a wording-robustness band.
   → **DONE, one control running.** E77 (P2.5): notes − none +1.04 [+0.65, +1.42] vs private +1.61; H3 failed; delivery unresolved. E78 band: para2 +0.24 vs +1.75 (failed). Open: E92 logbook control (5/15, chain5 analyses once). Auditor views on the notes arm are in E89 (chain3); views on para2 are new (directive 3). Headline consequence → directive 1.
2. **Labels by behaviour, not condition**: break label = condition. Label every run from the private chat
   (agreement yes/no, judge tier="big" + Claude subset) AND realised behaviour (agreement followed?). Add
   channel-but-no-agreement runs and no-channel tacit-high runs; re-evaluate all auditors against the
   behaviour labels.
   → **MOSTLY DONE** (E84/E84b–e, P2.4: 14/50 followed; premium .80; Δ_hybrid −0.03 [−0.14, +0.06]; Claude second judge 24/30 class agreement; label sensitivity; tacit-high search 0 runs). Open: apply to p2rep (directive 2) and the 3-way family label (directive 4).
3. **Second (and third) seller family**: deepseek via Go (≥ 30 runs over private/none), gpt-6.1-sol
   sellers (~20 runs), Claude Sonnet sellers (≤ 10 runs). Do premium, text-adds-nothing, and the placebo
   effect replicate?
   → **IN PROGRESS** [priority 3]. Claude 10/10 DONE (+ E91 views). deepseek 24/30, sol 14/21 (finals via chain4/6, E91-ext views). glm **DROPPED** (3 runs; replaced by deepseek with thinking off). Answer as a 3-way label (directive 4). Note sol = same vendor as luna.
4. **Second replication of the premium statistic**: ≥ 60 fresh seeds, statistic frozen exactly as
   published (pre-register in EXPERIMENTS.tsv + data/SPLITS.md first). Removes the "chosen after seeing
   test data" bias.
   → **IN PROGRESS** [priority 1 for compute]. E80 registered; llm_p2rep 5/60 at 09:32, ETA ~11:00; then labels + E89 views (chain3). Report the condition and followed labels, and pooled with v1-rep (directive 2).
5. **Monitor-aware adversarial colluders**: tell the channel pair (and in a control, all firms) that a
   regulator screens price premiums over rivals / public messages. Does the premium collapse? Does
   collusion move elsewhere (smaller premium, alternation, text)? Which auditor survives?
   → **QUEUED** (E86, llm_p2aware 20 runs, chain2 after p2rep, ~11:00–11:30). Add frozen auditor views (directive 5).
6. **Explain the 0.98 supervised text classifier**: top TF-IDF features, ablate them, check if signal is
   style shift after channel offer (present in placebo / notes-to-self?) vs coordination content.
   → **DONE** (E82, E82b: diffuse signal; placebo 1.00, notes 0.86, own none 0.40). The classifier detects the condition, not coordination content.
7. **Cost asymmetry hard negative** for the premium: firms with legitimately lower costs / differentiated
   quality but no channel. Premium's FPR there; does a cost-adjusted markup fix it?
   → **QUEUED** (E87, llm_p2asym 20 runs, chain2). Premium FPR + cost-adjusted markup only; cite Q1.4 P2.4.
8. **Hidden signals in public text (exploration)**: one condition where the pair may agree on a code in the
   private channel and is told public messages are monitored; does any auditor catch coded public
   coordination? (Shows the limit of text auditing; one small condition is enough.)
   → **QUEUED, likely DROP** (E88, llm_p2coded 10 runs). Drop if chain2 hasn't reached it by Sun 10:00.
Items 1–4 must be done by Sat 20:00 if at all possible; 5–8 by Sun 15:00.

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

