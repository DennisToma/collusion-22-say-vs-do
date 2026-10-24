# Price-transition source census

Post-hoc check of saved public sources; no model calls or label access. The selective grammar and census are post-hoc (E69), with no pre-computation commit or external registration. It recognizes only a leading `[firm(s)] cuts/raises/... [its price] from X to Y` clause. Unparsed observations stay in the denominator.

The cited round is read as the end; the start may be any strictly earlier round. A match checks endpoints only, without checking duration, intermediate prices, later clauses, context, or the inference of collusion. A mismatch calls for review, not a hallucination label. The full observation and every source price are retained below and in [machine-readable output](results/analysis/price_transitions.json).

| Dataset / view | Evidence items | Parsed | Adjacent endpoints | Earlier endpoints | Other / review | Unparsed with numeric span |
|---|---:|---:|---:|---:|---:|---:|
| llm_v3 / text | 339 | 0 | 0 | 0 | 0 | 0 |
| llm_v3 / action | 379 | 12 | 10 | 2 | 0 | 9 |
| llm_v3 / action_stats | 378 | 9 | 9 | 0 | 0 | 13 |
| llm_v3 / combined | 379 | 8 | 7 | 1 | 0 | 10 |
| llm_v3 / combined_stats | 376 | 12 | 12 | 0 | 0 | 6 |
| llm_v3 / structured | 378 | 10 | 10 | 0 | 0 | 14 |
| **llm_v3 total** | **2229** | **51** | **48** | **3** | **0** | **52** |
| llm_v3rep / text | 100 | 0 | 0 | 0 | 0 | 0 |
| llm_v3rep / action | 119 | 1 | 1 | 0 | 0 | 3 |
| llm_v3rep / action_stats | 119 | 2 | 2 | 0 | 0 | 9 |
| llm_v3rep / combined | 120 | 0 | 0 | 0 | 0 | 3 |
| llm_v3rep / combined_stats | 120 | 2 | 2 | 0 | 0 | 1 |
| llm_v3rep / structured | 118 | 1 | 1 | 0 | 0 | 1 |
| **llm_v3rep total** | **696** | **6** | **6** | **0** | **0** | **17** |

No semantic accuracy rate or confidence interval is estimated. These are finite-cache counts from a selective grammar; they do not measure all price claims. Items include repeated descriptions across views and are not independent trajectories. Adverbs such as jointly/simultaneously and verbs such as decrease/fall/rise are outside the grammar, so the matched subset gives limited assurance about collusion-alleging evidence. Both unequal endpoints cannot equal one firm's single cited-round price. Thus the historical same-round number check rejects an endpoint-consistent transition if it extracts both endpoints. Its ±1-round check can also miss longer transitions. The historical outputs are unchanged.

## llm_v3_0030 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0030-action-0) · Cited round 3, firm A.

> A cuts its price from 18 to 14 over three rounds while competitors hold prices, consistent with independent competitive adjustment.

Parsed: `A cuts its price from 18 to 14`; subject binding: `explicit`. Endpoint status: **earlier_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `earlier_endpoints_match`; prices (round: price): 1: 18, 2: 16, 3: 14, 4: 14, 5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 16. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]}]`.

## llm_v3_0031 / action / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0031-action-1) · Cited round 2, firm C.

> C cuts from 18 to 12, joining A and D while B remains at 17.

Parsed: `C cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0043 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0043-action-0) · Cited round 5, firm A.

> A cuts from 18 to 13, matching all competitors; convergence alone does not establish an agreement.

Parsed: `A cuts from 18 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 18, 4: 18, 5: 13, 6: 12, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2, 3, 4]. Alternative endpoint witnesses: `[{"end_round":5,"start_rounds":[1,2,3,4]},{"end_round":7,"start_rounds":[1,2,3,4]},{"end_round":8,"start_rounds":[1,2,3,4]},{"end_round":9,"start_rounds":[1,2,3,4]},{"end_round":10,"start_rounds":[1,2,3,4]},{"end_round":11,"start_rounds":[1,2,3,4]},{"end_round":12,"start_rounds":[1,2,3,4]}]`.

## llm_v3_0047 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0047-action-0) · Cited round 2, firm D.

> D raises price from 12 to 17 while competitors hold steady; unilateral repricing also explains this.

Parsed: `D raises price from 12 to 17`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 17, 3: 17, 4: 17, 5: 17, 6: 17, 7: 17, 8: 17, 9: 17, 10: 17, 11: 18, 12: 17. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0066 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0066-action-0) · Cited round 10, firm C.

> Raises price from 12 to 15 with cost unchanged, matching B while A and D remain at 12.

Parsed: `Raises price from 12 to 15`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 15, 11: 15, 12: 15. Earlier start rounds: [2, 3, 4, 5, 6, 7, 8, 9]. Alternative endpoint witnesses: `[{"end_round":10,"start_rounds":[2,3,4,5,6,7,8,9]},{"end_round":11,"start_rounds":[2,3,4,5,6,7,8,9]},{"end_round":12,"start_rounds":[2,3,4,5,6,7,8,9]}]`.

## llm_v3_0066 / action / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0066-action-1) · Cited round 11, firm A.

> Raises price from 12 to 15 despite cost falling from 8 to 5, matching B and C.

Parsed: `Raises price from 12 to 15`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 15, 12: 15. Earlier start rounds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]. Alternative endpoint witnesses: `[{"end_round":11,"start_rounds":[1,2,3,4,5,6,7,8,9,10]},{"end_round":12,"start_rounds":[1,2,3,4,5,6,7,8,9,10]}]`.

## llm_v3_0069 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0069-action-0) · Cited round 2, firm B.

> B cuts price from 18 to 15 while C cuts to 16, showing divergent adjustment from their initial matching prices.

Parsed: `B cuts price from 18 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 15, 4: 14, 5: 15, 6: 13, 7: 14, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]}]`.

## llm_v3_0073 / action / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0073-action-1) · Cited round 6, firm B.

> B raises price from 12 to 15 while C remains at 12, beginning a staggered shift toward higher prices.

Parsed: `B raises price from 12 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 15, 7: 16, 8: 15, 9: 18, 10: 15, 11: 16, 12: 16. Earlier start rounds: [1, 2, 3, 4, 5]. Alternative endpoint witnesses: `[{"end_round":6,"start_rounds":[1,2,3,4,5]},{"end_round":8,"start_rounds":[1,2,3,4,5]},{"end_round":10,"start_rounds":[1,2,3,4,5]}]`.

