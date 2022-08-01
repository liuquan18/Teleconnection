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



# To dataframes
# %%
all_dfs = sis.pc_column([all_all, all_first,all_last])
first_dfs = sis.pc_column([first_first,first_all,first_last])
last_dfs = sis.pc_column([last_first,last_all,last_last])

# check Z500
# %%
sept.tenyr_hist(all_dfs, hlayer = 50000)

# %%
sept.tenyr_hist(first_dfs, hlayer = 50000)

# %%
sept.tenyr_hist(last_dfs, hlayer = 50000)
# %%

sept.tenyr_hist(last_dfs, hlayer = 'all')
# %%
sept.tenyr_hist(last_dfs, hlayer = 100000)
# %%
sept.tenyr_hist(last_dfs, hlayer = 20000)
# %%
sept.tenyr_hist(mix_dfs, hlayer = 'all')
# %%


mix_first = first_first.to_dataframe().join(first_all.to_dataframe(),
lsuffix = '_first',rsuffix = '_all')
mix_last = last_last.to_dataframe().join(last_all.to_dataframe(),
lsuffix = '_last',rsuffix = '_all'
)


# %%
bins = 50
fig,ax = plt.subplots()
hf = sns.histplot(data = mix_first,x = 'pc_all',y = 'pc_first',
ax = ax,color= 'b', bins = bins,label = 'first',legend = False,alpha = 0.9)

hl = sns.histplot(data = mix_last,x = 'pc_all',y = 'pc_last',
ax = ax,color = 'r', bins = bins,label = 'last',legend = False,alpha = 0.9)

line = ax.plot(np.arange(-3,4,1),np.arange(-3,4,1),linestyle = 'dotted',color = 'k')

blue_patch = mpatches.Patch(color='blue',label="first")
red_patch = mpatches.Patch(color='red', label='last')

plt.legend(handles=[blue_patch,red_patch],loc = 'upper left')
# %%

fig,ax = plt.subplots()
sns.scatterplot(data = mix_first, x = "pc_all", y = "pc_first",ax = ax)
sns.scatterplot(data = mix_last, x = "pc_all", y = "pc_last",ax = ax,
color = 'r',alpha = 0.3)
line = ax.plot(np.arange(-3,5,1),np.arange(-3,5,1),linestyle = 'dotted',color = 'k')
ax.set_xlim(2,4)
ax.set_ylim(2,4)

# %%
fig,ax = plt.subplots()
sns.scatterplot(data = mix_first, x = "pc_all", y = "pc_first",ax = ax)
sns.scatterplot(data = mix_last, x = "pc_all", y = "pc_last",ax = ax,
color = 'r',alpha = 0.3)
line = ax.plot(np.arange(-5,5,1),np.arange(-5,5,1),linestyle = 'dotted',color = 'k')
ax.set_xlim(-4,-2)
ax.set_ylim(-4,-2)

# %%
