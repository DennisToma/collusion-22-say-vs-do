"""Per-pair features from observable trajectories only (never reads ground_truth).

text_doc(pair)      : concatenated public messages of the two agents (for TF-IDF)
action_feats(pair)  : prices/state/outcome statistics
cross_feats(pair)   : say-vs-do consistency (keyword-parsed claimed direction vs actual move,
                      announcement follow-through by self and by partner)
"""
import json, re
from collections import defaultdict
from itertools import combinations
import numpy as np

AGENTS = ["A", "B", "C", "D"]
PAIRS = ["".join(p) for p in combinations(AGENTS, 2)]

CUT = re.compile(r"\b(trim|lower|cheaper|cut|drop|undercut|discount|down)\w*", re.I)
RAISE = re.compile(r"\b(nudg|rais|up\b|higher|increase|rise|more margin)\w*", re.I)
HOLD = re.compile(r"\b(keep|no change|hold|same|steady|not moving|leaving it)\w*", re.I)
ANN = re.compile(r"(?:next round|next period|upcoming price|next price)[^0-9]*(\d+)|(?:move to|price at) (\d+) next", re.I)


def load(path):
    runs = defaultdict(list)
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            runs[r["run_id"]].append(r)
    for v in runs.values():
        v.sort(key=lambda r: r["round"])
    return dict(runs)


def series(rows):
    P = {a: np.array([[x["price"] for x in r["agents"] if x["id"] == a][0] for r in rows], float) for a in AGENTS}
    M = {a: [[x["public_message"] for x in r["agents"] if x["id"] == a][0] for r in rows] for a in AGENTS}
    cost = np.array([r["market"]["cost"] for r in rows], float)
    return P, M, cost


def parse_claim(msg):
    first = msg.split(".")[0] if msg else ""
    c, ra, h = bool(CUT.search(first)), bool(RAISE.search(first)), bool(HOLD.search(first))
    if c + ra + h != 1:
        return None
    return "cut" if c else ("raise" if ra else "hold")


def parse_announce(msg):
    m = ANN.search(msg or "")
    if not m:
        return None
    return float(m.group(1) or m.group(2))


def _corr(x, y):
    if x.std() < 1e-9 or y.std() < 1e-9:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def consistency(P, M, a):
    ok, n = 0, 0
    p = P[a]
    for t in range(1, len(p)):
        c = parse_claim(M[a][t])
        if c is None:
            continue
        d = "hold" if p[t] == p[t - 1] else ("raise" if p[t] > p[t - 1] else "cut")
        ok += c == d
        n += 1
    return ok / n if n else 0.5, n


def follow(P, M, a, b):
    """Fraction of a's announcements 'x next round' that b (or a) actually priced at."""
    hits_b, hits_a, n = 0, 0, 0
    for t in range(len(P[a]) - 1):
        x = parse_announce(M[a][t])
        if x is None:
            continue
        n += 1
        hits_b += P[b][t + 1] == x
        hits_a += P[a][t + 1] == x
    return (hits_b / n if n else 0.0), (hits_a / n if n else 0.0), n


def pair_features(rows):
    P, M, cost = series(rows)
    out = {}
    cons = {a: consistency(P, M, a)[0] for a in AGENTS}
    for pr in PAIRS:
        a, b = pr
        others = [x for x in AGENTS if x not in pr]
        pa, pb = P[a], P[b]
        po = np.mean([P[o] for o in others], axis=0)
        da, db = np.diff(pa), np.diff(pb)
        both_high = np.mean((pa >= 14) & (pb >= 14))
        act = {
            "pair_markup": float(np.mean((pa + pb) / 2 - cost)),
            "pair_minus_others": float(np.mean((pa + pb) / 2 - po)),
            "frac_equal": float(np.mean(pa == pb)),
            "frac_both_high": float(both_high),
            "corr_level": _corr(pa - cost, pb - cost),
            "corr_change": _corr(da, db),
            "others_markup": float(np.mean(po - cost)),
            "pair_profit_share": float(np.mean([sum(x["profit"] for x in r["agents"] if x["id"] in pr) /
                                                 max(1e-9, sum(x["profit"] for x in r["agents"])) for r in rows])),
        }
        fab, faa, na = follow(P, M, a, b)
        fba, fbb, nb = follow(P, M, b, a)
        others_cons = np.mean([cons[o] for o in others])
        cross = {
            "cons_mean": (cons[a] + cons[b]) / 2,
            "cons_min": min(cons[a], cons[b]),
            "cons_minus_others": (cons[a] + cons[b]) / 2 - others_cons,
            "partner_follow": (fab * na + fba * nb) / max(1, na + nb),
            "self_follow": (faa * na + fbb * nb) / max(1, na + nb),
        }
        text = " ".join(M[a] + M[b])
        out[pr] = {"text": text, "action": act, "cross": cross}
    return out


def load_gt(path):
    with open(path) as f:
        return {g["run_id"]: g for g in map(json.loads, f)}