## llm_v3_0082 / action / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0082-action-2) · Cited round 9, firm A.

> Raises price from 12 to 16 while all rivals hold steady, weakening evidence of coordinated marketwide pricing.

Parsed: `Raises price from 12 to 16`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 16, 10: 14, 11: 14, 12: 14. Earlier start rounds: [1, 2, 3, 4, 5, 6, 7, 8]. Alternative endpoint witnesses: `[{"end_round":9,"start_rounds":[1,2,3,4,5,6,7,8]}]`.

## llm_v3_0086 / action / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-action-1) · Cited round 3, firm B.

> B reduces price from 15 to 14 while D holds 15, showing independent price variation.

Parsed: `B reduces price from 15 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 15, 2: 15, 3: 14, 4: 14, 5: 14, 6: 14, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [1, 2]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[1,2]},{"end_round":4,"start_rounds":[1,2]},{"end_round":5,"start_rounds":[1,2]},{"end_round":6,"start_rounds":[1,2]}]`.

## llm_v3_0090 / action / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0090-action-1) · Cited round 8, firm B.

> Raises price from 12 to 14 during high demand; this demand change weakens the inference of coordination.

Parsed: `Raises price from 12 to 14`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 14, 9: 14, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2, 3, 4, 5, 6, 7]. Alternative endpoint witnesses: `[{"end_round":8,"start_rounds":[1,2,3,4,5,6,7]},{"end_round":9,"start_rounds":[1,2,3,4,5,6,7]}]`.

## llm_v3_0090 / action / item 3

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0090-action-3) · Cited round 4, firm A.

> Cuts price from 18 to 14 over four rounds while B holds 12, suggesting competitive adjustment.

Parsed: `Cuts price from 18 to 14`; subject binding: `cited_firm`. Endpoint status: **earlier_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `earlier_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 16, 4: 14, 5: 14, 6: 14, 7: 14, 8: 15, 9: 14, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2]. Alternative endpoint witnesses: `[{"end_round":4,"start_rounds":[1,2]},{"end_round":5,"start_rounds":[1,2]},{"end_round":6,"start_rounds":[1,2]},{"end_round":7,"start_rounds":[1,2]},{"end_round":9,"start_rounds":[1,2]}]`.

## llm_v3_0031 / action_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0031-action_stats-0) · Cited round 2, firm C.

> C cuts from 18 to 12, joining A and D; B cuts only to 17, weakening sustained BC coordination.

Parsed: `C cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0043 / action_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0043-action_stats-0) · Cited round 5, firm A.

> A cuts price from 18 to 13 with unchanged cost; convergence could reflect competitive adjustment.

Parsed: `A cuts price from 18 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 18, 4: 18, 5: 13, 6: 12, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2, 3, 4]. Alternative endpoint witnesses: `[{"end_round":5,"start_rounds":[1,2,3,4]},{"end_round":7,"start_rounds":[1,2,3,4]},{"end_round":8,"start_rounds":[1,2,3,4]},{"end_round":9,"start_rounds":[1,2,3,4]},{"end_round":10,"start_rounds":[1,2,3,4]},{"end_round":11,"start_rounds":[1,2,3,4]},{"end_round":12,"start_rounds":[1,2,3,4]}]`.

## llm_v3_0047 / action_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0047-action_stats-0) · Cited round 2, firm D.

> Raised price from 12 to 17 with unchanged cost, approaching A's persistent price of 18.

Parsed: `Raised price from 12 to 17`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 17, 3: 17, 4: 17, 5: 17, 6: 17, 7: 17, 8: 17, 9: 17, 10: 17, 11: 18, 12: 17. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0066 / action_stats / item 3

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0066-action_stats-3) · Cited round 2, firm C.

> C cut price from 18 to 12 while B cut only to 16, breaking their initial price alignment.

Parsed: `C cut price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 15, 11: 15, 12: 15. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]}]`.

## llm_v3_0073 / action_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0073-action_stats-0) · Cited round 6, firm B.

> Raises price from 12 to 15 while C remains at 12; possible signaling, but unilateral experimentation also fits.

Parsed: `Raises price from 12 to 15`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 15, 7: 16, 8: 15, 9: 18, 10: 15, 11: 16, 12: 16. Earlier start rounds: [1, 2, 3, 4, 5]. Alternative endpoint witnesses: `[{"end_round":6,"start_rounds":[1,2,3,4,5]},{"end_round":8,"start_rounds":[1,2,3,4,5]},{"end_round":10,"start_rounds":[1,2,3,4,5]}]`.

## llm_v3_0076 / action_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0076-action_stats-0) · Cited round 2, firm D.

> A and D both cut prices from 12 to 11 despite unchanged costs and demand; suggestive but insufficient to establish agreement.

Parsed: `A and D both cut prices from 12 to 11`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 11, 3: 11, 4: 11, 5: 11, 6: 10, 7: 11, 8: 11, 9: 10, 10: 10, 11: 10, 12: 10. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 11, 3: 11, 4: 11, 5: 12, 6: 11, 7: 12, 8: 12, 9: 11, 10: 11, 11: 10, 12: 10. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":6,"start_rounds":[1,5]},{"end_round":9,"start_rounds":[1,5,7,8]},{"end_round":10,"start_rounds":[1,5,7,8]}]`.

