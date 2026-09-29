# Task 6.5 — Coverage report

**Dataset:** [merged_v0.csv](data/datasets/processed/merged_v0.csv)  
**Reproduce:** run [task6_5.ipynb](notebooks/task6_5.ipynb) from top to bottom.  
**Scope:** local project files only; the original paper's absent occupations were not independently enumerated.

## Meeting snapshot

| Measure | Result |
| --- | --- |
| Final dataset | 798 jobs × 214 columns |
| Jobs dropped by the main left joins | 0 |
| Distinct 2018 codes across the prepared sources | 808 |
| Codes outside the chosen Eloundou base | 10 |
| Jobs with all four index score columns | 663/798 |
| Jobs present in every prepared source | 650/798 |
| Final broad job titles missing | 0 |

“All four index score columns” means AIOE, Frey–Osborne, Eloundou GPT-4 beta, and Eloundou human beta. Presence in every source is a code-coverage measure, not a claim that every feature value is nonmissing. No complete-case filtering is applied to v0.

## 1. Original-source coverage

An original job is **represented** if at least one mapped 2018 code appears in v0. Partly represented jobs are included in that count, not added to it. Counts of original jobs, expanded mapping rows, and unique 2018 codes must not be mixed.

| Source | Original reference | Available source jobs | Represented source jobs | Partly represented | Share of original reference |
| --- | --- | --- | --- | --- | --- |
| Eloundou | 923 | 923 | 923 | 0 | 100.0% |
| AIOE | 774 | 774 | 769 | 6 | 99.4% |
| Frey–Osborne | 702 | 653 | 650 | 2 | 92.6% |

Frey–Osborne's 702 is the paper-reference count recorded in the project documentation. Its supplied file has 653 jobs. Therefore 650/702 describes coverage against that reference, while 650/653 describes retention from the available source. Eloundou's original unit is an eight-digit detailed occupation; AIOE and Frey–Osborne use original six-digit 2010 jobs.

## 2. Main join funnel

Each row is a sequential left join onto the selected base. **Unmatched rows are retained, not dropped.** BLS titles are a lookup; the final coverage-flag join adds audit flags, not scores.

| Join step | Rows in | Rows matched | Unmatched rows kept | Rows dropped | Rows out |
| --- | --- | --- | --- | --- | --- |
| bls_titles | 798 | 798 | 0 | 0 | 798 |
| aioe | 798 | 790 | 8 | 0 | 798 |
| frey | 798 | 663 | 135 | 0 | 798 |
| job_zones | 798 | 798 | 0 | 0 | 798 |
| abilities | 798 | 774 | 24 | 0 | 798 |
| skills | 798 | 774 | 24 | 0 | 798 |
| work_activities | 798 | 774 | 24 | 0 | 798 |
| work_context | 798 | 774 | 24 | 0 | 798 |
| coverage flags | 798 | 798 | 0 | 0 | 798 |

Ten AIOE target codes and five Frey–Osborne target codes are outside the base; the five Frey–Osborne codes are among the ten AIOE codes. These are excluded right-side codes, not losses of the 798 left-side jobs. The full side-by-side accounting and the separate outer audit are in Appendix E.

## 3. What happened to each source

**Eloundou.** All 923/923 original detailed occupations (100.0%) contribute to the 798 broad jobs used as the v0 base. The reduction of 125 rows comes from averaging detailed occupations within the same six-digit code, not dropping jobs. The 24 groups without a .00 base entry still contribute scores; Task 6 supplied official BLS broad titles for them.

**AIOE.** 769/774 original jobs (99.4%) contribute at least one score to v0. This includes 6 partly retained splits. Of the 5 jobs contributing nothing, one is Biologists (19-1020), whose broad code has no exact crosswalk entry; the other four map only to codes outside the Eloundou base. The expanded crosswalk has 827 rows, including that unmatched row; 826 mapped rows average to 800 unique 2018 codes. Of these, 790 appear in v0 and 10 are outside the base. Thus 790/798 v0 jobs have AIOE scores; this target-code fraction is different from the original-job fraction.

