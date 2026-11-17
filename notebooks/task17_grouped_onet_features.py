"""Task 17: fixed, interpretable O*NET composites. Standard library only.

Run: python3 notebooks/task17_grouped_onet_features.py
Grouping is specified in config/task17_onet_groups.json, independent of targets.
"""
import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/datasets/processed'
CONFIG = ROOT / 'config/task17_onet_groups.json'
DOMAINS = {'ability': 'onet_abilities', 'skill': 'onet_skills',
           'activity': 'onet_work_activities', 'context': 'onet_work_context',
           'job_zone': 'onet_job_zones'}
SAMPLE_SHA = '7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee'


def read(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def write(path, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    assert read(path) == rows, f'CSV read-back failed: {path}'


def keyed(rows, key):
    result = {row[key]: row for row in rows}
    assert len(result) == len(rows), f'Duplicate {key}'
    assert all(re.fullmatch(r'\d{2}-\d{4}', code) for code in result)
    return result


def aggregate(values):
    """Equal-weight mean, requiring all group members. Missing is never zero."""
    if not values:
        raise ValueError('An empty group is invalid')
    numbers = []
    for value in values:
        if value == '':
            numbers.append(None)
        else:
            number = float(value)
            if not math.isfinite(number) or not 1 <= number <= 5:
                raise ValueError('O*NET value outside finite [1, 5] range')
            numbers.append(number)
    if any(v is None for v in numbers):
        return ''
    return repr(math.fsum(numbers) / len(numbers))


def main():
    assert aggregate(['1', '3', '5']) == '3.0'
    assert aggregate(['2.5']) == '2.5'
    assert aggregate(['1', '', '5']) == ''
    for invalid in ([], ['nan'], ['inf'], ['0'], ['6']):
        try:
            aggregate(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid group accepted')

    sample_path = DATA / 'agreement_analysis_sample.csv'
    assert hashlib.sha256(sample_path.read_bytes()).hexdigest() == SAMPLE_SHA, 'Frozen sample changed'
    sample = read(sample_path)
    sample_by_soc = keyed(sample, 'soc2018')
    assert len(sample) == 663
    targets_path = DATA / 'divergence_targets.csv'
    targets = keyed(read(targets_path), 'soc2018')
    assert set(targets) == set(sample_by_soc), 'Task 16 join keys differ'
    assert all(targets[k]['title'] == r['title'] for k, r in sample_by_soc.items())

    groups = json.loads(CONFIG.read_text())['groups']
    assert len(groups) == len({g['feature'] for g in groups}) == 40
    assert all(g['domain'] in DOMAINS for g in groups)
    dictionary_path = DATA / 'onet_feature_dictionary.csv'
    dictionary = read(dictionary_path)
    assert len(dictionary) == 183
    elements = {row['element_id']: row for row in dictionary}
    assert len(elements) == 183
    elements['job_zone'] = dict(dataset='onet_job_zones', source_workbook='onet_job_zones.xlsx',
                                column_name='job_zone', element_name='Job Zone', scale_id='Job Zone',
                                rollup_rule='preserve Task 5 category and SOC rollup')
    members = [id for group in groups for id in group['element_ids']]
    assert len(members) == len(set(members)) == 184, 'Repeated or omitted source elements'
    assert set(members) == set(elements), 'Grouping does not cover the source dictionary exactly'

    source_paths = [DATA / f'{name}_6digit.csv' for name in DOMAINS.values()]
    tables = {domain: keyed(read(path), 'soc_6digit')
              for (domain, _), path in zip(DOMAINS.items(), source_paths)}
    for domain, table in tables.items():
        assert len(table) == (798 if domain == 'job_zone' else 774)
    mapping = []
    for group in groups:
        assert group['element_ids']
        for id in group['element_ids']:
            item = elements[id]
            assert item['dataset'] == DOMAINS[group['domain']]
            assert item['scale_id'] == ('CX' if group['domain'] == 'context' else
                                        'Job Zone' if group['domain'] == 'job_zone' else 'IM')
            assert all(item['column_name'] in row for row in tables[group['domain']].values())
            mapping.append(dict(group_feature=group['feature'], domain=group['domain'],
                                group_size=str(len(group['element_ids'])), element_id=id,
                                element_name=item['element_name'], source_column=item['column_name'],
                                source_file=DOMAINS[group['domain']]+'_6digit.csv',
                                source_workbook=item['source_workbook'], source_scale=item['scale_id'],
                                source_rollup=item['rollup_rule'],
                                aggregation='identity' if id == 'job_zone' else 'unweighted mean; require all members',
                                interpretation=group['interpretation']))

    rows, audit = [], []
    for occupation in sample:
        soc = occupation['soc2018']
        out = dict(soc2018=soc, title=occupation['title'])
        missing_groups = []
        flags = {}
        for domain in DOMAINS:
            flags[f'has_{domain}_source_row'] = str(soc in tables[domain])
        for group in groups:
            source = tables[group['domain']].get(soc)
            values = [source[elements[id]['column_name']] if source else ''
                      for id in group['element_ids']]
            result = aggregate(values)
            if group['domain'] == 'job_zone' and result:
                number = float(result)
                assert number.is_integer(), 'Job Zone must remain an ordinal category'
                result = str(int(number))
            out[group['feature']] = result
            if result == '':
                missing_groups.append(group['feature'])
        rows.append(out)
        audit.append(dict(soc2018=soc, title=occupation['title'], **flags,
                          available_feature_count=str(40-len(missing_groups)),
                          missing_feature_count=str(len(missing_groups)),
                          feature_coverage_status='complete' if not missing_groups else 'incomplete_onet_ratings',
                          missing_features=';'.join(missing_groups)))
    assert len(rows) == 663 and len(rows[0]) == 42
    assert sum(row['feature_coverage_status'] == 'complete' for row in audit) == 650
    assert Counter(row['missing_feature_count'] for row in audit) == {'0': 650, '39': 13}
    assert all(row['job_zone_preparation'] for row in rows)
    assert set(keyed(rows, 'soc2018')) == set(targets)

    outputs = {'grouped_onet_features.csv': rows, 'onet_grouping_dictionary.csv': mapping,
               'grouped_onet_coverage.csv': audit}
    for name, content in outputs.items():
        write(DATA / name, content)
    inputs = [CONFIG, sample_path, targets_path, dictionary_path, *source_paths]
    counts = Counter(g['domain'] for g in groups)
    note = '''# Task 17 — Grouped O*NET features

## Purpose and fixed design

Reduce 183 prepared O*NET rating elements plus Job Zone to **40 predictors**:
8 ability, 7 skill, 6 work-activity, 18 work-context features and 1 Job Zone.
These are analyst-defined descriptive composites, not official O*NET scales or
validated latent factors. Group membership follows element meaning and IDs.
No divergence values, correlations with targets, model results, PCA, clustering,
or sample-fitted weights were used to choose or calculate the groups.

`config/task17_onet_groups.json` is the editable grouping specification. Every
one of the 183 rating elements and Job Zone maps to exactly one feature, with no
overlap or dropped items. Singleton groups preserve distinct concepts, including
automation, accuracy, sitting and physical proximity. Communication, technical
skills and other broad composites sacrifice detail for a compact model.

## Calculation and scales

Each rating feature is the equal-weight arithmetic mean of its listed members.
All members must be present and finite. A missing member or missing source row
leaves that group blank; no partial-group average or zero substitution occurs.
Groups use existing six-digit SOC means from Task 5 without repeating its rollup.
Abilities, skills and work activities retain IM (Importance). Context retains CX.
Observed and required input/output rating bounds are [1, 5]. Job Zone is copied
as an integer ordinal category (1–5), never averaged with other elements.
No source rating is reversed and no data-derived scaling is performed.

Context items share numeric endpoints but have different response anchors
(frequency, degree, importance and responsibility). Their means are descriptive
summaries, not equivalent units or calibrated probabilities. See each dictionary
row for interpretation. Decisions/responsibility, routine/equipment pace, and
pressure/competition and communication deliberately mix related anchors; inspect their source
items in sensitivity work if these composites become influential. Outdoor and
indoor work, sitting and physical activity, and automation and repetition remain
separate. Protective equipment use remains separate from hazard exposure.
No group is an AI-risk score. Importance ratings describe job requirements,
not an individual worker's skills.

## Sample, coverage and outputs

Use the frozen Task 9 663-occupation sample and preserve its SOC order and titles.
The SOC set matches Task 16's targets exactly. Each rating-domain source has 774
occupations; Job Zones has 798. Of the 663 modeling occupations, **650 have all
40 features** and **13 have only Job Zone**, with all 39 rating composites blank.
No occupation is discarded. Missing source coverage must not be interpreted as
low requirements or zero exposure.

- `grouped_onet_features.csv`: 663 rows, `soc2018`, `title`, and 40 predictors.
- `onet_grouping_dictionary.csv`: 184 source-to-group mappings including source
  column, element ID/name, scale, workbook, upstream rollup, group size, aggregation
  rule and interpretation. A source element's within-group weight is 1/group_size.
- `grouped_onet_coverage.csv`: 663 rows with source-row flags, available/missing
  feature counts, coverage status and exact missing feature names. These are audit
  fields, not part of the 40-predictor feature table.

The 13 occupations without rating data:

'''
    missing_socs = [r for r in audit if r['feature_coverage_status'] != 'complete']
    note += '\n'.join(f"- `{r['soc2018']}` — {r['title']}" for r in missing_socs)
    note += '''

## Task 18 handoff

Load SOCs as text. Join `grouped_onet_features.csv` to `divergence_targets.csv`
one-to-one on `soc2018`; all 663 targets survive. Use only the 40 configured
feature columns as candidate predictors. Exclude titles, SOC identifiers, input
ranks, consensus scores, disagreement fields and coverage audit fields.
Use the same held-out occupations for GPT-4 and human targets. This task does
not create or tune a split, fill missing values, fit a scaler or select features.
Fit any median imputation and scaling on training data only (inside CV pipelines
when tuning). Document the handling of 13 largely missing rows and compare with
a 650-occupation complete-feature sensitivity analysis without silently dropping
targets. Job Zone can be treated as ordinal or encoded within the training pipeline.

AIOE itself uses occupational abilities, so predictive relationships may partly
reflect construction of an input index rather than a new causal explanation.
Correlated composites can share importance. Held-out performance and permutation
importance cannot establish causality or predict job loss.

## Reproduction and validation

Run `python3 notebooks/task17_grouped_onet_features.py` from the repository root
or by absolute path from another directory. Uses only Python's standard library.
Writes only the three Task 17 CSVs and this note. All upstream inputs are read only.

Checks enforce the frozen Task 9 fingerprint, 663 unique valid SOCs, matching
Task 16 keys/titles, 40 unique groups, exactly-once coverage of all 184 inputs,
domain/scale consistency, complete-group averaging, finite [1, 5] values,
integer Job Zone, known-answer/invalid-input behavior, 650 complete and 13
incomplete occupations, and exact CSV read-back. If source counts or coverage
change, investigate rather than overriding checks.

## Input fingerprints (SHA-256)

'''
    note += '\n'.join(f'- `{path.relative_to(ROOT)}`: `{hashlib.sha256(path.read_bytes()).hexdigest()}`'
                      for path in inputs)
    note += '\n\n## Feature summary\n\n'
    note += '| Feature | Source elements | Available occupations | Minimum | Maximum |\n'
    note += '| --- | ---: | ---: | ---: | ---: |\n'
    for group in groups:
        values = [float(row[group['feature']]) for row in rows if row[group['feature']]]
        assert len(set(values)) > 1, f"Constant feature: {group['feature']}"
        note += (f"| `{group['feature']}` | {len(group['element_ids'])} | {len(values)} | "
                 f"{min(values):.4f} | {max(values):.4f} |\n")
    note += '\n## Output fingerprints (SHA-256)\n\n'
    note += '\n'.join(f'- `{name}`: `{hashlib.sha256((DATA/name).read_bytes()).hexdigest()}`' for name in outputs)
    note += '\n'
    (DATA / 'grouped_onet_methods.md').write_text(note, encoding='utf-8')
    print(f'Exported {len(rows)} occupations, {len(groups)} features, {len(mapping)} mappings.')
    print('Coverage: 650 complete; 13 with Job Zone only. Task 16 one-to-one join passed.')
    print('Features by domain:', dict(counts))


if __name__ == '__main__':
    main()
