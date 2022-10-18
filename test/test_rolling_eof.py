import importlib

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import src.Teleconnection.rolling_eof as rolling_eof
import src.Teleconnection.tools as tools

importlib.reload(rolling_eof)

# genrate random data
time = pd.date_range("2000-10-01", "2020-10-01", freq="Y")
lon = np.linspace(-180, 180, 30)
lat = np.linspace(-90, 90, 30)
ens = np.arange(20)
hlayers = np.linspace(1000, 100, 20)
values = np.random.random((20, 30, 30, 20, 20))  # time, lon, lat, ens, hlayers

ex = xr.DataArray(
    values,
    dims=["time", "lon", "lat", "ens", "hlayers"],
    coords={"time": time, "lon": lon, "lat": lat, "ens": ens, "hlayers": hlayers},
)

# rolling eof on generated dataset.
eof, pc, fra = rolling_eof.rolling_eof(ex, nmode=2, window=6, fixed_pattern="False")


# test
def test_rolling_eof():
    assert len(ex) == 20
