# Task 15: Occupation Case Studies

Generated: 2026-11-10

## Purpose

Compare six occupations across the AIOE, Frey-Osborne, Eloundou GPT-4 beta, and Eloundou human beta measures.

**Important:** AI exposure is not predicted job loss. Frey-Osborne computerisation probabilities and modern AI exposure scores measure different constructs.

## Method

- Source: `data/datasets/processed/agreement_analysis_sample.csv`.
- Raw-score verification: `data/datasets/processed/merged_v0.csv`.
- Percentile ranks are the frozen Task 9 average-tie ranks, not recalculated ranks.
- Consensus tiers follow Task 13's approved cutoffs of 0.25, 0.50, and 0.75.
- GPT-4 consensus averages AIOE, Frey-Osborne, and GPT-4 beta percentile ranks.
- Human consensus replaces GPT-4 beta with human beta.
- Rank spread is maximum minus minimum of the three GPT-4 consensus component ranks.
- No Task 14 confidence flags are assigned.

## Compact comparison table

| Case | SOC / Occupation | Raw AIOE / FO / GPT / Human | Ranks AIOE / FO / GPT / Human | GPT tier | Human tier | GPT rank spread |
|---|---|---|---|---|---|---|
| High exposure / high agreement | 43-4041 / Credit Authorizers, Checkers, and Clerks | 1.4403 / 0.9700 / 0.6500 / 0.5750 | 0.9834 / 0.9344 / 0.9351 / 0.9103 | Very High | Very High | 0.0490 |
| Low exposure / high agreement | 49-9051 / Electrical Power-Line Installers and Repairers | -1.0814 / 0.0970 / 0.0000 / 0.0000 | 0.1719 / 0.2443 / 0.0347 / 0.0415 | Low | Low | 0.2097 |
| High exposure / contested | 19-3033 / Clinical and Counseling Psychologists | 1.4564 / 0.0047 / 0.3704 / 0.5093 | 0.9887 / 0.0354 / 0.5875 / 0.8356 | High | High | 0.9532 |
| Middle exposure / contested | 51-9111 / Packaging and Filling Machine Operators and Tenders | -0.9786 / 0.9800 / 0.0000 / 0.0750 | 0.2142 / 0.9683 / 0.0347 / 0.2376 | Medium | Medium | 0.9336 |
| GPT-4 versus human label switch | 27-2041 / Music Directors and Composers | 0.8830 / 0.0150 / 0.7105 / 0.2807 | 0.7376 / 0.1003 / 0.9548 / 0.5354 | High | Medium | 0.8544 |
| Crosswalk-sensitive occupation | 15-1243 / Database Architects | 1.2588 / 0.0300 / 0.9112 / 0.6460 | 0.8733 / 0.1606 / 0.9910 / 0.9608 | High | High | 0.8303 |

Raw values have different measurement scales. Compare percentile ranks for relative positioning, not the raw values directly.

## Six occupation profiles

### 1. Credit Authorizers, Checkers, and Clerks (43-4041)

**Case category:** High exposure / high agreement

**GPT-4 consensus:** 0.9510 (Very High)

**Human consensus:** 0.9427 (Very High)

**Component rank spread:** 0.0490

**Comparison:** The three GPT-4-based component percentile ranks are relatively close.

**Interpretation:** Credit authorizing and checking work involves information processing, accuracy, and structured administrative tasks. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 2

**Relevant O*NET context:**

