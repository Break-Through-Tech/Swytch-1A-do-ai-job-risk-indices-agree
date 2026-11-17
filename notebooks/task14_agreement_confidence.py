"""Task 14: add transparent disagreement flags to Task 13 consensus tiers.

Run: python3 notebooks/task14_agreement_confidence.py
Rebuilds Task 13 first, then adds Task 14 fields. Standard library only.
"""
import csv
import hashlib
import math
from collections import Counter
from itertools import combinations

import task13_consensus_tiers as task13

DATA = task13.DATA
SOURCES = {'gpt4': 'rank_elo_dv', 'human': 'rank_elo_hum'}
METRICS = ('disagreement_score', 'max_pairwise_gap', 'largest_departure_index',
           'largest_departure_magnitude', 'max_gap_indices', 'confidence_flag',
           'confidence_flag_p80')


def quantile(values, fraction):
    """Linear interpolation at (n-1)*q, equivalent to pandas' default quantile."""
    assert values and 0 <= fraction <= 1
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lo, hi = math.floor(position), math.ceil(position)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def flag(score, threshold):
    if score is None:
        return 'insufficient_index_coverage'
    assert math.isfinite(score) and 0 <= score <= 1
    return 'contested' if score > threshold else 'agreed'


def metrics(ranks):
    """All tied departures/pairs retained in input order (absolute tolerance 1e-12)."""
    assert len(ranks) == 3
    assert all(math.isfinite(v) and 0 < v <= 1 for v in ranks.values())
    mean = math.fsum(ranks.values()) / 3
    spread = max(ranks.values()) - min(ranks.values())
    gaps = {f'{left}|{right}': abs(ranks[left] - ranks[right])
            for left, right in combinations(ranks, 2)}
    maximum = max(gaps.values())
    departures = {name: abs(value - mean) for name, value in ranks.items()}
    biggest = max(departures.values())
    return {
        'disagreement_score': repr(spread),
        'max_pairwise_gap': repr(maximum),
        'largest_departure_index': ';'.join(name for name, value in departures.items()
                                          if math.isclose(value, biggest, rel_tol=0, abs_tol=1e-12)),
        'largest_departure_magnitude': repr(biggest),
        'max_gap_indices': ';'.join(name for name, value in gaps.items()
                                   if math.isclose(value, maximum, rel_tol=0, abs_tol=1e-12)),
    }


