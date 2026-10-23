# STATUS

## Current state (2026-10-23 22:30 UTC, end of iteration 4)
- **Generation** llm_v3 running (~60/125, ETA ~00:00 UTC); `pipeline.sh llm_v3` labels + audits (6 views) in bg.
- **Frozen analysis** `final_analysis.py` (+ `evidence.py`, `gallery.py`), codex-reviewed (`logs/review_final_analysis.md`,
  9 fixes applied). Headline = `final_analysis.py --split test` run ONCE; it asserts every view audited every run.
  Primary endpoints: run AUROC + within-market AUROC; comparators: untrained pair premium, dev-fitted late fusion.
- **Dev (n=30, 20 pos)**: run AUROC premium 1.00 · action_stats .89 · structured .83 · combined .83 · fusion .83 ·
  action .78 · text .58. Within-market: premium .98, structured/action_stats .91, action/combined .85, text .62.
  → text adds nothing; stats table helps; untrained premium beats all LLM views. Evidence: cited firm in colluding
  pair ≈ chance (47–59%). Gallery: legit pair has +premium, LLM discounts it via public partnership notice.
- Input repairs done: prompt-hash/len cache check (0 stale), frozen context-matched shuffle donors, tie-aware argmax/top-pair.
## Next steps
1. When generation ends (~00:00): launch shuffle ablation on TEST runs, 3 seeds, in parallel with pipeline:
   `for s in 0 1 2; do uv run python auditors.py --ds llm_v3 --variant shuffle --shuffle-seed $s --only-test --views combined,structured,text --workers 2; done`
   (text only needed for seed 0 — use `--views combined,structured` for seeds 1,2). Then add intact−shuffled paired
   contrast script (reuse orig action scores). Claude subset re-run: `auditors.py --auditor claude-sonnet-5-5 --subset mod3`
   (all 6 views), then `cross_family.py`.
2. After all orig audits complete: `final_analysis.py --split test` ONCE, `evidence.py --split test`, `gallery.py --split test`, `make_figures.py --split test`,
   baselines LR on test; figures; REPORT headline; codex review of REPORT claims.
3. Optional (if codex idle by 01:00): 15–20 firm-framing private runs as "channel, no agreement" stratum (separate).
- Risks: audit throughput (~5 sol calls/min shared); dev base rate 2/3 → dev thresholds weak; label = communication.

## Log
- 22:30 iter 4: input repairs (prompt hash check, frozen donor maps, ties); final_analysis.py frozen after codex
  review; evidence.py, gallery.py; dev results in REPORT (premium dominates; text adds nothing); SPLITS: headline=test once.
- 21:55 iter 3: SPLITS.md + EXPERIMENTS.tsv; hardset.py (0/32 flagged); baselines on llm_v3 (donor fallback for tiny
  folds, counted); analyze_llm --split + hardset flags; action_stats ablation view; Claude Sonnet subset launched;
  REPORT interim LLM section.
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
