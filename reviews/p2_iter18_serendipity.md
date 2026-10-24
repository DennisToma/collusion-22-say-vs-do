# Iteration 18: E108 transcript exploration and review

Two Codex helpers read the frozen 40-game sample, 20 transcripts each; the q14
reader then independently checked the new calculations and reviewed their scope.
No helper wrote files, contacted another service, or inspected in-flight strongF.
This review did not use Claude while its manager quota was recovering.

The independent q14 calculation reproduced all eight opening-target rows and both
q14 disclaimer rows: 37/40 within-band rounds versus 1/40 exactly at target,
28 consecutive asymmetric rounds, and premiums +0.567 / +1.694. The q22 reader's
independent counts matched the script: 10/20 final transitions with a price drop,
21/80 dropping firms; 3/8 and 3/32 with public state unchanged; 143 narrow own-price
declarations (72 private / 71 public), zero same-response mismatches.

All five framing findings were applied:

1. Relative observed profit is not a competitive counterfactual. E108c describes
   constant pricing despite earning less than every rival; its broad initial
   mutual-profitability question remains inconclusive.
2. Final-transition counts cover mixed conditions and all firms. Claude's withdrawal
   and GLM's continued commitment are selected counterexamples, not an estimated
   rate of colluder defection or a causal horizon effect.
3. Messages and prices are generated in the same response. Zero contradictions
   among 143 narrow matches checks field consistency, not temporal honesty or
   promise keeping; observations cluster in ten games.
4. Q1.4's original pilot uses a ±1 band; Q2.2 uses a lower-bound floor. Removed
   REPORT's incorrect equality claim. Their E66 cross-repo adapter explicitly
   mirrors Q2.2's lower-bound rule, so the pending shared-class handoff remains
   consistent; no execution rule, frozen label or registered analysis changed.
5. Corrected a code comment that suggested before/after disclaimer comparisons;
   only at-or-after summaries are produced. Numbers in private text include costs
   and past prices and are not semantic disclosure classifications.

Further safeguards: the opening-only scope of many promises is explicit; focal
12/13 persistence is not automatically collusion; lexical disclaimers/equality
cannot identify intent or causal coordination; dataset-balanced sampling overweights
old small pilots and cannot estimate population prevalence. All checks are post hoc.

Verification: all 40 portable transcripts and original selected-dataset blob hashes
were compared with the recorded git objects, including ground truth and private chat.
Sample hash, count, order, unique IDs, expected horizon and contiguous four-firm
rounds pass. Analysis regeneration is byte-identical; a second freeze refuses
without changing the archive. Independent main-agent endpoint/rigidity census
matches the JSON. The case figure was generated and visually inspected; its profit
totals assert equality with the analysis. Existing 17 strongF completion tests and
the read-only transition-source checker pass. Static exports/manifest were not rebuilt.
