# Task 16 — Divergence targets

## Definition

For each occupation, divergence is the maximum minus minimum of three component
percentile ranks. Each index receives equal standing; GPT-4 and human Eloundou
labels are alternatives, not two independent indices in a four-index target.

- `divergence_gpt4` = range of `rank_aioe`, `rank_fo`, `rank_elo_dv`.
- `divergence_human` = range of `rank_aioe`, `rank_fo`, `rank_elo_hum`.

This is exactly Task 14's continuous `disagreement_score_gpt4` and
`disagreement_score_human`, exported under explicit modeling-target names.
Range was chosen to preserve the existing disagreement definition and provide a
direct percentile-point interpretation. It equals the largest pairwise rank gap;
it does not capture the middle index's position or which index ranks highest.
We do not introduce a different standard-deviation target or binary cutoff.

Values are in [0, 1]; larger values mean greater disagreement. Ranks of
0.20, 0.50, 0.80 yield 0.60, a 60-percentile-point gap. Equal ranks yield zero.
This is disagreement about relative occupation rankings, not statistical
confidence, a probability of automation, or predicted job loss. The indices
measure different constructs, so disagreement need not indicate an error.

## Fixed sample and output schema

Input: `agreement_analysis_sample.csv`, the frozen Task 9 complete-case sample
of 663 unique six-digit 2018 SOC occupations from 798 candidates. All four raw
scores must be present upstream, giving identical occupations for both targets.
The 135 excluded occupations receive no targets; they are absent from this file.
No ranks are recomputed, missing values filled, or feature-completeness filters
applied. Task 9 ranks are ascending average-tie percentiles within these 663 jobs.
These are unweighted occupation ranks, not employment-weighted ranks.

`divergence_targets.csv` has 663 rows and eight columns:

| Columns | Meaning |
| --- | --- |
| `soc2018` | Unique join key; load as text |
| `title` | Occupation title preserved from Task 9 |
| `rank_aioe`, `rank_fo`, `rank_elo_dv`, `rank_elo_hum` | Frozen component ranks, preserved verbatim |
| `divergence_gpt4`, `divergence_human` | Continuous regression targets |

For Task 18, join Task 17's O*NET features one-to-one by `soc2018` and use the
same held-out occupations for both versions. The rank columns are provenance,
not predictors: including them, consensus scores, or other target-derived fields
would leak the answer. Fit preprocessing on training data only. Task 16 applies
no contested/agreed threshold and does not create a train/test split.

## Descriptive results

| Target | Minimum | Mean | Median | Maximum |
| --- | ---: | ---: | ---: | ---: |
| gpt4 | 0.012066 | 0.466716 | 0.472851 | 0.953243 |
| human | 0.010558 | 0.471024 | 0.472851 | 0.953243 |

## Reproduction and checks

Run `python3 notebooks/task16_divergence_target.py` from the repository root;
only the standard library is needed. Paths also resolve from other directories.
The script writes only its target CSV and this note. Upstream files are read only.
Run with `--check-task14` to additionally require exact equality of all 1,326
targets and their source ranks against the existing enriched `consensus_tiers.csv`.
That optional comparison requires Task 14 outputs; ordinary reproduction does not.

Checks cover the frozen input fingerprint, 663 unique SOC keys, complete and
finite ranks, bounds, zero disagreement, an outlier, a known gap, order invariance,
invalid inputs, and exact CSV read-back. A changed input fingerprint stops export
and requires investigation. Sample selection and original index vintage/crosswalk
limitations carry forward; findings apply to the common complete-case sample.

SHA-256 fingerprints:

- Input: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`
- Target CSV: `e6957c44b94c0c726c47d5a3352b72dfde2762d70ec26c7ec4be96a89e5278ef`
