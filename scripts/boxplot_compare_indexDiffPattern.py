#%%
import xarray as xr
import numpy as np
import pandas as pd
import seaborn as sns

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.pattern_statistic as sps
import src.Teleconnection.index_statistic as sis
import src.Teleconnection.temporal_index as sti
#%%
import importlib
importlib.reload(sis)
importlib.reload(sti)
importlib.reload(ssp)
importlib.reload(sps)

#%%
all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind_nonstd.nc')
all_first_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_first_ind_nonstd.nc')
all_last_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_ind_nonstd.nc')

all_all_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_dep_nonstd.nc')
all_first_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_frist_dep_nonstd.nc')
all_last_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_dep_nonstd.nc')


#%%
pattern = xr.DataArray(['all','first','last'],dims = 'pattern')
ind = xr.concat([all_all_ind,all_first_ind,all_last_ind],dim = pattern)
dep = xr.concat([all_all_dep,all_first_dep,all_last_dep],dim = pattern)

#%%
method = xr.DataArray(['False','True'],dims='vcommon')
index = xr.concat([ind,dep],dim = method)

index_plot = index.sel(mode = 'EA',hlayers = 100000,vcommon = 'True').pc.to_dataframe().reset_index()

# %%
sns.boxplot(data = index_plot,x = 'pattern',y = 'pc')
# %%
