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
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

#%%
import sys
sys.path.append("..")
import src.spatial_pattern as ssp
import src.pattern_statistic as sps
import src.index_statistic as sis
import src.eof_plots as sept

import importlib
importlib.reload(ssp) # after changed the source code
importlib.reload(sps)
importlib.reload(sis)
importlib.reload(sept)



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

# standarize
"""
all standard with mean and std of all_all
"""
#%%
all_mean = all_all.mean(dim = 'time')
all_std = all_all.std(dim = 'time')

all_all = (all_all-all_mean)/all_std
all_first = (all_first-all_mean)/all_std
all_last = (all_last-all_mean)/all_std

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


# The first_on_all and first_on_first, vs last_on_all and last_on_last
#%%
mix_first = first_first.to_dataframe().join(first_all.to_dataframe(),
lsuffix = '_first',rsuffix = '_all')
mix_last = last_last.to_dataframe().join(last_all.to_dataframe(),
lsuffix = '_last',rsuffix = '_all'
)


#%%
sept.tenyr_scatter(mix_first,mix_last,hlayer = 'all')


# %%
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 'all')


# %%
first_np = first_first.to_dataframe().loc[50000,'NAO']['pc'].values
last_np = last_last.to_dataframe().loc[50000,'NAO']['pc'].values
mix_np = np.c_[first_np,last_np]
mix_mix = pd.DataFrame(data = mix_np,columns = ['pc_first','pc_last'])
# %%
