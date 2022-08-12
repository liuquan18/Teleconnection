# import 
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.Teleconnection.index_statistic as sis

# load data
## independent
all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind.nc').pc
changing_ind = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_index_nonstd.nc")

## dependent
all_all_dep = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_dep.nc').pc
changing_dep = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_index_nonstd.nc")


# %%
# transpose to the same order
all_all_ind = all_all_ind.transpose('time','ens','mode','hlayers')
all_all_dep = all_all_dep.transpose('time','ens','mode','hlayers')

# %%
# standardization
mean_ind = all_all_ind.mean(dim = 'time')
std_ind = all_all_ind.std(dim = 'time')
ind_std = (changing_ind - mean_ind)/std_ind

mean_dep = all_all_dep.mean(dim = 'time')
std_dep = all_all_dep.std(dim = 'time')
dep_std = (changing_dep - mean_dep)/std_dep
# %%
