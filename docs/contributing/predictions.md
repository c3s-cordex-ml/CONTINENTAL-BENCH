# Prepare your predictions

Produce one prediction for every test block and predictor type listed in [Prediction experiments](../introduction/experiments.md#prediction-experiments),
with one file per target variable. Predictions stay at your centre.

## File names

Prediction files follow the [Impetus4Change DRS for emulator output](https://doi.org/10.5281/zenodo.18230654), which builds on
the CORDEX-CMIP6 DRS of the target files. The guide gives the full details of the nomenclature.

```
<var>_<domain>_<driving_source_id>_<driving_experiment_id>_<driving_variant_label>_<institution_id>_<source_id>_<version_realization>_<frequency>_<start>-<end>.nc
```

with `<source_id>` = `<target_source_id>-emul-<emulator_id>-<training_id>`. For example, `tas` predicted by CorrDiff, run by
CSIC and trained in experiment A, from the imperfect MPI-ESM1-2-HR predictors of 2041-2060, member 1:

```
tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-CorrDiff-A_v1-r1_day_20410101-20601231.nc
```

| Facet | Value | Example |
|---|---|---|
| `<var>`, `<domain>`, `<driving_experiment_id>`, `<driving_variant_label>`, `<frequency>`, `<start>-<end>` | those of the target file of the same block | `tas`, `EUR-12`, `ssp370`, `r1i1p1f1`, `day`, `20410101-20601231` |
| `<driving_source_id>` | imperfect predictors: the driver of the target file; perfect predictors: `UPS-RegCM5-0-<driver>` | `MPI-ESM1-2-HR`, `UPS-RegCM5-0-MPI-ESM1-2-HR` |
| `<institution_id>` | the institution that runs the emulator | `CSIC` |
| `<target_source_id>` | the emulated regional model | `RegCM5-0` |
| `<emulator_id>` | the name of your model, with letters and digits only | `CorrDiff` |
| `<training_id>` | the training experiment | `A`, `B` or `C` |
| `<version_realization>` | `v1-r<N>`, where `<N>` is the member: `r1` to `r5` for ensembles, `r1` for deterministic models | `v1-r1` |

The same prediction with the perfect predictors:

```
tas_EUR-12_UPS-RegCM5-0-MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-CorrDiff-A_v1-r1_day_20410101-20601231.nc
```

### Participating models

The `<institution_id>` and `<emulator_id>` of the participating models, with the file name of their `tas` prediction from the
imperfect MPI-ESM1-2-HR predictors of 2041-2060, experiment A, member 1:

| Institution | `<institution_id>` | `<emulator_id>` | File name |
|---|---|---|---|
| UKMO | `UKMO` | `FlowMatching` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UKMO_RegCM5-0-emul-FlowMatching-A_v1-r1_day_20410101-20601231.nc` |
| ICTP | `ICTP` | `GNN4CD` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_ICTP_RegCM5-0-emul-GNN4CD-A_v1-r1_day_20410101-20601231.nc` |
| UiB | `UiB` | `CorrDiff` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UiB_RegCM5-0-emul-CorrDiff-A_v1-r1_day_20410101-20601231.nc` |
| UiB | `UiB` | `UNET` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UiB_RegCM5-0-emul-UNET-A_v1-r1_day_20410101-20601231.nc` |
| CSIC | `CSIC` | `CorrDiff` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-CorrDiff-A_v1-r1_day_20410101-20601231.nc` |
| CSIC | `CSIC` | `DownViT` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-DownViT-A_v1-r1_day_20410101-20601231.nc` |
| CSIC | `CSIC` | `UNET` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-UNET-A_v1-r1_day_20410101-20601231.nc` |
| UOB-CSIC | `UOB-CSIC` | `RCMGEM` | `tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UOB-CSIC_RegCM5-0-emul-RCMGEM-A_v1-r1_day_20410101-20601231.nc` |

## File contents

- One variable per file, named as in the target file (`tas`, `pr`, ...) and in the same units.
- One member per file. The variable has the dimensions `(time, rlat, rlon)`, in this order:

    ```
    float tas(time, rlat, rlon)
    ```

- The same grid as the target file: the same `rlat`, `rlon`, `lat`, `lon` coordinates and grid mapping.
- One time step per day of the test block, at the same time of day as the target file (12:00). The calendar is that of the
  predictors, so it may differ from the target calendar by the 29 February days.
- No missing values.

We suggest keeping them in a tree that mirrors the evaluation one, e.g. `PREDICTIONS/Experiment_<A|B|C>/<institution_id>-<emulator_id>/<driver>/<period>/`.

## Validate your predictions

Check every prediction file with [`scripts/validate.py`](https://github.com/c3s-cordex-ml/CONTINENTAL-BENCH/blob/main/scripts/validate.py)
before evaluating it. It needs `numpy`, `xarray`, `netCDF4` and `cftime`.

1. Get the script from your clone of the repository (`git pull` to update it).
2. Run it on one prediction file, giving as `--target` the target file of the same test block and variable:

    ```bash
    python scripts/validate.py \
      PREDICTIONS/Experiment_A/CSIC-CorrDiff/MPI-ESM1-2-HR/2041-2060/tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_CSIC_RegCM5-0-emul-CorrDiff-A_v1-r1_day_20410101-20601231.nc \
      --target SOURCE_FILES/test/MPI-ESM1-2-HR/2041-2060/target/tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_20410101-20601231.nc
    ```

3. Read the report. Each check prints `OK` or `FAIL`, and the last line summarises them:

    ```
    OK   file name follows <var>_<domain>_<driving_source_id>_..._<start>-<end>.nc
    OK   facets match the target file
    OK   target_source_id 'RegCM5-0' (target file 'RegCM5-0')
    OK   driving_source_id 'MPI-ESM1-2-HR': imperfect predictors
    OK   member r1 (expected r1 to r5)
    OK   variable 'tas' present
    OK   units 'K' (target 'K')
    OK   dimensions ('time', 'rlat', 'rlon') (expected ('time', 'rlat', 'rlon'))
    ...
    OK   no missing values where the target has data (0 found)
    == SUMMARY tas: 0 FAIL, 19 OK
    ```

4. Fix every `FAIL` and run it again. The script exits with code 0 when all checks pass and 1 otherwise.
