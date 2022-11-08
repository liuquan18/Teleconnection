#%%
import xarray as xr
import numpy as np
import pandas as pd
import src.composite.composite as comp

# %%

#%%
# genrate random temporal index
period_time = pd.date_range("2010-10-01", "2021-10-01", freq="Y")

period_values = np.arange(-5, 6, 1)
np.random.seed(0)

index = xr.DataArray(period_values, dims=["time"], coords={"time": period_time})

# %%

values_data = np.random.randn(11,10,10)
lon = np.arange(10)
lat = np.arange(10)
data = xr.DataArray(values_data,dims = ['time','lat','lon'],coords = {'time':period_time,'lat':lat,'lon':lon})


# %%
comp._composite(index,data)
# %%
