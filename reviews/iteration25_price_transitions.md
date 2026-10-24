# Iteration 25 — price-transition source census

Scope: a selective, deterministic source check of leading price-transition
clauses in the six original GPT views on already-exposed test and replication
data. No seller generation, new scientific model audits, private-chat label
judging, AUROC/bootstrap calculations, threshold fitting, or changes to frozen
detection results. Model calls below were implementation/claims reviews.

Independent Codex gpt-6.1-sol (read-only, high reasoning) and Claude Opus 5.5
(Read/Glob/Grep only) reviewed the implementation, caches and report additions.
Codex independently recounted the raw items and checked every selected item's
endpoints for every named firm. Opus independently reproduced the selected-item
counts using raw-cache searches and checked the historical example; it did not
execute tests or recount the full denominators. Its statements about unfinished
exports/manifest described an earlier working-tree snapshot.

Findings and resolutions:

- Both critics confirmed 51/2,229 selected test items and 6/696 replication
  items; 54 adjacent endpoint matches and three earlier-start matches. Nine
  multi-firm items require all named firms to match. These are repeated-view
  item counts, not independent trajectories or semantic accuracy estimates.
- Opus identified selection bias: the grammar skips modifiers such as jointly
  and simultaneously, and verbs such as decrease/fall/rise. The report and
  README now explicitly limit assurance about collusion-alleging evidence.
  The validation grammar was not widened. A review-added lexical diagnostic
  exposes 52 additional unparsed test items and 17 replication items containing
  numeric from-to spans anywhere in the observation. They can describe costs,
  later clauses or quoted wording. They receive no endpoint status or semantic
  label and never add successes. A negative-control test enforces this separation.
- The source example is illustrative, not a correction or re-estimate of the
  historical dev/test regex rates. Source prices 18 → 16 → 14 demonstrate why
  both the same-round and ±1-round proxies can reject endpoint-consistent
  descriptions. A test reads the frozen historical regex as syntax, without
  importing/running its analysis module, and confirms both failures.
- Replace “correct transition” with “endpoint-consistent transition.” Numeric
  matches establish neither intermediate paths nor duration, rival behaviour,
  market context, later clauses, causal interpretation or coordination.
- Remove any implication of external advance registration. The scope was
  self-reported before implementation, but there was no pre-computation commit
  or external registration. All these analyses are explicitly post-hoc.
- Tie REPORT and README coverage/endpoint counts, the zero-conflict claim,
  and the new omitted-span counts to reconstructed output. Preserve unparsed
  and malformed-anchor items in the denominator; test multi-firm mismatches,
  missing prior history, alternate endpoints, decimals, negations and modal text.
- During implementation the manager found conjunction letters being read as
  firm IDs; word-boundary tokenization fixed this before the final census.
  Synthetic compound-subject tests cover the bug. This was an implementation
  repair, not a search for higher source agreement.
- Refresh exports and the post-hoc manifest after finalizing prose/code.
  Existing manifest update/extension history is preserved. The first Codex
  recheck passed; a second focused check independently reproduced the lexical
  diagnostic counts, verified disjointness from parsed items and found
  **no consequential findings**.

Manager verification:

- `uv run python -m unittest discover -s tests -v`: **47 tests pass**, including
  eleven new transition/coverage tests. Missing private/label/ground-truth files
  do not prevent the new checker from running. Corruption and prose drift fail
  without writes.
- Standard-library verifier: **412 hashes** pass, including saved evaluation
  arithmetic, all prior receipts, fresh exports and both source censuses.
- Cached prompt checker remains **1,903 recorded hash matches / 310 length-only**.
- Exports preserve **26 report pages**, 18 headings, 317 table cells, 444 report
  text fragments and eight figures; talk remains seven pages / 100 fragments.
- Clean Git-index export without local evaluation locks passes six read-only
  checkers and refuses the completed headline entry point. File hashes,
  modification times and inventory are unchanged by those commands. The
  exported repository remains below the 100 MB limit.
- **403 pre-existing manifested artifacts remain byte-identical**. Only verifier
  code and four report/export artifacts change; four manifested files are added.
  Every original scientific dataset, cache, result, figure, analysis and
  evaluation/provenance receipt is unchanged. No estimates are recomputed.

Residual parser limits include natural-language ambiguity from case-insensitive
firm tokens, explicit subject binding overriding the citation anchor, and any
earlier round being eligible as a start. The selected frozen items were checked
against raw sources; these rules are not a general semantic validator. The
text-only view yields no parsed price transitions. Explanation quality remains
unvalidated, and the matched subset is particularly restrictive for coordination
claims.