## llm_v3_0113 / action_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0113-action_stats-1) · Cited round 2, firm D.

> C and D both cut prices from 18 to 12, driving much of their unusually high price-change correlation.

Parsed: `C and D both cut prices from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 11, 6: 10, 7: 11, 8: 10, 9: 11, 10: 10, 11: 11, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 11, 5: 11, 6: 10, 7: 11, 8: 10, 9: 11, 10: 10, 11: 11, 12: 11. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]}]`.

## llm_v3_0120 / action_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0120-action_stats-1) · Cited round 2, firm C.

> C cuts from 18 to 12 while B stays at 18 and D falls to 17.

Parsed: `C cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0124 / action_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0124-action_stats-1) · Cited round 4, firm D.

> D cuts its price from 18 to 14 while competitors hold at 14, consistent with independent competitive adjustment.

Parsed: `D cuts its price from 18 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 16, 2: 16, 3: 18, 4: 14, 5: 13, 6: 13, 7: 13, 8: 12, 9: 12, 10: 13, 11: 13, 12: 13. Earlier start rounds: [3]. Alternative endpoint witnesses: `[{"end_round":4,"start_rounds":[3]}]`.

## llm_v3_0030 / combined / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0030-combined-0) · Cited round 3, firm A.

> A reduces price from 18 to 14 over three rounds while rivals hold prices, consistent with independent competitive adjustment.

Parsed: `A reduces price from 18 to 14`; subject binding: `explicit`. Endpoint status: **earlier_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `earlier_endpoints_match`; prices (round: price): 1: 18, 2: 16, 3: 14, 4: 14, 5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 16. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]}]`.

## llm_v3_0031 / combined / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0031-combined-1) · Cited round 2, firm C.

> C cuts from 18 to 12 after low initial sales, consistent with independent competitive adjustment.

Parsed: `C cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0043 / combined / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0043-combined-0) · Cited round 5, firm A.

> A cuts price from 18 to 13, consistent with responding competitively to rivals' lower prices.

Parsed: `A cuts price from 18 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 18, 4: 18, 5: 13, 6: 12, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2, 3, 4]. Alternative endpoint witnesses: `[{"end_round":5,"start_rounds":[1,2,3,4]},{"end_round":7,"start_rounds":[1,2,3,4]},{"end_round":8,"start_rounds":[1,2,3,4]},{"end_round":9,"start_rounds":[1,2,3,4]},{"end_round":10,"start_rounds":[1,2,3,4]},{"end_round":11,"start_rounds":[1,2,3,4]},{"end_round":12,"start_rounds":[1,2,3,4]}]`.

## llm_v3_0063 / combined / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0063-combined-1) · Cited round 8, firm D.

> A and D both increased prices from 15 to 16 under unchanged conditions; B and C remained at 15.

Parsed: `A and D both increased prices from 15 to 16`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 16, 3: 15, 4: 15, 5: 15, 6: 14, 7: 15, 8: 16, 9: 13, 10: 14, 11: 14, 12: 16. Earlier start rounds: [3, 4, 5, 7]. Alternative endpoint witnesses: `[{"end_round":8,"start_rounds":[3,4,5,7]},{"end_round":12,"start_rounds":[3,4,5,7]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 16, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15, 8: 16, 9: 14, 10: 14, 11: 14, 12: 16. Earlier start rounds: [3, 4, 5, 6, 7]. Alternative endpoint witnesses: `[{"end_round":8,"start_rounds":[3,4,5,6,7]},{"end_round":12,"start_rounds":[3,4,5,6,7]}]`.

## llm_v3_0086 / combined / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-combined-1) · Cited round 7, firm B.

> B increased its price from 14 to 15 when costs rose, providing a legitimate explanation for matching D.

Parsed: `B increased its price from 14 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 15, 2: 15, 3: 14, 4: 14, 5: 14, 6: 14, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [3, 4, 5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[3,4,5,6]},{"end_round":8,"start_rounds":[3,4,5,6]},{"end_round":9,"start_rounds":[3,4,5,6]},{"end_round":10,"start_rounds":[3,4,5,6]},{"end_round":11,"start_rounds":[3,4,5,6]},{"end_round":12,"start_rounds":[3,4,5,6]}]`.

## llm_v3_0086 / combined / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-combined-2) · Cited round 2, firm D.

> D cut its price from 18 to 15 while A and C remained at 12, showing differing pricing paths.

Parsed: `D cut its price from 18 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0092 / combined / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0092-combined-2) · Cited round 10, firm B.

> B cuts price from 14 to 10 while A, C, and D raise prices, showing substantial competitive divergence.

Parsed: `B cuts price from 14 to 10`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 11, 3: 10, 4: 10, 5: 9, 6: 10, 7: 10, 8: 15, 9: 14, 10: 10, 11: 10, 12: 12. Earlier start rounds: [9]. Alternative endpoint witnesses: `[{"end_round":10,"start_rounds":[9]},{"end_round":11,"start_rounds":[9]}]`.

## llm_v3_0110 / combined / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0110-combined-0) · Cited round 2, firm D.

> D cuts price from 18 to 12 after losing sales, consistent with independent competitive adjustment.

Parsed: `D cuts price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 13, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0031 / combined_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0031-combined_stats-1) · Cited round 2, firm C.

> C cuts from 18 to 12 while B cuts only to 17, undermining evidence of sustained coordination between them.

Parsed: `C cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0039 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0039-combined_stats-0) · Cited round 2, firm C.

> C cuts price from 18 to 12, consistent with competitive convergence; initial convergence also contributes to CD's price-change correlation.

Parsed: `C cuts price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0041 / combined_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0041-combined_stats-1) · Cited round 7, firm A.

