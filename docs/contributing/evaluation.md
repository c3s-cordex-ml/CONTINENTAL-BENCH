# Evaluate your predictions

Evaluate your predictions with [ml-evaluation](https://github.com/c3s-cordex-ml/ml-evaluation) for every case listed in
[Evaluation](../introduction/evaluation.md), and write the outputs to `EVALUATIONS/Experiment_<A|B|C>/<MODEL>/<case>/<season>/`.

*An evaluation launcher that runs all cases and creates this tree automatically is in preparation.* Until then, each case is one
`ml-eval` call per variable and season, e.g. the `fast` metrics of `tas` for the ERA5 perfect case:

```bash
ml-eval fast \
  --x0 SOURCE_FILES/ERA5/1981-2000/target/tas_EUR-12_ERA5_evaluation_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19810101-20001231.nc \
  --x1 PREDICTIONS/Experiment_A/UNET/ERA5/1981-2000/tas_EUR-12_ERA5_evaluation_r1i1p1f1_UNET_A-perfect_day_19810101-20001231.nc \
  --var tas \
  --output EVALUATIONS/Experiment_A/UNET/ERA5_perfect_1981-2000/annual/tas
```

and the climate-change signal of the same model with MPI-ESM1-2-HR imperfect predictors:

```bash
ml-eval signal \
  --hist PREDICTIONS/Experiment_A/UNET/MPI-ESM1-2-HR/1981-2000/tas_EUR-12_MPI-ESM1-2-HR_historical_r1i1p1f1_UNET_A-imperfect_day_19810101-20001231.nc \
  --fut  PREDICTIONS/Experiment_A/UNET/MPI-ESM1-2-HR/2041-2060/tas_EUR-12_MPI-ESM1-2-HR_ssp370_r1i1p1f1_UNET_A-imperfect_day_20410101-20601231.nc \
  --var tas \
  --output EVALUATIONS/Experiment_A/UNET/MPI-ESM1-2-HR_imperfect_1981-2000_2041-2060/annual/tas
```

Seasons are selected with `--season DJF` (MAM, JJA, SON); see the ml-evaluation documentation for all options.
