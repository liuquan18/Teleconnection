"""
This file generate the seasonal pc, from different fixed patterns,
which is also different in all levels. 
The scripts should generate 9 index.
    spatial pattern: all    first10    last10
    temporal pattern:
    all               X       X           X
    first10           X       X           X
    last10            X       X           X
"""
# imports
import numpy as np
import pandas as pd
from pyparsing import line
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import scipy.stats as stats
import pylab 

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.pattern_statistic as sps
import src.Teleconnection.index_statistic as sis
import src.Teleconnection.eof_plots as sept
import src.Teleconnection.temporal_index as sti

# Data load and pre-process
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
# split ens
splitens = ssp.split_ens(allens)
# demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')
#select traposphere
trop = demean.sel(hlayers = slice(20000,100000))
trop = trop.var156


# all periods on three patterns
print("independent index")
all_all_ind,all_first_ind,all_last_ind = sti.index_diff_pattern(trop,
independent=True,standard=True)

print("dependent index")
all_all_dep, all_first_dep,all_last_dep = sti.index_diff_pattern(trop,
independent=False, standard=True)

#save the data
all_all_ind.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind.nc')
all_first_ind.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_first_ind.nc')
all_last_ind.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_ind.nc')

all_all_dep.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_dep.nc')
all_first_dep.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_frist_dep.nc')
all_last_dep.to_netcdf('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_dep.nc')

