#%%
# import
from os import sched_param
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.composite.composite as scp

#%%
import importlib
importlib.reload(scp)
# %%
# Data
var = "precip"

fname='/work/mh0033/m300883/3rdPanel/data/influence/'+var+'/'+'onepct_1850-1999_ens_1-100.'+var+'.nc'
file = xr.open_dataset(fname)
fdata = file[var]

# demean (ens-mean)
demean = fdata-fdata.mean(dim = 'ens')
# %%
# index
all_all_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/allPattern/dep_index_nonstd.nc').pc
changing_dep = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_index_nonstd.nc").pc
all_all_dep = all_all_dep.transpose('time','ens','mode','hlayers')

mean_dep = all_all_dep.mean(dim = 'time')
std_dep = all_all_dep.std(dim = 'time')
dep_std = (changing_dep - mean_dep)/std_dep
index = dep_std.sel(hlayers = 100000)
# %%
varcomp = scp.composite(index = index,data = demean,,)