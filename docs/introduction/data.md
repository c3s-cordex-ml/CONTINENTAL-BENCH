# Data

## Regional simulations

The targets come from the **ICTP RegCM5-0** simulations over the **EUR-12** domain (rotated pole, 0.11°, 412 × 424 grid points),
produced within CORDEX-CORE-CMIP6. Four runs are used:

| Driver | Experiments | Variant | Calendar |
|---|---|---|---|
| EC-Earth3-Veg | historical, ssp370 | r1i1p1f1 | proleptic Gregorian (ssp370 ends 2099-11-30) |
| MPI-ESM1-2-HR | historical, ssp370 | r1i1p1f1 | proleptic Gregorian |
| NorESM2-MM | historical, ssp370 | r1i1p1f1 | 365-day (no leap years) |
| ERA5 | evaluation | r1i1p1f1 | proleptic Gregorian |

## Variables

All fields are daily.

**Predictors (20):** geopotential height `zg`, air temperature `ta`, eastward and northward wind `ua`, `va`, and specific humidity
`hus`, each at 850, 700, 500 and 250 hPa (e.g. `ta850`). They cover a regular 1° box, 104 × 52 cells, with cell centres from
42.5°W to 60.5°E and from 19.5°N to 70.5°N.

**Targets (11):** `uas`, `vas`, `tas`, `pr`, `hurs`, `psl`, `rsds`, `rlds`, `sfcWind`, `tasmax`, `tasmin`, on the native EUR-12 grid
and in the units of the RegCM5-0 output (e.g. `pr` in kg m-2 s-1).

## Perfect and imperfect predictors

The same 20 predictors exist in two versions:

- **Perfect**: RegCM5-0 itself, upscaled to the 1° grid (*UPS-RegCM*). Predictors and targets come from the same simulation, so
  only the downscaling step has to be learned. Models are always **trained** on perfect predictors.
- **Imperfect**: the driving model, interpolated to the same 1° grid: the CMIP6 GCM for the GCM-driven runs, and the ERA5
  reanalysis for the evaluation run. This is the operational setting, in which the emulator is applied to a GCM or reanalysis it
  has never seen as predictor.

The 1° box is larger than the rotated EUR-12 domain. In the **perfect** predictors the cells outside the RegCM5-0 domain are set
to NaN (43 % of the box); the file `mask_EUR-100_ICTP_RegCM5-0_fx.nc` marks the valid cells. The **imperfect** predictors are
delivered as full fields; apply the same mask at inference if your model needs it.

## Data blocks

The data are organised in **blocks**, one per driver and period, so that every file exists only once and every experiment
is a list of blocks. A block never mixes historical and scenario years (the split is at 2014/2015).

```
SOURCE_FILES/
├── mask_EUR-100_ICTP_RegCM5-0_fx.nc
├── <driver>/
│   └── <period>/
│       ├── predictors/
│       │   ├── predictors_EUR-100_<driver>_<experiment>_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_<start>-<end>.nc   # perfect
│       │   └── predictors_EUR-100_<driver>_<experiment>_r1i1p1f1_day_<start>-<end>.nc                       # imperfect
│       └── target/
│           └── <var>_EUR-12_<driver>_<experiment>_r1i1p1f1_ICTP_RegCM5-0_v1-r1_day_<start>-<end>.nc        # one per variable
```

File names follow the CORDEX-CMIP6 data reference syntax (DRS). The perfect predictors keep the RegCM5-0 facets because they are
RegCM5-0 output on the 1° `EUR-100` grid; the imperfect predictors drop them because no regional model is involved.

| Block | Predictors | Used for |
|---|---|---|
| EC-Earth3-Veg/1961-1980 | perfect | training A, B, C |
| EC-Earth3-Veg/1981-2000 | perfect | test (historical) |
| EC-Earth3-Veg/2001-2014 | perfect | training B |
| EC-Earth3-Veg/2015-2040 | perfect | training B |
| EC-Earth3-Veg/2041-2060 | perfect, imperfect | test (mid-century) |
| EC-Earth3-Veg/2061-2079 | perfect | training B |
| EC-Earth3-Veg/2080-2099 | perfect | training A, B, C |
| MPI-ESM1-2-HR/1961-1980 | perfect | training C |
| MPI-ESM1-2-HR/1981-2000 | perfect, imperfect | test (historical) |
| MPI-ESM1-2-HR/2041-2060 | perfect, imperfect | test (mid-century) |
| MPI-ESM1-2-HR/2080-2099 | perfect | training C |
| NorESM2-MM/1961-1980 | perfect | training C |
| NorESM2-MM/1981-2000 | perfect, imperfect | test (historical) |
| NorESM2-MM/2041-2060 | perfect, imperfect | test (mid-century) |
| NorESM2-MM/2080-2099 | perfect | training C |
| ERA5/1981-2000 | perfect, imperfect | test (evaluation) |

The imperfect predictors of `EC-Earth3-Veg/1981-2000` will be added once the CMIP6 historical fields of EC-Earth3-Veg are available.
The complete definition of blocks and experiments is in `experiments.yaml` at the root of the repository.
