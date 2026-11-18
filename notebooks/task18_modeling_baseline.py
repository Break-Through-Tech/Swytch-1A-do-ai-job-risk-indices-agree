"""Task 18: build the modeling table, fix the held-out split, fit baselines.

Run from any directory: python3 notebooks/task18_modeling_baseline.py
Requires pandas, numpy and scikit-learn (see requirements.txt).

Inputs (read only): Task 16 divergence targets and Task 17 grouped O*NET
features. Outputs: the modeling table with a saved train/test split that
Tasks 19 and 20 reuse, baseline results, and a methods note.
"""
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/datasets/processed'
TARGETS_CSV = DATA / 'divergence_targets.csv'
FEATURES_CSV = DATA / 'grouped_onet_features.csv'
INPUT_SHA256 = {
    TARGETS_CSV: 'e6957c44b94c0c726c47d5a3352b72dfde2762d70ec26c7ec4be96a89e5278ef',
    FEATURES_CSV: 'fb5bad85db165cab04ecf38106e7960edb24232d8a9df02e33d98efcea59b697',
}
TABLE_CSV = DATA / 'modeling_table.csv'
RESULTS_CSV = DATA / 'task18_baseline_results.csv'
NOTE_MD = DATA / 'task18_modeling_baseline.md'

SEED = 42
TEST_SIZE = 0.20
N_STRATA = 5
CV = KFold(n_splits=5, shuffle=True, random_state=SEED)
RIDGE_ALPHAS = np.logspace(-3, 4, 29)
TARGETS = {'gpt4': 'divergence_gpt4', 'human': 'divergence_human'}
LEAKY = ('rank_aioe', 'rank_fo', 'rank_elo_dv', 'rank_elo_hum')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_table():
    for path, expected in INPUT_SHA256.items():
        if sha256(path) != expected:
            raise ValueError(f'{path.name} changed upstream; investigate before modeling.')
    targets = pd.read_csv(TARGETS_CSV, dtype={'soc2018': str})
    features = pd.read_csv(FEATURES_CSV, dtype={'soc2018': str})
    feature_cols = [c for c in features.columns if c not in ('soc2018', 'title')]
    assert len(feature_cols) == 40 and len(set(feature_cols)) == 40
    assert not set(feature_cols) & set(targets.columns), 'feature/target name clash'
    assert targets.soc2018.is_unique and features.soc2018.is_unique

    table = targets[['soc2018', 'title', *TARGETS.values()]].merge(
        features.drop(columns='title'), on='soc2018', how='inner', validate='one_to_one')
    assert len(table) == len(targets) == len(features) == 663
    assert table[list(TARGETS.values())].notna().all().all()
    assert (table.title.values == features.title.values).all()

    rating_cols = [c for c in feature_cols if c != 'job_zone_preparation']
    missing = table[rating_cols].isna()
    # Rows are either complete or missing every rating composite (Task 17).
    assert (missing.all(axis=1) | ~missing.any(axis=1)).all()
    table['rating_features_missing'] = missing.all(axis=1)
    assert table.rating_features_missing.sum() == 13
    assert table.job_zone_preparation.notna().all()

    # Stratify on quintiles of the two targets' mean so both share one split.
    strata = pd.qcut(table[list(TARGETS.values())].mean(axis=1), N_STRATA, labels=False)
    train_idx, test_idx = train_test_split(
        table.index, test_size=TEST_SIZE, random_state=SEED, stratify=strata)
    table['split'] = 'train'
    table.loc[test_idx, 'split'] = 'test'
    assert len(train_idx) == 530 and len(test_idx) == 133
    return table[['soc2018', 'title', 'split', 'rating_features_missing',
                  *TARGETS.values(), *feature_cols]], feature_cols


def models():
    pre = [SimpleImputer(strategy='median'), StandardScaler()]
    ridge = GridSearchCV(make_pipeline(*pre, Ridge()), {'ridge__alpha': RIDGE_ALPHAS},
                         cv=CV, scoring='neg_mean_squared_error')
    return {
        'mean_baseline': make_pipeline(DummyRegressor(strategy='mean')),
        'ols': make_pipeline(*pre, LinearRegression()),
        'ridge': ridge,
    }


