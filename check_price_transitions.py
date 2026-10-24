"""Check narrowly parsed price-transition endpoints against saved public logs.

This is a post-hoc source census, not an explanation-accuracy judge. A fixed
grammar recognizes ONLY a leading clause of the form "[A [and B] ...] cuts
[its price] from X to Y" (also raises/reduces/lowers/drops/increases/moves/
changes, present or past tense). An omitted subject binds to the cited firm.
It does not parse later clauses, price levels, ranges, paraphrases, or inference.

The cited round is treated as the endpoint, explicitly a reading rather than
an assertion about the author's intended time window. We distinguish an
adjacent start from any earlier start and expose alternative endpoint rounds.
Neither a matching endpoint pair nor a mismatch validates/refutes the whole
observation. No label, private chat, LLM, metric, CI, or threshold is accessed.

    python3 -S check_price_transitions.py          # saved-source census
    python3 -S check_price_transitions.py --check  # read-only freshness check
"""
import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from check_evidence_sources import ROOT, VIEWS, load

OUTPUTS = ("results/analysis/price_transitions.json", "PRICE_TRANSITIONS.md")
NUMBER = r"(?:0|[1-9]\d*)(?:\.\d+)?"
SUBJECT = r"[A-D](?:(?:,\s*(?:and\s+)?|\s+and\s+|\s*&\s*)[A-D])*"
VERBS = {
    "cut": "down", "cuts": "down", "reduce": "down", "reduces": "down", "reduced": "down",
    "lower": "down", "lowers": "down", "lowered": "down", "drop": "down", "drops": "down", "dropped": "down",
    "raise": "up", "raises": "up", "raised": "up", "increase": "up", "increases": "up", "increased": "up",
    "move": "either", "moves": "either", "moved": "either", "change": "either", "changes": "either", "changed": "either",
}
TRANSITION = re.compile(
    rf"^\s*(?:(?P<subject>{SUBJECT})\s+)?(?:both\s+)?(?P<verb>{'|'.join(VERBS)})\s+"
    rf"(?:(?:(?:its|their|the)\s+)?prices?\s+)?from\s+\$?(?P<before>{NUMBER})"
    rf"\s+to\s+\$?(?P<after>{NUMBER})(?![\w%]|\.\d)", re.I)
# Added after the first census, in response to independent review. This lexical
# diagnostic never expands the validated subset and makes no price-claim label:
# spans may describe costs, later clauses, quoted wording, or other quantities.
LITERAL_FROM_TO = re.compile(rf"\bfrom\s+\$?{NUMBER}\s+to\s+\$?{NUMBER}(?![\w%]|\.\d)", re.I)
STATUSES = ("adjacent_endpoints_match", "earlier_endpoints_match", "cited_endpoint_differs",
            "no_earlier_start_price", "round_1_no_prior_source", "invalid_anchor")


def parse(observation, cited_firm):
    if not isinstance(observation, str):
        raise ValueError("evidence observation must be a string")
    m = TRANSITION.match(observation)
    if not m:
        return None
    firms = re.findall(r"\b[A-D]\b", m["subject"].upper()) if m["subject"] else [cited_firm]
    if m["subject"] and len(set(firms)) != len(firms):
        return None
    before, after = Decimal(m["before"]), Decimal(m["after"])
    direction = VERBS[m["verb"].lower()]
    return {"span": [m.start(), m.end()], "clause": observation[m.start():m.end()],
            "firms": firms, "subject_binding": "explicit" if m["subject"] else "cited_firm",
            "before": m["before"], "after": m["after"], "verb": m["verb"].lower(),
            "direction_agrees_with_numbers": direction == "either" or
                (after > before if direction == "up" else after < before)}


