import checkdoc

#%%
import xarray as xr
import pandas as pd
import numpy as np

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.tools as tools
# %%
ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/sample.nc")
# %%
data = ex.isel(hlayers = 0).var156
# %%
data = xr.
eof,pc,fra = ssp.doeof(ex,nmode = 1)
# %%
