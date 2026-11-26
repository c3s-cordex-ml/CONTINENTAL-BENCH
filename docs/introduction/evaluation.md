# Evaluation

Predictions are evaluated with [ml-evaluation](https://github.com/c3s-cordex-ml/ml-evaluation) (`ml-eval`), which writes its
metrics as zarr stores.

## Evaluation cases

Each [prediction experiment](experiments.md#prediction-experiments) is evaluated as one or more cases:

| Prediction experiment | Case | ml-eval modes | Reference |
|---|---|---|---|
| 1. Period transferability | `EC-Earth3-Veg_perfect_2041-2060` | fast, slow, prob, multivar | RegCM5-0 driven by EC-Earth3-Veg |
| 2a. Driver transferability, perfect | `ERA5_perfect_1981-2000` | fast, slow, prob, multivar | RegCM5-0 driven by ERA5 |
| 2b. Driver transferability, imperfect | `ERA5_imperfect_1981-2000` | fast, slow, prob, multivar | ERA5-Land (*source TBD*) |
| 3a. Period and GCM transferability, perfect | `<GCM>_perfect_1981-2000_2041-2060` | signal | climate-change signal of RegCM5-0 driven by the same GCM |
| 3b. Period and GCM transferability, imperfect | `<GCM>_imperfect_1981-2000_2041-2060` | signal | climate-change signal of RegCM5-0 driven by the same GCM |

- **fast**: RMSE, spectral error and biases of the mean, extremes and autocorrelation.
- **slow**: distribution scores and additional variable-specific biases.
- **prob**: CRPS, Brier score and spread-error ratio; only for models that produce an ensemble.
- **multivar**: correlation between pairs of variables and its bias.
- **signal**: change of each climatological index between 1981-2000 and 2041-2060. The signal cases cover EC-Earth3-Veg,
  MPI-ESM1-2-HR and NorESM2-MM with perfect predictors and MPI-ESM1-2-HR and NorESM2-MM with imperfect predictors
  (EC-Earth3-Veg will be added).


## Metrics per track

Each track writes its metrics to a set of zarr stores, per variable (or pair of variables) and season. *Map* is a field on the
EUR-12 grid, *scalar* is a single value for the whole domain. Maps of the index itself are stored for both the truth (`targ_`) and
the prediction (`pred_`) next to the bias.

| Track | Metrics | Format | Store |
|---|---|---|---|
| **fast** | RMSE; bias of the mean, standard deviation, P01, P99, lag-1 autocorrelation, annual maximum and minimum | map | `metrics_fast_field` |
| | precipitation only: bias of P98 of wet days, R01 (wet days ≥ 1 mm), SDII; relative bias of P98 wet, SDII, RX1day | map | `metrics_fast_pr_field` |
| | RMSE, RALSD (radially averaged log spectral distance), temporal LSD, raw and normalised | scalar | `metrics_fast_float` |
| | spatial power spectrum of truth and prediction, raw and normalised | spectrum (wavenumber) | `metrics_fast_psd` |
| | temporal power spectrum of truth and prediction, raw and normalised | spectrum (frequency) | `metrics_fast_tpsd` |
| **slow** | bias of the interannual standard deviation and of P90; Pearson and Spearman correlation in time; distribution scores (Wasserstein distance, PSS, FCSS, LHD) | map | `metrics_slow_field` |
| | precipitation only: bias of P90/P95/P99 of wet days, R95p, R99p, RX5day, R10, R20, CDD, CWD | map | `metrics_slow_pr_field` |
| | `tasmax` only: summer days, hot days, ice days; `tasmin` only: tropical nights, frost days | map | `metrics_slow_tasmax_field`, `metrics_slow_tasmin_field` |
| | distribution scores (Wasserstein distance, PSS, FCSS, LHD) | scalar | `metrics_slow_hist` |
| | histogram of truth and prediction | histogram | `metrics_slow_hist` |
| | spatial RMSE, Pearson and Spearman correlation | time series | `metrics_slow_series` |
| | temporal coherence between truth and prediction | spectrum (frequency) | `metrics_slow_tcoh` |
| **prob** | CRPS, Brier score (median threshold), spread-error ratio (ensembles of 2 or more members) | map, scalar | `metrics_prob_field`, `metrics_prob_float` |
| **multivar** | Pearson and Spearman correlation between the two variables and its bias; bivariate distribution scores (PSS, LHD) | map | `metrics_mv_field` |
| | bivariate distribution scores (PSS, LHD) | scalar | `metrics_mv_float` |
| | `tasmax`–`tasmin` only: maximum diurnal temperature range | map | `metrics_dtr_field` |
| **signal** | change (absolute and relative) of the mean, P01 and P99; for precipitation of R01, SDII and RX1day | map, annual series, annual cycle, scalar | `metrics_signal_field`, `_series`, `_month`, `_float` |

The list follows the current version of ml-evaluation, which is under development.
