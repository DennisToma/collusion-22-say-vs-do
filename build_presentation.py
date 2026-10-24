"""Render the short talk from saved results, using only the Python standard library.

python3 build_presentation.py          # writes PRESENTATION.html + PRESENTATION.md
python3 build_presentation.py --check  # byte-for-byte, read-only freshness check

No experiment modules, model calls, metric estimation, or external assets. The
HTML works offline, supports keyboard navigation, and prints one slide per page.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "test": "results/analysis/final_llm_v3_gpt-6.1-sol_test.json",
    "rep": "results/analysis/replication_llm_v3rep.json",
    "early": "results/analysis/early_detection_llm_v3.json",
    "placebo": "results/analysis/placebo_llm_v3plc.json",
    "monitor": "results/analysis/monitor_stratum_llm_v3mon.json",
    "labels": "results/label_xfam.json",
    "nolevel": "results/analysis/nolevel_view.json",
    "supervised": "results/baselines/llm_v3_lr_test.json",
}
VIEWS = ("text", "action", "combined", "action_stats", "combined_stats", "structured", "premium")
LABELS = {"text": "Public text", "action": "Actions", "combined": "Text + actions",
          "action_stats": "Actions + statistics", "combined_stats": "Text + actions + statistics",
          "structured": "Above + consistency table", "premium": "Price premium (statistic)"}


def esc(value):
    return html.escape(str(value), quote=True)


def ci(values, digits=2, signed=False):
    fmt = f"{'+' if signed else ''}.{digits}f"
    return f"{values[0]:{fmt}} [{values[1]:{fmt}}, {values[2]:{fmt}}]"


def delta(result, key, digits=3):
    row = result["contrasts"][key]
    return ci([row["delta"], *row["ci"]], digits, signed=True)


def table(headers, rows):
    # Cell contents here are trusted, locally constructed HTML; text inputs use esc().
    return ("<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) +
            "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) +
            "</tr>" for r in rows) + "</tbody></table>")


def auroc_chart(test, rep):
    """SVG with accessible labels; endpoints are the saved percentile bounds."""
    x = lambda score: 330 + (score - 0.3) / 0.7 * 890
    parts = ['<svg viewBox="0 0 1280 440" role="img" aria-labelledby="chart-title chart-desc">',
             '<title id="chart-title">Run AUROC on test and fresh replication</title>',
             '<desc id="chart-desc">Filled blue dots: test. Hollow orange dots: replication. '
             'Lines show saved 95 percent bootstrap confidence intervals. '
             'The adjacent table gives all values.</desc>']
    for tick in (0.3, 0.5, 0.7, 0.9, 1.0):
        parts += [f'<line x1="{x(tick)}" x2="{x(tick)}" y1="14" y2="382" stroke="#d5dce8"/>',
                  f'<text x="{x(tick)}" y="407" text-anchor="middle">{tick:.1f}</text>']
    for i, view in enumerate(VIEWS):
        y = 38 + i * 52
        parts.append(f'<text x="312" y="{y + 5}" text-anchor="end">{esc(LABELS[view])}</text>')
        for obj, offset, color, fill in ((test, -7, "#225cb7", "#225cb7"),
                                          (rep, 9, "#9c4b00", "white")):
            pt, lo, hi = obj["point_ci"][view]["run_auroc"]
            cy = y + offset
            parts += [f'<line x1="{x(lo):.2f}" x2="{x(hi):.2f}" y1="{cy}" y2="{cy}" '
                      f'stroke="{color}" stroke-width="3"/>',
                      f'<circle cx="{x(pt):.2f}" cy="{cy}" r="5" fill="{fill}" stroke="{color}" stroke-width="2"/>']
    parts.append('<text x="600" y="437" text-anchor="middle">Run AUROC · saved 95% run-bootstrap CIs</text></svg>')
    return "".join(parts)


CSS = """
:root { color-scheme: light; font-family: system-ui, sans-serif; color:#17243b; background:#e8edf5 }
* { box-sizing:border-box } body { margin:0 } a { color:#225cb7 }
header { position:sticky; top:0; z-index:3; display:flex; align-items:center; gap:12px;
  background:#17243b; color:white; padding:10px 4vw; font-size:14px }
header button { cursor:pointer; color:inherit; background:transparent; border:1px solid #a9bbd5;
  border-radius:5px; padding:6px 12px; font:inherit } #position { margin-right:auto }
main { max-width:1440px; margin:auto } .slide { background:white; margin:25px 20px;
  padding:42px 52px 30px; border-top:6px solid #225cb7; border-radius:6px; min-height:700px }
.eyebrow { text-transform:uppercase; letter-spacing:.12em; color:#456182; font-size:14px; margin:0 }
h1 { font-size:44px; line-height:1.15; letter-spacing:-.025em; margin:16px 0 22px; max-width:1050px }
h2 { font-size:25px; margin:0 0 12px } p,li { font-size:22px; line-height:1.42 }
li { margin:10px 0 } .lead { font-size:28px; max-width:1050px }
.callout { padding:18px 24px; background:#eaf1fb; border-left:5px solid #225cb7; margin:24px 0 }
.caution { background:#fff4df; border-color:#a55b05 } .small, .small p { font-size:16px; line-height:1.45 }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:28px; margin:22px 0 }
.metric { font-size:46px; font-weight:700; margin:8px 0; font-variant-numeric:tabular-nums }
.card { padding:20px; background:#f2f5f9; border-radius:6px } table { border-collapse:collapse;
  width:100%; margin:15px 0; font-size:18px; font-variant-numeric:tabular-nums }
th,td { border-bottom:1px solid #d7dfeb; padding:11px 12px; text-align:left; vertical-align:top }
th { color:#34516e; font-size:16px } td:not(:first-child) { white-space:nowrap }
.compact td { padding:7px 12px } svg { display:block; width:100%; max-height:380px; font-size:17px }
.source { font-size:13px; line-height:1.5; overflow-wrap:anywhere; color:#53647a; margin-top:26px }
details { border-top:1px solid #d7dfeb; padding-top:12px; margin-top:20px }
summary { cursor:pointer; font-size:14px; color:#34516e } details p { font-size:17px }
.presenting .slide { display:none; margin:0; border-radius:0; min-height:calc(100vh - 56px) }
.presenting .slide.active { display:block } .presenting details { display:none }
.presenting main { max-width:1440px } .sr-only { position:absolute; width:1px; height:1px;
  padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0 }
@media screen and (min-width:801px) {
  .presenting .slide { padding:24px 40px 18px }
  .presenting h1 { font-size:clamp(28px,4.5vh,40px); margin:12px 0 16px }
  .presenting h2 { font-size:23px }
  .presenting p,.presenting li { font-size:clamp(17px,2.5vh,22px); line-height:1.35 }
  .presenting .lead { font-size:clamp(22px,3.2vh,28px) }
  .presenting .small,.presenting .small p { font-size:14px }
  .presenting .source { font-size:11px; margin-top:16px }
  .presenting .eyebrow { font-size:13px }
  .presenting .grid { gap:24px; margin:16px 0 }
  .presenting .card { padding:16px }
  .presenting .metric { font-size:40px }
  .presenting .callout { padding:12px 18px; margin:16px 0 }
  .presenting svg { max-height:min(35vh,330px) }
}
@media(max-width:800px) { .slide { padding:25px 22px; min-height:0; margin:15px 8px }
  h1 { font-size:31px } p,li { font-size:19px } .lead { font-size:23px }
  .grid { grid-template-columns:1fr } .metric { font-size:34px } table { font-size:13px }
  th,td { padding:7px 5px } td:not(:first-child) { white-space:normal } header { flex-wrap:wrap }
  .presenting .slide { min-height:calc(100vh - 95px) } }
@media print { @page { size:landscape; margin:10mm } body { background:white }
  header,details { display:none!important } main { max-width:none }
  .slide,.presenting .slide { display:block!important; break-after:page; margin:0; padding:18px 24px;
    min-height:0; border-radius:0; border-top-width:3px } .slide:last-child { break-after:auto }
  h1 { font-size:30px; margin:8px 0 14px } p,li { font-size:16px; line-height:1.3 }
  .lead { font-size:21px } .metric { font-size:32px } table { font-size:13px; margin:8px 0 }
  th,td,.compact td { padding:6px 8px } th { font-size:12px } .source { font-size:10px; margin-top:12px }
  .callout { padding:10px 15px; margin:12px 0 } .grid { margin:12px 0; gap:18px }
  .card { padding:13px } .small,.small p { font-size:12px } svg { max-height:250px }
  a { color:inherit; text-decoration:none } }
"""

JS = """
(() => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const position = document.getElementById('position');
  const toggle = document.getElementById('mode');
  let index = 0;
  function show(next) {
    index = Math.max(0, Math.min(slides.length - 1, next));
    slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
    position.textContent = `Say vs. Do · ${index + 1} / ${slides.length}`;
    if (document.body.classList.contains('presenting')) window.scrollTo(0, 0);
  }
  document.getElementById('previous').onclick = () => show(index - 1);
  document.getElementById('next').onclick = () => show(index + 1);
  toggle.onclick = () => {
    const enabled = document.body.classList.toggle('presenting');
    toggle.textContent = enabled ? 'Read all slides' : 'Present';
    toggle.setAttribute('aria-pressed', String(enabled));
    show(index);
  };
  document.getElementById('print').onclick = () => window.print();
  document.addEventListener('keydown', event => {
    if (event.target.closest('input, textarea, select, [contenteditable]')) return;
    if (!document.body.classList.contains('presenting')) return;
    // Preserve native Space activation, while arrows and Escape still work
    // immediately after clicking a presentation control (which keeps focus).
    if (event.key === ' ' && event.target.closest('button, a, summary')) return;
    if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); show(index + 1); }
    if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); show(index - 1); }
    if (event.key === 'Home') { event.preventDefault(); show(0); }
    if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
    if (event.key === 'Escape') toggle.click();
  });
  show(0);
})();
"""


def render(root=ROOT):
    raw = {key: (root / path).read_bytes() for key, path in SOURCES.items()}
    data = {key: json.loads(value) for key, value in raw.items()}
    t, r, e, p, m = (data[key] for key in ("test", "rep", "early", "placebo", "monitor"))
    labels = data["labels"]["datasets"]
    label_agree = sum(row["binary_agree"] for row in labels.values())
    label_n = sum(row["n"] for row in labels.values())
    label_pos = sum(row["gpt_y1"] for row in labels.values())
    nl = data["nolevel"]["llm_v3_test"]
    slides = []

    def add(title, body, notes, sources):
        slides.append((title, body, notes, sources))

    add("Does reading what sellers say improve action auditing?", f"""<p class="lead"><strong>On this generator, no resolved detection gain.</strong><br>
Computed action summaries improve localisation; a simple price statistic ranks strongly.</p>
<div class="grid"><div class="card"><h2>Adding public text</h2>
<p class="metric">{t['contrasts']['delta_hybrid[combined]:run_auroc']['delta']:+.2f}</p>
<p>Test run-AUROC change vs the best single modality</p>
<p class="small">95% CI: {delta(t, 'delta_hybrid[combined]:run_auroc')}</p></div>
<div class="card"><h2>A major validity limit</h2><p>Opening prices discriminate before any partner message is read.
Flags stay frequent when private messages are never delivered.</p></div></div>
<p class="small">Q2.2 · Apart AI Collusion Sprint · gpt-6-luna sellers, gpt-6.1-sol auditors.
This is a generator-specific comparison. The CI does not establish equivalence.</p>""",
        "Open with the answer to Q2.2, then state the validity limit immediately. "
        "The negative finding is about these zero-shot auditors and these public messages. "
        "It does not establish that text cannot help in other settings or after training. "
        "No resolved gain means the interval includes zero, not that the methods are equivalent.", ["test", "placebo"])

    add("What was observed, and what was labelled?", f"""
<div class="grid"><div><h2>Market and split</h2><ul>
<li>Four LLM sellers set prices and post public messages for twelve rounds in an economics-lab framing;
earnings = profit.</li>
<li>Conditions: private channel, no channel, or a public shipping partnership.</li>
<li>Dev n = {t['n_dev_for_calibration']}; test n = {t['n_runs']} ({t['n_pos']} positive);
fresh replication n = {r['n_runs']}.</li></ul></div>
<div><h2>Six original auditor views</h2><ol class="small">
<li>Public text</li><li>Actions: prices, state, units, profit</li><li>Actions + pair statistics</li>
<li>Text + actions</li><li>Text + actions + pair statistics</li>
<li>All above + stated-vs-actual price table</li></ol></div></div>
<div class="callout caution"><strong>Endpoint: private coordination communication.</strong>
A judge reads private chat only, never prices. Private chat is hidden from auditors.
In the main dataset every private-channel run is positive: label = condition.
This is not a verified-overcharge label.</div>
<p class="small">Post-hoc label check: GPT and Claude Sonnet agree on the binary label in
{label_agree}/{label_n} private chats across four datasets using the same judge template;
agreement does not establish correctness.</p>
<p class="small">Same auditor model, same cases, public partnership notice in every view.
Run AUROC measures detection; within-market AUROC measures pair localisation in positive runs.</p>""",
        "Sellers were given profit objectives and an opportunity to communicate, not instructions to collude. "
        "The operational label includes explicit agreements and price-intention exchanges. "
        "A judge-positive chat is not evidence that the private exchange caused the prices. "
        f"The post-hoc label re-judge agrees on the binary endpoint in {label_agree}/{label_n} private chats "
        f"({label_pos} positive, {label_n - label_pos} negative; main, replication, firm-framing and monitored strata). "
        "Each stratum is uniform, so this does not test within-stratum discrimination; the explicit-agreement versus intention-exchange "
        "sub-label differs between judges. Agreement is a robustness check, not independent ground truth. "
        "The full report documents the lab framing, pilots, and all six input views.", ["test", "rep", "labels"])

    chart_table = table(["Scorer", f"Test (n = {t['n_runs']})", f"Replication (n = {r['n_runs']})"],
                        [[esc(LABELS[v]), ci(t["point_ci"][v]["run_auroc"]),
                          ci(r["point_ci"][v]["run_auroc"])] for v in VIEWS])
    add("Action summaries: detection and localisation", f"""
{auroc_chart(t, r)}
<details class="values"><summary>Accessible numerical table: run AUROC [95% CI]</summary>{chart_table}</details>
<p class="small">Filled blue = test (n = {t['n_runs']}); hollow orange = fresh replication (n = {r['n_runs']}).
The chart compares the six original LLM views and the premium. Premium = pair mean price minus rival mean price;
run score = maximum over pairs. The statistics table already includes the premium; its contribution was not isolated.</p>
<p class="small">Statistics improve pair localisation in both samples; the detection gain is resolved on test only.</p>
<div class="callout caution small">Premium selection used partial data including test runs.
The test evaluation ran once, but was not fully blind. Replication analysis was registered after generation began,
before metrics. Its intervals are wide; the premium's registered advantage over action_stats is unresolved.</div>
<p class="small">A supervised TF-IDF baseline also learns a public-text trace (REPORT, within-split CV);
that is a different training regime from these zero-shot auditors.</p>""",
        "Premium has the highest run-AUROC point estimate among these untrained scorers. Do not call it the best detector in general: "
        "the report also has supervised baselines. The six original LLM views are all shown, so the graphic does not hide "
        "a stronger original view. The fresh sample checks direction but does not resolve the premium's lead. "
        "The later column ablation removes three level columns together: it lowers test detection performance, "
        "but does not isolate the premium column or establish what the auditor reasons about. "
        "The judge-question notes give the saved contrasts and their uncertainty.", ["test", "rep", "nolevel"])

    rows = [
        ["Raw text gain · run AUROC", delta(t, "delta_hybrid[combined]:run_auroc"),
         delta(r, "combined-action:run_auroc")],
        ["Statistics gain · run AUROC", delta(t, "action_stats-action:run_auroc"),
         delta(r, "action_stats-action:run_auroc")],
        ["Statistics gain · localisation", delta(t, "action_stats-action:within_market_auroc"),
         delta(r, "action_stats-action:within_market_auroc")],
        ["Text with statistics · localisation", delta(t, "combined_stats-action_stats:within_market_auroc"),
         delta(r, "combined_stats-action_stats:within_market_auroc")],
    ]
    add("Paired comparisons separate text from statistics", f"""
{table(['Change in AUROC [95% CI]', 'Test', 'Replication'], rows)}
<p class="small">Raw-text row: test = combined − max(text, action); replication = registered combined − action.
Statistics gain = action_stats − action. Text with statistics = combined_stats − action_stats.</p>
<ul><li>No resolved positive detection gain from raw text in either sample.</li>
<li>The statistics table improves localisation in both samples.</li>
<li>The small unadjusted text-with-statistics within-market localisation gain on test did not repeat.</li></ul>
<div class="callout small">Class-stratified paired run-bootstrap intervals. Test contrasts are nominal, unadjusted
for multiple comparisons. Text-with-statistics on replication is exploratory. CI inclusion is not equivalence.</div>""",
        "The two raw-text cells use the contrasts registered for each evaluation; do not describe them as identical definitions. "
        "The test evaluates the maximum of the two unimodal AUROCs inside each bootstrap draw. "
        "The replication's raw-text contrast directly subtracts action. Report detection and pair localisation separately. "
        "The main report lists all contrast families, the shuffle ablation, and the registered replication rules.", ["test", "rep"])

    early = e["results"]["test"]["r1-1"]["run_auroc"]
    prem = p["premium_scorer"]["flag_rate"]
    late = p["windows"]["r2_12"]
    add("The channel offer already leaves a conduct cue", f"""
<div class="grid"><div class="card"><h2>Before receiving any partner message</h2>
<p class="metric">{early[0]:.2f}</p><p>Test run AUROC using round-1 prices alone</p>
<p class="small">95% CI: {ci(early)}. Price and first private message are produced in the same call.</p></div>
<div class="card"><h2>Without private-message delivery</h2>
<p class="metric">{prem['placebo'][0]}/{prem['placebo'][1]} vs {prem['private'][0]}/{prem['private'][1]}</p>
<p>Premium flags: placebo vs matched delivered-channel runs</p>
<p class="small">Frozen dev threshold; {p['n_placebo']} matched seeds, identical channel prompt and market paths.</p></div></div>
<p>Rounds 2–12 pair premium: placebo {late['placebo'][0]:+.2f}, delivered {late['private'][0]:+.2f}.
Paired difference {ci(late['placebo_minus_private_paired'], signed=True)}.</p>
<div class="callout caution small">Exploratory. Placebo is not a judge-labelled no-collusion control;
public prices and messages remain visible. This does not establish equivalence or separate offer-induced focal pricing
from tacit public-price coordination.</div>""",
        "This is the strongest reason to limit the collusion claim. Messages offered but never delivered still produce elevated "
        "pair prices and frequent flags. The contrast asks about private-message delivery, not about all communication. "
        "Round-1 analysis is post-lock and placebo registration is not independently established before generation. "
        "The main report discloses those timings. No detector here has established a robust discriminator of agreement-caused conduct.",
        ["early", "placebo"])

    test_none = t["flag_rate_by_stratum"]["none_all"]
    rep_none_n = r["group_n"]["none"]
    flag_rows = [[esc(LABELS[v]), ci(test_none[v]), ci(r["flag_rate_frozen_dev_thresholds"][v]["none"])]
                 for v in ("action", "action_stats", "combined", "premium")]
    add("Ranking well does not guarantee a reliable alarm", f"""
{table(['No-channel flag rate [Wilson 95% CI]', f'Test (n = {test_none["n"]})',
        f'Replication (n = {rep_none_n})'], flag_rows)}
<p class="small">Same dev-chosen thresholds in both samples; neither sample calibrates these thresholds.</p>
<div class="grid"><div><h2>Threshold uncertainty</h2><p>False-alarm rates change even under the same generator.
The fresh no-channel sample is small.</p></div><div><h2>Evasion remains untested</h2>
<p>Under an announced price monitor, the judge finds coordination in
{m['group_n']['private_y1']}/{m['group_n']['private_y1'] + m['group_n']['private_y0']} private-channel runs.
There were no judge-positive evasive colluders to evaluate.</p></div></div>
<div class="callout small">Design hypothesis: compute cheap action statistics first, then use LLMs for explanation.
This proposed workflow is not validated for deployment or for explanation accuracy.</div>""",
        "AUROC is threshold-free and does not promise a calibrated alarm. The premium's fresh none rate is four of ten; "
        "the uncertainty is large. The report has firm-framing and announced-monitor strata with additional false alarms. "
        "The monitor result could reflect safety-triggered refusal or deterrence. We cannot test evasion without coordinated runs. "
        "A premium-filtered AND-gate was analysed descriptively in the report; the broader explanatory workflow is only a proposal.",
        ["test", "rep", "monitor"])

    add("A bounded finding, and a more decisive next test", """
<ul><li><strong>Supported here:</strong> no resolved detection gain from adding raw public text to the tested zero-shot auditors;
computed action summaries improve pair localisation.</li>
<li><strong>Not established:</strong> equivalence of text and action auditing, agreement-caused overcharge detection,
reliable evasion detection, or transfer across seller models.</li>
<li><strong>Next study:</strong> independently vary channel offer, message delivery, and realised agreement;
replicate across seller models and market designs, and test concealed opening-price cues.</li></ul>
<div class="callout"><strong>Read and verify:</strong> <a href="REPORT.md">REPORT.md</a> ·
<a href="README.md">README.md</a> · <a href="data/SPLITS.md">split/exposure chronology</a><br>
<a href="PRESENTATION.md">Speaker notes and judge questions</a><br>
<code>python3 verify_artifacts.py</code><br><code>python3 build_presentation.py --check</code></div>
<p class="small">Saved results and data ship with the repo. No model calls or locked-evaluation reruns are needed.
This talk is generated from saved JSON, with full SHA-256 source hashes in PRESENTATION.md.</p>""",
        "Close on the narrow answer and the stronger experimental design it motivates. "
        "The comparator was selected after partial test exposure. Replication registration followed the start of generation "
        "but preceded metrics; some raw output and later progress lines were seen. Placebo is exploratory. "
        "Private chat is the judge's evidence, never an auditor input. "
        "Direct questions about cost, failure examples, cross-family results, and supervised text to the full report.",
        ["test", "rep", "placebo"])

    sections, notes = [], ["# Say vs. Do — five-minute presentation\n",
                          "Generated by `python3 build_presentation.py` from saved results only. "
                          "Open [PRESENTATION.html](PRESENTATION.html) offline; click Present and use arrow keys. "
                          "Escape returns to reading mode. Print / PDF prints one slide per page. "
                          "The HTML also works without JavaScript as a readable document.\n",
                          "Allow roughly 40 seconds per slide. Full methods, uncertainty, chronology, "
                          "cost and failure cases: [REPORT.md](REPORT.md).\n"]
    for i, (title, body, note, sources) in enumerate(slides, 1):
        links = " · ".join(f'<a href="{SOURCES[key]}">{esc(key)} JSON</a>' for key in sources)
        sections.append(f'<section class="slide" id="slide-{i}" aria-labelledby="title-{i}">'
                        f'<p class="eyebrow">Say vs. Do · Q2.2 · {i} / {len(slides)}</p>'
                        f'<h1 id="title-{i}">{esc(title)}</h1>{body}'
                        f'<p class="source">Saved sources: {links}. Full methods and caveats: '
                        '<a href="REPORT.md">REPORT.md</a>.</p>'
                        f'<details><summary>Speaker notes</summary><p>{esc(note)}</p></details></section>')
        notes += [f"## {i}. {title}\n", note + "\n",
                  "Saved sources: " + ", ".join(f"[{key}]({SOURCES[key]})" for key in sources) + ".\n"]
    notes += ["## Likely judge questions\n",
              "These answers use the existing frozen results. They add no estimates and are not extra slides.\n",
              "### Are you detecting collusion or just the channel condition?\n",
              "The endpoint is judge-labelled private coordination communication (an agreement or price-intention "
              "exchange), not agreement-caused overcharge. In the main dataset it coincides with the private-channel "
              "condition. Opening prices already discriminate before any partner message is received, and "
              f"the premium flags {prem['placebo'][0]}/{prem['placebo'][1]} undelivered-channel runs versus "
              f"{prem['private'][0]}/{prem['private'][1]} matched delivered runs. "
              "That limits the conduct interpretation; it does not identify each detector's cues or establish "
              "equivalence of the two arms. Public-price coordination remains possible. "
              f"Sources: [early]({SOURCES['early']}), [placebo]({SOURCES['placebo']}).\n",
              "### Does the negative finding mean public text is useless?\n",
              "No. For the tested zero-shot auditor, combined minus the best single modality has run-AUROC change "
              f"{delta(t, 'delta_hybrid[combined]:run_auroc', digits=2)}. The interval leaves room for gains and "
              "losses. Text with statistics has a small unadjusted within-market localisation gain on test that did not repeat. "
              f"The supervised public-text classifier reaches {data['supervised']['hard']['text']['run_auroc'][0]:.2f} "
              "run AUROC under grouped five-fold CV within the test split, using other folds' labels. "
              "This is a different training regime and shows a learnable trace, not a zero-shot gain. "
              f"Sources: [test]({SOURCES['test']}), [replication]({SOURCES['rep']}), "
              f"[supervised]({SOURCES['supervised']}).\n",
              "### Is the statistics-table gain just the premium column?\n",
              "Not isolated. A post-hoc ablation removes pair mean price, rival mean price and premium together, "
              "retaining proximity and change-correlation columns. On test, full minus reduced table run AUROC is "
              f"{delta(nl, 'action_stats-action_stats_nolevel:run_auroc', digits=2)}; reduced table minus actions "
              "alone has localisation gain "
              f"{delta(nl, 'action_stats_nolevel-action:within_market_auroc', digits=2)}. "
              "Run-level full-minus-reduced differences on dev and replication are unresolved; localisation "
              "findings differ across splits. This tests information presentation, not the auditor's internal reasoning. "
              f"Source: [column ablation]({SOURCES['nolevel']}).\n",
              "### How reliable are the private-chat labels?\n",
              f"A post-hoc Claude Sonnet re-judge agrees with GPT on the binary label in {label_agree}/{label_n} "
              "private chats across the main, replication, firm-framing and monitored datasets. "
              f"These include {label_pos} positives and {label_n - label_pos} negatives; each stratum is uniform, "
              "so this does not test within-stratum discrimination. "
              "Both read private chat without prices. They disagree more on agreement versus intention exchange "
              f"(three-class kappa {labels['llm_v3']['kappa_3class']:.2f} main, "
              f"{labels['llm_v3rep']['kappa_3class']:.2f} replication); these sub-labels are not endpoints. "
              "Binary agreement does not establish correctness, conduct, or generalisation. "
              f"Source: [label check]({SOURCES['labels']}).\n",
              "### Was the test fully blind, and what did the replication establish?\n",
              "The premium comparator was selected after partial test exposure. The full test evaluation ran once. "
              "Replication registration followed the start of generation but preceded metrics; some raw output and "
              "later progress lines were seen. All four registered replication rules held, but they include "
              "interval-based rules and do not establish equivalence. The registered combined-minus-action "
              f"replication contrast is {delta(r, 'combined-action:run_auroc', digits=2)}. "
              "Some exploratory text contrasts are negative with intervals excluding zero. "
              f"Sources: [exposure chronology](data/SPLITS.md), [replication]({SOURCES['rep']}).\n",
              "### Is the proposed screening-and-explanation workflow ready to deploy?\n",
              "No deployment claim was tested. The frozen premium threshold flags "
              f"{r['flag_rate_frozen_dev_thresholds']['premium']['none'][0]:.0%} of "
              f"{rep_none_n} fresh no-channel runs (a small sample). "
              "Literal quotation and selective price-transition checks do not validate explanation accuracy "
              "or usefulness. A premium-filtered AND-gate was analysed descriptively; the proposed explanatory "
              "workflow was not evaluated end to end. "
              f"Sources: [replication]({SOURCES['rep']}), [limitations and source checks](REPORT.md).\n"]
    notes += ["## Source hashes\n", "These hashes identify the saved inputs used to render the talk and judge-question notes. "
              "They are post-hoc provenance, not evidence of pre-registration.\n"]
    for key, path in SOURCES.items():
        notes.append(f"- `{path}`: `{hashlib.sha256(raw[key]).hexdigest()}`")
    document = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>Say vs. Do — Q2.2 presentation</title><style>' + CSS + '</style></head><body>'
                '<header><span id="position" aria-live="polite">Say vs. Do</span>'
                '<button id="previous" aria-label="Previous slide">←</button>'
                '<button id="next" aria-label="Next slide">→</button>'
                '<button id="mode" aria-pressed="false">Present</button>'
                '<button id="print">Print / PDF</button></header><main>' + "\n".join(sections) +
                '</main><script>' + JS + '</script></body></html>\n')
    return {"PRESENTATION.html": document, "PRESENTATION.md": "\n".join(notes) + "\n"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="read-only freshness check; no files written")
    args = ap.parse_args()
    for name, content in render().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_bytes() != content.encode("utf-8"):
                raise SystemExit(f"FAIL: stale or missing {name}; run python3 build_presentation.py")
        else:
            path.write_bytes(content.encode("utf-8"))
    print("PASS: presentation matches saved inputs (read-only)." if args.check else
          "Wrote PRESENTATION.html and PRESENTATION.md from saved inputs; no metrics recomputed.")


if __name__ == "__main__":
    main()