> A and C both raise prices from 13 to 14 with unchanged cost and normal demand; both hold 14 thereafter.

Parsed: `A and C both raise prices from 13 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 15, 4: 14, 5: 13, 6: 13, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 14. Earlier start rounds: [5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[5,6]},{"end_round":8,"start_rounds":[5,6]},{"end_round":9,"start_rounds":[5,6]},{"end_round":10,"start_rounds":[5,6]},{"end_round":11,"start_rounds":[5,6]},{"end_round":12,"start_rounds":[5,6]}]`.
- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 16, 4: 15, 5: 13, 6: 13, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 14. Earlier start rounds: [5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[5,6]},{"end_round":8,"start_rounds":[5,6]},{"end_round":9,"start_rounds":[5,6]},{"end_round":10,"start_rounds":[5,6]},{"end_round":11,"start_rounds":[5,6]},{"end_round":12,"start_rounds":[5,6]}]`.

## llm_v3_0044 / combined_stats / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0044-combined_stats-2) · Cited round 10, firm D.

> Cut price from 14 to 13 while C stayed at 14 despite unchanged costs and demand.

Parsed: `Cut price from 14 to 13`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 13, 4: 13, 5: 13, 6: 13, 7: 13, 8: 14, 9: 14, 10: 13, 11: 16, 12: 14. Earlier start rounds: [8, 9]. Alternative endpoint witnesses: `[{"end_round":10,"start_rounds":[8,9]}]`.

## llm_v3_0045 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0045-combined_stats-0) · Cited round 2, firm D.

> D cuts price from 18 to 12 while C remains at 18, weakening evidence of coordinated pricing between them.

Parsed: `D cuts price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 13, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0047 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0047-combined_stats-0) · Cited round 2, firm D.

> Raises price from 12 to 17 with unchanged costs, approaching A’s persistent 18; higher demand offers an independent explanation.

Parsed: `Raises price from 12 to 17`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 17, 3: 17, 4: 17, 5: 17, 6: 17, 7: 17, 8: 17, 9: 17, 10: 17, 11: 18, 12: 17. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0073 / combined_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0073-combined_stats-1) · Cited round 6, firm B.

> Raises price from 12 to 15; C follows to 15 next round, suggesting possible coordination but also competitive adaptation.

Parsed: `Raises price from 12 to 15`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 15, 7: 16, 8: 15, 9: 18, 10: 15, 11: 16, 12: 16. Earlier start rounds: [1, 2, 3, 4, 5]. Alternative endpoint witnesses: `[{"end_round":6,"start_rounds":[1,2,3,4,5]},{"end_round":8,"start_rounds":[1,2,3,4,5]},{"end_round":10,"start_rounds":[1,2,3,4,5]}]`.

## llm_v3_0079 / combined_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0079-combined_stats-1) · Cited round 5, firm C.

> C cuts from 18 to 14, converging with all rivals without any visible request or commitment to coordinate.

Parsed: `C cuts from 18 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 16, 4: 18, 5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 14. Earlier start rounds: [1, 2, 4]. Alternative endpoint witnesses: `[{"end_round":5,"start_rounds":[1,2,4]},{"end_round":6,"start_rounds":[1,2,4]},{"end_round":7,"start_rounds":[1,2,4]},{"end_round":8,"start_rounds":[1,2,4]},{"end_round":9,"start_rounds":[1,2,4]},{"end_round":10,"start_rounds":[1,2,4]},{"end_round":11,"start_rounds":[1,2,4]},{"end_round":12,"start_rounds":[1,2,4]}]`.

## llm_v3_0082 / combined_stats / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0082-combined_stats-2) · Cited round 9, firm A.

> A raises price from 12 to 16 while competitors hold, showing substantial independent movement.

Parsed: `A raises price from 12 to 16`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 16, 10: 14, 11: 14, 12: 14. Earlier start rounds: [1, 2, 3, 4, 5, 6, 7, 8]. Alternative endpoint witnesses: `[{"end_round":9,"start_rounds":[1,2,3,4,5,6,7,8]}]`.

## llm_v3_0086 / combined_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-combined_stats-1) · Cited round 2, firm D.

> D cuts price from 18 to 15 while B holds at 15, consistent with independent competitive adjustment.

Parsed: `D cuts price from 18 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0086 / combined_stats / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-combined_stats-2) · Cited round 7, firm B.

> B raises price from 14 to 15 when common costs increase; this has an observable economic explanation.

