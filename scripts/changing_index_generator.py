# imports
#%%
import xarray as xr
import numpy as np
import pandas as pd
# %%

#%%
import sys
sys.path.append("..")
import src.spatial_pattern as ssp
import src.pattern_statistic as sps
import src.index_statistic as sis
import src.eof_plots as sept
import src.temporal_index as sti

import importlib
importlib.reload(ssp) # after changed the source code
importlib.reload(sps)
importlib.reload(sis)
importlib.reload(sept)
importlib.reload(sti)
# %%

# Data load and pre-process
#%%
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
# split ens
splitens = ssp.split_ens(allens)
# demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')
#select traposphere
trop = demean.sel(hlayers = slice(20000,100000))
trop = trop.var156
#%%

# index from changing patterns
#%%
print("independent index")
all_all_ind,all_first_ind,all_last_ind = sti.index_diff_pattern(trop,
independent=True,standard=True)

print("dependent index")
all_all_dep, all_first_dep,all_last_dep = sti.index_diff_pattern(trop,
independent=False, standard=True)