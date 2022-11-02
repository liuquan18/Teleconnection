import importlib

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.tools as tools

# genrate random data
time = pd.date_range("2010-10-01", "2020-10-01", freq="Y")
lon = np.linspace(-180, 180, 30)
lat = np.linspace(-90, 90, 30)
ens = np.arange(20)
hlayers = np.linspace(1000, 100, 20)
values = np.random.random((10, 30, 30, 20, 20))  # time, lon, lat, ens, hlayers

ex = xr.DataArray(
    values,
    dims=["time", "lon", "lat", "ens", "hlayers"],
    coords={"time": time, "lon": lon, "lat": lat, "ens": ens, "hlayers": hlayers},
)
data = ex.isel(hlayers=0)
data = tools.stack_ens(data, withdim="time")
eof, pc, fra = ssp.doeof(data, nmode=2)

# do eof
def test_doeof():
    assert fra.sum().values > 0