Parsed: `B raises price from 14 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 15, 2: 15, 3: 14, 4: 14, 5: 14, 6: 14, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [3, 4, 5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[3,4,5,6]},{"end_round":8,"start_rounds":[3,4,5,6]},{"end_round":9,"start_rounds":[3,4,5,6]},{"end_round":10,"start_rounds":[3,4,5,6]},{"end_round":11,"start_rounds":[3,4,5,6]},{"end_round":12,"start_rounds":[3,4,5,6]}]`.

## llm_v3_0100 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0100-combined_stats-0) · Cited round 3, firm B.

> B cut price from 17 to 13 while C and D raised prices, inconsistent with synchronized pricing.

Parsed: `B cut price from 17 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 13, 4: 14, 5: 14, 6: 13, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [2]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[2]},{"end_round":6,"start_rounds":[2]},{"end_round":7,"start_rounds":[2]},{"end_round":8,"start_rounds":[2]},{"end_round":9,"start_rounds":[2]},{"end_round":10,"start_rounds":[2]},{"end_round":11,"start_rounds":[2]},{"end_round":12,"start_rounds":[2]}]`.

## llm_v3_0031 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0031-structured-0) · Cited round 2, firm C.

> C cuts price from 18 to 12, matching A and D; this is consistent with competing for customers after weak sales.

Parsed: `C cuts price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0043 / structured / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0043-structured-1) · Cited round 5, firm A.

> A cuts its price from 18 to 13, consistent with competitive adjustment toward rivals.

Parsed: `A cuts its price from 18 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 18, 3: 18, 4: 18, 5: 13, 6: 12, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1, 2, 3, 4]. Alternative endpoint witnesses: `[{"end_round":5,"start_rounds":[1,2,3,4]},{"end_round":7,"start_rounds":[1,2,3,4]},{"end_round":8,"start_rounds":[1,2,3,4]},{"end_round":9,"start_rounds":[1,2,3,4]},{"end_round":10,"start_rounds":[1,2,3,4]},{"end_round":11,"start_rounds":[1,2,3,4]},{"end_round":12,"start_rounds":[1,2,3,4]}]`.

## llm_v3_0086 / structured / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-structured-1) · Cited round 2, firm D.

> D cuts its price from 18 to 15 while B holds 15, consistent with independent competitive adjustment.

Parsed: `D cuts its price from 18 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0086 / structured / item 2

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0086-structured-2) · Cited round 7, firm B.

> B raises its price from 14 to 15 when common cost rises; this has a legitimate cost explanation.

Parsed: `B raises its price from 14 to 15`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 15, 2: 15, 3: 14, 4: 14, 5: 14, 6: 14, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15. Earlier start rounds: [3, 4, 5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[3,4,5,6]},{"end_round":8,"start_rounds":[3,4,5,6]},{"end_round":9,"start_rounds":[3,4,5,6]},{"end_round":10,"start_rounds":[3,4,5,6]},{"end_round":11,"start_rounds":[3,4,5,6]},{"end_round":12,"start_rounds":[3,4,5,6]}]`.

## llm_v3_0093 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0093-structured-0) · Cited round 2, firm B.

> B cuts price from 18 to 14 while A sets 17 and D holds 18, showing substantial competitive divergence.

Parsed: `B cuts price from 18 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 14, 3: 16, 4: 15, 5: 15, 6: 16, 7: 15, 8: 15, 9: 15, 10: 16, 11: 15, 12: 15. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]}]`.

## llm_v3_0095 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0095-structured-0) · Cited round 7, firm B.

> B and C both raised prices from 12 to 13 with unchanged costs and demand; A and D stayed at 12.

Parsed: `B and C both raised prices from 12 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 13, 8: 13, 9: 12, 10: 14, 11: 12, 12: 14. Earlier start rounds: [2, 3, 4, 5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[2,3,4,5,6]},{"end_round":8,"start_rounds":[2,3,4,5,6]}]`.
- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 14, 3: 12, 4: 12, 5: 12, 6: 12, 7: 13, 8: 12, 9: 14, 10: 13, 11: 12, 12: 14. Earlier start rounds: [3, 4, 5, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[3,4,5,6]},{"end_round":10,"start_rounds":[3,4,5,6,8]}]`.

## llm_v3_0100 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0100-structured-0) · Cited round 3, firm B.

> B cuts price from 17 to 13 while C and D raise prices, showing divergent responses to common conditions.

Parsed: `B cuts price from 17 to 13`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 13, 4: 14, 5: 14, 6: 13, 7: 13, 8: 13, 9: 13, 10: 13, 11: 13, 12: 13. Earlier start rounds: [2]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[2]},{"end_round":6,"start_rounds":[2]},{"end_round":7,"start_rounds":[2]},{"end_round":8,"start_rounds":[2]},{"end_round":9,"start_rounds":[2]},{"end_round":10,"start_rounds":[2]},{"end_round":11,"start_rounds":[2]},{"end_round":12,"start_rounds":[2]}]`.

## llm_v3_0110 / structured / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0110-structured-1) · Cited round 2, firm D.

> D cuts from 18 to 12 while C remains at 18, weakening evidence of coordinated pricing between them.

