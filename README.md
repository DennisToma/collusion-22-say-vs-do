# Say vs. Do — Q2.2

Read [REPORT.md](REPORT.md) for the research question, results, uncertainty, figures,
and limitations. [PLAN.md](PLAN.md) defines the project, [data/SPLITS.md](data/SPLITS.md)
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
and the primary report table and image links. It makes no LLM calls and does not recompute
AUROC, bootstrap intervals, or thresholds. The manifest and completion receipt were recorded
**after** the experiments in iteration 19; they preserve the handoff, not evidence of
pre-registration. Some early audit rows have a recorded prompt length but no historical
prompt hash; the manifest authenticates their current bytes, not their original prompts.

For deterministic table/figure rendering, install the pinned environment with `uv sync --frozen`, then:

```sh
uv run python report_tables.py --split test
uv run python fig_summary.py
```

These render from saved results; they do not refit detectors. More generator, audit, and
post-hoc analysis commands are in REPORT Appendix E. Generated artifacts already ship with
the repository. Re-rendering images in a different environment may change their byte hashes.

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
