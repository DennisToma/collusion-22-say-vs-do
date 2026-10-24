# Iteration 31 — summary claims and presentation handoff

Scope: finalization of existing results, with no seller generation, scientific
LLM audits, label judging, AUROC/bootstrap recomputation, threshold fitting, or
changes to detection estimates. Reviewer model calls were claims reviews only.

## Independent review and wording changes

A read-only Codex gpt-6.1-sol critic checked the report opening, README and talk
against saved JSON. It found no headline numerical mismatches and recommended:

- Remove the TL;DR's causal explanation of weak zero-shot text performance.
  Zero explicit-public-screen flags do not establish that public text lacks
  information; supervised text CV demonstrates a learnable trace.
- Replace the claim that all detectors respond to the channel offer with the
  observed placebo result. Flags without delivery neither identify each
  detector's cues nor establish equivalence between placebo and delivered arms.
- Use run-level, uncertainty-aware wording for the 0.47 text estimate; separate
  detection from within-market localisation and scope statistics gains by split.
- Add the recent E74 label check to slide 2 and update the stale monitor-section
  caveat that described only one judge.

Claude Opus 5.5 independently reviewed an in-memory snapshot of the revised
opening, presenter notes and saved test/replication/ablation/label values with
no tools. It confirmed the supplied numbers and requested clearer language:

- Replaced ambiguous "nominal" with "unadjusted within-market localisation" in
  the short summary and talk. "Nominal" had meant uncorrected for multiplicity,
  not unresolved; the test interval excludes zero. No statistical conclusion
  changed, and the gain still did not repeat on fresh data.
- Clarified that statistics are always supplied with raw action logs. The
  earlier "no text + statistics view" meant no such view without raw actions;
  combined_stats does exist. The abstract now enumerates the relationship.
- Added the label-check composition (85 positive / 30 negative; every stratum
  uniform) to speaker notes and Q&A. Agreement is not ground truth or a test of
  within-stratum discrimination. Independently reading the raw label caches
  reproduced all 115 binary agreements, class counts, model and run coverage.
- Scoped the premium's highest point estimate to run AUROC, qualified its
  unresolved replication lead, and softened attribution to channel offer or
  prompt framing. Round-1 0.90 is independently sourced from the existing
  early_detection JSON, not the rounds-2+ scorer.

Raw critic outputs were saved locally to `/var/tmp/iter31_summary_review.txt`
and `/var/tmp/iter31_opus_review.txt`; this tracked record preserves the findings
and decisions. Six source-linked judge answers are generated in PRESENTATION.md,
with their saved-input hashes. They add no scientific estimates or extra slides.

## Browser finding and repair

The initial layout probe only sent arrow keys without asserting slide IDs.
Screenshots exposed that it had stayed on slide 1: clicking Present leaves the
button focused, and the keyboard handler ignored every event from a button.
The strengthened check asserts every actual slide transition before measuring
layout. The original committed HTML reproduces the failure; the fixed HTML
advances with the same interaction.

Arrow/Page/Home/End/Escape shortcuts now work with focused presentation controls;
native Space activation of buttons remains intact. The corrected all-slide
check also found slide 3 overflowing at 1024 x 768; a shorter title fixed it.
All seven slides pass at 1440 x 900, 1366 x 768, 1280 x 720, 1024 x 768 and
1920 x 1080. Mobile reading/presentation has no horizontal overflow. Reading
without JavaScript exposes all seven slides, with no remote requests.
The standalone old/fixed comparison was rerun in the pinned handoff environment
after an initial system-Python invocation lacked Playwright.

## Verification

Exports retain seven talk pages, 28 report pages, 18 headings, 341 table cells,
477 report text fragments, 102 slide fragments and eight embedded figures.
The standard-library manifest verifier passes all 424 hashes. Of the previous
424 manifested files, 417 remain identical: only presentation rendering code,
talk HTML/notes/PDF, report HTML/PDF and the export receipt change.
Every scientific dataset, label cache, audit cache, result, figure, analysis
module and scientific/input receipt remains byte-identical. The manifest update
is post-hoc preservation, not registration evidence.

Final checks: 47 existing isolation tests; 2,368 cached audit inputs (2,058
recorded prompt hashes / 310 length-only rows); presentation/export freshness;
evidence and transition-ledger freshness; clean Git-index export without local
evaluation locks; completed headline/replication refusal; write-free exported
verification. No locked analysis was rerun.