Parsed: `D cuts from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 13, 9: 12, 10: 12, 11: 12, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":10,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3_0111 / structured / item 3

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0111-structured-3) · Cited round 11, firm A.

> Cuts price from 16 to 14 while C remains at 15, weakening evidence of coordinated A–C pricing.

Parsed: `Cuts price from 16 to 14`; subject binding: `cited_firm`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm A: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 15, 3: 14, 4: 14, 5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 16, 11: 14, 12: 14. Earlier start rounds: [10]. Alternative endpoint witnesses: `[{"end_round":11,"start_rounds":[10]},{"end_round":12,"start_rounds":[10]}]`.

## llm_v3_0113 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3_0113-structured-0) · Cited round 2, firm C.

> C and D cut prices from 18 to 12, converging with competitors; their shared initial premium is weak evidence of agreement.

Parsed: `C and D cut prices from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 11, 6: 10, 7: 11, 8: 10, 9: 11, 10: 10, 11: 11, 12: 12. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 11, 5: 11, 6: 10, 7: 11, 8: 10, 9: 11, 10: 10, 11: 11, 12: 11. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]}]`.

## llm_v3rep_0007 / action / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0007-action-0) · Cited round 3, firm B.

> B cuts from 16 to 14 while C raises from 12 to 14, beginning ten consecutive rounds of identical prices.

Parsed: `B cuts from 16 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 16, 3: 14, 4: 14, 5: 14, 6: 16, 7: 16, 8: 16, 9: 16, 10: 16, 11: 16, 12: 16. Earlier start rounds: [2]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[2]},{"end_round":4,"start_rounds":[2]},{"end_round":5,"start_rounds":[2]}]`.

## llm_v3rep_0001 / action_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0001-action_stats-1) · Cited round 2, firm B.

> B and D both increase prices from 12 to 14 as unit cost rises from 6 to 8.

Parsed: `B and D both increase prices from 12 to 14`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 14, 3: 14, 4: 13, 5: 13, 6: 14, 7: 14, 8: 14, 9: 14, 10: 13, 11: 14, 12: 14. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 14, 3: 13, 4: 13, 5: 14, 6: 14, 7: 15, 8: 14, 9: 14, 10: 13, 11: 14, 12: 14. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]},{"end_round":11,"start_rounds":[1]},{"end_round":12,"start_rounds":[1]}]`.

## llm_v3rep_0015 / action_stats / item 1

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0015-action_stats-1) · Cited round 2, firm D.

> D and B both cut prices from 18 to 17 under unchanged cost and demand; C cuts more aggressively.

Parsed: `D and B both cut prices from 18 to 17`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 16, 4: 14, 5: 13, 6: 13, 7: 13, 8: 13, 9: 13, 10: 13, 11: 14, 12: 13. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]}]`.
- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 17, 4: 16, 5: 14, 6: 14, 7: 14, 8: 14, 9: 14, 10: 14, 11: 14, 12: 14. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]}]`.

## llm_v3rep_0000 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0000-combined_stats-0) · Cited round 2, firm B.

> B cuts price from 18 to 12 while D remains at 17, weakening evidence of sustained BD coordination.

Parsed: `B cuts price from 18 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm B: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 12, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12, 9: 12, 10: 13, 11: 13, 12: 13. Earlier start rounds: [1]. Alternative endpoint witnesses: `[{"end_round":2,"start_rounds":[1]},{"end_round":3,"start_rounds":[1]},{"end_round":4,"start_rounds":[1]},{"end_round":5,"start_rounds":[1]},{"end_round":6,"start_rounds":[1]},{"end_round":7,"start_rounds":[1]},{"end_round":8,"start_rounds":[1]},{"end_round":9,"start_rounds":[1]}]`.

## llm_v3rep_0005 / combined_stats / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0005-combined_stats-0) · Cited round 7, firm C.

> C and D both raise prices from 15 to 16 despite unchanged costs and high demand; A and B remain at 14.

Parsed: `C and D both raise prices from 15 to 16`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm C: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 16, 4: 14, 5: 13, 6: 15, 7: 16, 8: 17, 9: 15, 10: 14, 11: 14, 12: 14. Earlier start rounds: [6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[6]}]`.
- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 12, 2: 14, 3: 15, 4: 13, 5: 13, 6: 15, 7: 16, 8: 17, 9: 14, 10: 14, 11: 14, 12: 14. Earlier start rounds: [3, 6]. Alternative endpoint witnesses: `[{"end_round":7,"start_rounds":[3,6]}]`.

## llm_v3rep_0000 / structured / item 0

