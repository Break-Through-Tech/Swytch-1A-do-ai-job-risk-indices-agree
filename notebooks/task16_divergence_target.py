"""Export Task 16 regression targets using frozen Task 9 percentile ranks.

Run from any directory: python3 notebooks/task16_divergence_target.py
Add --check-task14 to compare with the existing enriched consensus table.
Uses only the Python standard library; never rebuilds upstream outputs.
"""
import argparse
import csv
import hashlib
import math
from pathlib import Path
from statistics import mean, median

DATA = Path(__file__).resolve().parents[1] / 'data/datasets/processed'
INPUT = DATA / 'agreement_analysis_sample.csv'
INPUT_SHA256 = '7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee'
RANKS = ('rank_aioe', 'rank_fo', 'rank_elo_dv', 'rank_elo_hum')
SOURCES = {'gpt4': 'rank_elo_dv', 'human': 'rank_elo_hum'}


def read(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def divergence(values):
    """Range of three complete, finite percentile ranks; no imputation."""
    if len(values) != 3 or not all(math.isfinite(v) and 0 < v <= 1 for v in values):
        raise ValueError('Expected three finite percentile ranks in (0, 1].')
    return max(values) - min(values)


def main(check_task14=False):
    assert divergence([.5, .5, .5]) == 0
    assert divergence([.25, .25, 1]) == .75
    assert math.isclose(divergence([.2, .5, .8]), .6)
    assert divergence([1, .25, .25]) == divergence([.25, .25, 1])
    for invalid in ([.5, float('nan'), .8], [.5, float('inf'), .8],
                    [0, .5, .8], [.5, 1.1, .8], [.5, .8]):
        try:
            divergence(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid ranks accepted')

    fingerprint = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    if fingerprint != INPUT_SHA256:
        raise ValueError('Frozen Task 9 input changed; investigate before exporting.')
    sample = read(INPUT)
    assert len(sample) == 663
    assert len({row['soc2018'] for row in sample}) == 663
    rows = []
    for row in sample:
        assert len(row['soc2018']) == 7 and row['soc2018'][2] == '-'
        assert row['included_in_analysis'] == 'True'
        ranks = {key: float(row[key]) for key in RANKS}
        assert all(math.isfinite(v) and 0 < v <= 1 for v in ranks.values())
        target = {key: row[key] for key in ('soc2018', 'title', *RANKS)}
        for source, label in SOURCES.items():
            value = divergence([ranks['rank_aioe'], ranks['rank_fo'], ranks[label]])
            assert 0 <= value <= 1
            target[f'divergence_{source}'] = repr(value)
        rows.append(target)

    if check_task14:
        existing = read(DATA / 'consensus_tiers.csv')
        assert len({row['soc2018'] for row in existing}) == len(existing)
        eligible = {row['soc2018']: row for row in existing
                    if row['included_in_analysis'] == 'True'}
        assert set(eligible) == {row['soc2018'] for row in rows}
        for row in rows:
            previous = eligible[row['soc2018']]
            assert all(row[key] == previous[key] for key in RANKS)
            for source in SOURCES:
                assert float(row[f'divergence_{source}']) == float(
                    previous[f'disagreement_score_{source}'])
        print('Task 14 comparison passed: all 1,326 target values match exactly.')

    output = DATA / 'divergence_targets.csv'
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    assert read(output) == rows
    summaries = []
    for source in SOURCES:
        values = [float(row[f'divergence_{source}']) for row in rows]
        summaries.append(f'| {source} | {min(values):.6f} | {mean(values):.6f} | '
                         f'{median(values):.6f} | {max(values):.6f} |')
    note = f'''# Task 16 — Divergence targets

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
{chr(10).join(summaries)}

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

- Input: `{fingerprint}`
- Target CSV: `{hashlib.sha256(output.read_bytes()).hexdigest()}`
'''
    (DATA / 'divergence_target_definition.md').write_text(note, encoding='utf-8')
    print(f'Exported {len(rows)} occupations with two divergence targets: {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-task14', action='store_true')
    main(parser.parse_args().check_task14)
