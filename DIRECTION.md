# DIRECTION — Phase 2, director review 2026-10-24 07:40 UTC (Sat)

**Verdict.**
1. Good design discipline: E77–E88 are all registered before data, an Opus design review was applied before any outcome, and shared gaps plus gaps 2 and 6 are done. E84 is a real finding: most "colluders" abandon the agreement, and the premium detects *attempts*. But the repo is generation-bound: one serial chain of ~195 luna runs (ETA ~11:00) plus a near-stalled second family (glm 2/30).
2. The Q2.2 question (does text + actions beat either alone?) has quietly dropped out of Phase 2. No new data gets the 4 auditor views, and Δ_hybrid against the new behaviour label is not stated. Phase 2 is turning into a premium-validity project, which is Q1.4-adjacent. Bring the text-vs-action contrast back into every new dataset.
3. Biggest risk for Sat 20:00: gap 3. "Second seller family" is currently one Go model at ~1 run per 2 h, and no gpt-6.1-sol or Claude seller runs have started. Second risk: the cue result (gap 1) arrives ~08:30 and must be written against the registered pattern, not re-interpreted.

## Top directives (in priority order)

1. **Gap 1 write-up exactly against E77 + amendment (when `llm_p2cue` is analysed, ~08:30–09:00).** Report the full registered contrast pattern on r2_12 (private − neutral, private − notes, private − randpartner partner_gap, placebo − none, notes − none), with paired CIs and the ±0.5 equivalence verdicts. Report round-1 premium and the judge's "agreement in messages" rate per arm. Add one figure: per-round pair premium by arm. Then re-run `p2_textlr.py` with the new arms: is notes-to-self flagged like placebo? That is what separates "offer-induced style" from "intended coordination", and it is the payoff of P2.3. Whatever the pattern, it goes in the TL;DR. Do not soften a "the offer itself drives it" outcome.
2. **Gap 3: start the non-Go families now. Don't wait for Go.** (a) Port Q1.4's 2-line deepseek fix from `../collusion-14-infotheory/llm.py` (`body["thinking"] = {"type": "disabled"}` for `deepseek*`). If deepseek with thinking off is faster per run than glm at max_tokens=6000, switch the Go run to deepseek and log the deviation. Q1.4 runs deepseek too, so the umbrella gets one non-OpenAI family in *both* markets. (b) Launch gpt-6.1-sol sellers, matched private/none/placebo × 7 seeds (~20 runs, codex quota), in parallel with the luna chain (keep total parallelism ≤ 6). (c) Claude Sonnet sellers: private/none × 5 seeds (10 runs), matched seeds. Register each as an amendment to E79 before generation. Note in the REPORT that sol is the same vendor as luna (Q1.4 P2.3 shows family matching matters), so only Go and Claude count as cross-family.
3. **Bring Δ_hybrid back.** (a) Now, no new calls: add the RQ number to P2.4. That is combined − max(text, action_stats) against the *followed* label, paired bootstrap CI, test and replication. (b) Register before p2rep finishes: run the frozen 4 auditor views (text, action_stats, combined, structured; same prompts, same sol model) on `llm_p2rep` (60 runs, ~240 calls) and on the private/placebo/notes/none arms of `llm_p2cue`. Then gap 4 replicates the paper's *headline* (Δ_hybrid ≈ 0, statistics table helps), not only the premium. The pooled replication n goes from 30 to 90, which is what's needed to resolve Δ.
4. **Gap 4 + gap 2 on fresh data.** When `llm_p2rep` lands, compute the frozen premium AUROC ONCE (E80; write the script and freeze it first), and apply `p2_behaviour.py` (registered as an E84 replication before running). With 30 private runs you get more *followed* positives than the current 14/5. Add a label-sensitivity row: floor − 2, and followed in ≥ 1/3 of rounds. Add a Claude Sonnet re-extraction of agreement terms on ~30 chats, because "start at 18 = opening-round only" decides the followed/abandoned split. Search the `none` arms of p2cue/p2rep for tacit-high runs; the first glm `none` run already sits at 14–15 vs Nash 11. If any exist, report the auditors on that label.
5. **Checkpoint (Sat 19:30).** Add a 5-line "Phase 2 takeaways" block at the top of the Phase 2 section, the way Q1.4 does. One sentence per gap with number, CI and source JSON, so the merging manager (Sun 08:00) can lift it. Update TL;DR item 6. Rebuild exports ONCE at the checkpoint.

Then (Sun, by 15:00): gaps 5 → 7 → 8 from `p2_chain2.sh` (already registered). For gap 5, include the frozen action_stats and text views, not only the premium; "which auditor survives" is the gap's question. For gap 7, cite Q1.4 P2.4: with *private* costs, level screens flag 30/30, so a cost-adjusted markup only helps when costs are observable. Consider starting chain2 now in parallel with p2rep rather than strictly after it, if codex throughput allows ≤ 6 parallel.

## STOP doing
- No more provenance/verification infrastructure: manifests, receipts, PRICE_TRANSITIONS.md, EVIDENCE.html, browser QA of slides, hash ledgers. v1 is frozen at a tag; rebuild the manifest once in the finalize window. Overnight iterations 19–31 went almost entirely here.
- No per-iteration export/PDF rebuilds (checkpoint + finalize only).
- Don't grow the REPORT further. It is ~1000 lines. Move v1 exploration strata and appendices out of the reader's path before adding P2.5+, and keep each P2 section ≤ 20 lines plus a table.
- Don't treat glm as the only route to gap 3, and don't wait on Go (directive 2).
- Don't re-litigate premium selection disclosure; it's disclosed. Spend the words on what the new data shows.