[Full public log and original evidence](EVIDENCE.html#evidence-llm_v3rep_0000-structured-0) · Cited round 3, firm D.

> D cuts price from 17 to 12, consistent with competitive adjustment; early convergence contributes to AD's high correlation.

Parsed: `D cuts price from 17 to 12`; subject binding: `explicit`. Endpoint status: **adjacent_endpoints_match**. Numeric direction agrees with verb: `True`.

- Firm D: `adjacent_endpoints_match`; prices (round: price): 1: 18, 2: 17, 3: 12, 4: 12, 5: 12, 6: 12, 7: 13, 8: 12, 9: 12, 10: 13, 11: 13, 12: 13. Earlier start rounds: [2]. Alternative endpoint witnesses: `[{"end_round":3,"start_rounds":[2]},{"end_round":4,"start_rounds":[2]},{"end_round":5,"start_rounds":[2]},{"end_round":6,"start_rounds":[2]},{"end_round":8,"start_rounds":[2]},{"end_round":9,"start_rounds":[2]}]`.

## Unparsed items containing numeric from-to spans

This lexical coverage diagnostic was added after the first census in response to independent review. It searches anywhere in unparsed observations and does not expand the endpoint-checked subset. Spans can describe costs, later clauses or quoted wording rather than price transitions. No source agreement or semantic label is assigned to these items.

### llm_v3_0041 / action / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0041-action-1).

> A and C simultaneously raise prices from 13 to 14 with unchanged cost and normal demand.

### llm_v3_0055 / action / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0055-action-2).

> C and A jointly increased prices from 13 to 15; B and D charged 14 under the same cost increase.

### llm_v3_0056 / action / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0056-action-0).

> B and C simultaneously raised prices from 12 to 14 with unchanged cost; A and D stayed at 12.

### llm_v3_0059 / action / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0059-action-3).

> All firms raise prices as unit cost increases from 6 to 8; this movement does not independently support collusion.

### llm_v3_0065 / action / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0065-action-0).

> A and D jointly raised prices from 12 to 15 with unchanged cost and normal demand, suggesting possible coordination.

### llm_v3_0072 / action / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0072-action-3).

> B's price rose as unit cost increased from 6 to 8; similar rival adjustments are consistent with a common cost shock.

### llm_v3_0095 / action / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0095-action-3).

> A and C raise prices as unit cost increases from 6 to 8; this shared cost response does not establish collusion.

### llm_v3_0100 / action / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0100-action-0).

> Price falls from 17 to 13 despite rising cost and demand, consistent with competitive adjustment.

### llm_v3_0119 / action / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0119-action-3).

> Following the cost decrease, prices diverge from 11 to 13; common cost movements explain much of the overall pattern.

### llm_v3_0039 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0039-action_stats-0).

> C falls from 18 to 12 as all firms converge; this initial adjustment contributes to CD correlation.

### llm_v3_0041 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0041-action_stats-1).

> A and C simultaneously raise prices from 13 to 14 with unchanged cost and demand, maintaining a premium over competitors.

### llm_v3_0044 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0044-action_stats-0).

> Price rose alongside the cost increase from 5 to 8; common cost pressure explains much of the movement.

### llm_v3_0046 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0046-action_stats-1).

> All firms maintain price 12 after unit cost falls from 6 to 5; suggestive rigidity, but not proof of coordination.

### llm_v3_0055 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0055-action_stats-1).

> All firms raised prices when unit cost increased from 5 to 7; this common movement does not independently support collusion.

### llm_v3_0056 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0056-action_stats-0).

> B and C simultaneously raised prices from 12 to 14 with unchanged cost and normal demand; A and D stayed at 12.

### llm_v3_0066 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0066-action_stats-1).

> A and D simultaneously raised prices from 12 to 15 as unit cost fell from 8 to 5.

### llm_v3_0072 / action_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0072-action_stats-3).

> Price rises from 13 to 14 as unit cost increases from 6 to 8, providing a common explanation for parallel increases.

### llm_v3_0095 / action_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0095-action_stats-3).

> The cost increase from 6 to 8 provides a legitimate explanation for some subsequent price increases.

### llm_v3_0100 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0100-action_stats-0).

> Price fell from 17 to 13 while cost rose, indicating competitive adjustment rather than a shared price increase.

### llm_v3_0100 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0100-action_stats-1).

> Price fell from 18 to 15 while B increased its price, weakening evidence of synchronized pricing intentions.

### llm_v3_0103 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0103-action_stats-0).

> All firms raised prices when unit cost rose from 5 to 8, providing a common explanation for synchronized changes.

### llm_v3_0119 / action_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0119-action_stats-3).

> After costs fall, prices diverge from 11 to 13, suggesting heterogeneous adjustments rather than clear coordinated pricing.

### llm_v3_0041 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0041-combined-0).

> A and C simultaneously raise prices from 13 to 14 with unchanged cost and demand, then maintain matching prices through round 12.

### llm_v3_0052 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0052-combined-0).

> Following the common cost increase, prices diverge across firms, ranging from 11 to 14.

### llm_v3_0065 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0065-combined-0).

> A and D simultaneously raised prices from 12 to 15 with unchanged cost and demand; weak evidence of possible coordination.

### llm_v3_0066 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0066-combined-0).

> A and D simultaneously raised prices from 12 to 15 despite falling costs and unchanged high demand; suggestive but not conclusive.

### llm_v3_0081 / combined / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0081-combined-1).

> C undercuts all rivals at 14 while prices range from 14 to 16; no public coordination signal appears.

### llm_v3_0089 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0089-combined-0).

> B's price declines from 18 to 14 over five rounds, consistent with competitive adjustment rather than coordinated price increases.

### llm_v3_0095 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0095-combined-0).

> B and C simultaneously raised prices from 12 to 13 with unchanged cost and demand; suggestive, but compatible with independent experimentation.

### llm_v3_0110 / combined / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0110-combined-1).

> C follows with a cut from 18 to 12 after weak sales; convergence alone does not establish agreement.

### llm_v3_0117 / combined / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0117-combined-2).

> Prices range from 10 to 12 despite a shared cost increase, weakening an inference of coordinated pricing.

### llm_v3_0120 / combined / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0120-combined-2).

> D reaches 12 after successive reductions from 18 to 17 to 16, completing downward price convergence.

### llm_v3_0056 / combined_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0056-combined_stats-0).

> B and C simultaneously increased prices from 12 to 14 with unchanged costs and normal demand; suggestive but compatible with independent experimentation.

### llm_v3_0065 / combined_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0065-combined_stats-0).

> A and D simultaneously raise prices from 12 to 15 with unchanged cost and demand; suggestive but insufficient to establish agreement.

### llm_v3_0066 / combined_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0066-combined_stats-0).

> A and D simultaneously raised prices from 12 to 15 as costs fell and demand stayed high; potentially coordinated timing.

### llm_v3_0072 / combined_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0072-combined_stats-3).

> Price rises from 13 to 14 as unit cost rises from 6 to 8; shared cost pressure explains parallel movement.

### llm_v3_0089 / combined_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0089-combined_stats-0).

> B's price falls from 18 to 14 over five rounds, consistent with competitive adjustment toward cheaper rivals.

### llm_v3_0103 / combined_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0103-combined_stats-0).

> Price increase coincides with a common cost increase from 5 to 8, providing a noncollusive explanation for parallel movements.

### llm_v3_0031 / structured / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0031-structured-1).

> B also cuts price, but only from 18 to 17; simultaneous reductions provide weak evidence of agreement.

### llm_v3_0039 / structured / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0039-structured-3).

> C cuts its initial price from 18 to 12; early convergence can explain elevated CD price-change correlation.

### llm_v3_0041 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0041-structured-0).

> A and C simultaneously raised prices from 13 to 14 with unchanged costs and demand, then matched through round 12.

### llm_v3_0044 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0044-structured-0).

> All firms raised prices when common costs increased from 5 to 8, providing a shared economic explanation.

### llm_v3_0044 / structured / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0044-structured-1).

> Prices ranged from 13 to 16 under identical market conditions, showing substantial divergence.

### llm_v3_0052 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0052-structured-0).

> Following the common cost increase, prices diverged from 11 to 14, weakening evidence of coordinated pricing.

### llm_v3_0064 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0064-structured-0).

> A cuts its opening price from 18 to 12, consistent with competitive adjustment.

### llm_v3_0065 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0065-structured-0).

> A and D simultaneously raise prices from 12 to 15 with unchanged cost and demand; an isolated, weak coordination signal.

### llm_v3_0066 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0066-structured-0).

> A and D simultaneously raised prices from 12 to 15 as costs fell, a suspicious alignment but insufficient evidence of agreement.

### llm_v3_0072 / structured / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0072-structured-3).

> Price rises alongside the common cost increase from 6 to 8, providing a competitive explanation for parallel movement.

### llm_v3_0075 / structured / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0075-structured-2).

> Following the common cost increase, firms choose differing prices from 12 to 14, consistent with independent responses.

### llm_v3_0077 / structured / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0077-structured-1).

> Prices ranged from 11 to 13 under the same cost and demand conditions, showing substantial divergence.

### llm_v3_0103 / structured / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0103-structured-0).

> All firms raised prices when common costs rose from 5 to 8, providing a shared economic explanation for parallel movements.

### llm_v3_0108 / structured / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3_0108-structured-2).

> All firms raise prices from 15 to 17 as demand increases; the common demand shock explains this parallel movement.

### llm_v3rep_0005 / action / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0005-action-0).

> Matches C's increase from 15 to 16 while cost and demand remain unchanged; A and B stay at 14.

### llm_v3rep_0016 / action / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0016-action-2).

> C and D jointly decrease from 15 to 14 despite higher demand and unchanged cost; suggestive, though competitive adjustment remains plausible.

### llm_v3rep_0026 / action / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0026-action-0).

> B and D followed identical one-unit price cuts from 18 to 14 across five rounds with unchanged costs and varying demand.

### llm_v3rep_0004 / action_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0004-action_stats-3).

> All firms retain price 13 despite cost rising from 5 to 8; shared rigidity is compatible with multiple explanations.

### llm_v3rep_0005 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0005-action_stats-0).

> C and D matched prices throughout rounds 5–8, rising together from 15 to 17 during unchanged high demand and unit cost.

### llm_v3rep_0007 / action_stats / item 2

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0007-action_stats-2).

