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
import plots.eof_plots as sept
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

# standardization
mean_ind = all_all_ind.mean(dim = 'time')
std_ind = all_all_ind.std(dim = 'time')
ind_std = (all_all_ind - mean_ind)/std_ind

mean_dep = all_all_dep.mean(dim = 'time')
std_dep = all_all_dep.std(dim = 'time')
dep_std = (changing_dep - mean_dep)/std_dep
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

#%% composite counts
ind_counts = sis.composite(ind_std,trop_std,reduction='count')
dep_counts = sis.composite(dep_std,trop_std,reduction='count')

#%%



#%% composite mean
ind = sis.composite(ind_std,trop_std)
dep = sis.composite(dep_std,trop_std)
# %%
sept.visu_composite_spa(ind,plev = 20000,levels=np.arange(-2,2.1,0.4))
sept.visu_composite_spa(ind,plev = 100000,levels=np.arange(-2,2.1,0.4))

#%%
# diff
diff_ind = ind.sel(extr_type = 'pos')+ind.sel(extr_type = 'neg')
sept.visu_eofspa(diff_ind,
plev = [20000,100000],levels = np.arange(-0.5,0.51,0.1))

#%%
diff_lat_height_ind_EA = sps.lat_height(diff_ind,mode = 'EA')
diff_lat_height_ind_EA.plot.contourf(x = 'lat',y = 'hlayers')

#%%
diff_lat_height_ind_NAO = sps.lat_height(diff_ind,mode = 'NAO')
diff_lat_height_ind_NAO.plot.contourf(x = 'lat',y = 'hlayers')

# %%
lon_height_EA_neg = sps.lon_height(ind.sel(extr_type = 'neg'),mode = 'EA')
lon_height_EA_pos = sps.lon_height(ind.sel(extr_type = 'pos'),mode = 'EA')
# %%
lat_height_NAO_neg = sps.lat_height(ind.sel(extr_type = 'neg'),mode = 'NAO')
lat_height_NAO_pos = sps.lat_height(ind.sel(extr_type = 'pos'),mode = 'NAO')
# %%


# time evolve
ind_first10 = sis.composite(ind_std,trop_std,period = 'first10')
ind_last10 = sis.composite(ind_std,trop_std, period = 'last10')

# %%
sept.visu_composite_spa(ind_first10,plev = 100000,levels=np.arange(-2,2.1,0.4))
sept.visu_composite_spa(ind_last10,plev = 100000,levels=np.arange(-2,2.1,0.4))

# %%
diff_time = ind_last10-ind_first10
sept.visu_composite_spa(diff_time,plev = 100000,levels=np.arange(-1,1.1,0.2))

# %%
diff_time = ind_last10-ind_first10
sept.visu_composite_spa(diff_time,plev = 20000,levels=np.arange(-1,1.1,0.2))
# %%
