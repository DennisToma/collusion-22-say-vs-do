"""Expose cached evidence beside public sources; no semantic judge or model calls.

Scope fixed before implementation: six original GPT views on llm_v3 test runs
0030..0124 and all 30 llm_v3rep runs. Quote-marked spans are located literally
(Unicode NFKC, casefold, whitespace normalization, word boundaries). A located
span is not proof that an observation or its collusion inference is correct.
No price claims are parsed: historical single-round price checks can fail price
transition descriptions. The browser shows all four firms and every round.

    python3 -S check_evidence_sources.py          # render saved-source ledger
    python3 -S check_evidence_sources.py --check  # read-only freshness check
"""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
VIEWS = ("text", "action", "action_stats", "combined", "combined_stats", "structured")
OUTPUTS = ("results/analysis/evidence_sources.json", "EVIDENCE.html")
QUOTE = re.compile(r'"([^"]+)"|“([^”]+)”|(?<!\w)\'(.+?)\'(?!\w)|(?<!\w)‘(.+?)’(?!\w)', re.S)
LOCATIONS = ("cited_firm_round", "cited_firm_other_round", "other_firm_cited_round",
             "other_firm_other_round", "not_found", "invalid_anchor")


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def quoted_spans(observation):
    # Quotation marks also delimit terminology, hypothetical language and partial
    # phrases. Use non-overlapping spans, ending at the first closing delimiter;
    # same-style nested quotes/plural possessives can be ambiguous. No such cases
    # occur among the four spans in the frozen scope (independently reviewed).
    if not isinstance(observation, str):
        raise ValueError("evidence observation must be a string")
    return [next(g for g in m.groups() if g is not None) for m in QUOTE.finditer(observation)
            if next(g for g in m.groups() if g is not None).strip()]


def contains(message, span):
    needle = normalized(span)
    return bool(needle) and re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", normalized(message)) is not None


def locate(span, rounds, firm, cited_round):
    hits = [{"round": t, "firm": f} for t, agents in sorted(rounds.items())
            for f, agent in sorted(agents.items()) if contains(agent["public_message"] or "", span)]
    if not (type(cited_round) is int and cited_round in rounds and isinstance(firm, str) and firm in rounds[cited_round]):
        return {"span": span, "location": "invalid_anchor", "hits": hits}
    for category, predicate in (
        (LOCATIONS[0], lambda h: h["firm"] == firm and h["round"] == cited_round),
        (LOCATIONS[1], lambda h: h["firm"] == firm),
        (LOCATIONS[2], lambda h: h["round"] == cited_round),
        (LOCATIONS[3], lambda h: True),
    ):
        if any(predicate(h) for h in hits):
            return {"span": span, "location": category, "hits": hits}
    return {"span": span, "location": "not_found", "hits": []}


def rows(root, name):
    return [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]


def unique(records, name):
    result = {r["run_id"]: r for r in records}
    if len(result) != len(records):
        raise ValueError(f"duplicate audit/public-info run: {name}")
    return result


def load(root):
    datasets, sources = {}, {"check_evidence_sources.py"}
    for ds, total, start in (("llm_v3", 125, 30), ("llm_v3rep", 30, 0)):
        all_ids = {f"{ds}_{i:04d}" for i in range(total)}
        ids = {f"{ds}_{i:04d}" for i in range(start, total)}
        traj_name, info_name = (f"data/{ds}/{n}.jsonl" for n in ("trajectories", "public_info"))
        sources.update((traj_name, info_name))
        trajectories, markets = {}, {}
        for row in rows(root, traj_name):
            rid, t = row["run_id"], row["round"] + 1
            rounds = trajectories.setdefault(rid, {})
            if t in rounds or len(row["agents"]) != 4 or {a["id"] for a in row["agents"]} != set("ABCD"):
                raise ValueError(f"duplicate round/firm or incomplete firms: {rid}/{t}")
            rounds[t] = {a["id"]: a for a in row["agents"]}
            markets.setdefault(rid, {})[t] = row["market"]
        if set(trajectories) != all_ids or any(set(r) != set(range(1, 13)) for r in trajectories.values()):
            raise ValueError(f"incomplete trajectory coverage: {ds}")
        info = unique(rows(root, info_name), info_name)
        if set(info) != all_ids:
            raise ValueError(f"incomplete public-info coverage: {ds}")
        audits = {}
        for view in VIEWS:
            name = f"results/llm_auditor/{ds}/gpt-6.1-sol/{view}_orig.jsonl"
            sources.add(name)
            cached = unique(rows(root, name), name)
            if set(cached) != all_ids:
                raise ValueError(f"incomplete audit coverage: {name}")
            audits[view] = {rid: cached[rid] for rid in sorted(ids)}
        datasets[ds] = {"ids": sorted(ids), "rounds": trajectories, "markets": markets,
                        "info": info, "audits": audits}
    return datasets, {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in sorted(sources)}


