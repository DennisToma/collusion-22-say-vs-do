# Say vs. Do — Q2.2

Read [REPORT.md](REPORT.md) for the research question, results, uncertainty, figures,
and limitations. For the five-minute talk, open [PRESENTATION.html](PRESENTATION.html)
locally in a browser; it works offline, with presentation controls and Print / PDF.
Ready to share: [slides PDF](PRESENTATION.pdf), [report PDF](REPORT.pdf), and
[report HTML](REPORT.html) (all figures embedded; readable as a single offline file).
[PRESENTATION.md](PRESENTATION.md) contains speaker notes and source hashes.
The [evidence source ledger](EVIDENCE.html) exposes all 2,925 original-view test and
replication evidence items alongside the public log. It works offline, with optional
search/view filters, and reports literal locations for quote-marked spans. It does
not judge whether the surrounding observation or collusion inference is correct.
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
It also checks freshness of the cached evidence source ledger and price-transition census.
It makes no LLM calls and does not recompute
AUROC, bootstrap intervals, or thresholds. The manifest and completion receipt were recorded
**after** the experiments in iteration 19; they preserve the handoff, not evidence of
pre-registration. Some early audit rows have a recorded prompt length but no historical
prompt hash; the manifest authenticates their current bytes, not their original prompts.

To reconstruct every cached auditor prompt against the shipped public data, use
the pinned environment (NumPy is required):

```sh
uv run python check_audit_inputs.py
```

This separate read-only check covers all 2,368 audits in 46 caches, including the
cross-family, shuffled and post-hoc hint and no-level views. It checks 2,058 recorded 64-bit
prompt-hash prefixes and 310 legacy prompt lengths (150 original-view dev, 120
original-view test and 40 cross-family rows), public partnership metadata, frozen
shuffle mappings and preservation of recipient actions. It also checks that the
current renderer ignores injected private fields, excludes public messages from
action-only views and numeric actions from text-only views, and retains each
view's observable inputs. Length-only rows cannot establish historical prompt
content. The post-hoc `data/audit_input_receipt.json` records this check and its
source hashes; the standard-library verifier validates receipt freshness without
reconstructing prompts. Use this checker for handoff inspection: the historical
`auditors.py --verify` entry point regenerates public metadata before checking.

To regenerate or check the evidence source ledger (saved caches only, no model calls):

```sh
python3 -S check_evidence_sources.py
python3 -S check_evidence_sources.py --check  # read-only, standard library only
```

The census covers the six original GPT views on 95 test and 30 replication runs.
Only 4 evidence items contain quote-marked phrases; all four can be located at
the cited firm and round. All four are text-view items, and two quote the generic
phrase "considered price" occurring across multiple firms and rounds. This sparse quotation coverage does not validate the
auditors' explanations. The ledger preserves all evidence and the complete public
price/message log for manual review, plus market state, units, profits and public
cost offsets. The renderer reads no private-chat or label files and does not export
injected agent-private fields. Well-formed source anchors do not establish relevance.

The separate [price-transition census](PRICE_TRANSITIONS.md) checks narrowly parsed
leading `from X to Y` price clauses against source endpoints. It recognizes 57 items
out of the 2,925; 54 match adjacent rounds and three have an earlier start. This explains
why checking both numbers against a single round can reject an endpoint-consistent transition.
The checker leaves other clauses, timing/duration and collusion inferences unvalidated;
it does not estimate explanation accuracy. Its grammar omits wording such as "jointly raised"
and "decrease", limiting assurance about coordination claims. The census also exposes
unparsed numeric from-to spans (including possible cost statements) without validating them.
To regenerate or check it without model calls:

```sh
python3 -S check_price_transitions.py
python3 -S check_price_transitions.py --check  # read-only, standard library only
```

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
