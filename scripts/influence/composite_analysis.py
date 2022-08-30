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
import src.Teleconnection.composite as scp
import src.plots.composite_plots as spcp

#%%
import importlib

importlib.reload(sis)
importlib.reload(sti)
importlib.reload(ssp)
importlib.reload(sept)
importlib.reload(sps)
importlib.reload(scp)
importlib.reload(spcp)
# %%
# read data
var = "precip"

fname='/work/mh0033/m300883/3rdPanel/data/influence/'+var+'/'+'onepct_1850-1999_ens_1-100.'+var+'.nc'
file = xr.open_dataset(fname)
fdata = file[var]
# %%
# demean (ens-mean)
demean = fdata-fdata.mean(dim = 'ens')
# %%