- Work context contact with others: 4.88 (source column: `work_context_contact_with_others__4_c_1_a_4`)
- Work context face to face discussions with individuals and within teams: 4.70 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)
- Work activity working with computers: 4.42 (source column: `work_activity_working_with_computers__4_a_3_b_1`)
- Work activity processing information: 4.10 (source column: `work_activity_processing_information__4_a_2_a_2`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `43-4041`
- AIOE crosswalk changed: `False`
- Frey source SOC code(s): `43-4041`
- Frey crosswalk changed: `False`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '43-4041'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

### 2. Electrical Power-Line Installers and Repairers (49-9051)

**Case category:** Low exposure / high agreement

**GPT-4 consensus:** 0.1503 (Low)

**Human consensus:** 0.1526 (Low)

**Component rank spread:** 0.2097

**Comparison:** The three GPT-4-based component percentile ranks are relatively close.

**Interpretation:** Power-line installation and repair involve physical work, hazardous conditions, and outdoor environments. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 2

**Relevant O*NET context:**

- Work context outdoors exposed to all weather conditions: 5.00 (source column: `work_context_outdoors_exposed_to_all_weather_conditions__4_c_2_a_1_c`)
- Work context exposed to hazardous conditions: 4.93 (source column: `work_context_exposed_to_hazardous_conditions__4_c_2_c_1_d`)
- Work context face to face discussions with individuals and within teams: 4.91 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)
- Work context contact with others: 4.56 (source column: `work_context_contact_with_others__4_c_1_a_4`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `49-9051`
- AIOE crosswalk changed: `False`
- Frey source SOC code(s): `49-9051`
- Frey crosswalk changed: `False`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '49-9051'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

### 3. Clinical and Counseling Psychologists (19-3033)

**Case category:** High exposure / contested

**GPT-4 consensus:** 0.5372 (High)

**Human consensus:** 0.6199 (High)

**Component rank spread:** 0.9532

**Comparison:** The component percentile ranks differ substantially, indicating a contested comparison.

**Interpretation:** Psychology combines language and information tasks with interpersonal judgment and direct client care. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 5

**Relevant O*NET context:**

- Work context face to face discussions with individuals and within teams: 4.80 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)
- Skill reading comprehension: 4.75 (source column: `skill_reading_comprehension__2_a_1_a`)
- Work context contact with others: 4.52 (source column: `work_context_contact_with_others__4_c_1_a_4`)
- Skill active listening: 4.25 (source column: `skill_active_listening__2_a_1_b`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `19-3031`
- AIOE crosswalk changed: `True`
- Frey source SOC code(s): `19-3031`
- Frey crosswalk changed: `True`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '19-3033'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

### 4. Packaging and Filling Machine Operators and Tenders (51-9111)

**Case category:** Middle exposure / contested

**GPT-4 consensus:** 0.4057 (Medium)

**Human consensus:** 0.4734 (Medium)

**Component rank spread:** 0.9336

**Comparison:** The component percentile ranks differ substantially, indicating a contested comparison.

**Interpretation:** Packaging-machine work can have high traditional automation potential while receiving low scores for modern language-model exposure. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 2

**Relevant O*NET context:**

- Work context pace determined by speed of equipment: 4.60 (source column: `work_context_pace_determined_by_speed_of_equipment__4_c_3_d_3`)
- Work context spend time using your hands to handle control or feel objects tools or controls: 4.55 (source column: `work_context_spend_time_using_your_hands_to_handle_control_or_feel_objects_tools_or_controls__4_c_2_d_1_g`)
- Work context contact with others: 4.40 (source column: `work_context_contact_with_others__4_c_1_a_4`)
- Work context face to face discussions with individuals and within teams: 4.18 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `51-9111`
- AIOE crosswalk changed: `False`
- Frey source SOC code(s): `51-9111`
- Frey crosswalk changed: `False`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '51-9111'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

### 5. Music Directors and Composers (27-2041)

**Case category:** GPT-4 versus human label switch

**GPT-4 consensus:** 0.5975 (High)

**Human consensus:** 0.4578 (Medium)

**Component rank spread:** 0.8544

**Comparison:** The component percentile ranks differ substantially, indicating a contested comparison.

**Interpretation:** Music composition and direction involve creative tasks whose exposure may be rated differently by GPT-4 and human evaluators. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 4

**Relevant O*NET context:**

- Work activity thinking creatively: 4.48 (source column: `work_activity_thinking_creatively__4_a_2_b_2`)
- Work context face to face discussions with individuals and within teams: 4.34 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)
- Work context contact with others: 4.17 (source column: `work_context_contact_with_others__4_c_1_a_4`)
- Skill active listening: 3.88 (source column: `skill_active_listening__2_a_1_b`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `27-2041`
- AIOE crosswalk changed: `False`
- Frey source SOC code(s): `27-2041`
- Frey crosswalk changed: `False`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '27-2041'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

**Label sensitivity:** The consensus tier changes when human beta replaces GPT-4 beta.

### 6. Database Architects (15-1243)

**Case category:** Crosswalk-sensitive occupation

**GPT-4 consensus:** 0.6750 (High)

**Human consensus:** 0.6649 (High)

**Component rank spread:** 0.8303

**Comparison:** The component percentile ranks differ substantially, indicating a contested comparison.

**Interpretation:** Database architecture involves computing and information analysis. Historical SOC mappings can affect which source scores are assigned. This is a plausible task-based explanation, not a causal finding established by the indices.

**O*NET Job Zone:** 4

**Relevant O*NET context:**

- Work activity working with computers: 4.86 (source column: `work_activity_working_with_computers__4_a_3_b_1`)
- Work activity analyzing data or information: 4.58 (source column: `work_activity_analyzing_data_or_information__4_a_2_a_4`)
- Work activity processing information: 4.43 (source column: `work_activity_processing_information__4_a_2_a_2`)
- Work context face to face discussions with individuals and within teams: 4.37 (source column: `work_context_face_to_face_discussions_with_individuals_and_within_teams__4_c_1_a_2_l`)

**SOC crosswalk trace:**

- AIOE source SOC code(s): `15-1141;15-1199`
- AIOE crosswalk changed: `True`
- Frey source SOC code(s): `15-1141`
- Frey crosswalk changed: `True`

**Source trace:** All raw scores, ranks, O*NET values, and SOC mappings come from the row where `soc2018 == '15-1243'` in `agreement_analysis_sample.csv`. Raw index scores were independently checked against `merged_v0.csv`.

## Limitations

- These six cases are illustrative, not a representative sample of all occupations.
- Rank spread is descriptive and does not constitute an approved confidence flag.
- SOC crosswalk mappings can introduce aggregation or historical classification effects.
- O*NET context supports interpretation but does not prove why a model assigned its score.
- Exposure does not equal automation, displacement, unemployment, or predicted job loss.
