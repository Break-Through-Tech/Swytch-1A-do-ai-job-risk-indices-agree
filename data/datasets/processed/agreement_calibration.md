# Task 12 — Agreement calibration against published results

**Bottom line:** our merged table reproduces the two published patterns it can be compared against: how strongly the modern indices agree, and how the older and newer measures relate to wages. It also reproduces the Budget Lab's finding that disagreement rises with exposure, but only when disagreement is measured on their z-score scale and only among the modern indices. On a rank scale (Task 11), that rise mostly disappears. Frey–Osborne measures something different and is treated separately throughout. Tracing occupations to the source files found no data errors, but did find two crosswalk side effects worth flagging downstream.

Analysis: `notebooks/task12.ipynb`. Tables: `calibration_results.csv`, `calibration_traced_occupations.csv`, `calibration_catch_all_codes.csv`. All results use the fixed 663-occupation sample from Task 9 (SHA-256 `7f0c6068…f782ee`). They are unweighted, occupation-level results.

## 1. What the published comparisons actually measure

| | Budget Lab at Yale (2026) | ILO research brief (2026) |
| --- | --- | --- |
| Indices | Seven modern metrics: AIOE (Felten et al. 2021), Eloundou GPT-4 beta and human beta, Eisfeldt et al. total and core, Webb pct_ai, Tomlinson et al. AI applicability. **No Frey–Osborne.** | Compares wage correlations for Frey–Osborne, Brynjolfsson et al., Webb, Felten et al. (2018), Eloundou et al., Septiandri et al., Gmyrek et al., and a mean normalised measure. |
| The "correlation" | Ranks of **DV Rating Beta vs each other metric**, one pair at a time: "linear with high correlation (.7-.9)", R² ".47 and .78". The highest is with human beta. It is not a full pairwise matrix. | Table 2 reports the correlation of **each measure with wages**, not between measures. The statistic and wage source are not stated. Taken from del Rio-Chanona et al. (2025). |
| Disagreement measure | Variance of z-scored metrics per occupation, regressed on a PCA-weighted exposure score. The slope is 0.0617 and significant, with controls for log salary, share of women and major group. Webb is dropped, leaving 778 occupations. The authors chose z-scores over ranks on purpose, because ranks "flatten the difference between occupations". | None quantified. The brief says, qualitatively, that older automation measures point to routine and lower-wage jobs, while capability-based measures point to cognitive, analytical and managerial jobs. |
| Occupations | SOC 2018. 710 occupations have all seven metrics; 778 have all but Webb. | US O*NET-based; the count is not stated in the brief. |
| Weighting | Unweighted occupations. Employment weighting is not mentioned. | Not stated. |

So "roughly 0.7–0.9" means modern-to-modern correlations anchored on GPT-4 beta. It says nothing about Frey–Osborne, which neither source puts in a correlation matrix with the modern indices.

## 2. Comparison table

