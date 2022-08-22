#%%
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%
eof_ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/allPattern/dep_EOF_nonstd.nc")
# %%
eof_ex = eof_ex.eof
# %%
index = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/allPattern/dep_index_nonstd.nc")
# %%
index = index.pc
# %%
eof = eof_ex.sel(hlayers = 50000)
# %%
index = index.sel(hlayers = 50000)
# %%
