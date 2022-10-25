#%%
import importlib
from os import sched_param

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr

import cartopy.feature as cfeat
import matplotlib.pyplot as plt

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point


import src.composite.composite as scp
import src.plots.composite_plots as spcp

importlib.reload(spcp)
importlib.reload(scp)
# %% Composite analysis
# u10
udata = scp.field_composite("u10", "dep", hlayer=100000)

# v10
vdata = scp.field_composite("v10", "dep", hlayer=100000)

# erase the white line
udata = [erase_white_line(da) for da in udata]
vdata = [erase_white_line(da) for da in vdata]


#%%
# function to erase the white line
def erase_white_line(data):
    data = data.transpose(..., "lon")  # make the lon as the last dim
    dims = data.dims  # all the dims
    res_dims = [dim for dim in dims if dim != "lon"]  # dims apart from lon

    # add one more longitude to the data
    data_value, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    # make the lons as index
    lon_dim = xr.IndexVariable(
        "lon", lons, attrs={"standard_name": "longitude", "units": "degrees_east"}
    )

    # the new coords with changed lon
    new_coords = res_dims + [lon_dim]  # changed lon but new coords

    new_data = xr.DataArray(data_value, coords=new_coords, name=data.name)

    return new_data


#%% to iris cube
def xr2iris(data, mode, extr_type, var="u10", long_name="10m u-velocity"):

    # select one map
    data = data.sel(mode=mode, extr_type=extr_type)
    data = data.drop_vars(["hlayers", "mode", "extr_type"])

    # standard
    glo_Con = "CF-1.8"
    data.attrs["Conventions"] = glo_Con
    data.attrs = {"long_name": long_name, "units": "m/s"}
    data = data.to_iris()

    return data


# %% Visulization

proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
mode = "EA"
extr_type = ["pos", "neg"]
periods = ["first10", "last10", "last10 - first10"]


fig = plt.figure(figsize=(12, 6), dpi=150)

for i in range(2):  # rows for extr_type
    for j in range(3):  # cols for periods

        axes = plt.subplot(2, 3, j + (i * 3) + 1, projection=proj)
        axes = spcp.buildax(axes)

        u = xr2iris(
            udata[j],
            mode=mode,
            extr_type=extr_type[i],
            var="u10",
            long_name="10m u-velocity",
        )

        v = xr2iris(
            vdata[j],
            mode=mode,
            extr_type=extr_type[i],
            var="v10",
            long_name="10m v-velocity",
        )

        windspeed = (u**2 + v**2) ** 0.5
        windspeed.rename("windspeed")

        # Plot the wind speed as a contour plot.
        qplt.contourf(
            windspeed,
            np.arange(0.2, 4.1, 0.4),
            transform=ccrs.PlateCarree(),
            add_colorbar=False,
            zorder=20,
        )
        cb = plt.colorbar()
        cb.remove()
        plt.gca().coastlines(linewidth=0.3)

        # Add arrows to show the wind vectors.
        iplt.quiver(
            u[::6, ::6],
            v[::6, ::6],
            pivot="middle",
            width=0.003,
            scale=30,
            units="width",
            transform=ccrs.PlateCarree(),
            zorder=100,
        )

        plt.title("composite wind")

# %%