**Frey–Osborne.** 650/702 paper-reference occupations (92.6%) are represented under the project data dictionary's stated 702-job reference. The supplied file contains only 653 occupations: the 49-job gap predates our joins. We used project files only, so those missing codes and the precise upstream reasons were not independently identified. Of the available jobs, 650/653 (99.5%) contribute to v0, including 2 partial splits; 3 map only to codes outside the base. The 681 expanded mapping rows average to 668 unique 2018 codes; 663 appear in v0 and five are outside the base. The 135 v0 jobs missing this score remain in the dataset.

**O*NET Job Zones.** All 923 detailed source jobs roll up to 798 broad codes, and all 798 appear in v0 (100% of source jobs; 100% of the base). No jobs are lost. Job Zone uses the base entry when available, otherwise the modal detailed value with the lower value used on a tie.

**O*NET Abilities.** All 894 detailed source jobs are represented within 774 broad source codes, and all 774 broad codes appear in v0 (100% source coverage; 97.0% of the base). The other 24 base jobs have no supplied source ratings; they are retained with blanks. Raw feature-record counts describe repeated job/element/scale measurements, not extra occupations.

**O*NET Skills.** All 894 detailed source jobs are represented within 774 broad source codes, and all 774 broad codes appear in v0 (100% source coverage; 97.0% of the base). The other 24 base jobs have no supplied source ratings; they are retained with blanks. Essential and Transferable Skills are combined into one table. Raw feature-record counts describe repeated job/element/scale measurements, not extra occupations.

**O*NET Work Activities.** All 894 detailed source jobs are represented within 774 broad source codes, and all 774 broad codes appear in v0 (100% source coverage; 97.0% of the base). The other 24 base jobs have no supplied source ratings; they are retained with blanks. Raw feature-record counts describe repeated job/element/scale measurements, not extra occupations.

**O*NET Work Context.** All 894 detailed source jobs are represented within 774 broad source codes, and all 774 broad codes appear in v0 (100% source coverage; 97.0% of the base). The other 24 base jobs have no supplied source ratings; they are retained with blanks. Raw feature-record counts describe repeated job/element/scale measurements, not extra occupations.

## 4. Interpreting the gaps

- **Base choice:** valid source codes outside Eloundou are omitted by design. They are not established as discontinued or misspelled.
- **Crosswalk granularity:** AIOE's 19-1020 cannot be matched exactly to the supplied detailed-code crosswalk. It remains separately accounted for; no replacement code is guessed.
- **Rollup:** repeated detailed jobs and repeated mapped targets were combined under the documented averaging rules. Those reductions are not reported as missing occupations.
- **Input coverage:** missing source predecessors explain the blank AIOE/Frey scores on retained jobs. The file evidence alone does not establish why every predecessor was absent upstream.
- **Two different sets of 24:** the 24 Eloundou groups formerly missing broad titles and the 24 v0 jobs absent from the O*NET rating tables have 0 codes in common. Resolving titles did not fill missing ratings.
- **No invented reasons:** we found no evidence here to classify the listed exclusions as typos or genuine discontinuations. Reasons below state observed membership facts or explicitly limited explanations.

## 5. Review and reproducibility

The notebook checks original-source accounting, saved source-presence flags, every main join's retained row count, outer-union counts, and the contributing 2010 codes recorded in v0. All checks passed when this report was generated. Task 6 separately checked 985 values/metadata fields across five selected occupations; this report does not re-claim those as newly rerun checks.

Primary local inputs: `data/datasets/occ_level.csv`, `AIOE_appendixA.xlsx`, `frey_osborne_probabilities.csv`, `eloundou_6digit.csv`, the six numeric O*NET source workbooks, and the crosswalk and prepared tables in `data/datasets/processed/`. The paper-reference counts and the pre-existing Frey–Osborne input gap are documented in [DATA-DICTIONARY.md](data/DATA-DICTIONARY.md).

## Appendices

Expand the tables below for the complete code lists. A job may appear in both a lineage table and a target-code table because those tables describe different units. Do not add their row counts together.


