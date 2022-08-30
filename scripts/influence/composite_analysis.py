#%%
# import
from os import sched_param
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.composite.composite as scp
import src.plots.composite_plots as spcp

#%%
import importlib
importlib.reload(spcp)
importlib.reload(scp)
# %%
var = "precip"
independent = "dep"

dataname = (
    "/work/mh0033/m300883/3rdPanel/data/influence/"
    + var
    + "/"
    + "onepct_1850-1999_ens_1-100."
    + var
    + ".nc"
)

indexname = (
    "/work/mh0033/m300883/3rdPanel/data/allPattern/" + independent + "_index_nonstd.nc"
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
index = dep_std.sel(hlayers=100000)

# change time
index["time"] = index.time.dt.year
demean["time"] = demean.time.dt.year
# %%
ComAll = scp.composite(
    index=index, data=demean, dim="mode", reduction="mean", period="all"
)
ComFirst = scp.composite(
    index=index, data=demean, dim="mode", reduction="mean", period="first10"
)
ComLast = scp.composite(
    index=index, data=demean, dim="mode", reduction="mean", period="last10"
)

# %%
