# Task 11 summary: Agreement versus exposure level

**Question:** Do AIOE, Frey–Osborne, and Eloundou disagree more about the most AI-exposed occupations?

## Method

- **Sample:** the fixed 663-occupation sample from Task 9, run once with Eloundou GPT-4 beta labels and once with human beta labels.
- **Exposure bands:** each occupation gets a consensus score, the mean of its three percentile ranks. Occupations are then split into five equal-size bands, Q1 (least exposed) to Q5 (most exposed).
- **Disagreement measures:** for each occupation, the SD of its three ranks, their range, and the three pairwise rank gaps.
- **Shuffled baseline:** ranks are capped between 0 and 1, so the spread is automatically smaller in the end bands. To correct for this, each index's ranks were shuffled 1,000 times to build a "no agreement" baseline for every band.
- **Sensitivity check:** bands built from AIOE + Eloundou only, because Frey–Osborne is negatively correlated with both (Task 10).

## Findings

1. **Disagreement does not rise at the top under the main rule; it falls.** Q5 has the lowest median rank SD (0.137 with GPT-4 labels, 0.135 with human labels), and it sits below the shuffled baseline. On the most-exposed jobs, the indices agree more than chance. Disagreement peaks in Q4 instead.
2. **Frey–Osborne drives the disagreement.** The AIOE–Eloundou gap stays small in every band (median 0.07–0.12). Both Frey–Osborne gaps are several times larger (0.26–0.60).
3. **The answer depends on how "exposure" is defined.** When bands come from the two modern indices only, Q5 has the *most* disagreement (0.26–0.29, above baseline). These are jobs AIOE and Eloundou rank as highly exposed to AI, but Frey–Osborne rates as low automation risk; managers are a typical example.
4. **GPT-4 and human labels lead to the same conclusions.**

| Median rank SD | Q1 | Q2 | Q3 | Q4 | Q5 (most exposed) |
|---|---|---|---|---|---|
| GPT-4 labels | 0.205 | 0.206 | 0.201 | 0.260 | 0.137 |
| Human labels | 0.205 | 0.197 | 0.195 | 0.263 | 0.135 |

*Bands from the mean of all three ranks (primary rule).*

## Caveats

- Q1 is tie-heavy: about a third of it has an Eloundou score of exactly 0.
- Results are unweighted, occupation-level associations, not causal claims or job-loss forecasts.
- P-values are not adjusted for multiple comparisons.

## Outputs

- `notebooks/task11.ipynb`
- `data/datasets/processed/exposure_band_summary.csv`, `exposure_band_occupations.csv` and `exposure_agreement_interpretation.md` (full methods, test results, and interpretation)
- `figures/task11_disagreement_vs_exposure.png` and `figures/task11_pairwise_gaps_by_band.png`

## Relevance to Task 12

The "disagreement is greatest at the high-exposure end" pattern from the Budget Lab analysis looks only partly reproduced. It appears between Frey–Osborne and the modern indices, but only weakly between AIOE and Eloundou.