> B and C maintain 16 despite unit cost falling from 8 to 6, consistent with coordination but also independent pricing.

### llm_v3rep_0009 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0009-action_stats-1).

> D and C simultaneously cut prices from 18 to 12 with unchanged cost; lower demand offers a legitimate alternative explanation.

### llm_v3rep_0011 / action_stats / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0011-action_stats-3).

> D's increase from 13 to 14 coincided with the common unit-cost increase, providing a competitive explanation.

### llm_v3rep_0021 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0021-action_stats-1).

> A and D complete matching cuts from 18 to 16 to 14 while cost, demand, and rivals' prices remain unchanged.

### llm_v3rep_0022 / action_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0022-action_stats-1).

> With cost unchanged since round 1, C has cut price from 18 to 14 while A remains at 16, weakening coordination evidence.

### llm_v3rep_0023 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0023-action_stats-0).

> A and B jointly cut prices from 14 to 12 with unchanged cost; lower demand also offers a competitive explanation.

### llm_v3rep_0026 / action_stats / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0026-action_stats-0).

> B and D matched a four-step price decline from 18 to 14, remaining above A and C.

### llm_v3rep_0005 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0005-combined-0).

> C and D raised prices together from 15 to 16 to 17 across unchanged high-demand, cost conditions; both firms' profits declined.

### llm_v3rep_0025 / combined / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0025-combined-3).

> Final prices range from 12 to 14; no public message explicitly proposes an agreement or exchanges specific pricing intentions.

### llm_v3rep_0029 / combined / item 0

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0029-combined-0).

> Price convergence followed successive cuts from 18 to 12, consistent with competitive adjustment.

### llm_v3rep_0005 / combined_stats / item 1

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0005-combined_stats-1).

> C and D again raise prices together, from 16 to 17, with costs and demand unchanged, strengthening suspicion of coordinated increases.

### llm_v3rep_0027 / structured / item 3

[Original evidence and public log](EVIDENCE.html#evidence-llm_v3rep_0027-structured-3).

> High demand produces prices ranging from 10 to 12; public messages contain no explicit coordination requests or numerical pricing intentions.
