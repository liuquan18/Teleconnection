#%%
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
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
all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind.nc').pc
all_first_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_first_ind.nc').pc
all_last_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_ind.nc').pc
# %%

"""
fA,fF,fL = sti.period_index([all_all_ind,all_first_ind,all_last_ind],period = 'first10')
# %%
lA,lF,lL = sti.period_index([all_all_ind,all_first_ind,all_last_ind],period = 'last10')

# %%
fAe = sti.extreme(fA)
lAe = sti.extreme(lA)
# %%
fAec = sis.count_nonzero(fAe)
lAec = sis.count_nonzero(lAe)
# %%
fAec = fAec.to_dataframe()
lAec = lAec.to_dataframe()
# %%
fAec.columns = ['extreme_counts']
lAec.columns = ['extreme_counts']
# %%
allDiff = lAec[['extreme_counts']]-fAec[['extreme_counts']]
# %%

"""
#%%% index y
fAi,fFi,fLi = sti.period_extreme([all_all_ind,all_first_ind,all_last_ind],
period = 'first10')
#%%%
lAi,lFi,lLi = sti.period_extreme([all_all_ind,all_first_ind,all_last_ind],
period = 'last10')

#%% count y
fAc = sis.count_nonzero(fAi)
lAc = sis.count_nonzero(lAi)
#%%



#%%

#%%

#%%
firstc,lastc = sis.extreme_count([all_all_ind,all_first_ind,all_last_ind])
#%%

countdf = sis.extr_count_df(firstc,lastc)

#%%

diff = sis.period_diff(countdf)
# %%
# %%
diff = diff.unstack([0,1])
# %%
countdf = countdf.reset_index().set_index(['hlayers','pattern','extr_type','period'])\
    
# %%
