# Evaluation

Predictions are evaluated with [ml-evaluation](https://github.com/c3s-cordex-ml/ml-evaluation) (`ml-eval`), which writes its
metrics as zarr stores.

## Evaluation cases

| Case | ml-eval modes | Reference |
|---|---|---|
| `EC-Earth3-Veg_perfect_2041-2060` | fast, slow, prob, multivar | RegCM5-0 driven by EC-Earth3-Veg |
| `ERA5_perfect_1981-2000` | fast, slow, prob, multivar | RegCM5-0 driven by ERA5 |
| `ERA5_imperfect_1981-2000` | fast, slow, prob, multivar | ERA5-Land (*source TBD*) |
| `<GCM>_perfect_1981-2000_2041-2060` | signal | climate-change signal of RegCM5-0 driven by the same GCM |
| `<GCM>_imperfect_1981-2000_2041-2060` | signal | climate-change signal of RegCM5-0 driven by the same GCM |

- **fast**: RMSE, spectral error and biases of the mean, extremes and autocorrelation.
- **slow**: distribution scores and additional variable-specific biases.
- **prob**: CRPS, Brier score and spread-error ratio; only for models that produce an ensemble.
- **multivar**: correlation between pairs of variables and its bias.
- **signal**: change of each climatological index between 1981-2000 and 2041-2060. The signal cases cover EC-Earth3-Veg,
  MPI-ESM1-2-HR and NorESM2-MM with perfect predictors and MPI-ESM1-2-HR and NorESM2-MM with imperfect predictors
  (EC-Earth3-Veg will be added).

The climate-change signal of the RegCM5-0 truth is computed once and stored in `EVALUATIONS/REFERENCE/`.

## Where the outputs go

```
EVALUATIONS/
├── REFERENCE/RegCM5-0/<GCM>_1981-2000_2041-2060/
└── Experiment_<A|B|C>/
    └── <MODEL>/
        └── <case>/
            └── <season>/                       # annual, DJF, MAM, JJA, SON
                ├── <var>/metrics_<mode>_*.zarr
                └── <var1>_<var2>/metrics_mv_*.zarr
```
