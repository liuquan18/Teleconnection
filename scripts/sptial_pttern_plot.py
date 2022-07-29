#%%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs


#%%
import sys
sys.path.append("..")
import src.pattern_statistic as ps
import src.eof_plots as ept

import importlib
importlib.reload(ps) # after changed the source code
importlib.reload(ept)

#%% read data
all_eofs = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/eof_all/eof_all.nc")
rolling_eofs = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_all/eof.nc")

# %% to array
all_eof = all_eofs.eof
first_eof = rolling_eofs.eof.isel(time = 0)
last_eof = rolling_eofs.eof.isel(time = -1)

# %% to lon-height
all_lon_height_ea = ps.lon_height(all_eof,mode='EA')
first10_lon_height_ea = ps.lon_height(first_eof,mode='EA')
last10_lon_height_ea = ps.lon_height(last_eof,mode='EA')

# %% plot
fig,axes = plt.subplots(1,3,figsize = (8,3),dpi = 150,sharey=True)

all_lon_height_ea.plot.contourf(x = 'lon',y = 'hlayers',ax = axes[0],
ylim = (1000,200))
first10_lon_height_ea.plot.contourf(x = 'lon',y = 'hlayers',ax = axes[1],
ylim = (1000,200))
last10_lon_height_ea.plot.contourf(x = 'lon',y = 'hlayers',ax = axes[2],
ylim = (1000,200))

plt.show()

# %%
ept.visu_eofspa(all_eof)
# %%
