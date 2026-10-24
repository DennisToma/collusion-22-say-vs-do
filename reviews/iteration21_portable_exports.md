# Iteration 21 — portable report and talk exports

Scope: handoff rendering only. No generator, labeller, auditor, AUROC/bootstrap,
threshold fit, or completed evaluation was run. The scientific text of REPORT.md
is unchanged; five opening lines link the exports and describe their reproduction.

An independent Codex gpt-6.1-sol reviewer read the initial exporter, verifier,
tests, report opening, documentation, and export receipt using a read-only sandbox.
It found no scientific claim changes or accidental metric/model calls. It verified
all 123 initial paragraph/heading blocks against extracted report PDF text.

One **P2** was found: Chromium's printed PDF annotations contained absolute
`file:///home/factory/...` source links, which would break after sharing. Fixed:
`prepare_pdf_links` replaces local anchor targets in the print document with
GitHub repository links before PDF creation. The shipped offline HTML retains its
local links. GitHub links point to `main`; the post-hoc receipt identifies exact
exported inputs independently of that mutable branch. Clicking these links needs
a network; reading the files does not. `pdfinfo -url` and a separate pypdf check
confirm all 35 PDF source links (9 report, 26 slides) are GitHub URLs and neither
PDF contains the build-machine path.

Final local verification (after the review and fixes):

- `python3 -S verify_artifacts.py`: 401 artifact hashes, cached coverage,
  original input/receipt checks, report tables/figures, talk freshness, export
  input/output hashes. `-S` disables optional installed packages.
- `python3 -S build_handoff.py --check`: standard-library, read-only verification.
- Export checks: 25 report pages; all 18 headings, 317 table cells and 441 text
  fragments (including the reproduction code block) survive PDF extraction;
  all 8 embedded figures load. All 100 visible talk text fragments survive on
  their corresponding slides; 7 slides produce exactly 7 PDF pages. PDF ligatures
  and whitespace are normalised for these checks; slide comparisons allow CSS
  uppercasing. No score, interval or threshold is computed.
- `uv run python -m unittest discover -s tests -v`: 14 tests. New isolation tests
  check write-free dependency-free export verification, stale report prose, and
  changed PDF bytes. Existing completed-evaluation guards remain tested.
- Standalone REPORT.html copied outside the repo, opened in Chromium with
  JavaScript disabled: all 8 figures, 18 headings and 317 table cells load, no
  external requests, no horizontal page overflow at 390, 1280 and 1920 pixels.
  Wide tables scroll within their containers on mobile.
- Both PDFs: all extracted word bounding boxes are within page margins.
  Report figures and representative pages were visually inspected, including
  the primary table/figure page and landscape appendix tables. Tables stay
  intact; wide-table labels/section heading share their landscape page.
- Git-index-only export without local evaluation locks passes the standard-library
  verifier, both handoff freshness checks, and completed-headline refusal; its
  file inventory, hashes, and modification times remain unchanged.

The renderer and its optional dependencies are pinned by uv.lock. Shipped outputs
require no browser installation; regeneration requires the optional `handoff`
dependency group and Chromium. PDF bytes can depend on renderer, fonts and creation
time. `data/handoff_exports.json` and the manifest extension are explicitly
post-hoc preservation records, not pre-registration evidence.

Every pre-existing data/result/figure/receipt and scientific analysis hash matches
the previous commit. Only the verifier, its tests, and optional dependency files
changed among pre-existing manifested artifacts. No scientific estimate changed.
