# STATUS

## Current state (2026-10-23 21:50 UTC, end of iteration 3)
- **Generation** `llm_market.py --ds llm_v3` (125 runs) still running: ~0.65 runs/min → ETA ~00:15 UTC. Log `logs/llm_v3.log`.
- **pipeline.sh llm_v3** (bg) labels + audits new runs; auditors.py default views now include `action_stats`
  (actions + pair stats, no text = ablation of structured) → the loop backfills it for all runs automatically.
- **Claude cross-family** (bg): `auditors.py --auditor claude-sonnet-5-5 --subset mod3` (runs with index%3==0, ~42),
  log `logs/claude_audit.log`. Re-run same command after generation ends (+ `--views action_stats,structured` check).
- Locked split frozen: `data/SPLITS.md` (dev 0000–0029, test 0030–0124; 0 tuning attempts). EXPERIMENTS.tsv started.
- Interim (n=36, 24 pos), GPT auditor pair-AUROC: text .58, action .78, combined .76, structured .86;
  Δ_struct(pair) +.086 [.006,.171]. Non-LLM LR: action .99, text .82 → ceiling. Public text 0/32 explicit (hardset.py).
- Key open question: structured gain = stats table or cross-modal? First look (n=40): action_stats ≈ structured
  (Δ −.024 [−.06,.005]); action_stats − action +.105 [.04,.17] → gain is from computed stats, not text. Views
  `action_stats` + `combined_stats` now in default auditor views (pipeline backfills). analyze_llm adds
  within-market AUROC, paired view contrasts, NaN-safe p_le_0.

- 22:10 codex interim review (`logs/review_interim.md`) → FIXED: legit runs lacked public partnership info in audits
  (all legit audits invalidated, pipeline restarted 22:10 and re-auditing); hard-set keyword fallback; failed LLM
  hard-set checks no longer cached. Interim numbers above predate this fix.

## Next steps (priority)
0. From review (still TODO): (a) shuffle donors change when the pool grows → run the LLM shuffle variant ONCE
   on the final cohort with a persisted donor map (results/.../shuffle_donors.json) + several seeds; include
   `action` comparator; (b) add view `combined_stats` (combined + pair stats, no stated-vs-actual table) so
   action_stats→combined_stats isolates text and combined_stats→structured isolates the consistency table;
   (c) within-market pair AUROC on positive runs; NaN-safe p_le_0; (d) baselines argmax tie bias; cross_family
   top-pair ties; (e) don't call repeated all-run analyses "locked" — compute test-only once at the end;
   (f) manual check of a stratified label sample.
1. When ≥90 runs: `hardset.py`, `analyze_llm.py` (all + `--split test`), baselines LR; shuffle variant
   (`auditors.py --variant shuffle --views text,combined,structured`) and pad (`--variant pad --views text,action`).
2. Claude subset: rerun `auditors.py --auditor claude-sonnet-5-5 --subset mod3` (+action_stats) after gen ends, then
   `cross_family.py` (written; n=12 so far: both auditors rank structured top, Spearman .74 on structured).
   Read `logs/review_interim.md` (codex critique of interim design, launched 21:50) and act on it.
3. Figures (AUROC bars w/ CIs, Δ forest plot, action_stats vs structured) → REPORT; codex adversarial review of claims.
4. Exploration: tacit `none` runs with supra-competitive prices (label = tacit) — how auditors score them.
- Sibling `collusion-14-infotheory/data/llm_v1`: T=20, empty public messages in cond A → not poolable for text auditing.
- Risks: action ceiling for trained baselines; label ≈ condition; same-family sellers/auditor; generation slow.

## Log
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