| Published pattern | Source | Our result | Verdict |
| --- | --- | --- | --- |
| Modern indices correlate at about 0.7–0.9 with GPT-4 beta | Budget Lab | GPT-4 beta vs AIOE: Spearman ρ = 0.863 (R² 0.744). GPT-4 beta vs human beta: ρ = 0.912 (R² 0.831). Human beta vs AIOE: ρ = 0.867. | **Reproduced.** AIOE sits inside the range. Human beta is slightly above it, which fits the Budget Lab's note that it is the closest pair. Holds for gamma (0.88). Fails for alpha (0.43 with GPT-4 labels), which the Budget Lab did not use (Task 10). |
| Disagreement rises with exposure | Budget Lab | Z-score variance among AIOE + both Eloundou ratings rises with their mean (slope 0.066, p < 10⁻¹⁵). It also rises when the variance excludes the x-axis metric (specification 2): slope 0.032 with GPT-4 beta on the x-axis, 0.062 with human beta, both p < 0.001. | **Reproduced among the modern indices, on their scale.** Our metric set is smaller (3 of their 7) and we use no controls, so the matching slope size is a coincidence, not a replication. |
| … the same, on ranks | (our Task 11) | Median AIOE–Eloundou rank gap is 0.065–0.080 in the least-exposed band and roughly flat at 0.09–0.12 in bands 2–5. Every band is far below the shuffled-ranks baseline. | **Partly reproduced.** On ranks the modern indices agree everywhere. Disagreement steps up out of the least-exposed band, which is full of tied Eloundou zeros, but does not keep climbing toward the top. The Budget Lab's finding is mostly about *how much* exposure there is, not *whether* there is exposure, which the authors also say. |
| … with Frey–Osborne included | (not published) | Specification 1 slopes are −0.045 (GPT-4) and −0.012 (human), both non-significant. On ranks, the three-index top band is the *most* consistent (Task 11). | **Not reproduced, and not expected to be.** Frey–Osborne disagrees about the most-exposed and least-exposed occupations alike, so it removes any trend. |
| Older automation measure has a negative wage correlation | ILO Table 2: Frey–Osborne −0.5576 | Frey–Osborne vs median wage, 656 occupations: Pearson −0.515, Pearson on log wage −0.559, Spearman −0.539. | **Reproduced.** |
| Capability-based measures have positive wage correlations, strongest for Felten | ILO: Felten (2018) 0.5375, Eloundou 0.4243 | AIOE (Felten 2021 data): log-wage 0.517, Spearman 0.520. GPT-4 beta: 0.390 / 0.434. Human beta: 0.406 / 0.434. | **Reproduced**, including AIOE being the strongest. Which Eloundou variant the ILO used is not stated. |
| Older and newer measures point at different jobs | ILO (qualitative) | Frey–Osborne is negatively correlated with AIOE (ρ = −0.368) and with Eloundou beta (−0.267 GPT-4, −0.340 human). Under modern-exposure bands, Frey–Osborne gaps in the top band are 0.52–0.60 rank. | **Reproduced.** The negative sign is the expected result, not a data error. |

## 3. Is disagreement greatest at the high-exposure end? Does it depend on the label source?

The answer depends on which indices are compared and on which scale:

- **Modern indices, z-score scale:** yes, as the Budget Lab found. This holds for both label sources. The specification 1 slope is larger with GPT-4 labels (0.085) than with human labels (0.035), but both are positive and significant.
- **Modern indices, rank scale:** barely. AIOE and Eloundou put occupations in nearly the same order at every exposure level. Their gap is smallest in the least-exposed band and flat from band 2 upward.
- **With Frey–Osborne:** on modern-exposure bands, the top band has the most disagreement (median rank SD 0.264 GPT-4, 0.290 human), above the shuffled baseline. On all-three-index bands, the top band has the least. Either way, the disagreement is Frey–Osborne against the modern pair, not disagreement within the modern pair.

GPT-4 and human labels never reverse a conclusion. They change magnitudes only.

## 4. Occupations traced to source values

In every case, the sample value equals the unweighted mean of the raw source values for its contributing 2010 codes; the notebook asserts this. None of the surprising results comes from a data-entry or join error.

| Occupation | Sample ranks: AIOE / F–O / GPT-4 / human | Source trace | What explains it |
| --- | --- | --- | --- |
| 19-3039 Psychologists, All Other | 0.96 / 0.02 / 0.70 / 0.54 | One-to-one: AIOE 1.390, F–O 0.0043 | **Construct difference.** F–O rated psychologists almost uncomputerisable in 2013, while AIOE scores the cognitive abilities the job needs as highly AI-related. This is the typical top-band case. |
| 21-1013 Marriage and Family Therapists | 0.95 / 0.09 / 0.26 / 0.53 | One-to-one: AIOE 1.367, GPT-4 beta 0.111 | **Construct difference within the modern pair.** AIOE is built from abilities (oral expression, reasoning), which are highly AI-related. Eloundou is built from tasks, and most therapy tasks are interpersonal. This is the largest AIOE–Eloundou gap in the sample. |
| 51-9162 CNC Tool Programmers | 0.35 / 0.37 / 0.97 / 0.63 | Many-to-one. AIOE averages 51-4012 (−0.024) with the catch-all 51-9199 "Production Workers, All Other" (−1.291). F–O uses 51-4012 only. | **Crosswalk side effect.** Without the catch-all, the AIOE rank would be 0.54, not 0.35. GPT-4 and human labels also differ sharply (0.80 vs 0.36 raw). |
| 19-3034 School Psychologists and 19-3033 Clinical and Counseling Psychologists | Both 0.99 / 0.04; GPT-4 0.61 vs 0.59; human 0.92 vs 0.84 | 2010 code 19-3031 was split in two, so both inherit AIOE 1.456 and F–O 0.0047. | **Split duplication.** AIOE and F–O cannot tell the two occupations apart; only Eloundou can. Their large rank SD is the usual F–O construct gap, not a crosswalk error. |
| 31-9094 Medical Transcriptionists | 0.80 / 0.75 / 0.98 / 0.47 | One-to-one. GPT-4 beta 0.875, human beta 0.232. | **Label-source disagreement.** This is the largest GPT-4 vs human gap in the sample. Three of the four scores call it highly exposed; the human annotators did not. |
| 53-1041 Aircraft Cargo Handling Supervisors | 0.34 / 0.22 / 0.51 / 0.04 | 2010 code 53-1011 was renumbered to 53-1041, with handling "1:1", so `crosswalk_changed` is False. Human beta is 0.000, GPT-4 beta 0.300. | **Flag meaning plus ties.** `crosswalk_changed` means the mapping was not one-to-one, not that the code number changed. The human zero puts this occupation in the large tied block at the bottom of the human ranks. |

