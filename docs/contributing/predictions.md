# Prepare your predictions

Produce one prediction for every test block and predictor type listed in [Predictions](../introduction/predictions.md),
with one file per target variable. Predictions stay at your centre.

## File names

Prediction files follow the CORDEX-CMIP6 DRS of the target files, with the regional-model facets replaced by the name of your
model, the experiment it was trained in and the predictor type:

```
<var>_EUR-12_<driver>_<experiment>_r1i1p1f1_<MODEL>_<A|B|C>-<perfect|imperfect>_day_<start>-<end>.nc
```

For example, `tas` predicted by model `UNET`, trained in experiment A, from the imperfect MPI-ESM1-2-HR predictors of 2041-2060:

```
tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UNET_A-imperfect_day_20410101-20601231.nc
```

`<driver>`, `<experiment>`, `<start>` and `<end>` are those of the target file of the same block.

## File contents

- One variable per file, named as in the target file (`tas`, `pr`, ...) and in the same units.
- The same grid as the target file: dimensions `time`, `rlat`, `rlon` and the same `rlat`, `rlon`, `lat`, `lon` coordinates and grid mapping.
- The same time axis as the target file (the NorESM2-MM blocks use a 365-day calendar).
- Ensemble models: an extra dimension `member`.

We suggest keeping them in a tree that mirrors the evaluation one, e.g. `PREDICTIONS/Experiment_<A|B|C>/<MODEL>/<driver>/<period>/`.
