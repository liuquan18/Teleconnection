#%%
import importlib
from os import sched_param

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr

import src.composite.composite as scp
import src.plots.composite_plots as spcp

importlib.reload(spcp)
importlib.reload(scp)
# %%


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

    ComFirst = scp.composite(
        index=index, data=demean, dim="mode", reduction="mean", period="first10"
    )
    ComLast = scp.composite(
        index=index, data=demean, dim="mode", reduction="mean", period="last10"
    )
    return ComFirst, ComLast, ComLast - ComFirst


#%%
# Precip
PrecipFirst, PrecipLast, PrecipDiff = field_composite("precip", "dep", hlayer=100000)

print("precip")
spcp.lastfirst_comp_map(PrecipFirst, PrecipLast, mode="NAO")

spcp.lastfirst_comp_map(PrecipFirst, PrecipLast, mode="EA")

#%%
# t2max
t2maxFirst, t2maxLast, t2maxDiff = field_composite("t2max", "dep", hlayer=100000)
print("t2max")
spcp.lastfirst_comp_map(
    t2maxFirst,
    t2maxLast,
    mode="NAO",
    levels=np.arange(-3, 3.1, 0.5),
    unit="max 2m-temperature / K",
)
spcp.lastfirst_comp_map(
    t2maxFirst,
    t2maxLast,
    mode="EA",
    levels=np.arange(-3, 3.1, 0.5),
    unit="max 2m-temperature / K",
)

#%%

# tsurf
tsurfFirst, tsurfLast, tsurfDiff = field_composite("tsurf", "dep", hlayer=100000)
print("tsurf")
spcp.lastfirst_comp_map(
    tsurfFirst,
    tsurfLast,
    mode="NAO",
    levels=np.arange(-3, 3.1, 0.5),
    unit="surface temperature / K",
)

spcp.lastfirst_comp_map(
    tsurfFirst,
    tsurfLast,
    mode="EA",
    levels=np.arange(-3, 3.1, 0.5),
    unit="surface temperature / K",
)

# %%

spcp.lastfirst_comp_var(PrecipDiff,t2maxDiff,tsurfDiff,mode = 'NAO')

# %% wind
# windspeed
# wspdFirst, wspdLast, wspdDiff = field_composite("windspeed","dep",hlayer = 100000)

#u10
uFirst, uLast, uDiff = field_composite("u10","dep",hlayer = 100000)

#v10
vFirst, vLast, vDiff = field_composite("v10","dep",hlayer = 100000)


#%% save
uFirst.to_netcdf("/work/mh0033/m300883/3rdPanel/data/influence/u10/uFirst.nc")
uLast.to_netcdf("/work/mh0033/m300883/3rdPanel/data/influence/u10/uLast.nc")

vFirst.to_netcdf("/work/mh0033/m300883/3rdPanel/data/influence/v10/vFirst.nc")
vLast.to_netcdf("/work/mh0033/m300883/3rdPanel/data/influence/v10/vLast.nc")


# wind plots
#%% 
import cartopy.feature as cfeat
import matplotlib.pyplot as plt

import iris
import iris.plot as iplt
import iris.quickplot as qplt


#%%
uwind = uFirst.sel(mode = 'NAO',extr_type = 'pos')
vwind = vFirst.sel(mode = 'NAO',extr_type = 'pos')

uwind = uwind.to_iris()
vwind = vwind.to_iris()

#%%
# windspeed 
windspeed = (uwind**2 + vwind**2)**0.5
windspeed = windspeed.rename("windspeed")

# plot windspeed as contour
qplt.contourf(windspeed,20)
iplt.quiver(uwind,vwind,pivot = "middle")
qplt.show()


#%%

print("windspeed")
spcp.lastfirst_comp_map(
    wspdFirst,
    wspdLast,
    mode="NAO",
    levels=np.arange(-3, 3.1, 0.5),
    unit="velocity [m/s]",
)
spcp.lastfirst_comp_map(
    wspdFirst,
    wspdLast,
    mode="EA",
    levels=np.arange(-3, 3.1, 0.5),
    unit="velocity [m/s]",
)
# %%
