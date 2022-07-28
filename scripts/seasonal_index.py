#%% import 
from tracemalloc import Snapshot
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#%%
import sys
sys.path.append("..")
import src.pattern_statistic as ps
import src.spatial_pattern as sp

import importlib
importlib.reload(ps) # after changed the source code

#%% Load seasonal PCs

# stanadarad-independent-rolling-fixed all
pc_sira=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_all/pc.nc")

# stanadarad-independent-rolling-fixed all
pc_sirf=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_first/pc.nc")

# stanadarad-independent-rolling-fixed all
pc_sirl=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_last/pc.nc")


#%%
# standard-alllevel-rolling eof all pattern
pc_snra=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_all/pc.nc")
pc_snrf=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_first/pc.nc")
pc_snrl=xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_last/pc.nc")


#%%
pc_sirf = sp.standardize(pc_sirf)
pc_sirl = sp.standardize(pc_sirl)


#%%
pc_snrf = sp.standardize(pc_snrf)
pc_snrl = sp.standardize(pc_snrl)


# %% to dataframe
df_sira = ps.pc_todf(pc_sira.isel(time = slice(0,10)),'all')
df_sirf = ps.pc_todf(pc_sirf.isel(time = slice(0,10)),'first')
df_sirl = ps.pc_todf(pc_sirl.isel(time = slice(0,10)),'last')
# %%
df_sir = ps.merge_df([df_sira,df_sirf,df_sirl])

# %%
df_sir
# %% to dataframe
df_snra = ps.pc_todf(pc_snra.isel(time = slice(0,10)),'all')
df_snrf = ps.pc_todf(pc_snrf.isel(time = slice(0,10)),'first')
df_snrl = ps.pc_todf(pc_snrl.isel(time = slice(0,10)),'last')
# %%
df_snr = ps.merge_df([df_snra,df_snrf,df_snrl])
# %%

# %%
fig,axes = plt.subplots(3,2,dpi = 150,figsize = (10,9))
plt.subplots_adjust(hspace = 0.4)
EA_ind = ps.show_allyears_ens(df_sir,'EA')
titles = ['200hpa','500hpa','850hpa']
for i,row in enumerate(axes):
    EA_ind[i].plot.hist(bins = 10,histtype = 'step',linewidth=1.,density = True,ax = row[0])
    EA_ind[i].boxplot(ax = row[1])
    row[0].set_title(titles[i])
    row[1].set_title(titles[i])
plt.suptitle("EA-independent-all-years&ens")
plt.show()

# %%
fig,axes = plt.subplots(3,2,dpi = 150,figsize = (10,9))
plt.subplots_adjust(hspace = 0.4)
EA_ind = ps.show_allyears_ens(df_sir,'NAO')
titles = ['200hpa','500hpa','850hpa']
for i,row in enumerate(axes):
    EA_ind[i].plot.hist(bins = 10,histtype = 'step',linewidth=1.,density = True,ax = row[0])
    EA_ind[i].boxplot(ax = row[1])
    row[0].set_title(titles[i])
    row[1].set_title(titles[i])
plt.suptitle("NAO-independent-all-years&ens")
plt.show()


# %%
fig,axes = plt.subplots(3,2,dpi = 150,figsize = (10,9))
plt.subplots_adjust(hspace = 0.4)
EA_ind = ps.show_allyears_ens(df_snr,'EA')
titles = ['200hpa','500hpa','850hpa']
for i,row in enumerate(axes):
    EA_ind[i].plot.hist(bins = 10,histtype = 'step',linewidth=1.,density = True,ax = row[0])
    EA_ind[i].boxplot(ax = row[1])
    row[0].set_title(titles[i])
    row[1].set_title(titles[i])
plt.suptitle("EA-non-independent-all-years&ens")
plt.show()
# %%
fig,axes = plt.subplots(3,2,dpi = 150,figsize = (10,9))
plt.subplots_adjust(hspace = 0.4)
EA_ind = ps.show_allyears_ens(df_snr,'NAO')
titles = ['200hpa','500hpa','850hpa']
for i,row in enumerate(axes):
    EA_ind[i].plot.hist(bins = 10,histtype = 'step',linewidth=1.,density = True,ax = row[0])
    EA_ind[i].boxplot(ax = row[1])
    row[0].set_title(titles[i])
    row[1].set_title(titles[i])
plt.suptitle("NAO-non-independent-all-years&ens")
plt.show()
# %%
