"""E112 participant replacement (Part E2, sprint Q1.2; registered in EXPERIMENTS.tsv before any replaced round was generated).

Paired on E99 (llm_p2strongF: luna, strong framing, T = 40). For each of the 20 private seeds and the first 10 none seeds
(k = 0..9), the replaced game replays rounds 1-20 from the ORIGINAL raw cache (byte-identical decisions, asserted), and
from round 21 one firm is run by a fresh gpt-6-luna manager (llm_market.REPLACE_NOTE: empty private plan, no earlier
private-channel messages; it sees the public price history, the public board and its firm's own sales/profit records).
Replaced firm: private arm = one of the two pair firms, none arm = any of the four firms, drawn with
random.Random(seed * 7 + 1) (fixed before generation). The original run's rounds 21-40 are the paired control.

    SIM_PAR=3 uv run python p2_replace.py gen --games-parallel 3      # generation (resumable; cache per run)
    uv run python p2_replace.py check                                 # prefix identity + coverage only
"""
import argparse, json, random, shutil, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import llm_market as M

SRC, DS, T0, R = "llm_p2strongF", "llm_p2repl", 20, 40
MODEL = "gpt-6-luna"


def design():
    gt = {g["run_id"]: g for g in map(json.loads, open(Path("data") / SRC / "ground_truth.jsonl"))}
    out = []
    for rid, g in sorted(gt.items()):
        k = int(rid.rsplit("_", 1)[1]) // 2
        if g["condition"] == "private" or (g["condition"] == "none" and k < 10):
            pool = g["assigned_pair"] if g["condition"] == "private" else M.AGENTS
            firm = random.Random(g["seed"] * 7 + 1).choice(pool)
            out.append({"src": rid, "rid": rid.replace(SRC, DS), "cond": g["condition"], "seed": g["seed"],
                        "pair": g["assigned_pair"], "firm": firm})
    assert len(out) == 30 and sum(d["cond"] == "private" for d in out) == 20
    return out


def prefix_lines(src_rid):
    rows = [l for l in open(Path("data") / SRC / "raw" / f"{src_rid}.jsonl").read().splitlines()
            if int(json.loads(l)["key"].split(":")[0]) < T0]
    assert len(rows) == 4 * T0 and len({json.loads(l)["key"] for l in rows}) == 4 * T0, src_rid
    return rows


def check(strict=True):
    D = Path("data") / DS
    orig = {}
    for r in map(json.loads, open(Path("data") / SRC / "trajectories.jsonl")):
        orig[(r["run_id"], r["round"])] = r
    new = {}
    if (D / "trajectories.jsonl").exists():
        for r in map(json.loads, open(D / "trajectories.jsonl")):
            new[(r["run_id"], r["round"])] = r
    gts = {g["run_id"]: g for g in map(json.loads, open(D / "ground_truth.jsonl"))} if (D / "ground_truth.jsonl").exists() else {}
    done = 0
    for d in design():
        raw = D / "raw" / f"{d['rid']}.jsonl"
        if raw.exists():
            assert raw.read_text().splitlines()[:4 * T0] == prefix_lines(d["src"]), f"{d['rid']}: raw prefix differs"
        if d["rid"] not in gts:
            continue
        g = gts[d["rid"]]
        assert g["replaced"] == {"round0": T0, "firm": d["firm"]} and g["model"] == MODEL, f"{d['rid']}: gt/model {g['model']}"
        for t in range(T0):
            a, b = dict(new[(d["rid"], t)]), dict(orig[(d["src"], t)])
            a.pop("run_id"); b.pop("run_id")
            assert a == b, f"{d['rid']} round {t + 1}: replayed prefix differs from original"
        assert all((d["rid"], t) in new for t in range(R)), d["rid"]
        done += 1
    print(f"E112 check: {done}/30 replaced games complete; prefixes byte-identical to {SRC} rounds 1-{T0}")
    if strict:
        assert done == 30
    return done


def gen(par):
    M.CFG.update(framing="strong", backend="codex", model=MODEL, sysvar=0, lang="en")
    D = Path("data") / DS; (D / "raw").mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["run_id"] for l in open(D / "ground_truth.jsonl")} if (D / "ground_truth.jsonl").exists() else set()
    lock = threading.Lock()

    def one(d):
        if d["rid"] in done:
            return
        raw = D / "raw" / f"{d['rid']}.jsonl"
        if not raw.exists():
            raw.write_text("\n".join(prefix_lines(d["src"])) + "\n")
        traj, private, gt = M.run_game(D, d["rid"], d["cond"], d["seed"], R, replace=(T0, d["firm"]))
        assert gt["assigned_pair"] == d["pair"], d["rid"]
        with lock:
            for fn, rows in (("trajectories.jsonl", traj), ("private.jsonl", [private]), ("ground_truth.jsonl", [gt])):
                with open(D / fn, "a") as f:
                    f.writelines(json.dumps(r) + "\n" for r in rows)
            print(d["rid"], d["cond"], "replaced", d["firm"], "pair", d["pair"], "last", [x["price"] for x in traj[-1]["agents"]],
                  "model", gt["model"], flush=True)

    # private seeds first so the primary arm completes first
    with ThreadPoolExecutor(par) as ex:
        list(ex.map(one, sorted(design(), key=lambda d: (d["cond"] != "private", d["rid"]))))
    M.write_public_info(D)
    check(strict=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["gen", "check", "design"]); ap.add_argument("--games-parallel", type=int, default=3)
    a = ap.parse_args()
    if a.cmd == "gen":
        gen(a.games_parallel)
    elif a.cmd == "check":
        check()
    else:
        for d in design():
            print(d)
