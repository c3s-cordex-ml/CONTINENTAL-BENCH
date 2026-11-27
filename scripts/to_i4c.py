#!/usr/bin/env python
"""Split a multi-variable prediction file into CONTINENTAL-BENCH prediction files: one file per variable and member, named
after the Impetus4Change DRS for emulator output (https://doi.org/10.5281/zenodo.18230654).

Usage:
    python to_i4c.py <prediction.nc> --target-dir <SOURCE_FILES/test/<driver>/<period>/target> \\
        --institution <institution_id> --emulator <emulator_id> --training <A|B|C> --predictors <perfect|imperfect> \\
        --out-dir <directory>

The input file holds the predicted variables with dimensions (member, time, rlat, rlon) or (time, rlat, rlon), as written by
e.g. `d4p-downscale`. For each variable, the target file of the same name in --target-dir gives the facets of the output file
name (domain, driver, experiment, variant, frequency, dates) and the grid information copied to the output (rlat, rlon, lat,
lon coordinates, grid mapping and, if missing, units). Members are written as r1, r2, ... in the order of the `member`
dimension.

Requirements: xarray, netCDF4.
"""
import argparse
import glob
import os
import re
import sys

import xarray as xr

ENCODING = {"zlib": True, "complevel": 1, "dtype": "float32"}
# CORDEX-CMIP6 DRS of the target files:
# <var>_<domain>_<driver>_<experiment>_<variant>_<institution>_<rcm>_<version>_<frequency>_<start>-<end>.nc
TARGET_FACETS = ("var", "domain", "driver", "experiment", "variant", "institution", "rcm", "version", "frequency", "dates")


def target_file(target_dir, var):
    files = sorted(glob.glob(os.path.join(target_dir, f"{var}_*.nc")))
    if len(files) != 1:
        raise FileNotFoundError(f"expected one target file for '{var}' in {target_dir}, found {len(files)}")
    parts = os.path.basename(files[0])[:-3].split("_")
    if len(parts) != len(TARGET_FACETS):
        raise ValueError(f"{files[0]} does not follow the CORDEX-CMIP6 DRS")
    return files[0], dict(zip(TARGET_FACETS, parts))


def with_target_grid(da, targ, var):
    """Give the prediction the coordinates, grid mapping and units of the target variable."""
    t = targ[var]
    da = da.assign_coords({c: targ[c] for c in ("rlat", "rlon", "lat", "lon") if c in targ.coords})
    out = da.to_dataset(name=var)
    gm = t.attrs.get("grid_mapping")
    if gm and gm in targ.variables:
        out[gm] = targ[gm]
        out[var].attrs["grid_mapping"] = gm
    for key in ("units", "standard_name", "long_name"):
        if key in t.attrs and key not in out[var].attrs:
            out[var].attrs[key] = t.attrs[key]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prediction", help="multi-variable prediction file")
    parser.add_argument("--target-dir", required=True, help="target directory of the same test block")
    parser.add_argument("--institution", required=True, help="institution_id, e.g. CSIC")
    parser.add_argument("--emulator", required=True, help="emulator_id, letters and digits only, e.g. UNET")
    parser.add_argument("--training", required=True, choices=["A", "B", "C"], help="training experiment")
    parser.add_argument("--predictors", required=True, choices=["perfect", "imperfect"])
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--version", type=int, default=1, help="v<version> of version_realization (default 1)")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9]+", args.emulator):
        sys.exit(f"ERROR: emulator_id '{args.emulator}' must contain only letters and digits")
    if not re.fullmatch(r"[A-Za-z0-9-]+", args.institution):
        sys.exit(f"ERROR: institution_id '{args.institution}' must contain only letters, digits and '-'")

    os.makedirs(args.out_dir, exist_ok=True)
    ds = xr.open_dataset(args.prediction)
    variables = [v for v in ds.data_vars if {"time", "rlat", "rlon"} <= set(ds[v].dims)]
    if not variables:
        sys.exit("ERROR: no variable with dimensions (time, rlat, rlon) in the prediction file")

    for var in variables:
        path, f = target_file(args.target_dir, var)
        targ = xr.open_dataset(path).isel(time=0, drop=True)
        driver = f["driver"] if args.predictors == "imperfect" else f"UPS-{f['rcm']}-{f['driver']}"
        source_id = f"{f['rcm']}-emul-{args.emulator}-{args.training}"
        da = ds[var]
        members = range(da.sizes["member"]) if "member" in da.dims else [None]
        for i, m in enumerate(members, start=1):
            one = da if m is None else da.isel(member=m, drop=True)
            one = with_target_grid(one.transpose("time", "rlat", "rlon"), targ, var)
            name = (f"{var}_{f['domain']}_{driver}_{f['experiment']}_{f['variant']}_{args.institution}_{source_id}_"
                    f"v{args.version}-r{i}_{f['frequency']}_{f['dates']}.nc")
            one.to_netcdf(os.path.join(args.out_dir, name), encoding={var: ENCODING})
            print(f"wrote {name}", flush=True)


if __name__ == "__main__":
    main()
