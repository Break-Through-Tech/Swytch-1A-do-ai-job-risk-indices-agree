# Task 14 — Agreement-confidence flags and validation

## Definition

For each of Task 13's two three-index versions, disagreement is the maximum minus
minimum component percentile rank, on the fixed 663-occupation sample. Scores
range from 0 to 1; larger values mean greater rank disagreement. A gap of 0.6 is
60 percentile points. `max_pairwise_gap` is mathematically identical to this range;
both fields are retained explicitly to satisfy the task and aid inspection.

`largest_departure_index` identifies the component(s) with the largest absolute
distance from that version's equal-weight consensus mean.
`largest_departure_magnitude` records that distance, and `max_gap_indices` lists
the pair(s) with the largest gap. Components are named `aioe`, `fo`, and
`eloundou_gpt4_beta` or `eloundou_human_beta`. All tied components/pairs are listed,
separated by semicolons, in component order; equality uses absolute tolerance
1e-12. This names the largest departure, not an index proven wrong.

## Threshold choice and sensitivity

The headline rule is **contested when disagreement > the pooled P75 threshold**;
otherwise **agreed**. Pool the 663 GPT-4-version and 663 human-version scores
(1,326 values, equal representation per version). One common threshold permits
comparison across label sources without forcing equal contested counts. Pooling
is descriptive calibration, not 1,326 independent occupations or an inferential
test. P75 flags the upper quarter approximately, an analyst-selected screening
rule, not a validated confidence probability or a team-approved scientific cutoff.

Use linear interpolation at sorted position `(n - 1) * q`. Scores exactly on the
threshold are agreed. Equal scores receive equal flags; tied cutoffs can make the
contested proportion differ from 25%. The nearby P80 rule is a less sensitive
check; all changes must be contested at P75 becoming agreed at P80.
CSV threshold values retain full precision; displayed thresholds are rounded.

| Label source | Threshold | Value | Agreed | Contested | Changed from P75 |
| --- | --- | ---: | ---: | ---: | ---: |
| gpt4 | P75 | 0.646870 | 502 | 161 | 0 |
| gpt4 | P80 | 0.686275 | 536 | 127 | 34 |
| human | P75 | 0.646870 | 492 | 171 | 0 |
| human | P80 | 0.686275 | 529 | 134 | 37 |

Headline cross-tab:

| Label source | Tier | Agreed | Contested |
| --- | --- | ---: | ---: |
| gpt4 | Low | 39 | 1 |
| gpt4 | Medium | 246 | 69 |
| gpt4 | High | 153 | 91 |
| gpt4 | Very High | 64 | 0 |
| human | Low | 37 | 1 |
| human | Medium | 250 | 70 |
| human | High | 142 | 99 |
| human | Very High | 63 | 1 |

Each label source additionally has **135 insufficient-coverage occupations**.
Their confidence flags are `insufficient_index_coverage`, with numeric disagreement,
departure, and pair fields blank. They are never classified as agreed or contested.
Threshold metadata is populated for every row but does not confer eligibility.

## Outputs and reproduction

- `consensus_tiers.csv`: all Task 13 columns and values preserved; added fields
  have `_gpt4` and `_human` suffixes. Headline `confidence_flag` uses P75;
  `confidence_flag_p80` is the sensitivity result.
- `confidence_by_tier.csv`: complete cross-tabs for both thresholds and sources,
  including zero-count combinations and insufficient coverage.
- `confidence_threshold_sensitivity.csv`: thresholds, eligible counts, contested
  shares and label changes.
- This note: method, results, validation, and input/output fingerprints.

Run `python3 notebooks/task14_agreement_confidence.py` from the repository root.
It rebuilds Task 13 first, then enriches the table; only the standard library is
required. Running Task 13 alone replaces the enriched CSV with its base output;
run Task 14 last to restore the confidence fields. No upstream sample is changed.
Read SOC codes as text. No missing component scores are imputed.

## Validation

Passed known-answer checks for zero disagreement, a single outlier, tied largest
departures, pair identities, interpolated quantiles, missing coverage, and exact
threshold boundaries with adjacent floating-point values. Task 13's frozen-rank,
source, sample and tier checks run before enrichment. Integration assertions check
798 unique occupations; 663 eligible; unchanged Task 13 fields; range equals maximum
pairwise gap; no missing coverage classified agreed; monotonic sensitivity; every
cross-tab totals 798; and exact CSV read-back for all three tables.

Additional independent verification compared every pre-existing field with the
Task 13 Git snapshot, recomputed gaps and largest departures, checked thresholds
with `statistics.quantiles(method="inclusive")`, and recounted all cross-tab cells.
A second complete run produced byte-identical CSVs and this validation note.

SHA-256 fingerprints:

- `agreement_analysis_sample.csv`: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`
- `agreement_sample_audit.csv`: `d1e58e4e6f2b65dc54db2a07a759d6872c51cbe077133e39dbbd5de9e5765d10`
- `consensus_tiers.csv`: `f57e5a072cadc80252e56f1b7787341494bad335542785be111ac190eb7b6870`

## Interpretation

These flags describe relative disagreement, not statistical confidence, source
accuracy, or predicted job loss. Even 'agreed' rows can have meaningful gaps;
inspect the continuous score. Tier stability across GPT-4/human labels is distinct
from component agreement within each version. Frey–Osborne's older computerisation
construct differs from modern AI exposure, so disagreement can reflect those
conceptual differences rather than data errors. Findings apply to the complete-case
occupations and the chosen thresholds; Task 15 can use the fields for case studies.
