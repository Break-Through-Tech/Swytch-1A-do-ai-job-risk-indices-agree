# Task 18 — Modeling table and baseline regression

## Modeling table

`modeling_table.csv` joins Task 16's targets to Task 17's 40 grouped O*NET
features one-to-one on `soc2018` (663 occupations, none dropped). Columns:

| Columns | Meaning |
| --- | --- |
| `soc2018`, `title` | Join key (load as text) and title; not predictors |
| `split` | `train` (530) or `test` (133); Tasks 19 and 20 must reuse it |
| `rating_features_missing` | Audit flag for the 13 occupations with only Job Zone; not a predictor |
| `divergence_gpt4`, `divergence_human` | Continuous targets from Task 16 |
| 40 feature columns | Task 17 predictors, unchanged; the only model inputs |

Rank columns, consensus fields and coverage audit fields are excluded to avoid
leaking the target.

## Held-out split

One 80/20 split (seed 42) is shared by both targets. It is stratified on
quintiles of the mean of the two targets, which correlate at Spearman 0.95, so
low- and high-disagreement occupations are balanced across train and test.
Target means by split:

| Split | divergence_gpt4 | divergence_human |
| --- | ---: | ---: |
| train | 0.467 | 0.472 |
| test | 0.468 | 0.465 |

The 13 occupations without rating features fall 12 in train and
1 in test.

## Models and preprocessing

All preprocessing is fit on training data only, inside each pipeline and CV fold:
median imputation, then standardization. Job Zone is treated as a numeric ordinal.

- `mean_baseline`: predicts the training mean; the no-signal reference.
- `ols`: ordinary least squares on all 40 features.
- `ridge`: L2-penalized regression; alpha chosen by 5-fold CV on training data
  over 29 log-spaced values from 0.001 to 10,000.

Test R² and RMSE are measured once on the 133 held-out occupations. The 5-fold
CV R² on training data (mean ± SD) shows how stable the scores are.

## Results (all 663 occupations, median imputation)

| Target | Sample | Model | Test R² | Test RMSE | 5-fold CV R² (train) | Ridge alpha |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| gpt4 | all_663 | mean_baseline | -0.000 | 0.213 | -0.011 ± 0.015 |  |
| gpt4 | all_663 | ols | 0.152 | 0.196 | 0.303 ± 0.035 |  |
| gpt4 | all_663 | ridge | 0.195 | 0.191 | 0.305 ± 0.042 | 17.8 |
| human | all_663 | mean_baseline | -0.001 | 0.215 | -0.009 ± 0.008 |  |
| human | all_663 | ols | 0.178 | 0.195 | 0.279 ± 0.052 |  |
| human | all_663 | ridge | 0.208 | 0.191 | 0.291 ± 0.057 | 17.8 |

## Sensitivity: 650 complete-feature occupations

Same split, with the 13 Job-Zone-only occupations removed from both train and test.

| Target | Sample | Model | Test R² | Test RMSE | 5-fold CV R² (train) | Ridge alpha |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| gpt4 | complete_650 | mean_baseline | -0.000 | 0.214 | -0.011 ± 0.014 |  |
| gpt4 | complete_650 | ols | 0.152 | 0.197 | 0.271 ± 0.137 |  |
| gpt4 | complete_650 | ridge | 0.195 | 0.192 | 0.281 ± 0.116 | 17.8 |
| human | complete_650 | mean_baseline | -0.002 | 0.216 | -0.005 ± 0.006 |  |
| human | complete_650 | ols | 0.178 | 0.195 | 0.260 ± 0.133 |  |
| human | complete_650 | ridge | 0.215 | 0.191 | 0.271 ± 0.105 | 31.6 |

## Reading the results

R² is the share of variance in cross-index disagreement explained by O*NET
features; RMSE is in percentile-rank points (0.10 = 10 points). A model is only
useful if it beats `mean_baseline`. These are associations, not causes, and
disagreement is not predicted job loss. AIOE is built from O*NET abilities, so
some signal may reflect how that index was constructed (see Task 17 note).

## Reproduction

Run `python3 notebooks/task18_modeling_baseline.py`. The script stops if
either input's SHA-256 changes, then checks the one-to-one join, 663 rows,
40 features, no leaked rank columns, the 530/133 split, a deterministic rebuild,
target balance across the split, and that ridge alpha is not at a grid edge.
It writes only `modeling_table.csv`, `task18_baseline_results.csv` and this note.
