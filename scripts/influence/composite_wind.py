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
import src.plots.utils as spu

importlib.reload(spcp)
importlib.reload(scp)
importlib.reload(spu)
# %% Composite analysis
# u10
udata = scp.field_composite("u10", "dep", hlayer=100000)

# v10
vdata = scp.field_composite("v10", "dep", hlayer=100000)

# erase the white line
udata = [spu.erase_white_line(da) for da in udata]
vdata = [spu.erase_white_line(da) for da in vdata]

#%%
# windspeed
windspeed = [(udata[i] ** 2 + vdata[i] ** 2) ** 0.5 for i in range(2)]
windspeed.append(windspeed[1] - windspeed[0])

#%% to iris cube
def xr2iris(data, mode, extr_type, long_name="10m u-velocity"):

    # select one map
    data = data.sel(mode=mode, extr_type=extr_type)
    data = data.squeeze()

    # standard
    glo_Con = "CF-1.8"
    data.attrs["Conventions"] = glo_Con
    data.attrs = {"long_name": long_name, "units": "m/s"}
    data = data.to_iris()

    return data


# %% Visulization
def wind_plots(mode):
    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
    mode = mode
    extr_type = ["pos", "neg"]
    periods = ["first10", "last10", "Diff"]


    fig = plt.figure(figsize=(10, 6), dpi=200)
    for i in range(2):  # rows for extr_type
        for j in range(3):  # cols for periods

            axes = plt.subplot(2, 3, j + (i * 3) + 1, projection=proj)
            axes = spu.buildax(axes, zorder=40)

            u = xr2iris(
                udata[j],
                mode=mode,
                extr_type=extr_type[i],
                long_name="10m u-velocity",
            )

            v = xr2iris(
                vdata[j],
                mode=mode,
                extr_type=extr_type[i],
                long_name="10m v-velocity",
            )

            wspd = xr2iris(
                windspeed[j],
                mode=mode,
                extr_type=extr_type[i],
                long_name=periods[j],
            )

            # Plot the wind speed as a contour plot.
            contourf = qplt.contourf(
                wspd,
                np.arange(-3.0,3.1,0.5),
                zorder=20,
                extend="max",
                cmap="RdBu",
            )
            cb = contourf.colorbar
            cb.remove()

            plt.gca().coastlines(linewidth=0.3, zorder=30)

            # Add arrows to show the wind vectors.
            iplt.quiver(
                u[::5, ::5],
                v[::5, ::5],
                pivot="middle",
                width=0.003,
                scale=25,
                units="width",
                zorder=100,
            )
    plt.subplots_adjust(bottom=0.15, wspace = 0.001)
    cbar_ax = fig.add_axes([0.33, 0.1, 0.4, 0.03])
    fig.colorbar(contourf, cax=cbar_ax, label="windspeed", orientation="horizontal")
    plt.show()

# %%
print("="*5+"NAO"+"="*5)
wind_plots("NAO")
# plt.savefig("/work/mh0033/m300883/3rdPanel/docs/source/plots/wrap_up_aftervoc/NAO_wind_composite.png",dpi = 200)

#%%
print("="*5+"EA"+"="*5)
wind_plots("EA")
# plt.savefig("/work/mh0033/m300883/3rdPanel/docs/source/plots/wrap_up_aftervoc/EA_wind_composite.png",dpi = 200)

# %%