def evaluate(table, feature_cols, sample):
    rows = []
    data = table if sample == 'all_663' else table[~table.rating_features_missing]
    train, test = data[data.split == 'train'], data[data.split == 'test']
    for label, target in TARGETS.items():
        for name, model in models().items():
            cv_r2 = cross_val_score(model, train[feature_cols], train[target], cv=CV, scoring='r2')
            model.fit(train[feature_cols], train[target])
            pred = model.predict(test[feature_cols])
            alpha = model.best_params_['ridge__alpha'] if name == 'ridge' else np.nan
            if name == 'ridge':
                assert RIDGE_ALPHAS[0] < alpha < RIDGE_ALPHAS[-1], 'alpha at grid edge'
            rows.append({
                'target': label, 'sample': sample, 'model': name,
                'n_train': len(train), 'n_test': len(test),
                'test_r2': r2_score(test[target], pred),
                'test_rmse': mean_squared_error(test[target], pred) ** 0.5,
                'cv_r2_mean': cv_r2.mean(), 'cv_r2_sd': cv_r2.std(ddof=1),
                'ridge_alpha': alpha,
            })
    return rows


def check(table, feature_cols, results):
    assert not set(LEAKY) & set(table.columns)
    split = table.set_index('soc2018').split
    assert split.value_counts().to_dict() == {'train': 530, 'test': 133}
    # Rebuilding gives the identical split and results.
    again, _ = build_table()
    assert again.split.equals(table.split)
    # Target balance across the split: means within 0.03 of each other.
    for target in TARGETS.values():
        means = table.groupby('split')[target].mean()
        assert abs(means.train - means.test) < 0.03
    assert results.test_rmse.gt(0).all() and np.isfinite(results.test_r2).all()


def note(table, results):
    def fmt(df):
        lines = ['| Target | Sample | Model | Test R² | Test RMSE | 5-fold CV R² (train) | Ridge alpha |',
                 '| --- | --- | --- | ---: | ---: | ---: | ---: |']
        for r in df.itertuples():
            alpha = '' if np.isnan(r.ridge_alpha) else f'{r.ridge_alpha:.3g}'
            lines.append(f'| {r.target} | {r.sample} | {r.model} | {r.test_r2:.3f} | '
                         f'{r.test_rmse:.3f} | {r.cv_r2_mean:.3f} ± {r.cv_r2_sd:.3f} | {alpha} |')
        return '\n'.join(lines)

    miss = table[table.rating_features_missing]
    split_means = table.groupby('split')[list(TARGETS.values())].mean().round(3)
    text = f"""# Task 18 — Modeling table and baseline regression

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

One 80/20 split (seed {SEED}) is shared by both targets. It is stratified on
quintiles of the mean of the two targets, which correlate at Spearman 0.95, so
low- and high-disagreement occupations are balanced across train and test.
Target means by split:

| Split | divergence_gpt4 | divergence_human |
| --- | ---: | ---: |
| train | {split_means.loc['train', 'divergence_gpt4']} | {split_means.loc['train', 'divergence_human']} |
| test | {split_means.loc['test', 'divergence_gpt4']} | {split_means.loc['test', 'divergence_human']} |

The 13 occupations without rating features fall {int((miss.split == 'train').sum())} in train and
{int((miss.split == 'test').sum())} in test.

## Models and preprocessing

All preprocessing is fit on training data only, inside each pipeline and CV fold:
median imputation, then standardization. Job Zone is treated as a numeric ordinal.

- `mean_baseline`: predicts the training mean; the no-signal reference.
- `ols`: ordinary least squares on all 40 features.
- `ridge`: L2-penalized regression; alpha chosen by 5-fold CV on training data
  over {len(RIDGE_ALPHAS)} log-spaced values from 0.001 to 10,000.

Test R² and RMSE are measured once on the 133 held-out occupations. The 5-fold
CV R² on training data (mean ± SD) shows how stable the scores are.

## Results (all 663 occupations, median imputation)

{fmt(results[results['sample'] == 'all_663'])}

## Sensitivity: 650 complete-feature occupations

Same split, with the 13 Job-Zone-only occupations removed from both train and test.

{fmt(results[results['sample'] == 'complete_650'])}

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
"""
    NOTE_MD.write_text(text, encoding='utf-8')


def main():
    table, feature_cols = build_table()
    results = pd.DataFrame(evaluate(table, feature_cols, 'all_663')
                           + evaluate(table, feature_cols, 'complete_650'))
    check(table, feature_cols, results)
    table.to_csv(TABLE_CSV, index=False)
    results.to_csv(RESULTS_CSV, index=False, float_format='%.6f')
    pd.testing.assert_frame_equal(
        pd.read_csv(TABLE_CSV, dtype={'soc2018': str}), table, check_dtype=False)
    note(table, results)
    print(results.round(3).to_string(index=False))


if __name__ == '__main__':
    main()
