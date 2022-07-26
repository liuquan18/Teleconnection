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
#%%
sex = ex.isel(time = slice(0,10),plev = slice(20,26),ens = slice(0,30))

#%%
sex = sp.standardize(sex)

# %%
sex = sex.var156.stack(com = ('time','ens'))
# %%
sex
# %%
eof,pc,fra = sp.doeof(sex,dim = 'com')

#%%
plt.plot(pc.sel(mode = 'NAO',plev = 100000,ens = 0))
# %%
ppc = sp.project_field(sex,eof)
#%%
plt.plot(ppc.sel(mode = 'NAO',plev = 100000,ens = 0))
# %%
ppc = sp.standardize(ppc)
# %%
