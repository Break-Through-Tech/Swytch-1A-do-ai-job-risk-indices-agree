"""Build Task 13 outputs. Run: python3 notebooks/task13_consensus_tiers.py.

Uses only the Python standard library; preserves Task 9's frozen ranks.
"""
import csv
import hashlib
import math
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/datasets/processed'
TIERS = ('Low', 'Medium', 'High', 'Very High')
RANKS = {'aioe': 'rank_aioe', 'fo_prob': 'rank_fo',
         'dv_rating_beta': 'rank_elo_dv', 'human_rating_beta': 'rank_elo_hum'}


def read(path):
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def keyed(rows):
    result = {row['soc2018']: row for row in rows}
    assert len(result) == len(rows), 'Duplicate SOC keys'
    assert all(result), 'Missing SOC key'
    return result


def equivalent(left, right):
    if left == right:
        return True
    try:
        return math.isclose(float(left), float(right), rel_tol=1e-14, abs_tol=1e-14)
    except ValueError:
        return False


def tier(score):
    if score is None:
        return ''
    assert math.isfinite(score) and 0 <= score <= 1
    return TIERS[sum(score > cutoff for cutoff in (0.25, 0.50, 0.75))]


def validate_ranks(sample):
    # Independently recompute Task 9 average ranks to detect stale/corrupt inputs.
    for raw, rank in RANKS.items():
        values = sorted(float(row[raw]) for row in sample)
        assert all(math.isfinite(value) for value in values)
        positions = {}
        for index, value in enumerate(values, 1):
            positions.setdefault(value, []).append(index)
        expected = {value: sum(p) / len(p) / len(values)
                    for value, p in positions.items()}
        for row in sample:
            assert math.isclose(float(row[rank]), expected[float(row[raw])],
                                rel_tol=0, abs_tol=1e-12), (row['soc2018'], rank)


def chart(counts, excluded):
    pieces = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 450">',
              '<rect width="900" height="450" fill="white"/>']
    def label(x, y, text, size=14, anchor='start'):
        pieces.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" text-anchor="{anchor}" fill="#202b3b">{escape(text)}</text>')
    label(45, 30, 'Task 13: consensus exposure tiers', 23)
    label(45, 56, '663 eligible occupations per source; approved cutoffs at 0.25, 0.50, 0.75')
    maximum = max(n for counter in counts.values() for n in counter.values())
    top = math.ceil(maximum / 50) * 50
    for tick in range(0, top + 1, 50):
        y = 335 - tick / top * 220
        pieces.append(f'<line x1="80" y1="{y}" x2="855" y2="{y}" stroke="#dce1e7"/>')
        label(68, y + 5, str(tick), anchor='end')
    label(80, 95, 'Occupations')
    for i, name in enumerate(TIERS):
        center = 175 + 195 * i
        for j, (source, color) in enumerate((('gpt4', '#276eaa'), ('human', '#d07427'))):
            n = counts[source][name]
            h = n / top * 220
            x = center - 60 + j * 62
            pieces.append(f'<rect x="{x}" y="{335-h}" width="55" height="{h}" fill="{color}"/>')
            label(x + 27.5, 328-h, str(n), anchor='middle')
        label(center, 360, name, anchor='middle')
    for x, color, text in ((270, '#276eaa', 'GPT-4 beta'), (470, '#d07427', 'Human beta')):
        pieces.append(f'<rect x="{x}" y="385" width="15" height="15" fill="{color}"/>')
        label(x + 23, 398, text)
    label(45, 432, f'{excluded} occupations retained as insufficient_index_coverage; exposure is not predicted job loss.', 13)
    pieces.append('</svg>')
    return '\n'.join(pieces) + '\n'


