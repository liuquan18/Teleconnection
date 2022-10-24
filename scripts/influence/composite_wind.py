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


#%%
# split periods

def erase_while_line(data):
    lats = data.lat
    data_value, lons = add_cyclic_point(data, coord = data.lon, axis = -1)
    new_data = xr.DataArray(data_value,dims = data.dims,coords = {'lat':lats,'lon':lons})
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
udata = split_periods(uFirst, uLast)
vdata = split_periods(vFirst, vLast)

proj=ccrs.Orthographic(central_longitude=-20, central_latitude=60)
mode = "NAO"
extr_type = ["pos", "neg"]
periods = ["first10", "last10", "last10 - first10"]

for i in range(2):  # for extr_type
    for j in range(3):  # for periods

        axes = plt.subplot(2,3,j+(i*3)+1,projection = proj)


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
        qplt.contourf(windspeed, np.arange(0, 3.1, 0.5))

        # Add arrows to show the wind vectors.
        iplt.quiver(
            u[::6, ::6],
            v[::6, ::6],
            pivot="middle",
            width=0.003,
            scale=30,
            units="width",
        )

        plt.title("composite wind")

# %%
