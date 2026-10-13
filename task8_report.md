# Task 8 — Per-index EDA and percentile ranks

Input: `data/datasets/processed/merged_v0.csv` (798 distinct 2018 SOC occupations).
Higher scores and ranks mean more exposed or automatable within each measure.
Missing scores remain blank. Ties receive their average rank; percentile = rank / nonmissing count.
These measures have different meanings, so raw score magnitudes are not compared across indices.

## Summary

| Score | N | Missing | Min | P25 | Median | P75 | Max | Mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AIOE | 790 | 8 | -2.670 | -0.835 | 0.032 | 1.014 | 1.528 | 0.028 |
| Frey–Osborne probability | 663 | 135 | 0.003 | 0.100 | 0.640 | 0.890 | 0.990 | 0.536 |
| Eloundou GPT-4 beta | 798 | 0 | 0.000 | 0.131 | 0.329 | 0.489 | 1.000 | 0.326 |
| Eloundou human beta | 798 | 0 | 0.000 | 0.091 | 0.280 | 0.448 | 0.844 | 0.286 |

## O*NET Job Zone

Job Zone is an ordinal preparation measure, so its distribution is shown as counts rather than an exposure percentile rank.

| Zone | Jobs |
| ---: | ---: |
| 1 | 0 |
| 2 | 322 |
| 3 | 184 |
| 4 | 166 |
| 5 | 126 |


## Extreme occupations

The five lowest and highest available values per index are listed below. Ties are ordered by SOC code.

### AIOE

| End | SOC | Occupation | Score |
| --- | --- | --- | ---: |
| Low | 27-2031 | Dancers | -2.670 |
| Low | 39-9031 | Exercise Trainers and Group Fitness Instructors | -2.112 |
| Low | 47-3014 | Helpers--Painters, Paperhangers, Plasterers, and Stucco Masons | -2.045 |
| Low | 47-2171 | Reinforcing Iron and Rebar Workers | -1.971 |
| Low | 51-6021 | Pressers, Textile, Garment, and Related Materials | -1.950 |
| High | 29-9092 | Genetic Counselors | 1.528 |
| High | 13-2061 | Financial Examiners | 1.526 |
| High | 15-2011 | Actuaries | 1.516 |
| High | 13-1023 | Purchasing Agents, Except Wholesale, Retail, and Farm Products | 1.509 |
| High | 13-2031 | Budget Analysts | 1.503 |

### Frey–Osborne probability

| End | SOC | Occupation | Score |
| --- | --- | --- | ---: |
| Low | 29-1125 | Recreational Therapists | 0.003 |
| Low | 11-9161 | Emergency Management Directors | 0.003 |
| Low | 49-1011 | First-Line Supervisors of Mechanics, Installers, and Repairers | 0.003 |
| Low | 21-1023 | Mental Health and Substance Abuse Social Workers | 0.003 |
| Low | 29-1181 | Audiologists | 0.003 |
| High | 13-2053 | Insurance Underwriters | 0.990 |
| High | 13-2082 | Tax Preparers | 0.990 |
| High | 23-2093 | Title Examiners, Abstractors, and Searchers | 0.990 |
| High | 25-4031 | Library Technicians | 0.990 |
| High | 41-9041 | Telemarketers | 0.990 |

### Eloundou GPT-4 beta

| End | SOC | Occupation | Score |
| --- | --- | --- | ---: |
| Low | 27-2021 | Athletes and Sports Competitors | 0.000 |
| Low | 31-1132 | Orderlies | 0.000 |
| Low | 35-2011 | Cooks, Fast Food | 0.000 |
| Low | 35-2015 | Cooks, Short Order | 0.000 |
| Low | 35-9011 | Dining Room and Cafeteria Attendants and Bartender Helpers | 0.000 |
| High | 15-2021 | Mathematicians | 1.000 |
| High | 43-9081 | Proofreaders and Copy Markers | 0.975 |
| High | 43-4021 | Correspondence Clerks | 0.964 |
| High | 27-3092 | Court Reporters and Simultaneous Captioners | 0.958 |
| High | 15-1251 | Computer Programmers | 0.950 |

### Eloundou human beta

| End | SOC | Occupation | Score |
| --- | --- | --- | ---: |
| Low | 13-1074 | Farm Labor Contractors | 0.000 |
| Low | 27-2021 | Athletes and Sports Competitors | 0.000 |
| Low | 35-2015 | Cooks, Short Order | 0.000 |
| Low | 35-9011 | Dining Room and Cafeteria Attendants and Bartender Helpers | 0.000 |
| Low | 35-9021 | Dishwashers | 0.000 |
| High | 19-1011 | Animal Scientists | 0.844 |
| High | 19-3022 | Survey Researchers | 0.844 |
| High | 27-3091 | Interpreters and Translators | 0.840 |
| High | 43-4011 | Brokerage Clerks | 0.800 |
| High | 27-3031 | Public Relations Specialists | 0.788 |

## Initial cross-index check

AIOE vs Frey–Osborne: Spearman rho = **-0.368**, using **663** jobs with both scores. This is descriptive agreement between rankings, not agreement about job loss.

## Score trace checks

Recomputed each available merged score from its prepared input. AIOE and Frey–Osborne repeat mapped source rows are averaged, matching Task 6. These checks verify the join and rollup; the source papers' estimates are not independently validated.

- AIOE: 790 values checked; 0 mismatches.
- Frey–Osborne probability: 663 values checked; 0 mismatches.
- Eloundou GPT-4 beta: 798 values checked; 0 mismatches.
- Eloundou human beta: 798 values checked; 0 mismatches.

## Original-file spot checks of extremes

For these occupations, the merged score matches the original AIOE workbook, Frey–Osborne CSV, or Eloundou occupation CSV. Each selected occupation has one original source row.

| Score | SOC | Original value | Merged value |
| --- | --- | ---: | ---: |
| AIOE | 27-2031 | -2.669758 | -2.669758 |
| AIOE | 29-9092 | 1.527667 | 1.527667 |
| Frey–Osborne probability | 29-1125 | 0.002800 | 0.002800 |
| Frey–Osborne probability | 51-9151 | 0.990000 | 0.990000 |
| Eloundou GPT-4 beta | 27-2021 | 0.000000 | 0.000000 |
| Eloundou GPT-4 beta | 15-2021 | 1.000000 | 1.000000 |
| Eloundou human beta | 13-1074 | 0.000000 | 0.000000 |
| Eloundou human beta | 19-3022 | 0.843750 | 0.843750 |

## What this first pass shows

- The eight checked extremes match their original files, so these examples are not transcription or join errors. This does not validate the research estimates themselves.
- Frey–Osborne is missing for 135 of the 798 merged jobs. The correlation uses the 663 jobs with both scores and should not be generalized to the missing jobs.
- AIOE and Frey–Osborne rank these shared jobs differently: their Spearman correlation is negative. This is plausible because AIOE measures AI exposure while Frey–Osborne estimates computerisation probability; it is not evidence that either source is wrong.
- The highest occupations differ by measure: Genetic Counselors lead AIOE, Photographic Process Workers are among the Frey–Osborne maximum ties, Mathematicians lead GPT-4 beta, and Survey Researchers tie at the top of human beta. The full extreme lists above make those differences reviewable.
- Job Zone is the available O*NET summary measure used here. The many individual O*NET ability, skill, activity, and context features are reserved for the later grouped-feature modeling task.

## Reproduce

Run `python notebooks/task8_eda_ranks.py` from the repository root. Outputs are `task8_ranked.csv`, this report, and four SVG histograms in `figures/`.
