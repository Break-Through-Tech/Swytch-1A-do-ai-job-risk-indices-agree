# Task 13 — Consensus exposure tiers

## Method and approved cutoffs

Cutoffs are **team-approved**, as confirmed by Samarth on October 27, 2026.
The approved boundaries are 0.25, 0.50, and 0.75 on the average component rank.

Use the frozen Task 9 complete-case sample: 663 of 798 occupations. Preserve its
average-tie percentile ranks without reranking or filling missing scores.
For each eligible occupation:

- `consensus_rank_gpt4` = (`rank_aioe` + `rank_fo` + `rank_elo_dv`) / 3.
- `consensus_rank_human` = (`rank_aioe` + `rank_fo` + `rank_elo_hum`) / 3.

Each version equally weights three indices; the two Eloundou label sources are
alternatives. No source-quality or employment weights are used. Higher ranks mean
higher exposure/computerisation risk within each component's own construct.

Apply fixed cutoffs directly to the average component rank:

| Tier | Mean percentile rank |
| --- | --- |
| Low | 0 < rank <= 0.25 |
| Medium | 0.25 < rank <= 0.50 |
| High | 0.50 < rank <= 0.75 |
| Very High | 0.75 < rank <= 1 |

The consensus is an average of percentiles, not a newly computed percentile of
that average. Tier sizes need not be equal. Boundary values belong to the lower
tier. Equal consensus scores always receive the same tier; no tie-breaking by SOC.
`label_source_stability` is `stable` for identical tiers and `changed` otherwise;
it measures tier stability only, not agreement among the underlying indices.

## Outputs and results

`consensus_tiers.csv` retains all original columns and all 798 occupations in their
original order, adding frozen ranks, inclusion/exclusion fields, coverage status,
two consensus scores/tiers, stability, and cutoff-approval status.
The 135 excluded occupations have `coverage_status=insufficient_index_coverage`,
blank rank/consensus/tier fields, their Task 9 exclusion reason, and
`label_source_stability=insufficient_index_coverage`. Even an available label score
does not qualify an occupation outside the common four-score sample.

| Tier | GPT-4 beta | Human beta |
| --- | ---: | ---: |
| Low | 40 | 38 |
| Medium | 315 | 320 |
| High | 244 | 241 |
| Very High | 64 | 64 |
| Insufficient coverage | 135 | 135 |

Stable: **590**; changed: **73**
(11.0% of the eligible sample).
Chart: `figures/task13_tier_distribution.svg`.

## Reproduce and validation

Run `python3 notebooks/task13_consensus_tiers.py` from the repository root.
Only the Python standard library is required. Outputs are the CSV, this note,
and the SVG chart; upstream files are read only. Read SOC codes as strings.

The script asserts unique keys; 798 total/663 eligible/135 excluded; agreement
between actual missingness, sample membership and audit; unchanged source values;
independently recomputed average-tie ranks; boundary values and their immediately
adjacent floating-point values; consistent tier assignment for ties; tier totals;
and exact CSV read-back. Failed input checks stop before outputs are written.

Input SHA-256 fingerprints:

- `merged_v0.csv`: `8b930bb83491ccb4cc875b1666984a71d10e091fcb42eebf526bde83044ad09f`
- `agreement_analysis_sample.csv`: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`
- `agreement_sample_audit.csv`: `d1e58e4e6f2b65dc54db2a07a759d6872c51cbe077133e39dbbd5de9e5765d10`

## Interpretation and next task

Exposure is not predicted job loss. Frey–Osborne computerisation risk and modern
AI exposure measure different concepts; averaging ranks is a transparent summary,
not a validated probability. Complete-case selection limits generalizability.
A stable tier can hide substantial component disagreement. Task 14 will add
separate disagreement/confidence fields; this task makes no agreed/contested claim.
