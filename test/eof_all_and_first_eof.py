
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

# %%

trop_std = ssp.standardize(trop.var156)
# %%
trop_com = ssp.stack_ens(trop_std,withdim='time')
# %%
eof_all, pc_all,fra_all = ssp.doeof(trop_com,standard=False)
# %%
trop_first = trop_std.isel(time = slice(0,10))
trop_first_com = ssp.stack_ens(trop_first,withdim = 'time')
eof_first, pc_first, fra_first = ssp.doeof(trop_first_com, standard=False)


# %%
eof_all, pc_all,fra_all = ssp.season_eof(trop.var156,independent=True,method='eof')

# %%
eof_first, pc_first, fra_first = ssp.season_eof(trop_first_com, standard=False,method = 'eof')

# %%