## Cross-pollination
- **From Q1.4 → here:** (a) the deepseek thinking-off fix (directive 2a). (b) P2.4 private cost asymmetry (level screens 30/30 false, pCMI ~ control): cite it in gap 7. (c) P2.3: same-model no-channel pairs don't hurt *pair-relative* level screens, but absolute statistics need model-matched references. This matters for interpreting the premium under sol/Claude sellers. (d) P2.4 all-firm cartel: relative statistics like the pair premium have AUROC 0.25, a limitation to state for the premium. (e) The CUSUM online screen (P2.4) next to your round-1 / early-detection result.
- **From here → Q1.4:** E84 behaviour labels and `p2_behaviour.py` (they are directed to apply them to their C games), and `llm_p2cue` labels. Publish `data/llm_p2cue/` labels promptly; Q1.4 will run frozen detectors on it as they did on llm_v3plc/mon.
- For the merger: your precision@prevalence uses class-stratified bootstrap, Q1.4's uses Jeffreys. Name the method in the table caption.

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
  → **DONE** (E81, REPORT P2.1; premium precision@5% 0.24 test / 0.16 rep). Add a behaviour-label row once p2rep exists, if cheap.
- **Independent reimplementation check:** have codex (gpt-6.1-sol, `-s workspace-write` in a scratch dir,
  given ONLY the REPORT's method description, not your code) reimplement your headline statistic(s); compare
  numbers on the same data. Report agreement; fix any bug found (and re-state affected numbers).
  → **DONE** (E83, REPORT P2.2: 31/32 match, one tie-handling difference, no bug).

## Gaps owned by THIS repo (Q2.2), in priority order (status as of 07:40 UTC; re-prioritised order in brackets)
1. **Is the "collusion" a prompt artifact?** (biggest validity threat). Round-1 prices already give AUROC
   0.90 and the undelivered placebo is flagged as often as delivered. Conditions (matched seeds):
   (a) current private-channel wording; (b) neutrally described channel ("a message box to firm X");
   (c) "notes to self" channel (same wording, no recipient); (d) channel to a random, changing partner;
   (e) placebo (offered, never delivered); (f) no channel. Measure round-1 premium, mean premium, and
   whether messages contain agreements. If the premium survives (b)/(d) but not (c), coordination is real;
   if (c) ≈ (a), the offer itself is the driver — either way that is a headline. Also 2–3 paraphrases of
   the base seller prompt as a wording-robustness band.
   → **IN PROGRESS** [priority 1]. llm_p2cue 45/90 runs at 07:28, ETA ~08:30, auto-labelled + analysed by p2_post.sh; para1/para2 (40) queued next. Registered pattern E77 + amendment (directive 1).
2. **Labels by behaviour, not condition**: break label = condition. Label every run from the private chat
   (agreement yes/no, judge tier="big" + Claude subset) AND realised behaviour (agreement followed?). Add
   channel-but-no-agreement runs and no-channel tacit-high runs; re-evaluate all auditors against the
   behaviour labels.
   → **PARTLY DONE** [priority 4]. E84 on llm_v3 test + rep (P2.4: only 14/50 followed; premium 0.80 vs followed). Open: Claude subset of term extraction, label-sensitivity rows, application to p2cue/p2rep, tacit-high search (0 so far), and Δ_hybrid against this label (directives 3a, 4).
3. **Second (and third) seller family**: deepseek via Go (≥ 30 runs over private/none), gpt-6.1-sol
   sellers (~20 runs), Claude Sonnet sellers (≤ 10 runs). Do premium, text-adds-nothing, and the placebo
   effect replicate?
   → **IN PROGRESS, AT RISK** [priority 2]. deepseek aborted (hidden reasoning), glm-5.3-flash 2/30 at ~1 run/2 h. sol and Claude sellers **NOT STARTED**: start now (directive 2).
4. **Second replication of the premium statistic**: ≥ 60 fresh seeds, statistic frozen exactly as
   published (pre-register in EXPERIMENTS.tsv + data/SPLITS.md first). Removes the "chosen after seeing
   test data" bias.
   → **REGISTERED, QUEUED** [priority 3]. E80; llm_p2rep (30 private / 20 none / 10 legit) after para1/2, ETA ~10:00–11:00. Extend to the 4 auditor views (directive 3b).
5. **Monitor-aware adversarial colluders**: tell the channel pair (and in a control, all firms) that a
   regulator screens price premiums over rivals / public messages. Does the premium collapse? Does
   collusion move elsewhere (smaller premium, alternation, text)? Which auditor survives?
   → **REGISTERED, QUEUED** (E86, llm_p2aware 20 runs in chain2). Needs the auditor views to answer "which auditor survives".
6. **Explain the 0.98 supervised text classifier**: top TF-IDF features, ablate them, check if signal is
   style shift after channel offer (present in placebo / notes-to-self?) vs coordination content.
   → **MOSTLY DONE** (E82, P2.3: diffuse signal, placebo AUROC 1.00). Remaining: score the notes-to-self / neutral / randpartner arms of llm_p2cue (directive 1).
7. **Cost asymmetry hard negative** for the premium: firms with legitimately lower costs / differentiated
   quality but no channel. Premium's FPR there; does a cost-adjusted markup fix it?
   → **REGISTERED, QUEUED** (E87, llm_p2asym 20 runs, public costs/quality). Cite Q1.4 P2.4 for the private-cost case.
8. **Hidden signals in public text (exploration)**: one condition where the pair may agree on a code in the
   private channel and is told public messages are monitored; does any auditor catch coded public
   coordination? (Shows the limit of text auditing; one small condition is enough.)
   → **REGISTERED, QUEUED** (E88, llm_p2coded 10 runs). Lowest priority; drop if chain2 runs past Sun 13:00.
Items 1–4 must be done by Sat 20:00 if at all possible; 5–8 by Sun 15:00.
