#%%
import xarray as xr
import numpy as np
import src.Teleconnection.season_eof as season_eof
import src.Teleconnection.tools as tools
import src.extreme.period_pattern_extreme as extreme

#%%
import importlib
importlib.reload(extreme)

#%%
# config
vertical_eof = 'dep'  # independently decompose each altitude levels
pattern = 'all'       # project onto the 'all' pattern (150 years and 100 ensemble members)

if vertical_eof == 'ind':
    independent = True
elif vertical_eof == 'dep':
    independent = False
# %%
# data
print("data reading")
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
print("decomposing first data...")

# all_fist, all_last and all_all, without the standardarization
_, all_first, _ = season_eof.season_eof(
    trop, nmode=2, window=10, fixed_pattern=pattern, 
    independent=independent, standard=False
)


# %%
print("decomposing last data...")
_, all_last, _ = season_eof.season_eof(
    trop, nmode=2, window=10, fixed_pattern="first", independent=True, standard=False
)

#%%
print("decomposing all data...")
eof_all_all, all_all, _ = season_eof.season_eof(
    trop, nmode=2, window=10, fixed_pattern="all", independent=True, standard=False
)

# %%
# select the first10 and last10 years
print("select periods ...")
first10_first = all_first.isel(time=slice(0, 10))
last10_last = all_last.isel(time=slice(-10, all_last.time.size))

#%%
# Normalize with the mean and std of all_all
print("Normalizing...")
first10_first = extreme.normalize(first10_first, all_all,dim = ('ens','time'))
last10_last = extreme.normalize(last10_last, all_all, dim = ('ens','time'))

#%%
# save
print("saving...")
first10_first.to_netcdf(
    "/work/mh0033/m300883/3rdPanel/data/first_last/dep/std_all/first10_first.nc"
)
last10_last.to_netcdf(
    "/work/mh0033/m300883/3rdPanel/data/first_last/dep/std_all/last10_last.nc"
)

#save all
# %%
all_first.to_netcdf("/work/mh0033/m300883/3rdPanel/data/allPattern/ind/first_pattern/all_first_nonstd.nc")
all_last.to_netcdf("/work/mh0033/m300883/3rdPanel/data/allPattern/ind/last_pattern/all_last_nonstd.nc")
all_all.to_netcdf("/work/mh0033/m300883/3rdPanel/data/allPattern/ind/all_pattern/all_all_nonstd.nc")

# %%
# save the spatial pattern for visulazation

# %%
eof_all_all.to_netcdf("/work/mh0033/m300883/3rdPanel/data/allPattern/ind/first_pattern/all_all_eof.nc")
# %%
