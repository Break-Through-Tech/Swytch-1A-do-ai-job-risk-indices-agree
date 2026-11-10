# Milestone 2: Agreement Analysis Report

Generated: 2026-11-10

## Executive summary

This milestone examines whether three occupation-level AI exposure and computerisation indices produce similar rankings.

The merged dataset contains 798 occupations. The fixed complete-case comparison sample contains 663 occupations.

**Exposure is not predicted job loss.**

## Completed analysis

### Task 8: Exploratory data analysis

The team generated exploratory statistics and occupation-level percentile rankings.

Reference: `task8_report.md`.

### Task 9: Analysis sample

- Merged occupations: 798
- Eligible occupations: 663
- Excluded occupations: 135
- No missing index values were imputed.
- The original average-tie percentile ranks were preserved.

Reference: `data/datasets/processed/agreement_sample_definition.md`.

### Task 10: Rank correlations

The existing analysis reports the following Spearman coefficients on the common sample:

| Comparison | Spearman correlation |
|---|---:|
| AIOE vs. Frey-Osborne | -0.3678 |
| AIOE vs. Eloundou GPT-4 beta | +0.8628 |
| Frey-Osborne vs. Eloundou GPT-4 beta | -0.2670 |
| AIOE vs. Eloundou human beta | +0.8669 |
| Frey-Osborne vs. Eloundou human beta | -0.3401 |

These coefficients are transcribed from the committed Task 10 sensitivity appendix; this script does not recompute them.

Reference: `data/datasets/processed/correlation_sensitivity_appendix.md`.

### Task 13: Consensus tiers

Approved cutoffs: 0.25, 0.50, and 0.75.

| Tier | GPT-4 beta | Human beta |
|---|---:|---:|
| Low | 40 | 38 |
| Medium | 315 | 320 |
| High | 244 | 241 |
| Very High | 64 | 64 |

Consensus tier changes between GPT-4 beta and human beta: **73** (11.0% of eligible occupations).

Reference: `data/datasets/processed/tier_method_note.md`.

### Task 15: Occupation case studies

Six occupations were selected to illustrate high and low agreement, contested rankings, GPT-4/human label sensitivity, and SOC crosswalk effects.

Reference: `occupation_case_studies.md`.

## Main findings

1. AIOE and Eloundou beta scores have strong positive rank association.
2. Frey-Osborne has negative rank association with both modern AI exposure measures.
3. Index definitions matter when interpreting occupational exposure.
4. Consensus tiers can change depending on whether GPT-4 or human beta labels are used.
5. An average consensus tier can conceal large differences between component ranks.

## Outstanding work

- Task 14 formal confidence flags have not been incorporated.
- Any unverified Tasks 11 and 12 deliverables must be reviewed separately.
- Optional K-Means clustering is deferred until Tasks 9 through 16 are validated.
- Notebook clean-kernel execution must be performed and recorded by the person running the project locally.

## November handoff

Investigate what drives disagreement using O*NET skills, abilities, work activities, work context, and Job Zone information.

Evaluate models using appropriate held-out performance metrics and interpretability methods, while documenting limitations.

## Output references

- `data/datasets/processed/merged_v0.csv`
- `data/datasets/processed/agreement_analysis_sample.csv`
- `data/datasets/processed/agreement_sample_audit.csv`
- `data/datasets/processed/pairwise_correlations.csv`
- `data/datasets/processed/tier_method_note.md`
- `data/datasets/processed/correlation_sensitivity_appendix.md`
- `task8_report.md`
- `occupation_case_studies.md`
- `milestone2_reproducibility_checklist.md`

## Interpretation warning

These measures describe different forms of AI exposure or computerisation potential. None should be interpreted as a direct prediction of job loss.