def inspect(datasets, hashes):
    out = {"schema_version": 1, "post_hoc": True,
           "scope": "Literal source location and coverage only; not semantic evidence accuracy, inference validity, or pre-registration.",
           "selection": {"llm_v3": "0030..0124 (test; already exposed)", "llm_v3rep": "0000..0029 (already exposed)"},
           "normalization": "Unicode NFKC, casefold, collapsed whitespace, word-boundary substring; punctuation retained",
           "span_extraction": "Non-overlapping paired straight/curly single/double quotes; first closing delimiter. Same-style nested quotes and plural possessives can be ambiguous; none in the four frozen-scope spans. Numeric spans retained.",
           "sources_sha256": hashes, "cohorts": {}, "marked_spans": []}
    for ds, data in datasets.items():
        summary = {}
        for view in VIEWS:
            counts = Counter(n_audits=len(data["ids"]), n_items=0, well_formed_source_items=0,
                             items_with_marked_span=0, n_marked_spans=0)
            locations = Counter({k: 0 for k in LOCATIONS})
            for rid, audit in data["audits"][view].items():
                for ix, e in enumerate(audit.get("evidence") or []):
                    counts["n_items"] += 1
                    # Reject coercion/truncation of malformed anchors. Invalid
                    # items remain in the denominator, with their raw fields.
                    t, f = e.get("round"), e.get("firm")
                    valid = type(t) is int and t in data["rounds"][rid] and f in ("A", "B", "C", "D")
                    counts["well_formed_source_items"] += int(valid)
                    spans = quoted_spans(e.get("observation", ""))
                    counts["items_with_marked_span"] += bool(spans)
                    for span in spans:
                        counts["n_marked_spans"] += 1
                        location = locate(span, data["rounds"][rid], f, t)
                        locations[location["location"]] += 1
                        out["marked_spans"].append({"dataset": ds, "view": view, "run_id": rid,
                                                    "item_index": ix, "round": t, "firm": f,
                                                    "well_formed_anchor": valid, "observation": e["observation"], **location})
            summary[view] = {**dict(counts), "span_locations": dict(locations)}
        out["cohorts"][ds] = summary
    return out


CSS = """
body{font:16px/1.5 system-ui,sans-serif;color:#17243b;margin:auto;max-width:1100px;padding:24px}
a{color:#1657a6}header,.controls{background:#eef3fa;padding:20px;border-radius:8px}
.controls{margin:16px 0;display:flex;gap:16px;flex-wrap:wrap}.controls label{display:flex;gap:8px;align-items:center}
input,select{font:inherit;max-width:100%}.audit{border-left:4px solid #b5c9e3;padding:0 14px;margin:22px 0}
.item{margin:15px 0;padding:10px;background:#f7f9fc}.claim{font-weight:600}.muted{color:#53647a}
details{margin:14px 0}summary{cursor:pointer}table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid #cbd6e5;padding:8px;text-align:left;vertical-align:top}caption{text-align:left;font-weight:600}
.table-wrap{overflow-x:auto}.source-round{scroll-margin-top:12px}.source-round:target{background:#fff3cc}
[hidden]{display:none!important}h2{margin-top:35px}code{overflow-wrap:anywhere}blockquote{margin:8px;border-left:3px solid #cbd6e5;padding-left:14px}
@media(max-width:600px){body{padding:12px}.controls{padding:12px}table{min-width:540px}}
"""

