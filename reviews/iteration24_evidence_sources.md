# Iteration 24 — cached evidence and public sources

Scope: a deterministic source ledger for the six original GPT auditor views on
95 already-exposed test runs and 30 already-exposed replication runs. No seller
generation, label judging, new LLM audits, AUROC/bootstrap calculations, threshold
fitting, or primary-result changes. Model calls below are independent reviews of
the implementation and claims, not scientific data generation.

Independent Codex gpt-6.1-sol (read-only, high reasoning) and Claude Opus 5.5
(Read/Glob/Grep only) checked the code, cached outputs and added report prose.
Both independently confirmed 2,229 + 696 = 2,925 evidence items, four quote-marked
phrases (all text-view), literal presence in the cited firm's cited-round message,
and unchanged scientific inputs. Codex additionally compared every HTML claim
against the cached observation and found exact preservation of all 2,925, no
duplicate IDs, broken fragment links or external rendering dependencies.

Findings and resolutions:

- Unquoted observations were not semantically classified. Remove the inferred
  statement that most are paraphrases/price claims. The report now says that the
  remaining items lack quote-marked spans and were not semantically classified.
- A located phrase and an existing source anchor do not validate relevance or
  inference. Use "well-formed" for integer-round/firm anchors; disclose that all
  four marked items come from the text view and two repeat generic "considered
  price" wording occurring across several firms/rounds. The LLM explanation
  role is explicitly unvalidated, including in the hint-view recommendation.
- Invalid anchors could receive ordinary source locations through Python's
  equality of True / 1.0 with 1, or through partial firm/round matches. Add an
  explicit invalid_anchor category, preserve all literal hits, and test malformed
  round and firm types without dropping them from the item denominator.
- Bind the new report/README coverage sentences to computed JSON counts during
  read-only freshness checks. An intentional prose-count edit is rejected.
- Keep numeric and multiline marked spans; fail clearly on non-string
  observations. Test these cases and disclose the delimiter parser's ambiguity
  for same-style nesting/plural possessives. This ambiguity is absent from the
  four observed marked spans; the extractor is not a general semantic quote judge.
- Source logs are open by default without JavaScript and collapsed by the fixed
  script when enabled. No-JavaScript source navigation works in Chromium.
- Add a public-setup corruption test as well as audit-cache corruption, and
  distinguish not opening private-chat/label files from ignoring injected
  private fields in public trajectory agents.

The final focused Codex recheck found **no consequential findings** after these
fixes; five targeted literal unit tests and the source freshness check passed.

Manager verification:

- Full suite: **36 tests pass**, including nine new source-ledger tests.
- Offline verifier: **408 hashes**, unchanged saved arithmetic and evaluation
  receipts, existing 2,213-input provenance check, and fresh evidence ledger.
- Cached prompt checker: **1,903 recorded hash matches / 310 length-only**,
  unchanged; historical authentication limits remain explicit.
- Browser: 125 runs, 750 audits, 2,925 items, 1,500 rounds and 6,000 firm
  observations present. Search/dataset/view/marked-span filters, source links
  with and without JavaScript, 390-pixel layout, zero network requests pass.
  Two initial browser assertions selected another item in the same four-item
  audit; correcting the test to target the marked item's round made them pass.
- Refreshed exports: **26 report pages**, 18 headings, 317 cells, 443 text
  fragments, eight figures; presentation remains seven pages / 100 fragments.
  Exporter checks preservation of the report text and table contents.
- Clean Git-index export, without local evaluation locks: all five read-only
  checkers and completed-headline refusal pass with file hashes, modification
  times and the complete inventory unchanged.
- Every pre-existing manifested scientific data/cache/result/figure/analysis
  artifact and original evaluation/provenance receipt stays byte-identical.
  Only the verifier and report/export artifacts change, alongside four new
  manifested ledger/code/test artifacts. Manifest extension is post-hoc.

The four literal matches validate neither the surrounding observations nor the
remaining evidence. This is a coverage census and a review aid, not a new semantic
accuracy estimate or a positive result for the proposed explanation architecture.
