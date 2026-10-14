# Task 9 — October agreement sample definition

## Input and fixed comparison group

Input: `merged_v0.csv`, 798 occupations × 214 columns.
Its SHA-256 fingerprint is `8b930bb83491ccb4cc875b1666984a71d10e091fcb42eebf526bde83044ad09f`.

One row per unique, nonmissing six-digit 2018 SOC code (`soc2018`).
Include an occupation only when all four scores are present: `aioe`, `fo_prob`,
`dv_rating_beta` (GPT-4 beta), and `human_rating_beta` (human beta).
The same 663 occupations must be used for both label-source comparisons.
No missing score is imputed. O*NET feature completeness is not an eligibility rule.

The sample has 663 occupations × 225 columns.
All 214 original columns and their values are retained, including
raw scores, alpha/gamma variants, O*NET features, and crosswalk provenance flags.

## Percentile ranks

Compute each rank within the fixed 663-occupation sample, after filtering.
Use ascending average ranks divided by 663:
`Series.rank(method='average', ascending=True, pct=True)`.
Ranks lie above zero and at or below one. Tied scores receive the same average
position; tied maxima can have ranks below one. Do not force endpoints to 0 or 1.
For example, `[0, 0.2, 0.2, 0.9]` gives `[0.25, 0.625, 0.625, 1.0]`.

| Preserved raw score | Added rank column |
| --- | --- |
| `aioe` | `rank_aioe` |
| `fo_prob` | `rank_fo` |
| `dv_rating_beta` | `rank_elo_dv` |
| `human_rating_beta` | `rank_elo_hum` |

All four source scores already increase with exposure or computerisation risk;
none is reversed. AIOE may be negative because it is standardized, not because
its direction is reversed. Alpha/gamma variants are preserved as raw scores;
they do not affect eligibility or receive rank columns in this task.
These are unweighted occupation ranks, not employment-weighted ranks.

## Inclusion audit

`agreement_sample_audit.csv` contains all 798 input occupations,
identifiers/titles, the four raw scores, and these fields:

- `missing_aioe`, `missing_fo_prob`, `missing_dv_rating_beta`,
  `missing_human_rating_beta`: True when that score is missing.
- `missing_index_count`: number of missing required scores.
- `included_in_analysis`: True only when all four required scores are present.
- `exclusion_reason`: semicolon-separated missing-score flags; blank for included rows.

The same audit fields are also saved on included rows in the sample.
Empty score cells mean missing data, not zero. Empty exclusion reasons mean eligible.

Included: 663. Excluded: 135.

| Exclusion reason | Occupations |
| --- | --- |
| missing_fo_prob | 127 |
| missing_aioe; missing_fo_prob | 8 |

## Reproduction and checks

Run `notebooks/task9.ipynb` from top to bottom, with pandas installed from
`requirements.txt`, from either the notebook directory or repository root.
Outputs are `data/datasets/processed/agreement_analysis_sample.csv`,
`agreement_sample_audit.csv`, and this note.
Reload CSV occupation codes as text: `dtype={'soc2018': 'string'}`.

The notebook checks required columns, valid/unique SOC keys, numeric and finite
scores, valid probability/share ranges, 798 input occupations, and exactly 663
complete occupations before exporting. It checks rank bounds, direction, equal
ranks for ties, unchanged original values, audit consistency, a known-answer
ranking example, and CSV read-back contents. A changed input/sample count stops
export and requires investigation; do not bypass the check to change the sample.
Reruns regenerate Task 9 outputs; the fingerprint above identifies the input used.
The upstream `merged_v0.csv` is not modified.

## Interpretation and limitations

A rank near 0.80 means roughly the 80th percentile among these 663 occupations;
it is not an 80% probability of automation or job loss. Rankings compare relative
position, not the size of raw-score differences or equivalent constructs.
The indices measure different concepts, and their original vintage/crosswalk
limitations remain. Missing-score exclusions may affect how representative this
sample is; findings apply to the occupations with complete coverage.
This task prepares the sample; correlations, consensus tiers, and disagreement
analysis are later tasks.
