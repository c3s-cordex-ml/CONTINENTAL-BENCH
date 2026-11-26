# Prepare your predictions

Produce one prediction for every test block and predictor type listed in [Prediction experiments](../introduction/experiments.md#prediction-experiments),
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
- **Ensembles** have **5 members**, in a dimension `member` of size 5. The variable has the dimensions
  `(member, time, rlat, rlon)`, in this order:

    ```
    float tas(member, time, rlat, rlon)
    ```

- **Deterministic models** have a single member. The variable has the dimensions `(time, rlat, rlon)`, in this order, or
  `(member, time, rlat, rlon)` with `member` of size 1.

- The same grid as the target file: the same `rlat`, `rlon`, `lat`, `lon` coordinates and grid mapping.
- One time step per day of the test block, at the same time of day as the target file (12:00). The calendar is that of the
  predictors, so it may differ from the target calendar by the 29 February days.
- No missing values.

We suggest keeping them in a tree that mirrors the evaluation one, e.g. `PREDICTIONS/Experiment_<A|B|C>/<MODEL>/<driver>/<period>/`.

## Validate your predictions

Check every prediction file with [`scripts/validate.py`](https://github.com/c3s-cordex-ml/CONTINENTAL-BENCH/blob/main/scripts/validate.py)
before evaluating it. It needs `numpy`, `xarray`, `netCDF4` and `cftime`.

1. Get the script from your clone of the repository (`git pull` to update it).
2. Run it on one prediction file, giving as `--target` the target file of the same test block and variable:

    ```bash
    python scripts/validate.py \
      PREDICTIONS/Experiment_A/UNET/MPI-ESM1-2-HR/2041-2060/tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UNET_A-imperfect_day_20410101-20601231.nc \
      --target SOURCE_FILES/test/MPI-ESM1-2-HR/2041-2060/target/tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_20410101-20601231.nc
    ```

3. Read the report. Each check prints `OK` or `FAIL`, and the last line summarises them:

    ```
    OK   variable 'tas' present
    OK   units 'K' (target 'K')
    OK   dimensions ('member', 'time', 'rlat', 'rlon') (expected ('member', 'time', 'rlat', 'rlon') or ('time', 'rlat', 'rlon'))
    OK   5 members (expected 1 or 5)
    ...
    OK   no missing values where the target has data (0 found)
    == SUMMARY tas: 0 FAIL, 15 OK
    ```

4. Fix every `FAIL` and run it again. The script exits with code 0 when all checks pass and 1 otherwise.