<details>
<summary>Appendix A — Original source jobs with no contribution to v0 (8 source/job entries)</summary>

All identifiable original source occupations excluded completely. The 49 unavailable Frey–Osborne paper jobs are not included: their individual codes were not supplied or independently checked.

| source | soc2010 | original_title | excluded_2018_codes | reason |
| --- | --- | --- | --- | --- |
| AIOE | 11-9039 | Education Administrators, All Other | 11-9039 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 19-1020 | Biologists |  | Crosswalk granularity gap: 19-1020 Biologists has no exact mapping; the supplied crosswalk lists detailed children 19-1021, 19-1022, 19-1023, and 19-1029. |
| AIOE | 27-3012 | Public Address System and Other Announcers | 27-3099 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 27-4013 | Radio Operators | 43-2099 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 47-5042 | Mine Cutting and Channeling Machine Operators | 47-5049 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| Frey–Osborne | 27-3012 | Public Address System and Other Announcers | 27-3099 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| Frey–Osborne | 27-4013 | Radio Operators | 43-2099 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| Frey–Osborne | 47-5042 | Mine Cutting and Channeling Machine Operators | 47-5049 | Mapped 2018 code(s) absent from the selected Eloundou base. |

</details>


<details>
<summary>Appendix B — Partly represented original jobs (8 source/job entries)</summary>

These jobs count as represented under the chosen rule. This lists every retained and excluded branch.

| source | soc2010 | original_title | retained_2018_codes | excluded_2018_codes | reason |
| --- | --- | --- | --- | --- | --- |
| AIOE | 25-3099 | Teachers and Instructors, All Other | 25-3031; 25-3041 | 25-3099 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 25-9041 | Teacher Assistants | 25-9042; 25-9043 | 25-9049 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 29-1067 | Surgeons | 29-1242; 29-1243 | 29-1249 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 51-9199 | Production Workers, All Other | 51-9161; 51-9162 | 51-9199 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 53-1031 | First-Line Supervisors/Managers of Transportation and Material-Moving Machine and Vehicle Operators | 53-1043; 53-1044 | 53-1049 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| AIOE | 53-7032 | Excavating and Loading Machine and Dragline Operators | 47-5022 | 53-7199 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| Frey–Osborne | 25-9041 | Teacher Assistants | 25-9042; 25-9043 | 25-9049 | Mapped 2018 code(s) absent from the selected Eloundou base. |
| Frey–Osborne | 53-7032 | Excavating and Loading Machine and Dragline Operators | 47-5022 | 53-7199 | Mapped 2018 code(s) absent from the selected Eloundou base. |

</details>


<details>
<summary>Appendix C — All 2018 codes outside the selected base (10 unique codes)</summary>

These codes appear in one or more prepared index files but not in the Eloundou base.

| 2018 SOC | Official title | Sources | Contributing 2010 codes | Reason |
| --- | --- | --- | --- | --- |
| 11-9039 | Education Administrators, All Other | AIOE | 11-9039 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 25-3099 | Teachers and Instructors, All Other | AIOE | 25-3099 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 25-9049 | Teaching Assistants, All Other | AIOE; Frey–Osborne | 25-9041 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 27-3099 | Media and Communication Workers, All Other | AIOE; Frey–Osborne | 27-3012 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 29-1249 | Surgeons, All Other | AIOE | 29-1067 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 43-2099 | Communications Equipment Operators, All Other | AIOE; Frey–Osborne | 27-4013 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 47-5049 | Underground Mining Machine Operators, All Other | AIOE; Frey–Osborne | 47-5042 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 51-9199 | Production Workers, All Other | AIOE | 51-9199 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 53-1049 | First Line Supervisors of Transportation Workers, All Other | AIOE | 53-1031 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |
| 53-7199 | Material Moving Workers, All Other | AIOE; Frey–Osborne | 53-7032 | Valid 2018 code absent from the selected Eloundou base; excluded by the left-join choice. |

</details>


<details>
<summary>Appendix D — Jobs retained in v0 with missing source coverage (148 jobs)</summary>