**Catch-all codes, checked across the whole sample:** the Frey–Osborne source file lacks most 2010 "All Other" codes, but the AIOE file includes them. Eleven occupations draw on a catch-all code for AIOE. In 10 of them a specific code is also present, so AIOE averages in the catch-all. In 8 of those 10, Frey–Osborne has no catch-all score to average. Removing the catch-alls changes those occupations' AIOE ranks by up to 0.18 (CNC Tool Programmers and Operators, and Installation, Maintenance and Repair Workers, All Other). Every headline correlation moves by 0.002 or less. This does not affect any sample-level conclusion, but these 10 occupations should carry a provenance flag in the Task 14 confidence flags (`calibration_catch_all_codes.csv`).

## 5. Calibration summary

**Reproduced**
- The modern indices agree at the published level: AIOE vs GPT-4 beta ρ = 0.86, inside 0.7–0.9.
- The modern indices disagree more about highly exposed occupations, on the Budget Lab's z-score scale, under both label sources.
- The ILO wage pattern holds: Frey–Osborne negative (−0.56), AIOE strongest positive (0.52), Eloundou positive (0.39–0.43).
- Older and newer measures identify different jobs (negative Frey–Osborne correlations).

**Partly reproduced**
- On ranks, modern-index disagreement barely rises with exposure (AIOE–Eloundou gap 0.065–0.080 in band 1, then flat at 0.09–0.12). Ranks remove the magnitude differences that drive the Budget Lab result.
- GPT-4 vs human beta is ρ = 0.91, slightly above the published upper bound. This is consistent with the Budget Lab's note that it is the closest pair.
- We cover 3 of the Budget Lab's 7 metrics and use none of their controls, so slope sizes are not comparable.

**Not reproduced, as expected**
- Adding Frey–Osborne removes the exposure–disagreement trend. No published source makes this comparison; it is this project's contribution, and it reflects a construct difference rather than a pipeline fault.
- The 0.7–0.9 range does not hold for the alpha variant (ρ = 0.43). The published results use beta.

**Pipeline status:** the merged table reproduces the published patterns wherever the comparison is like for like. The occupation traces found no source or join errors. Two crosswalk side effects (split duplication and catch-all averaging) are documented for downstream flags.

## Sources

- Gimbel, M., Kendall, J. & Kulsakdinun, R. (19 February 2026). *Labor Market AI Exposure: What Do We Know?* The Budget Lab at Yale. https://budgetlab.yale.edu/research/labor-market-ai-exposure-what-do-we-know
- Merola, R., Ernst, E., Samaan, D., del Rio-Chanona, M. & Teutloff, O. (2026). *Workers' exposure to AI: What indicators tell us – and what they don't.* ILO Research Brief. Geneva: International Labour Office. https://doi.org/10.54394/00033279. The PDF is dated February 2026; the web page lists 17 April 2026 for the updated version. Table 2 is sourced from del Rio-Chanona, M. et al. (2025), *AI and jobs: A review of theory, estimates, and evidence*, https://arxiv.org/abs/2509.15265.
- U.S. Bureau of Labor Statistics, Employment Projections 2025–35, Table 1.2 (median annual wage, 2025), `data/datasets/bls_occupation.xlsx`.
