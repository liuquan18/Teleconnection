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
import seaborn as sns

#%%
import sys
sys.path.append("..")
import src.spatial_pattern as ssp
import src.pattern_statistic as sps
import src.index_statistic as sis

import importlib
importlib.reload(ssp) # after changed the source code
importlib.reload(sps)
importlib.reload(sis)


# Data load and pre-process
#%%
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
# split ens
splitens = ssp.split_ens(allens)
# demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')
#select traposphere
trop = demean.sel(hlayers = slice(20000,100000))


# first row: project all onto the three spatial patterns.
# %%
_,all_all,_ = ssp.season_eof(trop.var156, nmode=2,window=10,
fixed_pattern="all")  # "method" doesn't matter since the pc is 
                      # calculated independently.
_, all_first,_ = ssp.season_eof(trop.var156,nmode=2,window=10,
fixed_pattern="first")
_, all_last,_ = ssp.season_eof(trop.var156,nmode=2,window=10,
fixed_pattern="last")

#%%
all_all.name = 'pc'
all_first.name = 'pc'
all_last.name = 'pc'

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
all_dfs = sis.pc_column([all_all, all_first,all_last])
# %%
