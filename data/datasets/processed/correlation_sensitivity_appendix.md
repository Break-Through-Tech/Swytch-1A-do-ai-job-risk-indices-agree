# Task 10 — Rank-correlation results and sensitivity appendix

Input: `agreement_analysis_sample.csv`; SHA-256: `7f0c606895d080d913ed147c8436a60ea61cafeebd1dfe3a9bba907509f782ee`.

## Methods

All runs use exactly the same 663 unique six-digit 2018 SOC occupations from Task 9. Beta uses the saved percentile ranks. Alpha/gamma are ranked within these same occupations using ascending average ranks divided by 663. No imputation, employment weighting, or pair-specific row deletion is performed. Missing sensitivity scores stop execution.

Spearman rho compares ranked positions; Kendall tau-b adjusts for ties. Each full matrix is symmetric with a diagonal of 1. Each pair has n = 663. The signed label difference is human minus GPT-4. A positive difference means the human coefficient is more positive; it does not necessarily mean stronger agreement when a coefficient is negative.

## Headline beta coefficients

| method | index_x | index_y | gpt4 | human | human_minus_gpt4 |
| --- | --- | --- | --- | --- | --- |
| kendall | aioe | eloundou | 0.6632 | 0.6712 | 0.0079 |
| kendall | aioe | frey_osborne | -0.2491 | -0.2491 | 0.0000 |
| kendall | frey_osborne | eloundou | -0.1828 | -0.2334 | -0.0506 |
| spearman | aioe | eloundou | 0.8628 | 0.8669 | 0.0041 |
| spearman | aioe | frey_osborne | -0.3678 | -0.3678 | 0.0000 |
| spearman | frey_osborne | eloundou | -0.2670 | -0.3401 | -0.0731 |

AIOE and Eloundou beta show a strong positive association: Spearman rho is 0.8628 for GPT-4 and 0.8669 for human labels. The label-source change is small (+0.0041). Frey–Osborne has a negative association with AIOE (-0.3678) and with Eloundou beta (-0.2670 for GPT-4; -0.3401 for human labels). Kendall tau-b gives the same directions in the headline runs.

Coefficients near +1 indicate similar ordering; near zero little consistent ordering; near −1 opposite ordering. Frey–Osborne estimates computerisation probability, while AIOE and Eloundou measure different forms of exposure. A negative relationship does not by itself establish a data error or show that either study is wrong.

## Sensitivity coefficient changes

All rows below also have n = 663. Change from beta is the alpha/gamma coefficient minus the beta coefficient for the same label source, method, and index pair.

| variant | label_source | method | index_x | index_y | coefficient | beta_coefficient | change_from_beta | human_minus_gpt4 | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| alpha | gpt4 | spearman | aioe | frey_osborne | -0.3678 | -0.3678 | 0.0000 | 0.0000 | 663 |
| alpha | gpt4 | spearman | aioe | eloundou | 0.4291 | 0.8628 | -0.4337 | 0.3157 | 663 |
| alpha | gpt4 | spearman | frey_osborne | eloundou | 0.0290 | -0.2670 | 0.2960 | -0.3390 | 663 |
| alpha | gpt4 | kendall | aioe | frey_osborne | -0.2491 | -0.2491 | 0.0000 | 0.0000 | 663 |
| alpha | gpt4 | kendall | aioe | eloundou | 0.3056 | 0.6632 | -0.3576 | 0.2444 | 663 |
| alpha | gpt4 | kendall | frey_osborne | eloundou | 0.0192 | -0.1828 | 0.2020 | -0.2386 | 663 |
| alpha | human | spearman | aioe | frey_osborne | -0.3678 | -0.3678 | 0.0000 | 0.0000 | 663 |
| alpha | human | spearman | aioe | eloundou | 0.7448 | 0.8669 | -0.1222 | 0.3157 | 663 |
| alpha | human | spearman | frey_osborne | eloundou | -0.3099 | -0.3401 | 0.0302 | -0.3390 | 663 |
| alpha | human | kendall | aioe | frey_osborne | -0.2491 | -0.2491 | 0.0000 | 0.0000 | 663 |
| alpha | human | kendall | aioe | eloundou | 0.5500 | 0.6712 | -0.1212 | 0.2444 | 663 |
| alpha | human | kendall | frey_osborne | eloundou | -0.2194 | -0.2334 | 0.0140 | -0.2386 | 663 |
| gamma | gpt4 | spearman | aioe | frey_osborne | -0.3678 | -0.3678 | 0.0000 | 0.0000 | 663 |
| gamma | gpt4 | spearman | aioe | eloundou | 0.8819 | 0.8628 | 0.0191 | -0.0153 | 663 |
| gamma | gpt4 | spearman | frey_osborne | eloundou | -0.3080 | -0.2670 | -0.0410 | -0.0304 | 663 |
| gamma | gpt4 | kendall | aioe | frey_osborne | -0.2491 | -0.2491 | 0.0000 | 0.0000 | 663 |
| gamma | gpt4 | kendall | aioe | eloundou | 0.6917 | 0.6632 | 0.0285 | -0.0176 | 663 |
| gamma | gpt4 | kendall | frey_osborne | eloundou | -0.2061 | -0.1828 | -0.0233 | -0.0250 | 663 |
| gamma | human | spearman | aioe | frey_osborne | -0.3678 | -0.3678 | 0.0000 | 0.0000 | 663 |
| gamma | human | spearman | aioe | eloundou | 0.8666 | 0.8669 | -0.0004 | -0.0153 | 663 |
| gamma | human | spearman | frey_osborne | eloundou | -0.3383 | -0.3401 | 0.0018 | -0.0304 | 663 |
| gamma | human | kendall | aioe | frey_osborne | -0.2491 | -0.2491 | 0.0000 | 0.0000 | 663 |
| gamma | human | kendall | aioe | eloundou | 0.6741 | 0.6712 | 0.0030 | -0.0176 | 663 |
| gamma | human | kendall | frey_osborne | eloundou | -0.2311 | -0.2334 | 0.0023 | -0.0250 | 663 |

