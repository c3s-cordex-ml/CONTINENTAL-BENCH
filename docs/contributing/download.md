# Download data

Each [data block](../introduction/data.md#data-blocks) is distributed as one `.tar` file, named `<driver>_<period>.tar`
(e.g. `EC-Earth3-Veg_1961-1980.tar`), that unpacks to `<driver>/<period>/`. Download only the blocks you need: the test blocks are
shared by all experiments, and the training blocks of A are also part of B and C.

*Download URL: TBD.*

| Blocks | Needed for |
|---|---|
| `mask_EUR-100_ICTP_RegCM5-0_fx.nc` | all |
| EC-Earth3-Veg 1961-1980, 2080-2099 | A, B, C |
| EC-Earth3-Veg 2001-2014, 2015-2040, 2061-2079 | B |
| MPI-ESM1-2-HR 1961-1980, 2080-2099; NorESM2-MM 1961-1980, 2080-2099 | C |
| EC-Earth3-Veg, MPI-ESM1-2-HR, NorESM2-MM 1981-2000 and 2041-2060; ERA5 1981-2000 | test, all experiments |

```bash
URL=TBD
mkdir -p SOURCE_FILES && cd SOURCE_FILES
for B in EC-Earth3-Veg_1961-1980 EC-Earth3-Veg_2080-2099; do   # experiment A, training blocks
  wget "$URL/$B.tar" && tar -xf "$B.tar" && rm "$B.tar"
done
```

The `.nc` files are already compressed, so the archives are plain (uncompressed) tar files.
