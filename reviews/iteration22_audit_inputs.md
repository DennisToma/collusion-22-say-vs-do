# Iteration 22 — cached auditor input provenance

Scope: post-hoc reconstruction of existing auditor inputs. No seller generation,
label judging, LLM auditing, AUROC/bootstrap computation, or threshold fitting.
The original auditor and all scientific analysis files remain byte-identical.

Independent reviews were performed by Codex gpt-6.1-sol (read-only sandbox,
high reasoning) and Claude Opus 5.5 (Read/Glob/Grep only). Both confirmed that
the checker makes no model calls or cache writes. Their findings and resolutions:

- The initial working tree lacked the new receipt and refreshed artifact manifest.
  Record the receipt only after implementation settles; extend the post-hoc
  manifest while asserting every scientific artifact remains unchanged. The
  final offline verifier and clean-export check pass.
- Require all 68 reconstruction sources, real per-file counts, and individual
  cache/run hash eligibility. The default checker now refuses a missing or stale
  receipt; removal or backfill of a recorded prompt hash changes eligibility.
- Execute the renderer from the same checkout that is being attested. Reject
  alternate-root API calls; integration tests execute the copied checker in its
  own process, including from a working directory outside the export.
- Replace “historical hash” with “recorded 64-bit prompt-hash prefix.” Report the
  legacy rows explicitly: 150 original-view dev, **120 original-view test**, and
  40 cross-family rows. A length match cannot authenticate historical content.
- Add independent shuffle-output checking, modality-retention positive controls,
  actual equal-length message corruption, missing/stale receipt tests, and
  source/count/eligibility rejection tests. Test bytecode suppression without
  relying on a PYTHONDONTWRITEBYTECODE environment setting.
- Scope injected-private-field checks to the current renderer. They do not prove
  historical prompts for length-only rows, seller-call isolation, or semantic
  accuracy of the auditors' evidence. Those limits are explicit in the receipt.

The final focused Codex review found **no consequential issues remaining** in
the receipt, coverage, count, eligibility and renderer-root fixes. It independently
ran `python3 -S verify_artifacts.py` successfully; it reviewed tests statically.

Final manager verification:

- `uv run python check_audit_inputs.py`: all 44 cache files / 2,213 rows;
  1,903 recorded 64-bit hash matches, 310 length-only matches. No mismatches.
  Frozen donors, public partnership metadata, unchanged recipient actions and
  current-renderer input boundaries pass.
- `uv run python -m unittest discover -s tests -v`: **27 tests pass**.
  An early development invocation also discovered the original handoff tests
  before the manifest was refreshed; three expected stale-manifest assertions
  failed. Duplicate test discovery was removed and the final full suite passes.
- `python3 -S verify_artifacts.py`: **404 hashes**, cached coverage, original
  scientific receipts, saved arithmetic, presentation/export freshness and the
  new post-hoc input receipt pass without optional dependencies.
- Report exports regenerated to include the provenance disclosure: 25 report
  pages, 18 headings, 317 table cells, 442 text fragments and 8 figures; talk
  remains 7 slides / 100 visible text fragments. Exporter checks all text.
- Clean Git-index export without local evaluation locks: the checker, offline
  verifier, both export freshness checks and completed-headline refusal pass.
  Every file's hash and modification time, plus the complete inventory, is
  unchanged after those commands.
- Compared with iteration 21, all 396 other pre-existing manifested artifacts
  remain identical. Only verifier code and the four report/export artifacts
  (REPORT.html, REPORT.pdf, PRESENTATION.pdf, handoff_exports.json) changed;
  the three additions are the checker, its tests and its post-hoc receipt.

The new receipt and manifest extension are preservation records created after
the experiments. They do not establish pre-registration or strengthen the
historical evidence available for the 310 length-only rows. Scientific point
estimates, intervals, thresholds, figures and evaluation receipts are unchanged.
