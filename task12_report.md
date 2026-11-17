# Task 12 summary: Calibration against the published pattern

**Question:** Does our merged table reproduce what published comparisons of these indices report? If not, why?

## What the published sources actually measure

- **Budget Lab at Yale** (Gimbel, Kendall & Kulsakdinun, Feb 2026):
  - **Its "0.7–0.9" correlation** compares the ranks of Eloundou GPT-4 beta with each of six other modern metrics, one at a time.
  - **Frey–Osborne is not included.**
  - **Its "disagreement rises with exposure" finding** uses the variance of z-scores, not ranks.
- **ILO research brief** (Merola et al., 2026):
  - **Its reported correlations** are each measure against **wages**, not the measures against each other.
  - **Its "older vs newer measures point at different jobs" point** is qualitative.

## Method

- **Sample:** the fixed 663-occupation sample from Task 9; results are unweighted and occupation-level.
- **Check A:** Spearman correlations of GPT-4 beta with AIOE, human beta, and Frey–Osborne (the Budget Lab correlation level).
- **Check B:** the Budget Lab disagreement method on our data. For each occupation, take the variance of the z-scored indices and regress it on their mean, or on one Eloundou rating. This is run for the modern indices alone, for each label source, and with Frey–Osborne added.
- **Check C:** each index correlated with the BLS 2025 median annual wage for 656 occupations (the ILO Table 2 comparison).
- **Tracing:** seven occupations followed from the raw source files through the crosswalk to the sample, plus a sample-wide check of "All Other" catch-all codes.

## Findings

| Published pattern | Our result | Verdict |
|---|---|---|
| Modern indices correlate at 0.7–0.9 with GPT-4 beta (Budget Lab) | AIOE ρ = 0.863; human beta ρ = 0.912 | Reproduced (human beta slightly above the range) |
| Disagreement rises with exposure (Budget Lab, z-score method) | Positive and significant among AIOE + Eloundou for both label sources (slope 0.066, p < 10⁻¹⁵) | Reproduced |
| … measured on ranks (Task 11) | AIOE–Eloundou gap is 0.07 in the least-exposed band, then flat at about 0.09–0.12 | Partly reproduced |
| … with Frey–Osborne added | No trend (slopes −0.045 and −0.012, not significant) | Not reproduced, as expected: no published source does this |
| Frey–Osborne negatively correlated with wages (ILO −0.558) | −0.559 (log wage) | Reproduced |
| AIOE (0.538) and Eloundou (0.424) positively correlated with wages (ILO) | 0.517 and 0.39–0.43 | Reproduced |

1. **The pipeline passes calibration.** Wherever the comparison is like for like, our numbers match the published ones.
2. **Scale matters for the disagreement finding.** The Budget Lab result comes from differences in *how much* exposure the indices assign (z-scores). Ranks hide those differences, so on ranks the modern indices agree at every exposure level.
3. **Frey–Osborne is a different construct, not a data problem.** Its negative correlations with the modern indices match the ILO's account of older vs newer measures.
4. **GPT-4 and human labels never flip a conclusion.** They change magnitudes only.

## Occupation tracing

Every traced value matches its raw source; there were no join or data-entry errors. Each surprising result had one of these explanations:

- **Construct difference:** psychologists and therapists rank near the top on AIOE but low on Frey–Osborne or Eloundou.
- **Label-source disagreement:** Medical Transcriptionists score 0.875 on GPT-4 beta but 0.232 on human beta.
- **Split duplication:** when a 2010 code was split, both new occupations inherit identical AIOE and Frey–Osborne scores (e.g., School vs Clinical and Counseling Psychologists).
- **Catch-all averaging:** 10 occupations have an "All Other" code averaged into AIOE that Frey–Osborne usually lacks. This moves CNC Tool Programmers from an AIOE rank of 0.54 to 0.35, but changes the headline correlations by at most 0.002.

## Caveats

- We have only 3 of the Budget Lab's 7 metrics and none of their controls, so slope sizes are not directly comparable.
- The ILO does not state its correlation statistic, its wage source, or which Eloundou variant it used.
- The 0.7–0.9 range holds for the beta and gamma variants but not for alpha (ρ = 0.43).

## Outputs

- `data/datasets/processed/agreement_calibration.md`: the full calibration write-up, with comparison table and citations
- `notebooks/task12.ipynb`
- `data/datasets/processed/calibration_results.csv`, `calibration_traced_occupations.csv` and `calibration_catch_all_codes.csv`

## Relevance to Tasks 13–14

The split-duplication and catch-all occupations, listed in `calibration_catch_all_codes.csv`, should carry provenance flags in the agreement-confidence flags (Task 14). Consensus tiers (Task 13) should treat Frey–Osborne separately from the modern indices rather than averaging all three.
