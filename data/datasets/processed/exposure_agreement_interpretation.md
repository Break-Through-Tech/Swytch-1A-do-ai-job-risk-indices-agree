# Task 11 — Agreement versus exposure level

Input: `agreement_analysis_sample.csv`; SHA-256: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`. Notebook: `notebooks/task11.ipynb`. Figures: `figures/task11_disagreement_vs_exposure.png`, `figures/task11_pairwise_gaps_by_band.png`.

## Methods

All results use the same 663 occupations from Task 9 and the saved beta percentile ranks, run once with Eloundou GPT-4 labels and once with human labels. No scores are imputed or weighted.

**Band rule.** Consensus is the unweighted mean of an occupation's percentile ranks. Occupations are sorted by consensus and split into 5 equal-count bands (133, 133, 133, 132, 132); exact ties are broken by SOC code. The primary rule averages all three indices. A sensitivity rule averages AIOE and Eloundou only, because Frey–Osborne is negatively correlated with both (Task 10).

**Disagreement.** Per occupation: standard deviation of the three ranks, range, and the three pairwise absolute rank gaps. Band summaries report medians and quartiles.

**Baseline.** Bounded ranks make spread mechanically smaller in the extreme bands. Each index's ranks were shuffled independently 1000 times (seed 11) and bands recomputed; the 2.5th–97.5th percentiles of the shuffled band medians are the no-agreement baseline.

**Flags.** A band is sparse if it has fewer than 30 occupations (none are). A band is tie-heavy if, for any one index, more than 25% of its occupations share a single raw score. Tie-heavy bands: gpt4/all_three/Q1; gpt4/aioe_eloundou/Q1; human/all_three/Q1; human/aioe_eloundou/Q1.

## Rank SD by band

| label_source | consensus_rule | band | n | consensus_min | consensus_max | median | q1 | q3 | null_lo | null_hi | vs_null | tie_heavy_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt4 | all_three | 1 | 133 | 0.104 | 0.339 | 0.205 | 0.132 | 0.268 | 0.147 | 0.182 | above | True |
| gpt4 | all_three | 2 | 133 | 0.341 | 0.438 | 0.206 | 0.121 | 0.279 | 0.225 | 0.266 | below | False |
| gpt4 | all_three | 3 | 133 | 0.439 | 0.537 | 0.201 | 0.131 | 0.290 | 0.241 | 0.281 | below | False |
| gpt4 | all_three | 4 | 132 | 0.537 | 0.649 | 0.260 | 0.168 | 0.323 | 0.225 | 0.266 | within | False |
| gpt4 | all_three | 5 | 132 | 0.649 | 0.958 | 0.137 | 0.077 | 0.245 | 0.147 | 0.185 | below | False |
| gpt4 | aioe_eloundou | 1 | 133 | 0.019 | 0.206 | 0.259 | 0.196 | 0.309 | 0.166 | 0.217 | above | True |
| gpt4 | aioe_eloundou | 2 | 133 | 0.207 | 0.391 | 0.170 | 0.113 | 0.247 | 0.203 | 0.241 | below | False |
| gpt4 | aioe_eloundou | 3 | 133 | 0.392 | 0.609 | 0.141 | 0.089 | 0.212 | 0.222 | 0.263 | below | False |
| gpt4 | aioe_eloundou | 4 | 132 | 0.609 | 0.805 | 0.218 | 0.139 | 0.293 | 0.202 | 0.241 | within | False |
| gpt4 | aioe_eloundou | 5 | 132 | 0.805 | 0.996 | 0.264 | 0.084 | 0.331 | 0.167 | 0.212 | above | False |
| human | all_three | 1 | 133 | 0.133 | 0.342 | 0.205 | 0.130 | 0.267 | 0.148 | 0.183 | above | True |
| human | all_three | 2 | 133 | 0.342 | 0.439 | 0.197 | 0.119 | 0.281 | 0.227 | 0.266 | below | False |
| human | all_three | 3 | 133 | 0.440 | 0.536 | 0.195 | 0.128 | 0.288 | 0.240 | 0.281 | below | False |
| human | all_three | 4 | 132 | 0.537 | 0.651 | 0.263 | 0.186 | 0.333 | 0.225 | 0.265 | within | False |
| human | all_three | 5 | 132 | 0.652 | 0.963 | 0.135 | 0.076 | 0.254 | 0.147 | 0.183 | below | False |
| human | aioe_eloundou | 1 | 133 | 0.022 | 0.209 | 0.257 | 0.199 | 0.302 | 0.167 | 0.214 | above | True |
| human | aioe_eloundou | 2 | 133 | 0.209 | 0.394 | 0.186 | 0.111 | 0.259 | 0.203 | 0.242 | below | False |
| human | aioe_eloundou | 3 | 133 | 0.395 | 0.609 | 0.135 | 0.086 | 0.198 | 0.223 | 0.263 | below | False |
| human | aioe_eloundou | 4 | 132 | 0.610 | 0.801 | 0.200 | 0.134 | 0.283 | 0.201 | 0.242 | below | False |
| human | aioe_eloundou | 5 | 132 | 0.804 | 0.987 | 0.290 | 0.117 | 0.346 | 0.166 | 0.214 | above | False |

## Tests

| label_source | consensus_rule | spearman_rho | spearman_p | kruskal_p | top_band_median_sd | other_bands_median_sd | mannwhitney_p | top_null_lo | top_null_hi | top_vs_null |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gpt4 | all_three | -0.0664 | 8.75e-02 | 3.65e-09 | 0.1371 | 0.2177 | 6.21e-08 | 0.1473 | 0.1852 | below |
| gpt4 | aioe_eloundou | -0.0387 | 3.20e-01 | 2.91e-18 | 0.2640 | 0.1993 | 5.02e-03 | 0.1675 | 0.2124 | above |
| human | all_three | -0.0403 | 3.00e-01 | 4.93e-10 | 0.1349 | 0.2181 | 1.00e-06 | 0.1466 | 0.1831 | below |
| human | aioe_eloundou | -0.0099 | 7.99e-01 | 2.03e-21 | 0.2901 | 0.1928 | 1.04e-06 | 0.1661 | 0.2143 | above |

p-values are unadjusted and descriptive. The Kruskal–Wallis and Mann–Whitney tests compare observed bands with each other and so include the ceiling effect; the baseline columns account for it.

## Interpretation

**Under the primary rule, disagreement does not rise among the most-exposed occupations; it falls.** Median rank SD by band (Q1→Q5) is 0.205, 0.206, 0.201, 0.260, 0.137 with GPT-4 labels and 0.205, 0.197, 0.195, 0.263, 0.135 with human labels. The top band is the most consistent of the five and sits below the shuffled baseline (0.147–0.185), so the three indices agree on these occupations more than chance alone would produce, even after allowing for the ceiling effect. Disagreement peaks in Q4 instead, and the least-exposed band (Q1) is the only one above its baseline. Because the pattern is not monotonic, the overall Spearman correlation between consensus and rank SD is near zero (-0.066 GPT-4; -0.040 human). The conclusion is the same for GPT-4 and human labels.

**That result depends on how exposure is defined, and Frey–Osborne drives nearly all of the disagreement.** The AIOE–Eloundou gap stays small in every band (medians 0.065–0.122), while the two Frey–Osborne gaps are several times larger (0.258–0.595). When bands are built from AIOE and Eloundou only, the most-exposed band has the *highest* median rank SD (0.264 GPT-4; 0.290 human), above the shuffled baseline. Those are occupations both modern indices rank as highly exposed to AI that Frey–Osborne ranks as low computerisation risk. So "disagreement is greatest at the high-exposure end" holds only when exposure means modern AI exposure, and the disagreement is between the older computerisation measure and the two modern ones. It is not disagreement among the modern indices.

**Caveats.** Bands are equal-count quintiles of an unweighted consensus, so their boundaries depend on which indices enter the consensus. Q1 is tie-heavy under every rule and label source: about a third of its occupations have an Eloundou score of exactly 0 and therefore share one average rank, so Q1 gaps partly reflect where that tied block lands rather than fine-grained disagreement. Frey–Osborne is also coarse (181 distinct values across 663 occupations). The tests are associations across occupations, unadjusted for multiple comparisons; they do not show that exposure causes disagreement, and none of these indices is a forecast of job loss.
