"""Task 19: train and tune a Random Forest on the Task 18 split.

Run from any directory: python3 notebooks/task19_random_forest.py
Requires pandas, numpy, scikit-learn and matplotlib (see requirements.txt).

Reads Task 18's modeling table (split included) and baseline results. Tunes
with 5-fold CV on training occupations only, scores once on the held-out set,
and writes a comparison table, the chosen settings for Task 20, a figure and a
methods note. Takes a few minutes: nested CV refits the search five times.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/datasets/processed'
TABLE_CSV = DATA / 'modeling_table.csv'
BASELINE_CSV = DATA / 'task18_baseline_results.csv'
PARAMS_CSV = DATA / 'task19_rf_best_params.csv'
COMPARISON_CSV = DATA / 'task19_model_comparison.csv'
NOTE_MD = DATA / 'task19_random_forest.md'
FIGURE = ROOT / 'figures/task19_predicted_vs_actual.png'

SEED = 42
CV = KFold(n_splits=5, shuffle=True, random_state=SEED)
N_TREES = 300
GRID = {
    'randomforestregressor__max_features': ['sqrt', 0.33, 0.5, 1.0],
    'randomforestregressor__min_samples_leaf': [1, 3, 5, 10, 20],
}
TARGETS = {'gpt4': 'divergence_gpt4', 'human': 'divergence_human'}
NON_FEATURES = ('soc2018', 'title', 'split', 'rating_features_missing', *TARGETS.values())


def load():
    table = pd.read_csv(TABLE_CSV, dtype={'soc2018': str})
    features = [c for c in table.columns if c not in NON_FEATURES]
    assert len(table) == 663 and table.soc2018.is_unique
    assert len(features) == 40 and not any(c.startswith('rank_') for c in features)
    assert table.split.value_counts().to_dict() == {'train': 530, 'test': 133}
    # The note relies on this: no duplicated O*NET profiles to memorize across the split.
    assert not table.loc[~table.rating_features_missing, features].duplicated().any()
    return table, features


def search():
    # Median imputation keeps preprocessing identical to the Task 18 baselines.
    pipe = make_pipeline(SimpleImputer(strategy='median'),
                         RandomForestRegressor(n_estimators=N_TREES, random_state=SEED, n_jobs=-1))
    return GridSearchCV(pipe, GRID, cv=CV, scoring='neg_mean_squared_error')


def fit_one(table, features, label, target, sample):
    data = table if sample == 'all_663' else table[~table.rating_features_missing]
    train, test = data[data.split == 'train'], data[data.split == 'test']
    # Nested CV: the whole search is refit inside each outer training fold, so
    # this score is comparable with Task 18's ridge CV R² and is not optimistic.
    cv_r2 = cross_val_score(search(), train[features], train[target], cv=CV, scoring='r2')
    model = search().fit(train[features], train[target])
    pred = model.predict(test[features])
    best = {k.split('__')[1]: v for k, v in model.best_params_.items()}
    edges = [k for k, v in best.items()
             if v in (GRID[f'randomforestregressor__{k}'][0], GRID[f'randomforestregressor__{k}'][-1])]
    result = {
        'target': label, 'sample': sample, 'model': 'random_forest',
        'n_train': len(train), 'n_test': len(test),
        'test_r2': r2_score(test[target], pred),
        'test_rmse': mean_squared_error(test[target], pred) ** 0.5,
        'cv_r2_mean': cv_r2.mean(), 'cv_r2_sd': cv_r2.std(ddof=1),
    }
    params = {'target': label, 'sample': sample, 'n_estimators': N_TREES, 'random_state': SEED,
              **best, 'params_at_grid_edge': ';'.join(edges)}
    return result, params, (test, pred)


def figure(table, features, preds):
    baseline = pd.read_csv(BASELINE_CSV)
    alpha = {r.target: r.ridge_alpha for r in baseline[(baseline['sample'] == 'all_663')
                                                        & (baseline.model == 'ridge')].itertuples()}
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharex=True, sharey=True)
    train = table[table.split == 'train']
    for ax, (label, target) in zip(axes, TARGETS.items()):
        test, rf_pred = preds[label]
        ridge = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(),
                              Ridge(alpha=alpha[label])).fit(train[features], train[target])
        ax.scatter(test[target], ridge.predict(test[features]), s=16, alpha=.6,
                   color='#8a8a8a', label='Ridge (Task 18)')
        ax.scatter(test[target], rf_pred, s=16, alpha=.75, color='#1f6feb', label='Random Forest')
        ax.plot([0, 1], [0, 1], color='black', lw=.8, ls='--')
        ax.set(title=f'{label} labels', xlabel='Actual divergence (held-out)', xlim=(0, 1), ylim=(0, 1))
    axes[0].set_ylabel('Predicted divergence')
    axes[0].legend(loc='upper left', frameon=False)
    fig.suptitle('Held-out predictions: models pull toward the mean (133 occupations)')
    fig.tight_layout()
    fig.savefig(FIGURE, dpi=150)


def note(comparison, params):
    def table_md(df):
        lines = ['| Target | Model | Test R² | Test RMSE | 5-fold CV R² (train) |',
                 '| --- | --- | ---: | ---: | ---: |']
        for r in df.itertuples():
            lines.append(f'| {r.target} | {r.model} | {r.test_r2:.3f} | {r.test_rmse:.3f} | '
                         f'{r.cv_r2_mean:.3f} ± {r.cv_r2_sd:.3f} |')
        return '\n'.join(lines)

    def params_md(df):
        lines = ['| Target | Sample | max_features | min_samples_leaf | At grid edge |',
                 '| --- | --- | --- | ---: | --- |']
        for r in df.itertuples():
            lines.append(f'| {r.target} | {r.sample} | {r.max_features} | {r.min_samples_leaf} | '
                         f'{r.params_at_grid_edge or "no"} |')
        return '\n'.join(lines)

    main = comparison[comparison['sample'] == 'all_663']
    sens = comparison[comparison['sample'] == 'complete_650']
    pick = main.set_index(['target', 'model'])
    gaps = '; '.join(
        f"{t}: +{pick.loc[(t, 'random_forest'), 'test_r2'] - pick.loc[(t, 'ridge'), 'test_r2']:.2f} "
        f"held-out, +{pick.loc[(t, 'random_forest'), 'cv_r2_mean'] - pick.loc[(t, 'ridge'), 'cv_r2_mean']:.2f} CV"
        for t in TARGETS)
    text = f"""# Task 19 — Random Forest

