#!/usr/bin/env python
"""Validate the format of one CONTINENTAL-BENCH prediction file against the target file of the same test block.

Usage:
    python validate.py <prediction.nc> --target <target.nc>

The target file (SOURCE_FILES/test/<driver>/<period>/target/<var>_*.nc) is the template. The prediction must hold the
same variable, in the same units, on the same grid. Ensembles add a leading dimension `member` of size 5; deterministic
models may leave it out or give it size 1:

    <var>(member, time, rlat, rlon)    or    <var>(time, rlat, rlon)

and one time step per day of the test period, at the same time of day as the target. Its calendar is that of the
predictors, which may differ from the target calendar only by the 29 February days.

Each check prints OK or FAIL. The exit code is 1 if any check fails, 0 otherwise.
Requirements: numpy, xarray, netCDF4, cftime.
"""
import argparse
import sys

import numpy as np
import xarray as xr

DIMS = ("member", "time", "rlat", "rlon")
N_MEMBERS = (1, 5)  # accepted sizes of the member dimension (absent = 1 member)
CHUNK = 100  # days read at a time when the prediction file has no internal chunks


class Report:
    def __init__(self):
        self.n = {"OK": 0, "FAIL": 0}

    def check(self, cond, msg):
        level = "OK" if cond else "FAIL"
        self.n[level] += 1
        print(f"{level:4s} {msg}", flush=True)
        return cond


def main_var(ds):
    names = [v for v in ds.data_vars if set(DIMS[1:]) <= set(ds[v].dims)]
    if len(names) != 1:
        raise ValueError(f"expected one variable with dimensions {DIMS[1:]} in the target, found {names}")
    return names[0]


def same(a, b):
    return a.shape == b.shape and np.allclose(a, b, rtol=0, atol=1e-6, equal_nan=True)


def day(t):
    return f"{t.year:04d}-{t.month:02d}-{t.day:02d}"


def check_metadata(rep, pred, targ, var):
    if not rep.check(var in pred.data_vars, f"variable '{var}' present"):
        return False
    p, t = pred[var], targ[var]

    pu, tu = p.attrs.get("units"), t.attrs.get("units")
    rep.check(pu == tu, f"units '{pu}' (target '{tu}')")

    if not rep.check(p.dims in (DIMS, DIMS[1:]), f"dimensions {p.dims} (expected {DIMS} or {DIMS[1:]})"):
        return False
    n = p.sizes.get("member", 1)
    rep.check(n in N_MEMBERS, f"{n} member{'s' if n > 1 else ''} (expected {' or '.join(map(str, N_MEMBERS))})")

    for c in ("rlat", "rlon"):
        rep.check(c in pred.coords and same(pred[c].values, targ[c].values), f"coordinate '{c}' matches the target")
    for c in ("lat", "lon"):
        if c in targ.coords:
            ok = c in pred.coords and pred[c].dims == targ[c].dims and same(pred[c].values, targ[c].values)
            rep.check(ok, f"coordinate '{c}' matches the target")

    gm_t = t.attrs.get("grid_mapping")
    if gm_t:
        gm_p = p.attrs.get("grid_mapping")
        if rep.check(gm_p is not None and gm_p in pred.variables, f"grid mapping variable '{gm_p}' present (target '{gm_t}')"):
            keys = ("grid_mapping_name", "grid_north_pole_latitude", "grid_north_pole_longitude")
            diff = [k for k in keys if pred[gm_p].attrs.get(k) != targ[gm_t].attrs.get(k)]
            rep.check(not diff, "grid mapping parameters match" + ("" if not diff else ": differ in " + ", ".join(diff)))

    return check_time(rep, pred, targ)


def check_time(rep, pred, targ):
    pt, tt = pred.time.values, targ.time.values
    pdays, tdays = [day(x) for x in pt], [day(x) for x in tt]
    ok = True
    ok &= rep.check(len(set(pdays)) == len(pdays) and pdays == sorted(pdays), "one time step per day, in increasing order")
    ok &= rep.check((pdays[0], pdays[-1]) == (tdays[0], tdays[-1]),
                    f"period {pdays[0]} to {pdays[-1]} (target {tdays[0]} to {tdays[-1]})")
    missing = sorted(set(tdays) - set(pdays))
    extra = sorted(set(pdays) - set(tdays))
    other = [d for d in missing + extra if not d.endswith("-02-29")]
    msg = "same days as the target"
    if other:
        msg += f": {len(other)} days differ, first {other[0]}"
    elif missing or extra:
        msg += f", except 29 February ({len(missing)} missing, {len(extra)} extra: calendar of the predictors)"
    ok &= rep.check(not other, msg)
    # ml-evaluation matches prediction and target time steps by their exact time stamp
    hours = sorted({(x.hour, x.minute) for x in pt})
    thours = sorted({(x.hour, x.minute) for x in tt})
    fmt = ", ".join(f"{h:02d}:{m:02d}" for h, m in hours)
    ok &= rep.check(hours == thours, f"time of day {fmt} (target {', '.join(f'{h:02d}:{m:02d}' for h, m in thours)})")
    return ok


def check_missing(rep, pred, targ, var):
    p = pred[var]
    mask = np.isfinite(targ[var].isel(time=0).values)  # cells where the target has data
    ch = p.encoding.get("chunksizes")
    tchunk, ychunk = tuple(ch[-3:-1]) if ch else (CHUNK, pred.sizes["rlat"])
    nt, ny = pred.sizes["time"], pred.sizes["rlat"]
    n_nan = 0
    for i in range(0, nt, tchunk):
        print(f"     reading days {i + 1}-{min(i + tchunk, nt)} of {nt}", flush=True)
        for j in range(0, ny, ychunk):
            pv = p.isel(time=slice(i, i + tchunk), rlat=slice(j, j + ychunk)).values
            n_nan += int((~np.isfinite(pv) & mask[j:j + ychunk]).sum())
    rep.check(n_nan == 0, f"no missing values where the target has data ({n_nan} found)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prediction", help="prediction file (one variable)")
    parser.add_argument("--target", required=True, help="target file of the same test block and variable")
    args = parser.parse_args()

    rep = Report()
    print(f"== {args.prediction}\n   target: {args.target}")
    targ = xr.open_dataset(args.target, use_cftime=True)
    var = main_var(targ)
    try:
        pred = xr.open_dataset(args.prediction, use_cftime=True)
    except Exception as e:
        rep.check(False, f"cannot open the prediction: {e}")
    else:
        if check_metadata(rep, pred, targ, var):
            check_missing(rep, pred, targ, var)
        else:
            print("     (missing-value check skipped)")
    print(f"== SUMMARY {var}: {rep.n['FAIL']} FAIL, {rep.n['OK']} OK")
    sys.exit(1 if rep.n["FAIL"] else 0)


if __name__ == "__main__":
    main()
