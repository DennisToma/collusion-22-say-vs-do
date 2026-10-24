# Iteration 20 — short presentation and independent claims review

Scope: presentation only. No seller/judge/auditor calls, AUROC/bootstrap reruns,
threshold fitting, or changes to saved scientific results.

An independent Codex reviewer read `build_presentation.py`, the generated HTML
and notes, REPORT.md, and the selected saved JSON. The reviewer found no blocking
scientific or generator defect. All numerical spot checks matched, and the
different raw-text contrasts (test combined minus max(text, action), replication
registered combined minus action) were labelled correctly. Three P3 caveats were
made visible on the slides:

- Economics-lab framing and earnings = profit in the setup.
- The statistics table already includes pair premium; its individual contribution
  was not isolated by an ablation.
- Replication registration followed generation start, before metrics; the full
  exposure chronology remains in the notes and REPORT.md.

The seven-slide HTML uses no external assets, fonts, libraries, or requests. It
renders a saved-CI SVG comparison, original versus replication contrast tables,
the round-1/placebo confound, and threshold instability. Local JSON source links
and speaker-note SHA-256 hashes identify its inputs. `--check` compares generated
bytes to the shipped talk without writing. The offline verifier also checks this
freshness; the manifest extension is explicitly post-hoc.

Verification:

- `python3 build_presentation.py --check` and `python3 verify_artifacts.py`.
- `uv run python -m unittest discover -s tests -v`: 11 tests, including
  write-free presentation checking and rejection of edited presentation text.
  An initial plain-system-Python suite invocation failed the existing evaluator
  subprocess tests because scikit-learn was not installed in that interpreter;
  the prescribed uv environment supplies it. No metric was computed by those
  failed imports.
- Headless Chromium opened the HTML using `file://`: all seven slides readable;
  Present, next/previous, Home/End, Escape, and return to reading mode worked;
  no JavaScript errors, external requests, or broken local links.
- All seven slides fit without page overflow at 1280×720, 1280×800, 1366×768,
  1440×900, and 1920×1080. Mobile reading mode has no horizontal overflow at
  390×844. Screenshots were inspected; scratch browser files are outside the repo.
- Browser Print / PDF produced exactly seven pages with one slide on each page.
  The generated PDF was a scratch verification artifact, not a shipped result.
- A Git-index-only export with no local evaluation locks passed the standard-library
  verifier, presentation freshness check, and completed-headline refusal. Its file
  inventory, hashes, and modification times remained unchanged.

The committed manifest now includes the renderer, HTML, and notes. All pre-existing
data, results, figures, receipts, and analysis code hashes remain unchanged, apart
from the verifier and its handoff tests, which now cover the presentation.