None of these jobs was dropped. Missing predecessor codes explain absent index coverage; absent O*NET ratings are listed as a source coverage gap.

| 2018 SOC | Official title | Missing sources | Evidence / likely reason |
| --- | --- | --- | --- |
| 11-1031 | Legislators | aioe; frey; abilities; skills; work_activities; work_context | aioe: mapped 2010 predecessor(s) absent from supplied index: 11-1031 / frey: mapped 2010 predecessor(s) absent from supplied index: 11-1031 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 11-2032 | Public Relations Managers | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 11-9171 | Funeral Home Managers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 11-9061 |
| 13-1021 | Buyers and Purchasing Agents, Farm Products | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1021 |
| 13-1022 | Wholesale and Retail Buyers, Except Farm Products | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1022 |
| 13-1023 | Purchasing Agents, Except Wholesale, Retail, and Farm Products | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1023 |
| 13-1071 | Human Resources Specialists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1071 |
| 13-1075 | Labor Relations Specialists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1075 |
| 13-1082 | Project Management Specialists | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 13-1131 | Fundraisers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 13-1131 |
| 13-2051 | Financial and Investment Analysts | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 13-2054 | Financial Risk Specialists | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 15-1212 | Information Security Analysts | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1122 |
| 15-1231 | Computer Network Support Specialists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1152 |
| 15-1232 | Computer User Support Specialists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1151 |
| 15-1241 | Computer Network Architects | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1143 |
| 15-1254 | Web Developers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1134 |
| 15-1255 | Web and Digital Interface Designers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-1134, 15-1199 |
| 15-2051 | Data Scientists | aioe; frey | aioe: mapped 2010 predecessor(s) absent from supplied index: 15-2099 / frey: mapped 2010 predecessor(s) absent from supplied index: 15-2099 |
| 15-2099 | Mathematical Science Occupations, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 15-2091, 15-2099 |
| 17-3028 | Calibration Technologists and Technicians | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 19-4044 | Hydrologic Technicians | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 21-1011 | Substance Abuse and Behavioral Disorder Counselors | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 21-1011 |
| 21-1014 | Mental Health Counselors | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 21-1014 |
| 21-1094 | Community Health Workers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 21-1094 |
| 23-1012 | Judicial Law Clerks | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 23-1012 |
| 23-1021 | Administrative Law Judges, Adjudicators, and Hearing Officers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 23-1021 |
| 23-1023 | Judges, Magistrate Judges, and Magistrates | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 23-1023 |
| 25-1011 | Business Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1011 |
| 25-1021 | Computer Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1021 |
| 25-1022 | Mathematical Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1022 |
| 25-1031 | Architecture Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1031 |
| 25-1032 | Engineering Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1032 |
| 25-1041 | Agricultural Sciences Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1041 |
| 25-1042 | Biological Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1042 |
| 25-1043 | Forestry and Conservation Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1043 |
| 25-1051 | Atmospheric, Earth, Marine, and Space Sciences Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1051 |
| 25-1052 | Chemistry Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1052 |
| 25-1053 | Environmental Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1053 |
| 25-1054 | Physics Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1054 |
| 25-1061 | Anthropology and Archeology Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1061 |
| 25-1062 | Area, Ethnic, and Cultural Studies Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1062 |
| 25-1063 | Economics Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1063 |
| 25-1064 | Geography Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1064 |
| 25-1065 | Political Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1065 |
| 25-1066 | Psychology Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1066 |
| 25-1067 | Sociology Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1067 |
| 25-1071 | Health Specialties Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1071 |
| 25-1072 | Nursing Instructors and Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1072 |
| 25-1081 | Education Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1081 |
| 25-1082 | Library Science Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1082 |
| 25-1111 | Criminal Justice and Law Enforcement Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1111 |
| 25-1112 | Law Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1112 |
| 25-1113 | Social Work Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1113 |
| 25-1121 | Art, Drama, and Music Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1121 |
| 25-1122 | Communications Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1122 |
| 25-1123 | English Language and Literature Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1123 |
| 25-1124 | Foreign Language and Literature Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1124 |
| 25-1125 | History Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1125 |
| 25-1126 | Philosophy and Religion Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1126 |
| 25-1192 | Family and Consumer Sciences Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1192 |
| 25-1193 | Recreation and Fitness Studies Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1193 |
| 25-1194 | Career/Technical Education Teachers, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1194 |
| 25-2051 | Special Education Teachers, Preschool | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-2051 |
| 25-2055 | Special Education Teachers, Kindergarten | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 25-2052 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 25-2056 | Special Education Teachers, Elementary School | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-2052 |
| 25-2059 | Special Education Teachers, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-2059 |
| 25-3031 | Substitute Teachers, Short-Term | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-3099 |
| 25-3041 | Tutors | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-3099 |
| 25-9044 | Teaching Assistants, Postsecondary | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 25-1191 |
| 27-2011 | Actors | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 27-2011 |
| 27-2031 | Dancers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 27-2031 |
| 27-2042 | Musicians and Singers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 27-2042 |
| 27-2091 | Disc Jockeys, Except Radio | aioe; frey; abilities; skills; work_activities; work_context | aioe: mapped 2010 predecessor(s) absent from supplied index: 27-2099 / frey: mapped 2010 predecessor(s) absent from supplied index: 27-2099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 27-4015 | Lighting Technicians | aioe; frey; abilities; skills; work_activities; work_context | aioe: mapped 2010 predecessor(s) absent from supplied index: 27-4099 / frey: mapped 2010 predecessor(s) absent from supplied index: 27-4099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-1128 | Exercise Physiologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1128 |
| 29-1129 | Therapists, All Other | aioe; frey | aioe: mapped 2010 predecessor(s) absent from supplied index: 29-1129 / frey: mapped 2010 predecessor(s) absent from supplied index: 29-1129 |
| 29-1141 | Registered Nurses | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1141 |
| 29-1151 | Nurse Anesthetists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1151 |
| 29-1161 | Nurse Midwives | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1161 |
| 29-1171 | Nurse Practitioners | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1171 |
| 29-1211 | Anesthesiologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1061 |
| 29-1212 | Cardiologists | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-1213 | Dermatologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1214 | Emergency Medicine Physicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1215 | Family Medicine Physicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1062 |
| 29-1216 | General Internal Medicine Physicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1063 |
| 29-1217 | Neurologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1218 | Obstetricians and Gynecologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1064 |
| 29-1221 | Pediatricians, General | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1065 |
| 29-1222 | Physicians, Pathologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1223 | Psychiatrists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1066 |
| 29-1224 | Radiologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1229 | Physicians, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1241 | Ophthalmologists, Except Pediatric | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1069 |
| 29-1242 | Orthopedic Surgeons, Except Pediatric | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1067 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-1243 | Pediatric Surgeons | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 29-1067 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-2011 | Medical and Clinical Laboratory Technologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2011 |
| 29-2012 | Medical and Clinical Laboratory Technicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2012 |
| 29-2034 | Radiologic Technologists and Technicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2034 |
| 29-2035 | Magnetic Resonance Imaging Technologists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2035 |
| 29-2036 | Medical Dosimetrists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2099 |
| 29-2042 | Emergency Medical Technicians | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-2043 | Paramedics | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-2057 | Ophthalmic Medical Technicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2057 |
| 29-2072 | Medical Records Specialists | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-2092 | Hearing Aid Specialists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-2092 |
| 29-9021 | Health Information Technologists and Medical Registrars | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 29-9092 | Genetic Counselors | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-9092 |
| 29-9093 | Surgical Assistants | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-9099 |
| 29-9099 | Healthcare Practitioners and Technical Workers, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 29-9099 |
| 31-1131 | Nursing Assistants | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 31-1014 |
| 31-1132 | Orderlies | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 31-1015 |
| 31-9097 | Phlebotomists | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 31-9097 |
| 31-9099 | Healthcare Support Workers, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 31-9099 |
| 33-1011 | First-Line Supervisors of Correctional Officers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-1011 |
| 33-1091 | First-Line Supervisors of Security Workers | aioe; frey | aioe: mapped 2010 predecessor(s) absent from supplied index: 33-1099 / frey: mapped 2010 predecessor(s) absent from supplied index: 33-1099 |
| 33-3011 | Bailiffs | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-3011 |
| 33-3012 | Correctional Officers and Jailers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-3012 |
| 33-3031 | Fish and Game Wardens | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-3031 |
| 33-9093 | Transportation Security Screeners | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-9093 |
| 33-9094 | School Bus Monitors | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 33-9099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 33-9099 | Protective Service Workers, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 33-9099 |
| 39-1013 | First-line Supervisors of Gambling Services Workers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 39-1011, 39-1012 |
| 39-1014 | First-line Supervisors of Entertainment and Recreation Workers, Except Gambling Services | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 39-4011 | Embalmers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 39-4011 |
| 39-4012 | Crematory Operators | aioe; frey; abilities; skills; work_activities; work_context | aioe: mapped 2010 predecessor(s) absent from supplied index: 39-9099 / frey: mapped 2010 predecessor(s) absent from supplied index: 39-9099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 39-4031 | Morticians, Undertakers, and Funeral Arrangers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 39-4031 |
| 39-7011 | Tour Guides and Escorts | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 39-7011 |
| 39-7012 | Travel Guides | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 39-7012 |
| 41-3091 | Sales Representatives of Services, Except Advertising, Insurance, Financial Services, and Travel | frey; abilities; skills; work_activities; work_context | frey: mapped 2010 predecessor(s) absent from supplied index: 41-3099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 45-2091 | Agricultural Equipment Operators | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 45-2091 |
| 45-2092 | Farmworkers and Laborers, Crop, Nursery, and Greenhouse | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 45-2092 |
| 45-2093 | Farmworkers, Farm, Ranch, and Aquacultural Animals | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 45-2093 |
| 45-3031 | Fishing and Hunting Workers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 45-3011, 45-3021 |
| 47-2231 | Solar Photovoltaic Installers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 47-2231 |
| 47-4091 | Segmental Pavers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 47-4091 |
| 47-4099 | Construction and Related Workers, All Other | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 47-4099 |
| 49-9081 | Wind Turbine Service Technicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 49-9081 |
| 51-2022 | Electrical and Electronic Equipment Assemblers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 51-2022 |
| 51-2023 | Electromechanical Equipment Assemblers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 51-2023 |
| 51-2092 | Team Assemblers | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 51-2092 |
| 53-1042 | First-Line Supervisors of Helpers, Laborers, and Material Movers, Hand | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 53-1021 |
| 53-1043 | First-Line Supervisors of Material-Moving Machine and Vehicle Operators | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 53-1031 |
| 53-1044 | First-line Supervisors of Passenger Attendants | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 53-3054 | Taxi Drivers | abilities; skills; work_activities; work_context | O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 53-6032 | Aircraft Service Attendants | aioe; frey; abilities; skills; work_activities; work_context | aioe: mapped 2010 predecessor(s) absent from supplied index: 53-6099 / frey: mapped 2010 predecessor(s) absent from supplied index: 53-6099 / O*NET: this broad code is absent from the supplied rating files; the upstream cause is not established. |
| 53-6041 | Traffic Technicians | frey | frey: mapped 2010 predecessor(s) absent from supplied index: 53-6041 |

