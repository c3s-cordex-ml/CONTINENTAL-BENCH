# Worked example

!!! warning "Under development, not tested yet"
    This example has not been run end to end yet. Commands and configuration files may change.

This example trains a UNET in experiment A with [deep4production](https://github.com/SantanderMetGroup/deep4production) and
produces the predictions of the ERA5 imperfect test block, ready to be evaluated. The model is the deterministic SongUNet of
deep4production, run by CSIC: `<institution_id>` = `CSIC`, `<emulator_id>` = `UNET`.

## 1. Set up

Install deep4production following its [instructions](https://github.com/SantanderMetGroup/deep4production), clone this repository
and [download](download.md) the data of experiment A into it. All commands below run from the root of the repository:

```
CONTINENTAL-BENCH/
├── SOURCE_FILES/            # downloaded data blocks
├── AI_READY_DATASETS/       # zarr datasets (step 2)
│   └── configs/
├── templates/               # output grid (step 4)
├── CSIC-UNET/               # train.yaml, inference.yaml and outputs/ (steps 5-6)
├── PREDICTIONS/             # prediction files (step 7)
└── scripts/                 # validate.py, to_i4c.py
```

```bash
mkdir -p AI_READY_DATASETS/configs templates CSIC-UNET PREDICTIONS
```

## 2. Create the AI-ready datasets

`d4p-create` converts the NetCDF files of each block into a zarr dataset with its normalisation statistics. Experiment A needs
the perfect predictors and the targets of its two training blocks, and the predictors of the test block to predict.

`AI_READY_DATASETS/configs/UPS_EC-Earth3-Veg_1961-1980.yaml` (perfect predictors):

```yaml
date_init: 1961-01-01 12:00:00
date_end: 1980-12-31 12:00:00
freq: 1D

data:
  paths: [./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/predictors/predictors_EUR-100_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc]
  vars: [zg850, zg700, zg500, zg250, ta850, ta700, ta500, ta250, ua850, ua700, ua500, ua250,
         va850, va700, va500, va250, hus850, hus700, hus500, hus250]

output_path: ./AI_READY_DATASETS/UPS_EC-Earth3-Veg_1961-1980.zarr
overwrite: true
```

`AI_READY_DATASETS/configs/RCM_EC-Earth3-Veg_1961-1980.yaml` (targets, one file per variable):

```yaml
date_init: 1961-01-01 12:00:00
date_end: 1980-12-31 12:00:00
freq: 1D

data:
  paths:
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/uas_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/vas_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/tas_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/pr_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/hurs_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/psl_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/rsds_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/rlds_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/sfcWind_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/tasmax_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
    - ./SOURCE_FILES/train/Experiment_A/EC-Earth3-Veg/1961-1980/target/tasmin_EUR-12_EC-Earth3-Veg_historical_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19610101-19801231.nc
  vars: [uas, vas, tas, pr, hurs, psl, rsds, rlds, sfcWind, tasmax, tasmin]

output_path: ./AI_READY_DATASETS/RCM_EC-Earth3-Veg_1961-1980.zarr
overwrite: true
```

Write the same two files for the block 2080-2099 (`UPS_EC-Earth3-Veg_2080-2099.yaml`, `RCM_EC-Earth3-Veg_2080-2099.yaml`):
`1961-1980` → `2080-2099`, `historical` → `ssp370`, `19610101-19801231` → `20800101-20991130`, and
`date_init: 2080-01-01 12:00:00`, `date_end: 2099-11-30 12:00:00`.

`AI_READY_DATASETS/configs/ERA5_1981-2000.yaml` (imperfect predictors of the test block ERA5/1981-2000):

```yaml
date_init: 1981-01-01 12:00:00
date_end: 2000-12-31 12:00:00
freq: 1D

data:
  paths: [./SOURCE_FILES/test/ERA5/1981-2000/predictors/predictors_EUR-100_ERA5_evaluation_r1i1p1f1_day_19810101-20001231.nc]
  vars: [zg850, zg700, zg500, zg250, ta850, ta700, ta500, ta250, ua850, ua700, ua500, ua250,
         va850, va700, va500, va250, hus850, hus700, hus500, hus250]

output_path: ./AI_READY_DATASETS/ERA5_1981-2000.zarr
overwrite: true
```

Create the five datasets:

```bash
for c in UPS_EC-Earth3-Veg_1961-1980 UPS_EC-Earth3-Veg_2080-2099 RCM_EC-Earth3-Veg_1961-1980 RCM_EC-Earth3-Veg_2080-2099 ERA5_1981-2000; do
  d4p-create AI_READY_DATASETS/configs/$c.yaml
done
```

## 3. Inspect the datasets

```bash
d4p-inspect AI_READY_DATASETS/UPS_EC-Earth3-Veg_1961-1980.zarr
d4p-inspect AI_READY_DATASETS/RCM_EC-Earth3-Veg_1961-1980.zarr
```

Check that the predictors have 20 variables on the 52 × 104 grid and the targets 11 variables on the 412 × 424 grid. The
perfect predictors have missing values in the cells outside the RegCM5-0 domain (43 % of the grid); the training configuration
masks them (step 5).

## 4. Create the output template

The predictions take the grid of a target file. A one-day copy is enough:

```bash
python -c "import xarray as xr; xr.open_dataset('SOURCE_FILES/test/ERA5/1981-2000/target/tas_EUR-12_ERA5_evaluation_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_19810101-20001231.nc').isel(time=[0]).to_netcdf('templates/EUR-12_template.nc')"
```

## 5. Train the model

`CSIC-UNET/train.yaml`. Training uses all years of the two blocks except the validation years 1967, 1975, 2087 and 2095. The
predictor `mask` sets the cells outside the RegCM5-0 domain to zero after normalisation.

```yaml
##### GENERAL INFO #####
run_ID: CSIC-UNET
output_dir: .
overwrite: true

##### TRAINER #####
d4p_trainer:
  name: trainer_custom
  module: deep4production.core.trainers.trainer_song_unet_det

##### TRAINING DATA #####
data:
  load_in_memory: true
  training_period: [1961, 1962, 1963, 1964, 1965, 1966, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1976, 1977, 1978, 1979, 1980,
                    2080, 2081, 2082, 2083, 2084, 2085, 2086, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2096, 2097, 2098, 2099]
  validation_period: [1967, 1975, 2087, 2095]

  predictors:
    paths:
      - ./AI_READY_DATASETS/UPS_EC-Earth3-Veg_1961-1980.zarr
      - ./AI_READY_DATASETS/UPS_EC-Earth3-Veg_2080-2099.zarr
    variables: null
    normalizer:
      path_reference: ./AI_READY_DATASETS/UPS_EC-Earth3-Veg_1961-1980.zarr
      default: mean_std
      mask: ./SOURCE_FILES/mask_EUR-100_ICTP_RegCM5-0_fx.nc
    transform_to_2D: true

  predictands:
    paths:
      - ./AI_READY_DATASETS/RCM_EC-Earth3-Veg_1961-1980.zarr
      - ./AI_READY_DATASETS/RCM_EC-Earth3-Veg_2080-2099.zarr
    variables: [uas, vas, tas, pr, hurs, psl, rsds, rlds, sfcWind, tasmax, tasmin]
    normalizer:
      path_reference: ./AI_READY_DATASETS/RCM_EC-Earth3-Veg_1961-1980.zarr
      default: mean_std
      pr: std
    transform_to_2D: true

##### DATA LOADER #####
dataloader:
  batch_size: 8
  shuffle: true
  num_workers: 4

##### MODEL #####
model_info:
  saving_params:
    model_save_name: UNET
  loss_params:
    name: MseLoss
    module: deep4production.deep.loss
    kwargs:
      ignore_nans: true
  model_params:
    name: SongUNet
    module: deep4production.deep.models.unet.song_unet
    kwargs:
      in_channels: 11          # target variables
      cond_low_channels: 20    # predictor variables
      cond_high_channels: 0
      widen_in_downsample: false
      nf: 64
      ch_mult: [1, 2, 2, 2]
      num_res_blocks: 2
      attn_at_levels: [3]
      dropout: 0.1
      fir: true
      fir_kernel: [1, 3, 3, 1]
      skip_rescale: true
      progressive_input: true
      cond_upsample: nearest   # predictors upsampled to the 412 x 424 grid
      spatial_pe_freqs: 1
  training_params:
    num_epochs: 1000
    patience_early_stopping: 30
    grad_clip: 1.0
    amp: true
    pad_to_multiple: 8         # 412 x 424 -> 416 x 424
    optimizer_params:
      lr: 0.0001
    ema_decay: 0.9999
```

```bash
d4p-train CSIC-UNET/train.yaml
```

The best model on the validation years is saved as `CSIC-UNET/outputs/models/UNET_best.pt`.

## 6. Predict the test block

`CSIC-UNET/inference.yaml`, for the ERA5 imperfect predictors of 1981-2000:

```yaml
run_ID: CSIC-UNET
output_dir: .

input_data:
  paths:
    - ./AI_READY_DATASETS/ERA5_1981-2000.zarr
  years: [1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
          1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000]
  load_in_memory: true

graph: null
ensemble_size: 1               # deterministic model: one member

model_file: UNET_best.pt

d4p_downscaler:
  name: downscaler_custom
  module: deep4production.core.downscalers.downscaler_song_unet_det

saving_info:
  file: ERA5_imperfect_1981-2000.nc
  template: ./templates/EUR-12_template.nc
  formatting: null

physical_bounds:
  pr: [0, null]
  hurs: [0, 100]
  rsds: [0, null]
  rlds: [0, null]
  sfcWind: [0, null]
```

```bash
d4p-downscale CSIC-UNET/inference.yaml
```

The predictions of the 11 variables are written to `CSIC-UNET/outputs/predictions/ERA5_imperfect_1981-2000.nc`.

## 7. Write and validate the prediction files

[`scripts/to_i4c.py`](https://github.com/c3s-cordex-ml/CONTINENTAL-BENCH/blob/main/scripts/to_i4c.py) splits the output into one
file per variable and member, with the [file names](predictions.md#file-names) of the benchmark:

```bash
python scripts/to_i4c.py CSIC-UNET/outputs/predictions/ERA5_imperfect_1981-2000.nc \
  --target-dir SOURCE_FILES/test/ERA5/1981-2000/target \
  --institution CSIC --emulator UNET --training A --predictors imperfect \
  --out-dir PREDICTIONS/Experiment_A/CSIC-UNET/ERA5/1981-2000
```

Then [validate](predictions.md#validate-your-predictions) every file against its target:

```bash
for f in PREDICTIONS/Experiment_A/CSIC-UNET/ERA5/1981-2000/*.nc; do
  var=$(basename "$f" | cut -d_ -f1)
  python scripts/validate.py "$f" --target SOURCE_FILES/test/ERA5/1981-2000/target/${var}_*.nc
done
```

## 8. Predict the other test blocks

Repeat steps 2, 6 and 7 for every test block and predictor type of the
[prediction experiments](../introduction/experiments.md#test-blocks): one `d4p-create` configuration per block and predictor
file, and one inference run with its `input_data`, `years` and `saving_info.file`. Use `--predictors perfect` in
`to_i4c.py` for the perfect predictors.

## 9. Keep the configuration files

`CSIC-UNET/train.yaml` and `CSIC-UNET/inference.yaml` are the files of
`REPRODUCIBILITY/Experiment_A/CSIC-UNET/` (see [Reproducibility](reproducibility.md)).
