# STATUS

## Current state (2026-10-23 ~21:00 UTC, iteration 2)
- Scripted set `data/scripted_v1` (320 runs, 8 conditions) + `features.py` + `baselines.py` run end-to-end
  (gate part 1 passes mechanically). BUT action features saturate (AUROC 1.0) → scripted set too easy on
  actions; Δ_hybrid is 0 there by ceiling. Needs weaker/noisier collusion before it says anything.
  Shuffle ablation already shows the GBM "structured" model leans on say-vs-do features (AUROC 1.0 → 0.48
  when messages are shuffled), while raw "combined" is unaffected.
- `llm_market.py` (LLM sellers, conditions private/none/legit, cached per decision) works; ~45 s/game.
- **Pilot finding:** gpt-6-luna sellers with "firm + competition-authority" framing do NOT collude even with a
  private channel ("I'll price independently...") and their public messages are near-identical boilerplate.
  Testing economics-lab framing (no regulator mention) with luna and gpt-6.1-sol sellers; Go/deepseek next.
- Next: pick framing/model that yields some verified agreements → launch ≥120 runs in background →
  label_llm.py (big judge on private chat) → LLM auditors A–D.
- Risks: LLM sellers may never collude (then report as negative result + use tacit/none contrast);
  text modality may be uninformative boilerplate on LLM data.

## Log
- 20:28 iter 2 start. Built llm_market.py, baselines.py, show_run.py. Pilots: data moved to /var/tmp (pilot0),
  data/llm_v2 (3 private runs, "firm" framing v0.2: zero collusion).