</details>


<details>
<summary>Appendix E1 — Full main-join accounting</summary>

Right-side codes outside the base are not left-side rows dropped. The BLS lookup includes occupations outside the research sources.

| Join step | Rows in | Right-side codes | Rows matched | Unmatched rows kept | Rows dropped | Rows out | Right-side codes outside base |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bls_titles | 798 | 867 | 798 | 0 | 0 | 798 | 69 |
| aioe | 798 | 800 | 790 | 8 | 0 | 798 | 10 |
| frey | 798 | 668 | 663 | 135 | 0 | 798 | 5 |
| job_zones | 798 | 798 | 798 | 0 | 0 | 798 | 0 |
| abilities | 798 | 774 | 774 | 24 | 0 | 798 | 0 |
| skills | 798 | 774 | 774 | 24 | 0 | 798 | 0 |
| work_activities | 798 | 774 | 774 | 24 | 0 | 798 | 0 |
| work_context | 798 | 774 | 774 | 24 | 0 | 798 | 0 |
| coverage flags | 798 | 808 | 798 | 0 | 0 | 798 | 10 |

</details>


<details>
<summary>Appendix E2 — Every full-outer audit step</summary>

This separate audit grows to the union of all prepared source codes; it does not enlarge v0.

| Source added | Rows in | Rows matched | Existing unmatched rows kept | New source-only codes | Rows dropped | Rows out |
| --- | --- | --- | --- | --- | --- | --- |
| aioe | 798 | 790 | 8 | 10 | 0 | 808 |
| frey | 808 | 668 | 140 | 0 | 0 | 808 |
| job_zones | 808 | 798 | 10 | 0 | 0 | 808 |
| abilities | 808 | 774 | 34 | 0 | 0 | 808 |
| skills | 808 | 774 | 34 | 0 | 0 | 808 |
| work_activities | 808 | 774 | 34 | 0 | 0 | 808 |
| work_context | 808 | 774 | 34 | 0 | 0 | 808 |

