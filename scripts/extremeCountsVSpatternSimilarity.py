#%%
import xarray as xr
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.pattern_statistic as sps
import src.Teleconnection.index_statistic as sis
import plots.eof_plots as sept
import src.Teleconnection.temporal_index as sti


import importlib

importlib.reload(sis)
importlib.reload(sti)
importlib.reload(ssp)
importlib.reload(sept)
importlib.reload(sps)


# first and last pattern
## changing EFO
indChangingEof = xr.open_dataset(
    "/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_EOF.nc"
).eof
depChangingEof = xr.open_dataset(
    "/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_EOF.nc"
).eof

### first and last pattern
indF = indChangingEof.isel(time=0)
indL = indChangingEof.isel(time=-1)

depF = depChangingEof.isel(time=0)
depL = depChangingEof.isel(time=-1)

# all pattern
indA = xr.open_dataset(
    "/work/mh0033/m300883/3rdPanel/data/allPattern/ind_EOF_nonstd.nc"
).eof
depA = xr.open_dataset(
    "/work/mh0033/m300883/3rdPanel/data/allPattern/dep_EOF_nonstd.nc"
).eof

# extreme counts
ind_extc = pd.read_csv("/work/mh0033/m300883/3rdPanel/data/extreme_counts/ind_extc.csv")
dep_extc = pd.read_csv("/work/mh0033/m300883/3rdPanel/data/extreme_counts/dep_extc.csv")

ind_rise = sis.period_diff(ind_extc.set_index(["extr_type", "mode", "hlayers"]))
dep_rise = sis.period_diff(dep_extc.set_index(["extr_type", "mode", "hlayers"]))

# diff from first pattern
ind_diff = sis.extc_diff_first(ind_rise)
dep_diff = sis.extc_diff_first(dep_rise)


# correlation from first eof
corr_cen = sis.spatial_corr(indA, indF, indL, center=True)
corr_uncen = sis.spatial_corr(indA, indF, indL, center=False)

# put counts rise and pattern chagne together
ind_cen = ind_diff.join(corr_cen)
ind_uncen = ind_diff.join(corr_uncen)

ind_cen["pattern_diff"] = 1 - ind_cen["eof"]
ind_uncen["pattern_diff"] = 1 - ind_uncen["eof"]


dep_cen = dep_diff.join(corr_cen)
dep_uncen = dep_diff.join(corr_uncen)
dep_cen["pattern_diff"] = 1 - dep_cen["eof"]
dep_uncen["pattern_diff"] = 1 - dep_uncen["eof"]

# scatter plot of count rise v.s pattern change centered 
# %%
sept.scatter_pattern_counts(ind_cen, dep_cen, mode="EA",fit_reg = False)
sept.scatter_pattern_counts(ind_cen, dep_cen, mode="NAO",fit_reg = False)


#%% uncentered
sept.scatter_pattern_counts(ind_uncen, dep_uncen, mode="EA")
sept.scatter_pattern_counts(ind_uncen, dep_uncen, mode="NAO")

# %%
