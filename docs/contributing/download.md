# Download data

The [data blocks](../introduction/data.md#data-blocks) are copied to your HPC with `rsync`, one directory per block
(`<driver>/<period>/`). Access is set up per centre: you will receive the `<user>` and `<host>` to use in the commands below.

Each experiment needs its training directory, the test blocks and the mask. For example, for experiment A:

```bash
mkdir -p SOURCE_FILES
rsync -avR --progress <user>@<host>:mask_EUR-100_ICTP_RegCM5-0_fx.nc :train/Experiment_A :test SOURCE_FILES/
```

For experiment B or C, replace `train/Experiment_A` by `train/Experiment_B` or `train/Experiment_C`; every experiment directory
contains all its training blocks. `-R` keeps the directory layout under `SOURCE_FILES/`. If the transfer is interrupted, run the same command again: it continues
where it stopped and skips the files already copied.
