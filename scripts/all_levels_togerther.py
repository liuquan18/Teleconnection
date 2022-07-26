# script for all levels together, common patterns. 
#%%
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

#%%
import sys
sys.path.append("..")
import src.spatial_pattern as sp

import importlib
importlib.reload(sp) # after changed the source code

# %%
ex = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/sep_ens_season.nc")
# %%
ex
# %%
sex = ex.var156.sel(ens = 0,plev = 50000)
# %%
sex
# %%
eof,pc,fra = sp.doeof(sex,dim = 'time')
# %%
ppc = sp.project_field(sex,eof)
# %%