def endpoints(claim, rounds, cited_round, cited_firm):
    valid = (type(cited_round) is int and cited_round in rounds and
             cited_firm in ("A", "B", "C", "D") and cited_firm in rounds[cited_round] and
             all(f in ("A", "B", "C", "D") and f in rounds[cited_round] for f in claim["firms"]))
    if not valid:
        return {"status": "invalid_anchor", "by_firm": {}}
    before, after = Decimal(claim["before"]), Decimal(claim["after"])
    details = {}
    for f in claim["firms"]:
        path = {t: Decimal(str(agents[f]["price"])) for t, agents in sorted(rounds.items())}
        # Alternative witnesses are recorded even when the cited endpoint fails.
        witnesses = [{"end_round": end, "start_rounds": [t for t in path if t < end and path[t] == before]}
                     for end in path if path[end] == after and any(t < end and path[t] == before for t in path)]
        starts = [t for t in path if t < cited_round and path[t] == before]
        if path[cited_round] != after:
            status = "cited_endpoint_differs"
        elif cited_round == 1:
            status = "round_1_no_prior_source"
        elif not starts:
            status = "no_earlier_start_price"
        elif path.get(cited_round - 1) == before:
            status = "adjacent_endpoints_match"
        else:
            status = "earlier_endpoints_match"
        details[f] = {"status": status, "prices_by_round": {str(t): str(p) for t, p in path.items()},
                      "earlier_start_rounds": starts, "alternative_endpoint_witnesses": witnesses}
    # Every named firm must satisfy the endpoint reading. A later start for one
    # firm is kept distinct from an adjacent start for the other.
    statuses = {d["status"] for d in details.values()}
    priority = ("cited_endpoint_differs", "round_1_no_prior_source", "no_earlier_start_price",
                "earlier_endpoints_match", "adjacent_endpoints_match")
    status = next(s for s in priority if s in statuses)
    return {"status": status, "by_firm": details}


def inspect(datasets, hashes):
    result = {"schema_version": 1, "post_hoc": True,
              "scope": "Leading from-X-to-Y price clauses only. Endpoint-source agreement under a cited-round reading; not semantic accuracy or collusion evidence.",
              "selection": {"llm_v3": "0030..0124 (already-exposed test)", "llm_v3rep": "0000..0029 (already-exposed replication)"},
              "grammar": TRANSITION.pattern,
              "reading": "The cited round is the end; the start may be any strictly earlier round, with adjacent matches reported separately. Explicit subjects override cited firm. Omitted subjects bind to cited firm. Only the first clause is parsed.",
              "limits": "A match does not check intermediate prices, duration, timing words, market context, subsequent clauses, or any causal/coordination inference. A mismatch requires source review; it is not a hallucination label. Unparsed items are never counted as successes.",
              "lexical_diagnostic": "Added after first census on review: numeric from-X-to-Y spans anywhere in unparsed items. These may describe costs or later clauses, not necessarily price claims. They never count as endpoint checks.",
              "sources_sha256": hashes, "cohorts": {}, "items": [], "unparsed_numeric_spans": []}
    for ds, data in datasets.items():
        summary = {}
        for view in VIEWS:
            counts = Counter(n_audits=len(data["ids"]), n_items=0, parsed_items=0, unparsed_items=0,
                             numeric_direction_conflicts=0, unparsed_with_numeric_span=0)
            statuses = Counter({s: 0 for s in STATUSES})
            for rid, audit in data["audits"][view].items():
                for ix, evidence in enumerate(audit.get("evidence") or []):
                    counts["n_items"] += 1
                    observation = evidence.get("observation", "")
                    t, f = evidence.get("round"), evidence.get("firm")
                    claim = parse(observation, f)
                    if claim is None:
                        counts["unparsed_items"] += 1
                        spans = [{"span": [m.start(), m.end()], "text": m.group()} for m in LITERAL_FROM_TO.finditer(observation)]
                        if spans:
                            counts["unparsed_with_numeric_span"] += 1
                            result["unparsed_numeric_spans"].append({"dataset": ds, "view": view, "run_id": rid,
                                "item_index": ix, "round": t, "firm": f, "observation": observation, "spans": spans})
                        continue
                    counts["parsed_items"] += 1
                    counts["numeric_direction_conflicts"] += not claim["direction_agrees_with_numbers"]
                    source = endpoints(claim, data["rounds"][rid], t, f)
                    statuses[source["status"]] += 1
                    result["items"].append({"dataset": ds, "view": view, "run_id": rid, "item_index": ix,
                                            "round": t, "firm": f, "observation": observation,
                                            "claim": claim, **source})
            summary[view] = {**dict(counts), "statuses": dict(statuses)}
        result["cohorts"][ds] = summary
    return result


