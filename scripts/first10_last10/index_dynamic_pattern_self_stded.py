#%%
import xarray as xr
import numpy as np

import src.Teleconnection.season_eof as season_eof
import src.Teleconnection.tools as tools

# %%
print("reading data...")
# data
allens = xr.open_dataset(
    "/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc"
)
# split ens
splitens = tools.split_ens(allens)

# demean ens-mean
demean = splitens - splitens.mean(dim="ens")

# select traposphere
trop = demean.sel(hlayers=slice(20000, 100000))

trop = trop.var156

# %%
# all_first_stdd
print("decomposign first 10")
_, all_first, _ = season_eof.season_eof(
    trop, nmode=2, window=10, fixed_pattern="first", independent=False, standard=False
)
# %%
print("decomposing last10..")
# all_last_stdd
_, all_last, _ = season_eof.season_eof(
    trop, nmode=2, window=10, fixed_pattern="last", independent=False, standard=False
)
# %%
print("selecting data...")
# select the first10 and last10 years.
first10_first = all_first.isel(time=slice(0, 10))
last10_last = all_last.isel(time=slice(-10, all_last.time.size))
# %%
print("standardizing...")
# first10_first = tools.standardize(first10_first)
# last10_last = tools.standardize(last10_last)

# def standardize(period_index):
#     mean = period_index.mean(dim = ('time','ens'))
#     std = period_index.std(dim = ('time','ens'))
#     return (period_index-mean)/std
    
# first10_first = standardize(first10_first)
# last10_last = standardize(last10_last)
#%%
# save
print("saving...")
first10_first.to_netcdf(
    "/work/mh0033/m300883/3rdPanel/data/first_last/dep/std_self/first10_first.nc"
)
last10_last.to_netcdf(
    "/work/mh0033/m300883/3rdPanel/data/first_last/dep/std_self/last10_last.nc"
)

# %%