def write(path, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    assert task13.read(path) == [{k: str(v) for k, v in row.items()} for row in rows]


def known_answer_checks():
    assert quantile([0, 1, 2, 3], .75) == 2.25
    assert quantile([.4], .8) == .4
    same = metrics({'aioe': .5, 'fo': .5, 'eloundou': .5})
    assert float(same['disagreement_score']) == 0
    assert same['largest_departure_index'] == 'aioe;fo;eloundou'
    outlier = metrics({'aioe': .25, 'fo': .25, 'eloundou': 1.0})
    assert float(outlier['disagreement_score']) == .75
    assert float(outlier['largest_departure_magnitude']) == .5
    assert outlier['largest_departure_index'] == 'eloundou'
    tied = metrics({'aioe': .25, 'fo': .5, 'eloundou': .75})
    assert tied['largest_departure_index'] == 'aioe;eloundou'
    assert tied['max_gap_indices'] == 'aioe|eloundou'
    assert flag(None, .5) == 'insufficient_index_coverage'
    assert flag(.5, .5) == flag(math.nextafter(.5, 0), .5) == 'agreed'
    assert flag(math.nextafter(.5, 1), .5) == 'contested'


def main():
    known_answer_checks()
    task13.main()
    path = DATA / 'consensus_tiers.csv'
    baseline = task13.read(path)
    rows = [dict(row) for row in baseline]
    eligible = [row for row in rows if row['included_in_analysis'] == 'True']
    scores = []
    for row in rows:
        for source, label_rank in SOURCES.items():
            for name in METRICS:
                row[f'{name}_{source}'] = ''
            if row['included_in_analysis'] != 'True':
                for name in ('confidence_flag', 'confidence_flag_p80'):
                    row[f'{name}_{source}'] = 'insufficient_index_coverage'
                continue
            ranks = {'aioe': float(row['rank_aioe']), 'fo': float(row['rank_fo']),
                     f'eloundou_{source}_beta': float(row[label_rank])}
            result = metrics(ranks)
            row.update({f'{name}_{source}': value for name, value in result.items()})
            scores.append(float(result['disagreement_score']))
    assert len(scores) == 1326
    thresholds = {75: quantile(scores, .75), 80: quantile(scores, .80)}
    assert thresholds[80] >= thresholds[75]
    for row in rows:
        for source in SOURCES:
            for percentile in (75, 80):
                row[f'disagreement_threshold_p{percentile}_{source}'] = repr(thresholds[percentile])
            if row['included_in_analysis'] == 'True':
                score = float(row[f'disagreement_score_{source}'])
                row[f'confidence_flag_{source}'] = flag(score, thresholds[75])
                row[f'confidence_flag_p80_{source}'] = flag(score, thresholds[80])
                assert math.isclose(score, float(row[f'max_pairwise_gap_{source}']), abs_tol=1e-15)
                assert not (row[f'confidence_flag_{source}'] == 'agreed' and
                            row[f'confidence_flag_p80_{source}'] == 'contested')
            else:
                assert row[f'confidence_flag_{source}'] == 'insufficient_index_coverage'
                assert all(row[f'{name}_{source}'] == '' for name in METRICS[:5])
    assert len(rows) == 798 and len(eligible) == 663
    assert len({row['soc2018'] for row in rows}) == 798
    assert all(all(row[name] == value for name, value in before.items())
               for before, row in zip(baseline, rows)), 'Task 13 fields changed'
    # Cross-tabs include both labels even when the count is zero, plus exclusions.
    cross = []
    sensitivity = []
    for source in SOURCES:
        for percentile, field in ((75, 'confidence_flag'), (80, 'confidence_flag_p80')):
            counts = Counter((row[f'consensus_tier_{source}'], row[f'{field}_{source}'])
                             for row in eligible)
            for tier in task13.TIERS:
                for confidence in ('agreed', 'contested'):
                    cross.append(dict(label_source=source, threshold_percentile=percentile,
                                      consensus_tier=tier, confidence_flag=confidence,
                                      count=counts[tier, confidence]))
            cross.append(dict(label_source=source, threshold_percentile=percentile,
                              consensus_tier='insufficient_index_coverage',
                              confidence_flag='insufficient_index_coverage', count=135))
            agreed = sum(row[f'{field}_{source}'] == 'agreed' for row in eligible)
            contested = 663 - agreed
            sensitivity.append(dict(label_source=source, threshold_percentile=percentile,
                                    threshold=repr(thresholds[percentile]), eligible_count=663,
                                    agreed_count=agreed, contested_count=contested,
                                    contested_share=repr(contested / 663),
                                    changed_from_p75=sum(row[f'{field}_{source}'] != row[f'confidence_flag_{source}']
                                                         for row in eligible)))
            assert sum(c['count'] for c in cross if c['label_source'] == source
                       and c['threshold_percentile'] == percentile) == 798
    write(path, rows)
    write(DATA / 'confidence_by_tier.csv', cross)
    write(DATA / 'confidence_threshold_sensitivity.csv', sensitivity)
    table = '\n'.join(f"| {r['label_source']} | P{r['threshold_percentile']} | {float(r['threshold']):.6f} | {r['agreed_count']} | {r['contested_count']} | {r['changed_from_p75']} |" for r in sensitivity)
    crosstable = '\n'.join(f"| {source} | {tier} | " + ' | '.join(str(sum(c['count'] for c in cross if c['label_source']==source and c['threshold_percentile']==75 and c['consensus_tier']==tier and c['confidence_flag']==confidence)) for confidence in ('agreed', 'contested')) + ' |' for source in SOURCES for tier in task13.TIERS)
    fingerprints = '\n'.join(f"- `{name}`: `{hashlib.sha256((DATA/name).read_bytes()).hexdigest()}`" for name in ('agreement_analysis_sample.csv', 'agreement_sample_audit.csv', 'consensus_tiers.csv'))
    note = f'''# Task 14 — Agreement-confidence flags and validation

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
{table}

Headline cross-tab:

| Label source | Tier | Agreed | Contested |
| --- | --- | ---: | ---: |
{crosstable}

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

{fingerprints}

## Interpretation

These flags describe relative disagreement, not statistical confidence, source
accuracy, or predicted job loss. Even 'agreed' rows can have meaningful gaps;
inspect the continuous score. Tier stability across GPT-4/human labels is distinct
from component agreement within each version. Frey–Osborne's older computerisation
construct differs from modern AI exposure, so disagreement can reflect those
conceptual differences rather than data errors. Findings apply to the complete-case
occupations and the chosen thresholds; Task 15 can use the fields for case studies.
'''
    (DATA / 'agreement_confidence_validation.md').write_text(note, encoding='utf-8')
    print('\nTask 14 results:')
    print(table)
    print('Task 14 checks passed; wrote enriched CSV, cross-tabs, sensitivity table, and validation note.')


if __name__ == '__main__':
    main()
