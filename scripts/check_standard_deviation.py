#%% import 
from tracemalloc import Snapshot
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
import src.Teleconnection.spatial_pattern as sp

# %%
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time_fldmean.nc")
# %%
#%%
splitens = sp.split_ens(allens)
trop = splitens.sel(hlayers = slice(20000,100000))

# %%
gph = trop.var156
# %% all year and ens, but different height
h_std = gph.std(dim=['time','ens'])
# %%

time_std = gph.std(dim = 'time')
# %%
ens_std = gph.std(dim = 'ens')
# %%
fig,axes = plt.subplots(2,2,figsize = (8,8),dpi = 150)
ens_std.sel(hlayers = 20000).plot(ax = axes[0,0])
ens_std.sel(hlayers = 50000).plot(ax = axes[0,1])
ens_std.sel(hlayers = 85000).plot(ax = axes[1,0])
ens_std.sel(hlayers = 100000).plot(ax = axes[1,1])
axes[0,0].set_title("std over 200hpa")
axes[0,1].set_title("std over 500hpa")
axes[1,0].set_title("std over 850hpa")
axes[1,1].set_title("std over 1000hpa")

# %%
fig,axes = plt.subplots(dpi = 150)
ens_std.plot(x = 'time',y = 'hlayers',ylim = (100000,20000),
levels = np.arange(4,10,1),extend = 'both',ax = axes)
# %%
