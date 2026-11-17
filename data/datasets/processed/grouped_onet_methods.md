# Task 17 — Grouped O*NET features

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

- `11-2032` — Public Relations Managers
- `13-1082` — Project Management Specialists
- `13-2051` — Financial and Investment Analysts
- `13-2054` — Financial Risk Specialists
- `17-3028` — Calibration Technologists and Technicians
- `19-4044` — Hydrologic Technicians
- `29-2042` — Emergency Medical Technicians
- `29-2043` — Paramedics
- `29-2072` — Medical Records Specialists
- `29-9021` — Health Information Technologists and Medical Registrars
- `39-1014` — First-line Supervisors of Entertainment and Recreation Workers, Except Gambling Services
- `53-1044` — First-line Supervisors of Passenger Attendants
- `53-3054` — Taxi Drivers

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

- `config/task17_onet_groups.json`: `930262cddce2ba3afe3457fbaabc78267a809ca7bc9fbc861a9d93af35d0f864`
- `data/datasets/processed/agreement_analysis_sample.csv`: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`
- `data/datasets/processed/divergence_targets.csv`: `e6957c44b94c0c726c47d5a3352b72dfde2762d70ec26c7ec4be96a89e5278ef`
- `data/datasets/processed/onet_feature_dictionary.csv`: `c43ba019bce783bddafb1c6429b88e1854fa8a6397eb45f9c1db7891d49c2376`
- `data/datasets/processed/onet_abilities_6digit.csv`: `d77d24045543a719d441466bb871c5dcfe9df51af574fc51b59cdfc1ef5087de`
- `data/datasets/processed/onet_skills_6digit.csv`: `377a34b07ed6c833bc60c96311607d6a3f71755a38a28969f6f277db72c46aad`
- `data/datasets/processed/onet_work_activities_6digit.csv`: `d941039a0973b78cb4caa6927ed59386ac75b71f0ecf55ea186693822eaa146a`
- `data/datasets/processed/onet_work_context_6digit.csv`: `730038035802a45b3ba82dbd01b323a8347a2219354f555971597b11df78f784`
- `data/datasets/processed/onet_job_zones_6digit.csv`: `435c9359d93eb57356c4e13374a32bba7000096d4de2049ef3c34479414038e6`

## Feature summary

| Feature | Source elements | Available occupations | Minimum | Maximum |
| --- | ---: | ---: | ---: | ---: |
| `ability_verbal` | 4 | 650 | 2.1275 | 4.6900 |
| `ability_reasoning_creativity` | 7 | 650 | 2.1971 | 4.0900 |
| `ability_quantitative` | 2 | 650 | 1.0000 | 4.8100 |
| `ability_memory_attention` | 3 | 650 | 1.8300 | 3.8733 |
| `ability_perceptual_spatial` | 5 | 650 | 1.5500 | 3.7760 |
| `ability_psychomotor` | 10 | 650 | 1.0380 | 3.7990 |
| `ability_physical` | 9 | 650 | 1.0133 | 3.5267 |
| `ability_sensory` | 12 | 650 | 1.7617 | 3.7083 |
| `skill_communication` | 4 | 650 | 1.9675 | 4.6575 |
| `skill_math_science` | 2 | 650 | 1.0000 | 4.4350 |
| `skill_learning_thinking` | 4 | 650 | 1.8750 | 4.3425 |
| `skill_social` | 6 | 650 | 1.7717 | 3.9800 |
| `skill_technical` | 11 | 650 | 1.0909 | 3.4327 |
| `skill_systems_problem_solving` | 4 | 650 | 1.6575 | 4.1525 |
| `skill_resource_management` | 4 | 650 | 1.4675 | 3.7800 |
| `activity_information_processing` | 9 | 650 | 1.7711 | 4.4800 |
| `activity_planning_decisions` | 6 | 650 | 1.9300 | 4.3833 |
| `activity_physical_equipment` | 6 | 650 | 1.0850 | 4.4167 |
| `activity_digital_documentation` | 3 | 650 | 1.2833 | 4.6100 |
| `activity_interpersonal` | 8 | 650 | 1.9050 | 4.4075 |
| `activity_leadership_administration` | 9 | 650 | 1.4500 | 4.2744 |
| `context_communication` | 7 | 650 | 1.8843 | 4.6314 |
| `context_teamwork` | 2 | 650 | 1.8200 | 4.8900 |
| `context_conflict` | 3 | 650 | 1.2267 | 4.2400 |
| `context_decisions_responsibility` | 5 | 650 | 2.1600 | 4.6900 |
| `context_autonomy` | 2 | 650 | 2.4700 | 4.9950 |
| `context_precision` | 1 | 650 | 2.3200 | 5.0000 |
| `context_automation` | 1 | 650 | 1.0400 | 3.8000 |
| `context_routine_equipment_pace` | 2 | 650 | 1.2850 | 4.4200 |
| `context_pressure_competition` | 2 | 650 | 1.6400 | 4.6850 |
| `context_hazards` | 12 | 650 | 1.0525 | 4.0317 |
| `context_outdoors` | 2 | 650 | 1.0000 | 4.4350 |
| `context_indoors` | 2 | 650 | 1.3800 | 4.6500 |
| `context_vehicles` | 2 | 650 | 1.0000 | 4.4450 |
| `context_physical_activity` | 6 | 650 | 1.1267 | 4.2100 |
| `context_sitting` | 1 | 650 | 1.0600 | 4.9900 |
| `context_manual_repetition` | 2 | 650 | 1.3050 | 5.0000 |
| `context_physical_proximity` | 1 | 650 | 1.2900 | 5.0000 |
| `context_protective_equipment` | 2 | 650 | 1.0000 | 4.8450 |
| `job_zone_preparation` | 1 | 663 | 2.0000 | 5.0000 |

## Output fingerprints (SHA-256)

- `grouped_onet_features.csv`: `fb5bad85db165cab04ecf38106e7960edb24232d8a9df02e33d98efcea59b697`
- `onet_grouping_dictionary.csv`: `5303f8234d0be946e11162faca49e46d3018fa2fdcfa7736bbd830c5ecd27caf`
- `grouped_onet_coverage.csv`: `24d1466f774ae5d7ca9ef174407fabaf4f9ba8960fb7935bc296735772d82903`