JS = """
const q=document.querySelector('#query'),ds=document.querySelector('#dataset'),v=document.querySelector('#view'),quotes=document.querySelector('#quotes');
// Keep logs open for browsers without JavaScript, including fragment navigation.
document.querySelectorAll('.sources').forEach(s=>s.open=false);
function update(){let n=0;document.querySelectorAll('.run').forEach(run=>{let any=false;run.querySelectorAll('.audit').forEach(a=>{
const show=(!ds.value||run.dataset.ds===ds.value)&&(!v.value||a.dataset.view===v.value)&&(!quotes.checked||a.dataset.quotes==='yes')&&(!q.value||a.textContent.toLowerCase().includes(q.value.toLowerCase())||run.dataset.rid.includes(q.value.toLowerCase()));
a.hidden=!show;any=any||show;if(show)n++;});run.hidden=!any;});document.querySelector('#count').textContent=n+' audits visible';}
[q,ds,v,quotes].forEach(e=>e.addEventListener('input',update));
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#source-"]');if(a){const t=document.getElementById(a.hash.slice(1));if(t)t.closest('details').open=true;}});
update();
"""


def render_html(datasets, result):
    esc = lambda s: html.escape(str(s), quote=True)
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Cached evidence and public sources</title><style>', CSS, '</style></head><body><header><h1>Cached evidence and public sources</h1>',
             '<p>Six original GPT auditor views; 95 test and 30 replication runs. This ledger locates non-overlapping spans marked with straight or curly single/double quotation marks and exposes the public log. ',
             '<strong>Source availability and literal matches do not validate an observation or its inference of collusion.</strong> ',
             'Price transitions, comparisons, paraphrases and causal claims require review. No semantic accuracy rate is estimated.</p>',
             '<p>All content is embedded and readable offline without JavaScript. Filters use JavaScript. ',
             'The full public log is available for comparison, including modalities withheld from a given view. ',
             '<a href="REPORT.html">Report</a> · <a href="results/analysis/evidence_sources.json">Counts and input hashes</a></p></header>',
             '<div class="controls"><label>Search <input id="query" type="search" placeholder="Run ID or evidence text"></label>',
             '<label>Dataset <select id="dataset"><option value="">Both</option><option>llm_v3</option><option>llm_v3rep</option></select></label>',
             '<label>View <select id="view"><option value="">All</option>',
             ''.join(f'<option>{v}</option>' for v in VIEWS), '</select></label>',
             '<label><input id="quotes" type="checkbox">Audits with quote-marked spans</label><output id="count" aria-live="polite"></output></div>']
    quote_index = {}
    for span in result["marked_spans"]:
        key = (span["dataset"], span["view"], span["run_id"], span["item_index"])
        quote_index.setdefault(key, []).append(span)
    for ds, data in datasets.items():
        for rid in data["ids"]:
            parts.append(f'<section class="run" data-ds="{ds}" data-rid="{rid}"><h2>{rid}</h2>')
            info = data["info"][rid].get("public_info", "")
            parts.append(f'<p>Public setup: {esc(info or "No partnership notice.")}</p>')
            parts.append(f'<p>Public cost offsets: {esc(json.dumps(data["info"][rid].get("cost_offset", {}), sort_keys=True))}.</p>')
            for view in VIEWS:
                audit = data["audits"][view][rid]
                evidence = audit.get("evidence") or []
                has_quotes = any((ds, view, rid, i) in quote_index for i in range(len(evidence)))
                parts.append(f'<article class="audit" data-view="{view}" data-quotes="{"yes" if has_quotes else "no"}"><h3>{view}</h3>')
                allowed = "public messages only" if view == "text" else "actions only" if view in ("action", "action_stats") else "public messages and actions"
                parts.append(f'<p class="muted">Auditor saw {allowed}, public facts, and the view-specific summaries defined in REPORT.md. ')
                parts.append(f'Run suspicion {esc(audit["collusion_present"])} / 100. Pair scores: {esc(json.dumps(audit["scores"], sort_keys=True))}.</p>')
                for i, e in enumerate(evidence):
                    t, f = e.get("round"), e.get("firm")
                    parts.append(f'<div class="item" id="evidence-{rid}-{view}-{i}"><p class="claim">{esc(e.get("observation", ""))}</p>')
                    rounds = data["rounds"][rid]
                    valid = type(t) is int and t in rounds and f in ("A", "B", "C", "D")
                    if valid:
                        parts.append(f'<p><a href="#source-{rid}-{t}">Cited round {t}, firm {f}: open all firms in the public log</a></p>')
                        if view not in ("action", "action_stats"):
                            parts.append(f'<blockquote>{esc(rounds[t][f]["public_message"] or "[empty message]")}</blockquote>')
                        if view != "text":
                            parts.append('<p>Cited-round prices: ' + esc(', '.join(f'{firm} = {agent["price"]}' for firm, agent in sorted(rounds[t].items()))) + '.</p>')
                    else:
                        parts.append(f'<p>Invalid source anchor: round {esc(t)}, firm {esc(f)}.</p>')
                    spans = quote_index.get((ds, view, rid, i), [])
                    if spans:
                        for span in spans:
                            parts.append(f'<p>Marked span “{esc(span["span"])}”: <code>{span["location"]}</code>. Literal location only.</p>')
                    else:
                        parts.append('<p class="muted">No quote-marked span; semantic support has not been checked.</p>')
                    parts.append('</div>')
                parts.append('</article>')
            parts.append('<details class="sources" open><summary>Full public log (all rounds and firms)</summary>')
            for t, agents in sorted(data["rounds"][rid].items()):
                parts.append(f'<div class="table-wrap source-round" id="source-{rid}-{t}"><p>Round {t} market: {esc(json.dumps(data["markets"][rid][t], sort_keys=True))}</p><table><caption>Round {t}</caption><thead><tr><th>Firm</th><th>Price</th><th>Units</th><th>Profit</th><th>Public message</th></tr></thead><tbody>')
                for f, a in sorted(agents.items()):
                    parts.append(f'<tr><td>{f}</td><td>{esc(a["price"])}</td><td>{esc(a["quantity"])}</td><td>{esc(a["profit"])}</td><td>{esc(a["public_message"] or "")}</td></tr>')
                parts.append('</tbody></table></div>')
            parts.append('</details></section>')
    parts.extend(['<script>', JS, '</script></body></html>\n'])
    return ''.join(parts)


