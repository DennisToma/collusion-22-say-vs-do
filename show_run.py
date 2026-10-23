"""Print a compact view of LLM-market runs: prices per round, public + private messages.
    uv run python show_run.py data/llm_v2 [run_id ...] [--every 2]"""
import json, sys
from pathlib import Path
d = Path(sys.argv[1]); ids = [a for a in sys.argv[2:] if not a.startswith("--")]
every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 1
for f in sorted((d / "raw").glob("*.jsonl")):
    if ids and f.stem not in ids:
        continue
    gt = {json.loads(l)["run_id"]: json.loads(l) for l in open(d / "ground_truth.jsonl")} if (d / "ground_truth.jsonl").exists() else {}
    g = gt.get(f.stem, {})
    print(f"===== {f.stem} cond={g.get('condition')} pair={g.get('assigned_pair')}")
    rows = {}
    for l in open(f):
        x = json.loads(l); t, a = x["key"].split(":"); rows.setdefault(int(t), {})[a] = x
    for t in sorted(rows):
        r = rows[t]
        print(f"r{t:2d} prices", {a: r[a]["price"] for a in sorted(r)})
        if t % every:
            continue
        for a in sorted(r):
            pv = r[a].get("private_message") or ""
            print(f"    {a} PUB: {r[a].get('public_message','')[:160]}" + (f"\n      PRIV: {pv[:200]}" if pv else ""))
