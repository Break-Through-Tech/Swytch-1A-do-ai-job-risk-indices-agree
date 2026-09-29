# O*NET Task 5 preparation methods

## Scope and outputs

This preparation pipeline writes five clean, six-digit-2018-SOC-indexed tables:

1. `onet_job_zones_6digit.csv`
2. `onet_abilities_6digit.csv`
3. `onet_skills_6digit.csv`
4. `onet_work_activities_6digit.csv`
5. `onet_work_context_6digit.csv`

All output files use `soc_6digit` as the join key. Each also carries `title` and
`title_rollup_method`, which is `base_00` when a broad O*NET occupation exists
and `first_detail` otherwise.

The shipped O*NET source coverage differs by domain. Job Zones produces 798
six-digit SOCs after rolling detailed codes up, whereas the rating-based
O*NET files contain 774 broad occupation codes. The pipeline preserves those
source-specific row counts; it does not manufacture ratings for occupations
absent from a source. This difference should be included in the Task 6.5
coverage report.

## SOC rollup

Raw O*NET-SOC codes are eight-digit codes such as `11-1011.03`. The pipeline
removes the suffix to create the six-digit 2018 SOC code `11-1011`. Numeric
feature values are then averaged across detailed O*NET occupations within each
six-digit SOC and O*NET element. This retains all supplied detailed occupations
without inventing employment weights.

## Scale choices

For Abilities, Skills, and Work Activities, the pipeline retains only the O*NET
`IM` (Importance) scale. It is the conventional single scale for a compact
feature table; `LV` (Level) is excluded so the same concept is not represented
twice in the first v0 table.

For Work Context, the pipeline retains `CX` (continuous Context) values. It
excludes the category-distribution scales (`CXP`, `CT`, and `CTP`), which would
otherwise expand one work-context concept into several proportions.

## Skills source reconciliation

The milestone calls for a single Skills file, but the repository supplies
`onet_essential_skills.xlsx` (basic skills, O*NET element IDs beginning `2.A`)
and `onet_transferable_skills.xlsx` (cross-functional skills, IDs beginning
`2.B`). These are combined into `onet_skills_6digit.csv`. The separate
`onet_software_skills.xlsx` workbook is not included in the five core outputs:
it contains categorical workplace-tool examples rather than numeric O*NET
importance/level ratings. It remains untouched for an optional later analysis.

## Job Zones

Job Zone is an ordinal category, not a value that should be averaged. For a
six-digit SOC with a `.00` broad occupation, its Job Zone is used. When no
`.00` row exists, the modal detailed-occupation Job Zone is used; ties use the
lower tied value and are labeled `detail_mode_tie_lower`. The output retains
`job_zone_rollup_method`, `job_zone_had_conflict`, and
`job_zone_source_value_count` so this decision remains auditable.

## Feature-column naming

Numeric feature columns have a source prefix (`ability_`, `skill_`,
`work_activity_`, or `work_context_`), a readable element-name slug, and the
O*NET element ID. `onet_feature_dictionary.csv` maps every output feature
column to its O*NET source workbook, element ID, element name, scale, and
rollup rule.
