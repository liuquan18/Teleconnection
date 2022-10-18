
import importlib

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import src.Teleconnection.season_eof as season_eof
import src.Teleconnection.tools as tools

importlib.reload(season_eof)

# #%% real data
# ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/sample.nc")
# ex = ex.var156


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

eof,pc,fra = season_eof.season_eof(ex,nmode=2,
window=6,fixed_pattern='all',independent = True,standard=True)

# test
def test_season_eof():
    assert eof.hlayers == ex.hlayers