</details>


<details>
<summary>Appendix E3 — Crosswalk preparation accounting</summary>

AIOE first expands to 827 rows including one unmatched row; setting aside that row and averaging repeated targets leaves 800 codes. Frey–Osborne expands to 681 rows and averages to 668 codes.

| Source | Original rows in | Original rows matched | Original rows without mapping | Rows after left crosswalk join | Unmapped rows set aside | Mapped rows before averaging | Unique 2018 codes after averaging | Unique codes outside v0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIOE | 774 | 773 | 1 | 827 | 1 | 826 | 800 | 10 |
| Frey–Osborne | 653 | 653 | 0 | 681 | 0 | 681 | 668 | 5 |

</details>


<details>
<summary>Appendix E4 — O*NET source records and occupation counts</summary>

Long-format records repeat occupations across elements and scales; they are not a denominator for job retention.

| Source | Raw records | Detailed source jobs | Broad source jobs | Broad jobs in v0 | Source jobs outside v0 |
| --- | --- | --- | --- | --- | --- |
| job_zones | 923 | 923 | 798 | 798 | 0 |
| abilities | 92976 | 894 | 774 | 774 | 0 |
| skills | 62580 | 894 | 774 | 774 | 0 |
| work_activities | 73308 | 894 | 774 | 774 | 0 |
| work_context | 297676 | 894 | 774 | 774 | 0 |

