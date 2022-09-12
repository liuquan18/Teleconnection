from typing_extensions import assert_type
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.path as mpath
from matplotlib.colorbar import Colorbar

import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter, LatitudeLocator
from cartopy.util import add_cyclic_point
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl


def comp_count_plot(count: xr.DataArray, mode: str):
    """
    plot the barplot of the extreme counts
    """
    count = count.sel(mode=mode).to_dataframe()
    count = count[["pc"]].unstack(1)
    count.plot(kind="bar", stacked=True)


def vertical_profile(counts, mode="NAO"):
    """
    using matplotlib to plot the vertical profile.
    solve the problem of y-axis sort.
    """

    y = (counts["hlayers"] / 100).astype(int)

    # plot
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    plt.subplots_adjust(wspace=0.3)

    modes = counts.mode
    extr_types = counts.extr_type

    colors = ["#1f77b4", "#ff7f0e"]
    styles = ["solid", "dashed"]

    for i, mode in enumerate(modes):  # modes for different color
        for j, extr_type in enumerate(extr_types):  # dash or solid for extr_type
            data = counts.sel(mode=mode, extr_type=extr_type)
            ax.plot(data, y, c=colors[i], ls=styles[j])
    ax.set_ylim(1000, 200)
    ax.set_ylabel("gph/hpa")
    ax.set_xlabel("extreme_counts")

    # legend
    custom_lines = [
        Line2D([0], [0], color=colors[0]),
        Line2D([0], [0], color=colors[1]),
        Line2D([0], [0], color=None, alpha=0),
        Line2D([0], [0], color="k", ls=styles[0]),
        Line2D([0], [0], color="k", ls=styles[1]),
    ]
    type_legend = ax.legend(
        custom_lines, ["NAO", "EA", "", "pos", "neg"], loc="upper left"
    )
    ax.add_artist(type_legend)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_visible(True)


def buildax(ax):
    """
    add grid coastline and gridlines
    """
    ax.set_global()
    ax.coastlines(linewidth=0.5, alpha=0.7)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=0.5)
    gl.xformatter = LongitudeFormatter(zero_direction_label=False)
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 45))

    gl.ylocator = mticker.FixedLocator([20, 40, 60])
    gl.yformatter = LatitudeFormatter()


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

    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)

    fig, axes = plt.subplots(
        2, 3, figsize=(10, 8), dpi=500, subplot_kw={"projection": proj}
    )

    data = [
        first.sel(mode=mode),
        last.sel(mode=mode),
        last.sel(mode=mode) - first.sel(mode=mode),
    ]
    extr_type = ["pos", "neg"]
    periods = ["first10", "last10", "last10 - first10"]

    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for first10, last10.
            data_p = data[j].sel(extr_type=extr_type[i])
            lats = data_p.lat
            data_c, lons = add_cyclic_point(data_p, coord=data_p.lon, axis=-1)

            im = col.contourf(
                lons,
                lats,
                data_c,
                levels=levels,
                extend="both",
                transform=ccrs.PlateCarree(),
                cmap="RdBu_r",
            )
            col.set_title(f"{extr_type[i]}  {periods[j]}")
            buildax(col)

    fig.subplots_adjust(hspace=-0.2, wspace=0.2, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.5])
    cbar = fig.colorbar(
        im,
        cax=cbar_ax,
        label=unit,
        ticks=levels,
    )
    if "precip" in unit:
        cbar_ax.set_yticklabels(np.arange(-1.5, 1.6, 0.5).astype(str))
        cbar_ax.set_title("1e-5", pad=20)

    plt.show()


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
            buildax(col)

            if i == 1:
                divider = make_axes_locatable(col)
                cax = divider.append_axes(
                    "bottom", size="5%", pad="4%", map_projection=None
                )
                cbar = fig.colorbar(
                    im, cax=cax, label=units[j], orientation="horizontal"
                )

    plt.show()


def composite_gph(first, last, hlayers=100000):
    """
    composite map of first10 and last10 years, contourf and contour
    respectively.
    """
    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(10, 8),
        dpi=500,
        subplot_kw={"projection": proj},
    )

    periods = ["first10", "last10"]
    modes = ["NAO", "EA"]
    extr_type = ["pos", "neg"]
    levels = np.arange(-2.0, 2.1, 0.5)

    shadings = []
    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for modes
            data_first = first.sel(
                extr_type=extr_type[i], mode=modes[j], hlayers=hlayers
            )
            data_last = last.sel(extr_type=extr_type[i], mode=modes[j], hlayers=hlayers)

            lats = data_first.lat
            data_first, lons = add_cyclic_point(
                data_first, coord=data_first.lon, axis=-1
            )
            data_last, lons = add_cyclic_point(data_last, coord=data_last.lon, axis=-1)

            imf = col.contourf(
                lons,
                lats,
                data_first,
                levels=levels,
                extend="both",
                transform=ccrs.PlateCarree(),
                cmap="RdBu_r",
            )
            shadings.append(imf)
            with mpl.rc_context({"lines.linewidth": 1}):
                iml = col.contour(
                    lons,
                    lats,
                    data_last,
                    levels=levels,
                    colors="k",
                    linewidth=0.1,
                    transform=ccrs.PlateCarree(),
                )

            col.set_title(f"{modes[j]}  {extr_type[i]}")
            buildax(col)
    fig.subplots_adjust(hspace=0.3, wspace=0.5, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.5])
    cbar = fig.colorbar(
        imf,
        cax=cbar_ax,
        label="gph / m",
    )

    plt.show()
