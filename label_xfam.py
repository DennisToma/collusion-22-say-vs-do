"""E74: cross-family re-judge of private-chat labels (label robustness only; never auditor input).

Re-runs label_llm.JUDGE verbatim (blind to prices) with Claude Sonnet 5.5 on every private chat of
llm_v3, llm_v3rep, llm_v3fp, llm_v3mon. Writes data/<ds>/labels_claude.jsonl (cached, append-only);
the primary labels.jsonl and all audit scores are untouched. Summary -> results/label_xfam.json.

    uv run python label_xfam.py            # call (cached) + summarise
    uv run python label_xfam.py --summary  # summarise only
"""
import argparse, json, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from llm import chat
from label_llm import JUDGE

DS = ["llm_v3", "llm_v3rep", "llm_v3fp", "llm_v3mon"]
MODEL = "claude-sonnet-5-5"
POS = ("explicit", "info_exchange")


def judge(priv):
    pair = priv["pair"]
    chat_txt = "\n".join(f"[round {m['round'] + 1}] {m['from']}: {m['text']}" for m in priv["chat"]) or "(empty)"
    r = chat(JUDGE.format(p0=pair[0], p1=pair[1], chat=chat_txt), backend="claude", model=MODEL,
             tier="cheap", max_tokens=400)
    m = re.search(r"\{.*\}", r["text"], re.S)
    try:
        d = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        d = {}
    return {"agreement": d.get("agreement"), "first_round": d.get("first_round"),
            "evidence": d.get("evidence", ""), "judge_model": r["model"], "backend": r["backend"]}


def load(p):
    return {json.loads(l)["run_id"]: json.loads(l) for l in open(p)} if p.exists() else {}


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return None if pe == 1 else (po - pe) / (1 - pe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    if not a.summary:
        for ds in DS:
            d = Path("data") / ds
            priv = load(d / "private.jsonl")
            gt = load(d / "ground_truth.jsonl")
            out = d / "labels_claude.jsonl"
            done = load(out)
            todo = [rid for rid in priv if gt[rid]["condition"] == "private" and rid not in done]

            def one(rid):
                try:
                    return {"run_id": rid, **judge(priv[rid])}
                except Exception as e:  # failed calls are not cached
                    print("FAIL", ds, rid, e, flush=True)
                    return None
            with ThreadPoolExecutor(3) as ex:
                for lab in ex.map(one, todo):
                    if lab and lab["agreement"] in ("explicit", "info_exchange", "none"):
                        with open(out, "a") as f:
                            f.write(json.dumps(lab) + "\n")
                        print(ds, lab["run_id"], lab["agreement"], flush=True)
    res = {"model": MODEL, "prompt": "label_llm.JUDGE (verbatim)", "datasets": {}}
    for ds in DS:
        d = Path("data") / ds
        gpt, cl = load(d / "labels.jsonl"), load(d / "labels_claude.jsonl")
        exp = {r for r, g in load(d / "ground_truth.jsonl").items() if g["condition"] == "private"}
        ids = sorted(cl)
        assert set(ids) == exp and exp <= set(gpt), f"{ds}: coverage mismatch"
        assert all(cl[r]["agreement"] in ("explicit", "info_exchange", "none") for r in ids), f"{ds}: bad label"
        assert all(cl[r]["judge_model"] == MODEL and cl[r]["backend"] == "claude" for r in ids), f"{ds}: wrong model"
        g3 = [gpt[r]["agreement"] for r in ids]
        c3 = [cl[r]["agreement"] for r in ids]
        gy = [int(x in POS) for x in g3]
        cy = [int(x in POS) for x in c3]
        n = len(ids)
        res["datasets"][ds] = {
            "n": n, "n_private_total": sum(1 for r in load(d / "ground_truth.jsonl").values() if r["condition"] == "private"),
            "gpt_y1": sum(gy), "claude_y1": sum(cy),
            "binary_agree": sum(x == y for x, y in zip(gy, cy)), "binary_agree_frac": round(sum(x == y for x, y in zip(gy, cy)) / n, 3) if n else None,
            "kappa_3class": None if not n else (round(k, 3) if (k := kappa(g3, c3)) is not None else None),
            "class3_agree": sum(x == y for x, y in zip(g3, c3)),
            "claude_counts": {k: c3.count(k) for k in sorted(set(c3))},
            "gpt_counts": {k: g3.count(k) for k in sorted(set(g3))},
            "disagreements": [{"run_id": r, "gpt": gpt[r]["agreement"], "claude": cl[r]["agreement"],
                               "claude_evidence": cl[r]["evidence"]} for r in ids
                              if int(gpt[r]["agreement"] in POS) != int(cl[r]["agreement"] in POS)],
        }
    Path("results/label_xfam.json").write_text(json.dumps(res, indent=1))
    for ds, v in res["datasets"].items():
        print(ds, {k: v[k] for k in v if k != "disagreements"}, "disagree:", [x["run_id"] for x in v["disagreements"]])


if __name__ == "__main__":
    main()