def totals(result, dataset):
    counts, statuses = Counter(), Counter()
    for v in result["cohorts"][dataset].values():
        counts.update({k: val for k, val in v.items() if k != "statuses"})
        statuses.update(v["statuses"])
    return counts, statuses


def markdown(result):
    lines = ["# Price-transition source census", "",
             "Post-hoc check of saved public sources; no model calls or label access. "
             "The selective grammar and census are post-hoc (E69), with no pre-computation commit or external registration. It recognizes only a leading "
             "`[firm(s)] cuts/raises/... [its price] from X to Y` clause. Unparsed observations stay in the denominator.", "",
             "The cited round is read as the end; the start may be any strictly earlier round. "
             "A match checks endpoints only, without checking duration, intermediate prices, later clauses, "
             "context, or the inference of collusion. A mismatch calls for review, not a hallucination label. "
             "The full observation and every source price are retained below and in "
             "[machine-readable output](results/analysis/price_transitions.json).", "",
             "| Dataset / view | Evidence items | Parsed | Adjacent endpoints | Earlier endpoints | Other / review | Unparsed with numeric span |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for ds, cohort in result["cohorts"].items():
        for view, c in cohort.items():
            s = c["statuses"]
            good = s["adjacent_endpoints_match"] + s["earlier_endpoints_match"]
            lines.append(f'| {ds} / {view} | {c["n_items"]} | {c["parsed_items"]} | {s["adjacent_endpoints_match"]} | {s["earlier_endpoints_match"]} | {c["parsed_items"] - good} | {c["unparsed_with_numeric_span"]} |')
        c, s = totals(result, ds)
        good = s["adjacent_endpoints_match"] + s["earlier_endpoints_match"]
        lines.append(f'| **{ds} total** | **{c["n_items"]}** | **{c["parsed_items"]}** | **{s["adjacent_endpoints_match"]}** | **{s["earlier_endpoints_match"]}** | **{c["parsed_items"] - good}** | **{c["unparsed_with_numeric_span"]}** |')
    lines.extend(["", "No semantic accuracy rate or confidence interval is estimated. "
                  "These are finite-cache counts from a selective grammar; they do not measure all price claims. "
                  "Items include repeated descriptions across views and are not independent trajectories. "
                  "Adverbs such as jointly/simultaneously and verbs such as decrease/fall/rise are outside the grammar, "
                  "so the matched subset gives limited assurance about collusion-alleging evidence. "
                  "Both unequal endpoints cannot equal one firm's single cited-round price. Thus the historical "
                  "same-round number check rejects an endpoint-consistent transition if it extracts both endpoints. "
                  "Its ±1-round check can also miss longer transitions. The historical outputs are unchanged.", ""])
    for item in result["items"]:
        rid, view, ix = item["run_id"], item["view"], item["item_index"]
        lines.extend([f'## {rid} / {view} / item {ix}', "",
                      f'[Full public log and original evidence](EVIDENCE.html#evidence-{rid}-{view}-{ix}) · '
                      f'Cited round {item["round"]}, firm {item["firm"]}.', "",
                      "> " + item["observation"].replace("\n", "\n> "), "",
                      f'Parsed: `{item["claim"]["clause"]}`; subject binding: `{item["claim"]["subject_binding"]}`. '
                      f'Endpoint status: **{item["status"]}**. Numeric direction agrees with verb: '
                      f'`{item["claim"]["direction_agrees_with_numbers"]}`.', ""])
        for f, detail in item["by_firm"].items():
            path = ", ".join(f'{t}: {p}' for t, p in detail["prices_by_round"].items())
            lines.append(f'- Firm {f}: `{detail["status"]}`; prices (round: price): {path}. '
                         f'Earlier start rounds: {detail["earlier_start_rounds"]}. '
                         f'Alternative endpoint witnesses: `{json.dumps(detail["alternative_endpoint_witnesses"], separators=(",", ":"))}`.')
        lines.append("")
    lines.extend(["## Unparsed items containing numeric from-to spans", "",
                  "This lexical coverage diagnostic was added after the first census in response to independent review. "
                  "It searches anywhere in unparsed observations and does not expand the endpoint-checked subset. "
                  "Spans can describe costs, later clauses or quoted wording rather than price transitions. "
                  "No source agreement or semantic label is assigned to these items.", ""])
    for item in result["unparsed_numeric_spans"]:
        rid, view, ix = item["run_id"], item["view"], item["item_index"]
        lines.extend([f'### {rid} / {view} / item {ix}', "",
                      f'[Original evidence and public log](EVIDENCE.html#evidence-{rid}-{view}-{ix}).', "",
                      "> " + item["observation"].replace("\n", "\n> "), ""])
    return "\n".join(lines)


def render(root=ROOT):
    datasets, hashes = load(root)
    hashes["check_price_transitions.py"] = hashlib.sha256((root / "check_price_transitions.py").read_bytes()).hexdigest()
    result = inspect(datasets, dict(sorted(hashes.items())))
    return {OUTPUTS[0]: json.dumps(result, indent=2, ensure_ascii=False) + "\n", OUTPUTS[1]: markdown(result)}


def check_claims(root, result):
    parts = []
    omitted = []
    total, statuses = Counter(), Counter()
    for ds in ("llm_v3", "llm_v3rep"):
        c, s = totals(result, ds)
        parts.append(f'{c["parsed_items"]}/{c["n_items"]:,}')
        omitted.append(c["unparsed_with_numeric_span"])
        total.update(c)
        statuses.update(s)
    claims = {
        "REPORT.md": (
            f'leading transition clauses in {parts[0]} test items and {parts[1]} replication items',
            f'All {total["parsed_items"]} parsed clauses have matching source endpoints',
            f'{statuses["adjacent_endpoints_match"]} adjacent-round matches and {statuses["earlier_endpoints_match"]} with an earlier, nonadjacent start',
            f'{omitted[0]} further unparsed test items and {omitted[1]} replication items containing numeric',
        ),
        "README.md": (
            f'It recognizes {total["parsed_items"]} items out of the {total["n_items"]:,}',
            f'{statuses["adjacent_endpoints_match"]} match adjacent rounds and three have an earlier start',
        ),
    }
    if (total["parsed_items"] != statuses["adjacent_endpoints_match"] + statuses["earlier_endpoints_match"] or
            total["numeric_direction_conflicts"] != 0):
        raise ValueError("price-transition prose no longer describes all parsed endpoints; review required")
    # This one word is kept in prose; bind it to the saved count as well.
    if statuses["earlier_endpoints_match"] != 3:
        raise ValueError("price-transition prose word 'three' differs from source count")
    for name, phrases in claims.items():
        text = " ".join((root / name).read_text().split())
        for phrase in phrases:
            if phrase not in text:
                raise ValueError(f"price-transition {name} coverage differs from saved-source counts: {phrase}")


def check(root=ROOT):
    outputs = render(root)
    for name, content in outputs.items():
        if (root / name).read_bytes() != content.encode("utf-8"):
            raise ValueError(f"stale price-transition census: {name}")
    check_claims(root, json.loads(outputs[OUTPUTS[0]]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        check()
    else:
        for name, content in render().items():
            (ROOT / name).write_text(content, encoding="utf-8")
    result = json.loads((ROOT / OUTPUTS[0]).read_text())
    print("PASS: price-transition census " + ("matches saved sources (read-only)" if args.check else "rendered from saved sources"))
    for ds in result["cohorts"]:
        c, s = totals(result, ds)
        print(f'{ds}: {c["parsed_items"]}/{c["n_items"]} parsed items; {dict(s)}; numeric-direction conflicts {c["numeric_direction_conflicts"]}; unparsed items with numeric from-to spans {c["unparsed_with_numeric_span"]}')


if __name__ == "__main__":
    main()
