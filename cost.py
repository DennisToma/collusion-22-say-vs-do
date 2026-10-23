"""Cost table (DIRECTION directive 4): what each detector costs per audited run.

Sources (all in-repo, regenerable):
  results/llm_auditor/<ds>/<auditor>/<view>_orig.jsonl  -> one row per audit call; `chars` = prompt characters
  data/<ds>/raw/*.jsonl                                 -> one row per simulated-seller call (generation cost)
  ~/collusion/llm_calls.jsonl (if present)              -> global call log, SHARED with the sibling project and
                                                           other work, so reported only as a backend/model total.
Tokens are approximated as chars/4 (no tokenizer for these backends). premium = 0 LLM calls (numpy on prices).

    uv run python cost.py --ds llm_v3
"""
import argparse, collections, json
from pathlib import Path
import numpy as np


def _rows(f):
    """jsonl reader that skips half-written lines (files may be appended to concurrently)"""
    out = []
    for l in open(f):
        try:
            out.append(json.loads(l))
        except json.JSONDecodeError:
            pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="llm_v3")
    a = ap.parse_args()
    base = Path("results") / "llm_auditor" / a.ds
    out = {"dataset": a.ds, "token_estimate": "chars/4", "audits": {}}
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        for f in sorted(d.glob("*_orig.jsonl")):
            rows = _rows(f)
            if not rows:
                continue
            ch = np.array([x["chars"] for x in rows], float)
            out["audits"][f"{d.name}/{f.stem.replace('_orig', '')}"] = {
                "calls": len(rows), "mean_prompt_chars": round(float(ch.mean())),
                "mean_prompt_tokens_est": round(float(ch.mean()) / 4), "total_prompt_chars": int(ch.sum())}
    raw = list((Path("data") / a.ds / "raw").glob("*.jsonl"))
    n_seller = sum(1 for f in raw for _ in open(f))
    out["generation"] = {"runs": len(raw), "seller_calls": n_seller, "seller_calls_per_run": round(n_seller / max(len(raw), 1), 1)}
    out["premium"] = {"llm_calls_per_run": 0, "note": "pair mean price minus other two firms; O(rounds) arithmetic"}
    g = Path.home() / "collusion" / "llm_calls.jsonl"
    if g.exists():
        c = collections.Counter()
        for x in _rows(g):
            c[f"{x.get('backend')}/{x.get('model')}"] += 1
        out["global_call_log_shared"] = dict(c)
    Path("results/analysis").mkdir(parents=True, exist_ok=True)
    (Path("results/analysis") / f"cost_{a.ds}.json").write_text(json.dumps(out, indent=1))
    print(f"{'auditor/view':38s} calls  prompt_chars  ~tokens")
    for k, v in out["audits"].items():
        print(f"{k:38s} {v['calls']:5d}  {v['mean_prompt_chars']:12d}  {v['mean_prompt_tokens_est']:7d}")
    print("generation:", out["generation"])


if __name__ == "__main__":
    main()
