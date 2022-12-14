import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LatitudeLocator, LongitudeFormatter
from cartopy.util import add_cyclic_point
from matplotlib.colorbar import Colorbar
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable

import src.plots.utils as utils


def comp_count_plot(count: xr.DataArray, mode: str):
    """
    plot the barplot of the extreme counts
    """
    count = count.sel(mode=mode).to_dataframe()
    count = count[["pc"]].unstack(1)
    count.plot(kind="bar", stacked=True)


def lastfirst_comp_map(
    first,
    last,
    mode,
    levels=np.arange(-1.5e-05, 1.6e-05, 0.5e-05),
    unit=r"precip / $m^{-2} s^{-2}$",
):
    """
    rows for time (first10, last10)
    cols for extr_type (pos, neg)
    """

    data = [
        first.sel(mode=mode),
        last.sel(mode=mode),
        last.sel(mode=mode) - first.sel(mode=mode),
    ]
    extr_type = ["pos", "neg"]
    periods = ["first10", "last10", "last10 - first10"]

    fig, axes = axes_grid(2, 3)

    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for first10, last10.
            data_p = data[j].sel(extr_type=extr_type[i])
            im = contourf(col, data_p, levels)
            col.set_title(f"{extr_type[i]}  {periods[j]}")
            utils.buildax(col)

    cbar_ax = cbar(levels, unit, fig, im)
    if "precip" in unit:
        cbar_ax.set_yticklabels(np.arange(-1.5, 1.6, 0.5).astype(str))
        cbar_ax.set_title("1e-5", pad=20)

    plt.show()


def cbar(levels, unit, fig, im):
    fig.subplots_adjust(hspace=-0.2, wspace=0.2, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.5])
    cbar = fig.colorbar(
        im,
        cax=cbar_ax,
        label=unit,
        ticks=levels,
    )

    return cbar_ax


def contourf(ax, data, levels):
    lats = data.lat
    data_c, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    im = ax.contourf(
        lons,
        lats,
        data_c,
        levels=levels,
        extend="both",
        transform=ccrs.PlateCarree(),
        cmap="RdBu_r",
    )

    return im


def axes_grid(
    nrow=2, ncol=3, proj=ccrs.Orthographic(central_longitude=-20, central_latitude=60)
):
    fig, axes = plt.subplots(
        nrow, ncol, figsize=(10, 8), dpi=500, subplot_kw={"projection": proj}
    )

    return fig, axes


def lastfirst_comp_var(
    precip,
    t2max,
    tsurf,
    mode,
):
    """
    rows for time (first10, last10)
    cols for extr_type (pos, neg)
    """

    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)

    fig, axes = plt.subplots(
        2, 3, figsize=(10, 8), dpi=500, subplot_kw={"projection": proj}
    )

    data = [
        precip.sel(mode=mode),
        t2max.sel(mode=mode),
        tsurf.sel(mode=mode),
    ]

    # some index
    levels = [
        np.arange(-1.5e-05, 1.6e-05, 0.5e-05),
        np.arange(-3, 3.1, 1),
        np.arange(-3, 3.1, 0.5),
    ]
    units = [r"precip / $m^{-2} s^{-2}$", "K", "K"]

    extr_type = ["pos", "neg"]
    vars = ["precip", "t2max", "tsurf"]
    IM = []

    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for vars.
            data_p = data[j].sel(extr_type=extr_type[i])
            lats = data_p.lat
            data_c, lons = add_cyclic_point(data_p, coord=data_p.lon, axis=-1)

            im = col.contourf(
                lons,
                lats,
                data_c,
                levels=levels[j],
                extend="both",
                transform=ccrs.PlateCarree(),
                cmap="RdBu_r",
            )
            col.set_title(f"{extr_type[i]}  {vars[j]}")
            utils.buildax(col)

            if i == 1:
                divider = make_axes_locatable(col)
                cax = divider.append_axes(
                    "bottom", size="5%", pad="4%", map_projection=None
                )
                cbar = fig.colorbar(
                    im, cax=cax, label=units[j], orientation="horizontal"
                )

    plt.show()