</details>


<details>
<summary>Appendix E5 — Source presence within the 798-job base</summary>

These percentages use final broad jobs as the denominator, unlike the original-source coverage table.

| Source | Jobs with source | Jobs without source | Share of v0 |
| --- | --- | --- | --- |
| eloundou | 798 | 0 | 100.0% |
| aioe | 790 | 8 | 99.0% |
| frey | 663 | 135 | 83.1% |
| job_zones | 798 | 0 | 100.0% |
| abilities | 774 | 24 | 97.0% |
| skills | 774 | 24 | 97.0% |
| work_activities | 774 | 24 | 97.0% |
| work_context | 774 | 24 | 97.0% |

</details>


<details>
<summary>Appendix E6 — Complete original-reference reconciliation</summary>

Represented + available but not represented + unavailable at input equals each original reference. Partly represented is a subset of represented.

| Source | Original reference | Available source jobs | Represented source jobs | Partly represented | Available but not represented | Unavailable at input | Share of original reference | Share of available source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Eloundou | 923 | 923 | 923 | 0 | 0 | 0 | 100.0% | 100.0% |
| AIOE | 774 | 774 | 769 | 6 | 5 | 0 | 99.4% | 99.4% |
| Frey–Osborne | 702 | 653 | 650 | 2 | 3 | 49 | 92.6% | 99.5% |

</details>
