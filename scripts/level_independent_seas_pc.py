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
from pyparsing import line
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import scipy.stats as stats
import pylab 

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



################# mix ###############################
# The first_on_all and first_on_first, vs last_on_all and last_on_last
#%%
mix_first = first_first.to_dataframe().join(first_all.to_dataframe(),
lsuffix = '_first',rsuffix = '_all')
mix_last = last_last.to_dataframe().join(last_all.to_dataframe(),
lsuffix = '_last',rsuffix = '_all'
)


## all levels
### all scatterplots
#%%
sept.tenyr_scatter(mix_first,mix_last,hlayer = 'all')

### extreme scatterplots
# %%
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 'all')

#%%
sept.tenyr_scatter(mix_first,mix_last,hlayer = 20000)
sept.tenyr_scatter(mix_first,mix_last,hlayer = 100000)


## different levels
#%%
### 200hpa
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 20000)
### 500hpa
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 50000)
### 850hpa
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 85000)
### 1000hpa
sept.tenyr_scatter_extreme(mix_first,mix_last,hlayer = 100000)


############### first 10 #########################
# first-first, first-all first-last
#%%
## hist
fig, axes = plt.subplots(1,2,figsize = (8,4),dpi = 150)
first_NAO_dfs = sis.pc_column([first_first,first_all,first_last])
sns.histplot(first_NAO_dfs.loc[100000],x = 'pc',hue = 'spap',kde=True,fill=False,
ax = axes[0])
first_EA_dfs = sis.pc_column([first_first,first_all,first_last],mode = 'EA')
sns.histplot(first_EA_dfs.loc[100000],x = 'pc',hue = 'spap',kde=True,fill=False,
ax= axes[1])
axes[0].set_title("NAO")
axes[1].set_title("EA")

# %%
## qq plot
first_first_NAO = first_first.sel(mode = 'NAO').values
first_all_NAO = first_all.sel(mode = 'NAO').values
first_last_NAO = first_last.sel(mode = 'NAO').values

fig,ax = plt.subplots()
stats.probplot(first_first_NAO.reshape(-1),dist = 'norm',plot = ax)
stats.probplot(first_all_NAO.reshape(-1),dist = 'norm',plot = ax)
stats.probplot(first_last_NAO.reshape(-1),dist = 'norm',plot =  ax)

ax.get_lines()[0].set_markerfacecolor('b')
ax.get_lines()[0].set_markeredgecolor('b')
ax.get_lines()[0].set_markersize(2)
ax.get_lines()[1].set_color('b')

ax.get_lines()[2].set_markerfacecolor('k')
ax.get_lines()[2].set_markeredgecolor('k')
ax.get_lines()[2].set_markersize(2)
ax.get_lines()[3].set_color('k')

ax.get_lines()[4].set_markerfacecolor('r')
ax.get_lines()[4].set_markeredgecolor('r')
ax.get_lines()[4].set_markersize(2)
ax.get_lines()[5].set_color('r')
line = ax.plot(np.arange(-5,5,1),np.arange(-5,5,1),linestyle = 'dotted',color = 'k')
ax.set_xlim(2,4)
ax.set_ylim(2,4)

# %%
first_first_all = first_first.to_dataframe().join(first_all.to_dataframe(),
lsuffix = '_first',rsuffix = '_all')
first_last_all = first_last.to_dataframe().join(first_all.to_dataframe(),
lsuffix = '_last',rsuffix = '_all'
)
# %%
## scatter plot
sept.tenyr_scatter(first_first_all,first_last_all,hlayer = 'all')

# %%
sept.tenyr_scatter_extreme(first_first_all,first_last_all,hlayer = 'all')

# %%
sept.tenyr_scatter(first_first_all,first_last_all,hlayer = 20000)
sept.tenyr_scatter(first_first_all,first_last_all,hlayer = 100000)

# %%
sept.tenyr_scatter_extreme(first_first_all,first_last_all,hlayer = 20000)
sept.tenyr_scatter_extreme(first_first_all,first_last_all,hlayer = 100000)


############### last 10 ################
# %%
last_first_all = last_first.to_dataframe().join(last_all.to_dataframe(),
lsuffix = '_first',rsuffix = '_all')
last_last_all = last_last.to_dataframe().join(last_all.to_dataframe(),
lsuffix = '_last',rsuffix = '_all')
# %%
sept.tenyr_scatter(last_first_all,last_last_all,hlayer = 'all')

# %%
sept.tenyr_scatter_extreme(last_first_all,last_last_all,hlayer = 'all')

# %%
sept.tenyr_scatter(last_first_all,last_last_all,hlayer = 20000)
sept.tenyr_scatter(last_first_all,last_last_all,hlayer = 100000)
# %%
sept.tenyr_scatter_extreme(last_first_all,last_last_all,hlayer = 20000)
sept.tenyr_scatter_extreme(last_first_all,last_last_all,hlayer = 100000)
# %%