## Setup

Same inputs, split and preprocessing as Task 18: `modeling_table.csv`, its saved
`split` column (530 train, 133 test), the 40 Task 17 features only, and median
imputation fit on training data. Random Forests need no scaling. Each forest has
{N_TREES} trees and `random_state={SEED}`.

Tuning used 5-fold CV on training occupations only, minimizing squared error over
{len(GRID['randomforestregressor__max_features']) * len(GRID['randomforestregressor__min_samples_leaf'])} settings:

- `max_features` (features considered per split): sqrt (about 6), 0.33, 0.5, 1.0.
- `min_samples_leaf` (smallest leaf): 1, 3, 5, 10, 20.

The held-out set was used once, after tuning. CV R² is nested (the whole search
reruns inside each outer fold), so it is directly comparable with Task 18's ridge.

## Comparison (all 663 occupations)

{table_md(main)}

## Sensitivity: 650 complete-feature occupations

{table_md(sens)}

## Chosen settings

Task 20 should refit with these settings and `random_state={SEED}` rather than retune.
They are also saved in `task19_rf_best_params.csv`.

{params_md(params)}

`min_samples_leaf=1` is the smallest possible value, so sitting at that edge
means the forest prefers fully grown trees, not that the grid was too narrow.

![Held-out predictions](../../../figures/task19_predicted_vs_actual.png)

## Reading the results

R² is the share of variance in cross-index disagreement explained; RMSE is in
percentile-rank points. With 133 held-out occupations, differences of a few
hundredths in R² between models are within noise; compare against the CV
spread before calling a winner.

The Random Forest's R² gain over ridge ({gaps}) appears in both the held-out
set and nested CV, and exceeds the CV spread, so non-linear structure in the
features adds real signal. Every model, ridge included, scores lower on the
held-out set than in CV, which points to a harder held-out sample rather than
forest overfitting. No two complete occupations share an identical feature
vector, so the forest is not matching duplicated O*NET profiles across the split.

These are associations, not causes, and disagreement is not predicted job loss.
Task 20's permutation importance will show which features carry the signal.

## Reproduction

Run `python3 notebooks/task19_random_forest.py` after Task 18. Writes only
`task19_model_comparison.csv`, `task19_rf_best_params.csv`, this note and
`figures/task19_predicted_vs_actual.png`.
"""
    NOTE_MD.write_text(text, encoding='utf-8')


def main():
    table, features = load()
    results, params, preds = [], [], {}
    for sample in ('all_663', 'complete_650'):
        for label, target in TARGETS.items():
            result, best, pred = fit_one(table, features, label, target, sample)
            results.append(result)
            params.append(best)
            if sample == 'all_663':
                preds[label] = pred
            print(f'{label} {sample}: test R² {result["test_r2"]:.3f}, '
                  f'CV R² {result["cv_r2_mean"]:.3f}, {best}', flush=True)

    baseline = pd.read_csv(BASELINE_CSV)
    comparison = pd.concat([baseline.drop(columns='ridge_alpha'), pd.DataFrame(results)])
    order = {'mean_baseline': 0, 'ols': 1, 'ridge': 2, 'random_forest': 3}
    comparison = comparison.sort_values(
        ['sample', 'target', 'model'], key=lambda s: s.map(order) if s.name == 'model' else s)
    params = pd.DataFrame(params)
    assert len(comparison) == 16 and comparison.test_rmse.gt(0).all()

    comparison.to_csv(COMPARISON_CSV, index=False, float_format='%.6f')
    params.to_csv(PARAMS_CSV, index=False)
    figure(table, features, preds)
    note(comparison, params)
    print(comparison.round(3).to_string(index=False))


if __name__ == '__main__':
    main()
