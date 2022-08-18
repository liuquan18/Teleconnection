#%%
# import 
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.Teleconnection.index_statistic as sis
import src.Teleconnection.temporal_index as sti
import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.eof_plots as sept
import src.Teleconnection.pattern_statistic as sps

#%%
import importlib
importlib.reload(sis)
importlib.reload(sti)
importlib.reload(ssp)
importlib.reload(sept)
importlib.reload(sps)

#%%
# load data
## index
## independent
all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/allPattern/ind_index_nonstd.nc').pc
changing_ind = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_index_nonstd.nc").pc
all_all_ind = all_all_ind.transpose('time','ens','mode','hlayers')

## dependent
all_all_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/allPattern/dep_index_nonstd.nc').pc
changing_dep = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_index_nonstd.nc").pc
all_all_dep = all_all_dep.transpose('time','ens','mode','hlayers')

#%%
## seasonal data
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
splitens = ssp.split_ens(allens)
# demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')
# select traposphere
trop = demean.sel(hlayers = slice(20000,100000))
trop = trop.var156
# standardize
trop_std = ssp.standardize(trop)
# transpose to the same order

#%%
# standardization
mean_ind = all_all_ind.mean(dim = 'time')
std_ind = all_all_ind.std(dim = 'time')
ind_std = (all_all_ind - mean_ind)/std_ind

mean_dep = all_all_dep.mean(dim = 'time')
std_dep = all_all_dep.std(dim = 'time')
dep_std = (changing_dep - mean_dep)/std_dep


#%% composite
ind = sis.composite(ind_std,trop_std)
dep = sis.composite(dep_std,trop_std)
# %%

# %%
lon_height_EA_neg = sps.lon_height(ind.sel(extr_type = 'neg'),mode = 'EA')
lon_height_EA_pos = sps.lon_height(ind.sel(extr_type = 'pos'),mode = 'EA')
# %%
