# STATUS

## Current state (2026-10-23 21:15 UTC, end of iteration 2)
- **Headline data generating in background:** `llm_market.py --ds llm_v3` (125 runs: 70 private / 35 none /
  20 legit, lab framing, gpt-6-luna sellers, 12 rounds), ~1.5 runs/min → ETA ~23:45 UTC. Log: `logs/llm_v3.log`.
- **Background loop `pipeline.sh llm_v3`** labels finished runs (judge = gpt-6.1-sol, private chat ONLY) and audits
  them (4 views, orig variant). Log: `logs/pipeline.log`. If it died: `nohup ./pipeline.sh llm_v3 > logs/pipeline.log 2>&1 &`
  (generation resumes exact ids: rerun the same llm_market command).
- Labels so far (19 runs): 14/15 private pairs → explicit agreement, 1 info_exchange. Pair price premium often ~0
  (rivals drift up too; a `none` run also ended all-at-14 = tacit supra-competitive pricing).
- Preliminary LLM-auditor numbers (n=14, 3 negatives — NOT reportable yet): pair-AUROC text .58, action .72,
  combined .74, structured .83.
- Scripted: scripted_v1 saturated (action AUROC 1.0). scripted_v2 (weak collusion) = mechanism demo:
  LR, fold-local same-condition shuffle: text .839/.837, action .951/.951, combined .961/.961, structured 1.00/.748
  (intact/shuffled run-AUROC); Δ_structured +.049 [.027,.079]. GBM version was still running at 21:35
  (`logs/baselines_scripted_v2_gbm.log` → results/baselines/scripted_v2_gbm.json) — check it.
- Methodology review done (`logs/review_methodology.md`); fixes 1-5,8(partly),10,11,12 applied.

## Next steps (priority)
1. When ≥60 runs labelled: `analyze_llm.py`; run shuffle variant (`auditors.py --variant shuffle --views text,combined,structured`).
2. Length control: run `auditors.py --variant pad --views text,action` (implemented, not yet run).
3. Cross-family: Claude auditor (`--auditor claude-sonnet-5-5`, use `--disallowedTools`/run in /var/tmp; isolate tools)
   on stratified ~40 runs × 4 views.
4. Non-LLM baselines on llm_v3 (`baselines.py --ds llm_v3`; features.py claim parser is template-specific → only
   TF-IDF + action features meaningful).
5. Figures + REPORT; codex review of final claims.
- Risks: label is ≈ condition (almost every private pair agrees) → task is effectively "private vs none/legit";
  few info_exchange/none-agreement private runs. Same-family (GPT) sellers/auditor.

## Log
- 21:35 fold-local shuffle donors in baselines.py (fixes donor-memorisation leak); `--variant pad` length control
  added to auditors.py; Claude auditor call isolated (no tools, /var/tmp cwd) and tested OK on 1 run.
- 20:28 iter 2 start. Built llm_market.py, baselines.py, show_run.py, label_llm.py, auditors.py, analyze_llm.py, pipeline.sh.
- Pilots: firm+regulator framing → luna sellers refuse to coordinate (data/llm_v2, /var/tmp/llm_v1_pilot0);
  lab framing → private intention exchange + lockstep (data/pilot_lab_luna). Chose lab + luna for llm_v3.
- 20:41 launched llm_v3. codex methodology review → fixed label leakage (judge no longer sees prices; primary label
  = communication), combined/structured now strict superset (units+profit), public partnership info in
  `public_info.jsonl`, strict parse + failure log + no silent model fallback, exact-id resume, LR for all
  baseline feature sets (GBM optional), price-context number extraction, same-condition shuffle donors.
- 20:50 scripted_v2 generated (levels 12/14, strength .15–.5).
