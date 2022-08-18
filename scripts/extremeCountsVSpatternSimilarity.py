#%%
import xarray as xr
from Teleconnection.temporal_index import index_changing_pattern
# %%
import src.Teleconnection.eof_plots as sept



# %%
indChangingEof = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/ind_EOF.nc").eof
depChangingEof = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/changingPattern/dep_EOF.nc").eof

#%%
indF = indChangingEof.isel(time = 0)
indL = indChangingEof.isel(time = -1)

depF = depChangingEof.isel(time = 0)
depL = depChangingEof.isel(time = -1)

#%%
indA = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/allPattern/ind_EOF_nonstd.nc").eof
depA = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/allPattern/dep_EOF_nonstd.nc").eof


#%%
sept.visu_eof_single(indChangingEof.isel(hlayers = 0, time = 0).eof)
# %%
