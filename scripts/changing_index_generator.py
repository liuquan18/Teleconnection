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
ind_EOF,ind_index,ind_fra= sti.index_changing_pattern(trop,
independent=True,standard=False)
#%%



#%%
print("dependent index")
dep_EOF,dep_index,dep_fra = sti.index_changing_pattern(trop,
independent=False,standard=False)
#%%


#%%
ind_EOF.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_EOF_nonstd.nc")
ind_index.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_index_nonstd.nc")
ind_fra.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_fra_nonstd.nc")

#%%
dep_EOF.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_EOF_nonstd.nc")
dep_index.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_index_nonstd.nc")
dep_fra.to_netcdf("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_fra_nonstd.nc")
# %%
