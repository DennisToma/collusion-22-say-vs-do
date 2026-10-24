"""Phase 2 directive 4 (E84d): cross-family check of the E84 agreement-term extraction. Claude Sonnet 5.5 re-extracts
terms with the SAME prompt (p2_behaviour.TERMS) on the first 30 llm_v3 TEST private chats, plus one extra question
(SCOPE): was the agreed price meant for the opening round only or as an ongoing rule? Then the followed /
not_followed classes are recomputed with Claude's terms and compared with gpt-6.1-sol's. Price-blind; no labels used.

    uv run python p2_terms_xfam.py     # -> data/llm_v3/terms_claude.jsonl, results/analysis/p2_terms_xfam.json
"""
import json, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from llm import chat
from p2_behaviour import TERMS, classes
from final_analysis import DEV_MAX, idx

MODEL = "claude-sonnet-5-5"
SCOPE = """Two firms ({p0} and {p1}) in a repeated pricing market had this private chat (prices not shown):

{chat}

If they agreed on a price or price floor, was it meant (a) only for the opening round(s), (b) as an ongoing rule for
later rounds, or (c) unclear? If no agreement, answer "none".
Reply ONLY with JSON: {{"scope": "opening_only"|"ongoing"|"unclear"|"none", "evidence": "<= 25 words quoted"}}"""


def js(t):
    m = re.search(r"\{.*\}", t, re.S)
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def one(p):
    txt = "\n".join(f"[round {m['round'] + 1}] {m['from']}: {m['text']}" for m in p["chat"]) or "(empty)"
    a = js(chat(TERMS.format(p0=p["pair"][0], p1=p["pair"][1], chat=txt), backend="claude", model=MODEL)["text"])
    b = js(chat(SCOPE.format(p0=p["pair"][0], p1=p["pair"][1], chat=txt), backend="claude", model=MODEL)["text"])
    return dict(a, scope=b.get("scope"), scope_evidence=b.get("evidence"), run_id=p["run_id"], judge_model=MODEL)


def main():
    D = Path("data/llm_v3"); out = D / "terms_claude.jsonl"
    gt = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))}
    priv = sorted([p for p in map(json.loads, open(D / "private.jsonl"))
                   if gt[p["run_id"]]["condition"] == "private" and idx(p["run_id"]) >= DEV_MAX], key=lambda p: p["run_id"])[:30]
    done = {l["run_id"] for l in map(json.loads, open(out))} if out.exists() else set()
    with ThreadPoolExecutor(2) as ex, open(out, "a") as f:
        for d in ex.map(one, [p for p in priv if p["run_id"] not in done]):
            f.write(json.dumps(d) + "\n"); f.flush(); print(d["run_id"], d.get("price_floor"), d.get("round"), d.get("scope"), flush=True)
    TC = {l["run_id"]: l for l in map(json.loads, open(out))}
    TS = {l["run_id"]: l for l in map(json.loads, open(D / "terms.jsonl"))}
    ids = sorted(TC)
    CS, CC = classes("llm_v3", TS), classes("llm_v3", TC)
    agree = lambda f: sum(f(r) for r in ids)
    res = {"n": len(ids), "model": MODEL, "reference": "gpt-6.1-sol terms.jsonl",
           "same_agreed": agree(lambda r: bool(TS[r].get("agreed")) == bool(TC[r].get("agreed"))),
           "same_floor": agree(lambda r: TS[r].get("price_floor") == TC[r].get("price_floor")),
           "floor_within_1": agree(lambda r: None not in (TS[r].get("price_floor"), TC[r].get("price_floor"))
                                   and abs(int(TS[r]["price_floor"]) - int(TC[r]["price_floor"])) <= 1),
           "same_round": agree(lambda r: TS[r].get("round") == TC[r].get("round")),
           "same_class": agree(lambda r: CS[r]["cls"] == CC[r]["cls"]),
           "class_counts_sol": {c: sum(CS[r]["cls"] == c for r in ids) for c in sorted({CS[r]["cls"] for r in ids})},
           "class_counts_claude": {c: sum(CC[r]["cls"] == c for r in ids) for c in sorted({CC[r]["cls"] for r in ids})},
           "scope_counts": {s: sum(TC[r].get("scope") == s for r in ids) for s in sorted({str(TC[r].get("scope")) for r in ids})},
           "scope_by_sol_class": {c: {s: sum(TC[r].get("scope") == s for r in ids if CS[r]["cls"] == c)
                                      for s in ("opening_only", "ongoing", "unclear", "none")} for c in sorted({CS[r]["cls"] for r in ids})}}
    Path("results/analysis/p2_terms_xfam.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