def render(root=ROOT):
    datasets, hashes = load(root)
    result = inspect(datasets, hashes)
    return {OUTPUTS[0]: json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            OUTPUTS[1]: render_html(datasets, result)}


def check(root=ROOT):
    outputs = render(root)
    for name, content in outputs.items():
        if (root / name).read_bytes() != content.encode("utf-8"):
            raise ValueError(f"stale evidence source ledger: {name}")
    check_claims(root, json.loads(outputs[OUTPUTS[0]]))


def check_claims(root, result):
    """Keep the new hand-written coverage sentences tied to saved-source counts."""
    test, rep = result["cohorts"]["llm_v3"], result["cohorts"]["llm_v3rep"]
    ntest, nrep = (sum(s["n_items"] for s in cohort.values()) for cohort in (test, rep))
    qtest, qrep = (sum(s["items_with_marked_span"] for s in cohort.values()) for cohort in (test, rep))
    claims = {
        "REPORT_APPENDIX.md": (f"test caches contain {ntest:,} evidence items and the replication {nrep:,}",
                      f"only {qtest} test items and {qrep} replication item contain quote-marked phrases"),
        "README.md": (f"all {ntest + nrep:,} original-view test and replication evidence items",
                      f"Only {qtest + qrep} evidence items contain quote-marked phrases"),
    }
    for name, phrases in claims.items():
        text = " ".join((root / name).read_text().split())
        for phrase in phrases:
            if phrase not in text:
                raise ValueError(f"evidence coverage prose differs from source counts: {name}: {phrase}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    outputs = render()
    if args.check:
        for name, content in outputs.items():
            if (ROOT / name).read_bytes() != content.encode("utf-8"):
                raise SystemExit(f"FAIL: stale evidence source ledger: {name}")
        check_claims(ROOT, json.loads(outputs[OUTPUTS[0]]))
    else:
        for name, content in outputs.items():
            (ROOT / name).write_text(content, encoding="utf-8")
    result = json.loads(outputs[OUTPUTS[0]])
    print("PASS: source ledger " + ("matches saved outputs (read-only)" if args.check else "rendered from saved inputs"))
    for ds, views in result["cohorts"].items():
        print(f"{ds}: {sum(s['n_audits'] for s in views.values())} audits; "
              f"{sum(s['n_items'] for s in views.values())} evidence items; "
              f"{sum(s['n_marked_spans'] for s in views.values())} quote-marked spans "
              f"({sum(s['span_locations']['cited_firm_round'] for s in views.values())} located at cited firm/round)")


if __name__ == "__main__":
    main()
