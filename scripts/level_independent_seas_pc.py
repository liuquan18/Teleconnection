"""
This file generate the seasonal pc, from different fixed patterns,
which is also different in all levels. 
The scripts should generate 9 index.
    spatial pattern: all    first10    last10
    temporal pattern:
    all               X       X           X
    first10           X       X           X
    last10            X       X           X
"""
# imports
#%%
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as pld

#%%
import sys
sys.path.append("..")
import src.spatial_pattern as sp
import src.pattern_statistic as ps

import importlib
importlib.reload(sp) # after changed the source code
importlib.reload(ps)


# Data load and pre-process
#%%
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
# split ens
splitens = sp.split_ens(allens)
# demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')
#select traposphere
trop = demean.sel(hlayers = slice(20000,100000))


# first row: project all onto the three spatial patterns.
# %%
_,all_all,_ = sp.season_eof(trop.var156, nmode=2,window=10,
fixed_pattern="all")  # "method" doesn't matter since the pc is 
                      # calculated independently.
_, all_first,_ = sp.season_eof(trop.var156,nmode=2,window=10,
fixed_pattern="first")
_, all_last,_ = sp.season_eof(trop.var156,nmode=2,window=10,
fixed_pattern="last")


# second row: first 10 years of data projected on all, first10,and last10 eofs.
# %%
first_all = all_all.isel(time=slice(0,10))
first_first = all_first.isel(time = slice(0,10))
first_last = all_last.isel(time = slice(0,10))


# third row: last 10 years of data projected on all, first10 and last10 eofs
#%%
last_all = all_all.isel(time = slice(-10,None))
last_first = all_first.isel(time = slice(-10,None))
last_last = all_last.isel(time = slice(-10,None))



# %%