def main():
    for boundary, lower, upper in ((.25, 'Low', 'Medium'), (.5, 'Medium', 'High'), (.75, 'High', 'Very High')):
        assert tier(boundary) == lower
        assert tier(math.nextafter(boundary, 0)) == lower
        assert tier(math.nextafter(boundary, 1)) == upper
    assert tier(0) == 'Low' and tier(1) == 'Very High' and tier(None) == ''
    merged = read(DATA / 'merged_v0.csv')
    sample = read(DATA / 'agreement_analysis_sample.csv')
    audit = keyed(read(DATA / 'agreement_sample_audit.csv'))
    all_rows, eligible = keyed(merged), keyed(sample)
    assert len(all_rows) == len(audit) == 798 and len(eligible) == 663
    assert all_rows.keys() == audit.keys() and eligible.keys() <= all_rows.keys()
    validate_ranks(sample)
    added = [*RANKS.values(), 'included_in_analysis', 'exclusion_reason', 'coverage_status',
             'consensus_rank_gpt4', 'consensus_rank_human', 'consensus_tier_gpt4',
             'consensus_tier_human', 'label_source_stability', 'tier_cutoff_status']
    fields = list(merged[0]) + added
    assert len(fields) == len(set(fields))
    output = []
    for original in merged:
        code = original['soc2018']
        row = dict(original)
        for field in added:
            row[field] = ''
        included = code in eligible
        required = list(RANKS)
        assert included == all(original[name] != '' for name in required)
        assert (audit[code]['included_in_analysis'] == 'True') == included
        assert bool(audit[code]['exclusion_reason']) != included
        row.update(included_in_analysis=str(included),
                   exclusion_reason=audit[code]['exclusion_reason'],
                   coverage_status='complete_index_coverage' if included else 'insufficient_index_coverage',
                   tier_cutoff_status='team_approved')
        if included:
            frozen = eligible[code]
            assert all(equivalent(frozen[name], original[name]) for name in original), code
            row.update({name: frozen[name] for name in RANKS.values()})
            for source, label_rank in (('gpt4', 'rank_elo_dv'), ('human', 'rank_elo_hum')):
                consensus = math.fsum(float(row[name]) for name in ('rank_aioe', 'rank_fo', label_rank)) / 3
                row[f'consensus_rank_{source}'] = repr(consensus)
                row[f'consensus_tier_{source}'] = tier(consensus)
            row['label_source_stability'] = ('stable' if row['consensus_tier_gpt4'] == row['consensus_tier_human'] else 'changed')
        else:
            row['label_source_stability'] = 'insufficient_index_coverage'
        output.append(row)
    counts = {source: Counter(row[f'consensus_tier_{source}'] for row in output if row['included_in_analysis'] == 'True') for source in ('gpt4', 'human')}
    stability = Counter(row['label_source_stability'] for row in output)
    assert all(sum(counter.values()) == 663 for counter in counts.values())
    assert stability['insufficient_index_coverage'] == 135
    for source in counts:
        tied = {}
        for row in output:
            if row['included_in_analysis'] == 'True':
                value = row[f'consensus_rank_{source}']
                assigned = row[f'consensus_tier_{source}']
                assert tied.setdefault(value, assigned) == assigned
    target = DATA / 'consensus_tiers.csv'
    with target.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(output)
    assert read(target) == output, 'CSV round-trip changed values'
    figures = ROOT / 'figures'
    figures.mkdir(exist_ok=True)
    (figures / 'task13_tier_distribution.svg').write_text(chart(counts, 135), encoding='utf-8')
    table = '\n'.join(f'| {name} | {counts["gpt4"][name]} | {counts["human"][name]} |' for name in TIERS)
    fingerprints = '\n'.join(f'- `{name}`: `{hashlib.sha256((DATA / name).read_bytes()).hexdigest()}`' for name in ('merged_v0.csv', 'agreement_analysis_sample.csv', 'agreement_sample_audit.csv'))
    note = f'''# Task 13 — Consensus exposure tiers

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
{table}
| Insufficient coverage | 135 | 135 |

Stable: **{stability['stable']}**; changed: **{stability['changed']}**
({stability['changed']/663:.1%} of the eligible sample).
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

{fingerprints}

## Interpretation and next task

Exposure is not predicted job loss. Frey–Osborne computerisation risk and modern
AI exposure measure different concepts; averaging ranks is a transparent summary,
not a validated probability. Complete-case selection limits generalizability.
A stable tier can hide substantial component disagreement. Task 14 will add
separate disagreement/confidence fields; this task makes no agreed/contested claim.
'''
    (DATA / 'tier_method_note.md').write_text(note, encoding='utf-8')
    print(table)
    print(f"Stable: {stability['stable']}; changed: {stability['changed']}; insufficient coverage: 135")
    print('All validation checks passed; wrote CSV, methods note, and SVG chart.')


if __name__ == '__main__':
    main()
