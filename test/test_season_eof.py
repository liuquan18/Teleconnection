
import importlib

import numpy as np
import pandas as pd
import pytest
import xarray as xr

import src.Teleconnection.season_eof as season_eof
import src.Teleconnection.tools as tools

importlib.reload(season_eof)


ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/sample.nc")
ex = ex.var156

eof,pc,fra = season_eof.season_eof(ex,nmode=2,
window=10,fixed_pattern='all',independent = True,standard=True)

# test
def test_season_eof():
    assert eof.hlayers == ex.hlayers
