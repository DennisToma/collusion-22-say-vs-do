# Independent reimplementation

Reproduce with `python3 reimpl.py`. Requires Python 3 and NumPy; uses only the supplied METHOD.md and data. Full precision results and evaluated run IDs are in `reimpl_results.json`.

All estimates below use the 0–1 scale. Brackets give pointwise 95% percentile bootstrap CIs from 2000 class-stratified whole-run resamples (seed 20261024).

## llm_v3 locked test

95 runs: 50 positive, 45 negative. Pooled pairs: 50 positive, 520 negative.

| Scorer | Run AUROC | Within-market AUROC | Pooled pair AUROC | Pair-ID accuracy |
|---|---|---|---|---|
| premium | 0.946667 [0.903328, 0.981333] | 0.958000 [0.910000, 0.992000] | 0.958885 [0.919125, 0.985811] | 0.890000 [0.800000, 0.970000] |
| text | 0.472000 [0.363539, 0.579789] | 0.648000 [0.590000, 0.712000] | 0.598173 [0.524289, 0.674213] | 0.353333 [0.263333, 0.453333] |
| action | 0.753333 [0.655328, 0.849344] | 0.794000 [0.715950, 0.864000] | 0.778808 [0.711896, 0.839692] | 0.420000 [0.280000, 0.560000] |
| combined | 0.740667 [0.638444, 0.834900] | 0.796000 [0.714000, 0.866050] | 0.782346 [0.725631, 0.838735] | 0.433333 [0.309917, 0.560083] |

## llm_v3rep replication

30 runs: 15 positive, 15 negative. Pooled pairs: 15 positive, 165 negative.

| Scorer | Run AUROC | Within-market AUROC | Pooled pair AUROC | Pair-ID accuracy |
|---|---|---|---|---|
| premium | 0.920000 [0.795556, 1.000000] | 0.986667 [0.960000, 1.000000] | 0.983232 [0.957576, 0.999798] | 0.933333 [0.800000, 1.000000] |
| text | 0.668889 [0.475500, 0.840000] | 0.686667 [0.553333, 0.813333] | 0.655354 [0.525833, 0.786884] | 0.411111 [0.233333, 0.611111] |
| action | 0.755556 [0.573333, 0.911111] | 0.813333 [0.666667, 0.933333] | 0.803434 [0.681985, 0.906687] | 0.466667 [0.200000, 0.733333] |
| combined | 0.615556 [0.400000, 0.806667] | 0.800000 [0.653333, 0.906667] | 0.787071 [0.664419, 0.881232] | 0.366667 [0.133333, 0.600000] |

## Dev threshold and test flag rates

Dev has 20 positive and 10 negative runs. Premium threshold: **0.666666666667**, flag when score ≥ threshold. Dev Youden J = 1.000000; TPR = 1.000000 (20/20), FPR = 0.000000 (0/10).

There are 27 threshold candidates (including +infinity). All maximising observed candidates: 0.666666666667.

- Test positive flag rate (TPR): 0.920000 [0.840000, 0.980000] (46/50).
- Test negative flag rate (FPR): 0.155556 [0.066667, 0.266667] (7/45).

## Paired test contrast

Combined minus max(text, action) run AUROC: **-0.012667 [-0.089556, 0.065333]**.

The better unimodal view at the observed sample is action; the better view is recomputed in every bootstrap draw.

## Interpretation choices

1. Ground truth is agreement in {explicit, info_exchange}; none and no_channel are negative. Ignore explicit_collusion, condition, and existing price-derived label fields.
2. Only the assigned unordered pair is a positive pair in a positive run. Every other pair is negative, including all six pairs of a negative run; assignment alone does not imply a positive label.
3. llm_v3 dev uses numeric suffixes 0000..0029; locked test uses 0030..0124. llm_v3rep uses all 30 runs, with no new fitting or threshold selection.
4. Premium uses every observed round (stored indices 0..11, corresponding to rounds 1..12): mean over rounds of (mean price of pair minus mean price of its two complementary firms). The rounds 5..12 conduct summary and 9..12 mechanism summary are separate quantities and are not used. Run premium is the maximum of the six pair premiums. Prices are equally weighted across firms and rounds.
5. Auditor pair scores come from scores; run detection scores come from collusion_present, not the maximum pair score or the separately reported top_pair. Require the specified model and one complete record per run/view; no missing-data imputation or silent run dropping.
6. AUROC is P(positive score > negative score) + 0.5 P(equal scores), with larger scores more suspicious.
7. Within-market AUROC is the mean across positive runs of the assigned pair's AUROC against that run's five other pairs. Each run and each of its five comparisons have equal weight.
8. Pooled pair AUROC pools all six pairs from all evaluated runs: one positive pair per positive run; the other pairs from positive runs and all pairs from negative runs form the negative class.
9. Pair-ID accuracy is evaluated on positive runs only. If the assigned pair is tied for the maximum among k pairs, give 1/k credit; otherwise give zero. Use exact numerical score ties, without rounding or a tolerance. Premium is computed from integer-valued price totals before division, so identical totals yield identical scores.
10. All CIs use 2000 class-stratified whole-run bootstrap replicates, independently drawing n_pos positive and n_neg negative runs with replacement. A resampled run carries all six pair scores and labels. Positive-only endpoints use the sampled positive runs. Percentile endpoints are the 2.5th and 97.5th percentiles with linear interpolation; these are pointwise, not simultaneous, CIs.
11. Use numpy default_rng with seed 20261024 and independent child streams for test and replication. Reuse each split's run draws for every scorer, metric, fixed-threshold flag rate, and paired contrast. The source gives no random seed or CI interpolation rule, so exact CI endpoints can differ from a report.
12. Dev Youden candidates are distinct observed dev run-premium scores plus +infinity (flag nobody); flags use score >= threshold. Maximise TPR-FPR and choose the largest threshold among exact objective ties (the most conservative maximiser). Compare the integer objective TP*n_neg - FP*n_pos to avoid floating tie errors. The minimum observed score already supplies the flag-everybody decision.
13. The dev-selected premium threshold is held fixed on test. Report flag rates separately among test positives (TPR) and negatives (FPR), with conditional bootstrap CIs; these do not include uncertainty from refitting the threshold on another dev sample. No threshold CI is specified or estimated.
14. The paired contrast is AUROC(combined) - max(AUROC(text), AUROC(action)); max selects between two scalar AUROCs, not per-run scores. Recompute all three AUROCs and the maximum in each shared test bootstrap draw, allowing the winning unimodal view to change. No dev-based view selection.
15. The requested scope excludes other datasets, auditor views, late fusion, conduct subgroups, and external label validation. No report results or precomputed analysis code are inputs.

## Validation

Input checks require the exact expected run IDs, all 12 unique rounds per run, four unique firms per round, complete six-pair scores in every view, finite prices/scores, and the specified auditor model. All supplied rows passed. Auditor files are joined by run_id, never by line order. No runs were discarded.

A separate direct positive-negative comparison calculation verified every observed AUROC, including positive-only per-market comparisons and fractional top-tie credit. Synthetic checks covered perfect/reversed/all-tied rankings, clustered multiplicities, and threshold ties. A repeat execution reproduced the output files byte for byte.
