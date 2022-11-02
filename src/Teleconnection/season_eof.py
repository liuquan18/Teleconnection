import numpy as np
import pandas as pd
import xarray as xr

import src.Teleconnection.tools as tools
import src.Teleconnection.vertical_eof as vertical_eof


###### high level APIs #################
def season_eof(
    xarr, nmode=2, window=10, fixed_pattern="all", independent=True, standard=True
):
    """high_level API for seasonal data eof analysis.

    **Arguments:**

        *xarr*: the DataArray to be decomposed. [time,ens,lat,lon,plev]
        *standard*: do standardization before the eof decompose or not.
        *independent*: all layers decompose independently or not.
        *rolling_eof*: whether to use rolling_eof or not.

    **Return:**
    
        EOF, PC and FRA
    """
    # if the data should be standarize
    if standard:
        xarr = tools.standardize(xarr)

    # passing parameters
    kwargs = {
        "nmode": nmode,  # for doeof
        "window": window,  # for rolling_eof
        "fixed_pattern": fixed_pattern,  # for rolling_eof
        "independent": independent,  # choose vetrical eof method.
    }

    eof, pc, fra = vertical_eof.vertical_eof(xarr, **kwargs)

    return eof, pc, fra

def main():
    """
    for debug
    """
    # ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/sample.nc")
    # ex = ex.var156
    allens = xr.open_dataset(
        "/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc"
    )
    # split ens
    splitens = tools.split_ens(allens)
    # demean ens-mean
    demean = splitens - splitens.mean(dim="ens")
    # select traposphere
    trop = demean.sel(hlayers=slice(85000, 100000)).isel(time=slice(0, 40))

    #     eof_sar,pc_sar,fra_sar = season_eof(ex,nmode=2,method ="rolling_eof",
    # window=10,fixed_pattern='all',return_full_eof= False,independent = True,standard=True)

    eof, index, fra = season_eof(
        trop.var156,
        nmode=2,
        window=10,
        fixed_pattern="all",
        independent=True,
        standard=True,
    )


if __name__ == "__main__":
    main()
