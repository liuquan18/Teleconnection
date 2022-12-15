#%%
# import
#%%
import importlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr

import composite.composite as scp
import plots.eof_plots as sept
import plots.composite_var as spcp
import src.Teleconnection.index_statistic as sis
import src.Teleconnection.pattern_statistic as sps
import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.temporal_index as sti

importlib.reload(sis)
importlib.reload(sti)
importlib.reload(ssp)
importlib.reload(sept)
importlib.reload(sps)
importlib.reload(scp)
importlib.reload(spcp)
# %%
## dependent
all_all_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/allPattern/dep_index_nonstd.nc').pc
changing_dep = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_index_nonstd.nc").pc
all_all_dep = all_all_dep.transpose('time','ens','mode','hlayers')

mean_dep = all_all_dep.mean(dim = 'time')
std_dep = all_all_dep.std(dim = 'time')
dep_std = (changing_dep - mean_dep)/std_dep
# %%
