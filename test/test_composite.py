#%%
import xarray as xr
import numpy as np
import pandas as pd
import src.composite.composite as comp
import pytest

# %%
import importlib
importlib.reload(comp)
#%%
# genrate random temporal index
time = pd.date_range("2010-10-01", "2021-10-01", freq="Y")

values_index = np.arange(-5, 6, 1)
np.random.seed(0)

index = xr.DataArray(values_index, dims=["time"], coords={"time": time})

values_data = np.ones((11,10,10))
lon = np.arange(10)
lat = np.arange(10)
data = xr.DataArray(values_data,dims = ['time','lat','lon'],coords = {'time':time,'lat':lat,'lon':lon})


# %%
composite = comp.composite(index,data,dim = 'time')
# %%
# test
def test_composite():
    assert composite.mean().values == 1
# %%
