#%%
import xarray as xr
import numpy as np
import pandas as pd

#%%
import src.Teleconnection.index_statistic as sis
from src.EVT.peaks_over_threshold import get_extremes_peaks_over_threshold
from src.EVT.return_periods import get_return_periods
# %%
all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind.nc').pc
all_first_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_first_ind.nc').pc
all_last_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_ind.nc').pc

#%%
mean = all_all_ind.mean(dim = 'time')
std = all_all_ind.std(dim = 'time')
ex = (all_first_ind-mean)/std

# %%
ex = ex.isel(hlayers = 0, mode = 0,ens = 0)
# %%
df = ex.to_dataframe()
# %%
df
# %%
series = df['pc']
# %%
series
# %%
extreme_series = get_extremes_peaks_over_threshold(series,'high',2,r="24H")
# %%
rePeriod = get_return_periods(series,extreme_series,'POT','high')
# %%
