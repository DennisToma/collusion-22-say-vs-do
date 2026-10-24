# Say vs. Do — Q2.2

Read [REPORT.md](REPORT.md) for the research question, results, uncertainty, figures,
and limitations. For the five-minute talk, open [PRESENTATION.html](PRESENTATION.html)
locally in a browser; it works offline, with presentation controls and Print / PDF.
Ready to share: [slides PDF](PRESENTATION.pdf), [report PDF](REPORT.pdf), and
[report HTML](REPORT.html) (all figures embedded; readable as a single offline file).
[PRESENTATION.md](PRESENTATION.md) contains speaker notes and source hashes.
[PLAN.md](PLAN.md) defines the project, [data/SPLITS.md](data/SPLITS.md)
records evaluation exposure and registration chronology, and [EXPERIMENTS.tsv](EXPERIMENTS.tsv)
records the experiments. [SCHEMA.md](SCHEMA.md) describes trajectory files.

The finding on this generator is no resolved detection gain from adding public text
to zero-shot action auditing. Computed action summaries help. A simple price premium
ranks strongly, but placebo-channel runs show that elevated premiums and detector
flags can arise without delivered private messages. The endpoint is private coordination
communication, not verified realised overcharge. See the report for the full caveats.

To check this checkout offline, with Python 3.12+ and no installed dependencies or API keys:

```sh
python3 verify_artifacts.py
```

The verifier reads a committed SHA-256 manifest, validates cached dataset/auditor coverage,
matched placebo market paths, frozen calibration inputs, saved CI/contrast arithmetic,
the primary report table and image links, presentation freshness against saved JSON, and
exported HTML/PDF hashes against their post-hoc source receipt.
It makes no LLM calls and does not recompute
AUROC, bootstrap intervals, or thresholds. The manifest and completion receipt were recorded
**after** the experiments in iteration 19; they preserve the handoff, not evidence of
pre-registration. Some early audit rows have a recorded prompt length but no historical
prompt hash; the manifest authenticates their current bytes, not their original prompts.

For deterministic table/figure rendering, install the pinned environment with `uv sync --frozen`, then:

```sh
uv run python report_tables.py --split test
uv run python fig_summary.py
python3 build_presentation.py          # standard library only, HTML + speaker notes
python3 build_presentation.py --check  # read-only, byte-for-byte freshness check
```

These render from saved results; they do not refit detectors. More generator, audit, and
post-hoc analysis commands are in REPORT Appendix E. Generated artifacts already ship with
the repository.

To regenerate the shareable HTML/PDF files (rendering only; optional browser dependencies):

```sh
uv sync --frozen --group handoff
uv run --group handoff playwright install chromium
uv run --group handoff python build_handoff.py
python3 -S build_handoff.py --check  # read-only; standard library, no browser needed
```

The report HTML embeds the existing PNG figures and preserves the complete Markdown report.
PDF export checks all report text fragments (including headings and table cells), figure
loading, and one page per slide.
Wide appendix tables use landscape pages. `data/handoff_exports.json` records source/output
hashes and renderer versions after export. PDF bytes can vary with renderer, fonts and creation
time; re-exporting requires updating the post-hoc artifact manifest as well. HTML source links
require the repository. PDF source links open the GitHub repository on `main` (network required
when clicked); the receipt identifies the exact exported sources. No external resources are
fetched during rendering. Re-rendering images may also change their byte hashes.

The headline test and fresh replication are **complete and must not be rerun**. Their
saved outputs are `results/analysis/final_llm_v3_gpt-6.1-sol_test.json` and
`results/analysis/replication_llm_v3rep.json`. The entry points (`finalize_test.sh`,
`final_analysis.py --split test`, and `replication.py`) respect the portable
`data/evaluation_receipt.json`, because the original `logs/` locks are local and gitignored.
Use the offline verifier to inspect this completed evaluation.

Cached inputs are under `data/<dataset>/`; frozen per-view audit responses are under
`results/llm_auditor/<dataset>/<model>/`. Private chats and labels are separate from the public
trajectory files and never auditor inputs. The main dataset is `llm_v3`, the separate fresh
replication is `llm_v3rep`, and exploration strata are `llm_v3plc` (undelivered channel),
`llm_v3fp` (firm framing), and `llm_v3mon` (announced monitor). Scripted data demonstrates
the pipeline mechanism only. Do not pool these strata into the headline.

The sibling information-theory results are already embedded in the saved headline JSON;
rendering or verifying them does not require the sibling checkout. Recomputing that external
comparator would require its source data. Generation and fresh LLM audits need a configured
backend (see `llm.py`) and are not needed to inspect or render the delivered results.