## Full alpha matrices

### gpt4 alpha — spearman, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.3678 | 0.4291 |
| frey_osborne | -0.3678 | 1.0000 | 0.0290 |
| eloundou | 0.4291 | 0.0290 | 1.0000 |

### gpt4 alpha — kendall, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.2491 | 0.3056 |
| frey_osborne | -0.2491 | 1.0000 | 0.0192 |
| eloundou | 0.3056 | 0.0192 | 1.0000 |

### human alpha — spearman, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.3678 | 0.7448 |
| frey_osborne | -0.3678 | 1.0000 | -0.3099 |
| eloundou | 0.7448 | -0.3099 | 1.0000 |

### human alpha — kendall, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.2491 | 0.5500 |
| frey_osborne | -0.2491 | 1.0000 | -0.2194 |
| eloundou | 0.5500 | -0.2194 | 1.0000 |

## Full gamma matrices

### gpt4 gamma — spearman, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.3678 | 0.8819 |
| frey_osborne | -0.3678 | 1.0000 | -0.3080 |
| eloundou | 0.8819 | -0.3080 | 1.0000 |

### gpt4 gamma — kendall, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.2491 | 0.6917 |
| frey_osborne | -0.2491 | 1.0000 | -0.2061 |
| eloundou | 0.6917 | -0.2061 | 1.0000 |

### human gamma — spearman, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.3678 | 0.8666 |
| frey_osborne | -0.3678 | 1.0000 | -0.3383 |
| eloundou | 0.8666 | -0.3383 | 1.0000 |

### human gamma — kendall, n = 663

| index | aioe | frey_osborne | eloundou |
| --- | --- | --- | --- |
| aioe | 1.0000 | -0.2491 | 0.6741 |
| frey_osborne | -0.2491 | 1.0000 | -0.2311 |
| eloundou | 0.6741 | -0.2311 | 1.0000 |

## Sensitivity summary

The largest absolute coefficient change from beta among pairs involving Eloundou is 0.4337: gpt4 alpha, spearman, aioe versus eloundou changes from 0.8628 to 0.4291. AIOE–Frey–Osborne is unchanged in all runs because neither score depends on the Eloundou label source or variant.

GPT-4 alpha gives a weaker AIOE association (Spearman 0.4291) than GPT-4 beta (0.8628). GPT-4 alpha versus Frey–Osborne is near zero (0.0290), compared with the negative beta result (-0.2670). The size, and in this case the sign, of a correlation can depend on the Eloundou measure. Alpha/gamma are alternative definitions, not new occupation samples; do not generalize the beta findings to every variant.

## Outputs and reproduction

Run `notebooks/task10.ipynb` from top to bottom from the repository root or `notebooks/`, using `requirements.txt`. Re-running replaces Task 10 outputs.

- `data/datasets/processed/pairwise_correlations.csv`: 36 rows; three unique pairs × two methods × two label sources × three variants. Full precision is retained; the tables in this appendix are rounded to four decimals.

- `figures/task10_gpt4_beta_heatmaps.png` and `figures/task10_human_beta_heatmaps.png`: two panels each, labeled Spearman/Kendall.

- This appendix records full alpha/gamma matrices, label-source differences, and changes from the beta headline results. The full beta matrices are also displayed below in the notebook.

Validated with pandas 2.3.3 and SciPy 1.13.1.

## Limits

These are descriptive correlations, not significance tests or causal evidence. The analysis applies to the 663 occupations with complete index coverage. Original code-vintage, crosswalk, source-coverage, and measurement differences remain. Percentile ranks and exposure scores are not probabilities of job loss.
