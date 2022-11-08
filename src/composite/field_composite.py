import xarray as xr
import numpy as np
import src.composite.composite as composite


def composite(
    index: xr.DataArray,
    data: xr.DataArray,
    dim: str = "hlayers",
    reduction: str = "mean",
    period: str = "all",
):
    """
    composite mean maps of extreme cases or counts of extreme cases.
    given the index and the data, determine the time and ens coordinates
    where extreme cases happen from the index, and select the data with
    those indexes, average the selected fields.
    **Arguments**
        *index* the index of NAO and EA
        *data* the original geopotential data.
        *reduction* mean or count
        *period* 'first10','last10','all'
    **Return**
        *compostie* the composite mean of the extreme cases.
    """
    if period == "all":
        index = index
    elif period == "first10":
        index = index.isel(
            time=slice(0, 10)
        )  # the index actually started from 1856,so wrong here.
    elif period == "last10":
        index = index.isel(time=slice(-10, None))
    data = data.sel(time=index.time)

    Composite = []
    for mode in index.mode:
        _index = index.sel(mode=mode)
        if dim == "hlayers":
            composite = _index.groupby(dim).apply(
                composite.composite, data=data, reduction=reduction
            )
        elif dim == "mode":
            composite = composite.composite(_index, data, reduction)
        Composite.append(composite)
    Composite = xr.concat(Composite, dim=index.mode)

    return Composite


def field_composite(var, independent="dep", hlayer=100000):
    """
    function to get the first and last composite mean field
    """
    dataname = (
        "/work/mh0033/m300883/3rdPanel/data/influence/"
        + var
        + "/"
        + "onepct_1850-1999_ens_1-100."
        + var
        + ".nc"
    )

    indexname = (
        "/work/mh0033/m300883/3rdPanel/data/allPattern/"
        + independent
        + "_index_nonstd.nc"
    )

    changing_name = (
        "/work/mh0033/m300883/3rdPanel/data/changingPattern/"
        + independent
        + "_index_nonstd.nc"
    )

    # Data
    file = xr.open_dataset(dataname)
    fdata = file[var]
    # demean (ens-mean)
    demean = fdata - fdata.mean(dim="ens")

    # index
    all_all_dep = xr.open_dataset(indexname).pc
    changing_dep = xr.open_dataset(changing_name).pc
    all_all_dep = all_all_dep.transpose("time", "ens", "mode", "hlayers")

    mean_dep = all_all_dep.mean(dim="time")
    std_dep = all_all_dep.std(dim="time")
    dep_std = (changing_dep - mean_dep) / std_dep
    index = dep_std.sel(hlayers=hlayer)

    # change time
    index["time"] = index.time.dt.year
    demean["time"] = demean.time.dt.year

    ComFirst = composite(
        index=index, data=demean, dim="mode", reduction="mean", period="first10"
    )
    ComLast = composite(
        index=index, data=demean, dim="mode", reduction="mean", period="last10"
    )
    return ComFirst, ComLast, ComLast - ComFirst