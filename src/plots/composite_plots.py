from typing_extensions import assert_type
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import cartopy.crs as ccrs


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


def lastfirst_comp_map(first, last, mode, levels=np.arange(-2e-05, 2e-05, 0.2e-05)):
    """
    rows for time (first10, last10)
    cols for extr_type (pos, neg)
    """

    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)

    fig, axes = plt.subplots(
        2, 2, figsize=(8, 8), dpi=500, subplot_kw={"projection": proj}
    )

    data = [first.sel(mode=mode), last.sel(mode=mode)]
    extr_type = ["pos", "neg"]
    periods = ["first10", "last10"]

    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for first10, last10.
            data_p = data[j].sel(extr_type=extr_type[i])
            im = col.contourf(
                data_p.lon,
                data_p.lat,
                data_p,
                levels=levels,
                extend="both",
                transform=ccrs.PlateCarree(),
                cmap="RdBu_r",
            )
            col.set_title(f"extreme:{extr_type[i]} period: {periods[j]}")

    fig.subplots_adjust(hspace=0.05, wspace=0.05, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.2, 0.03, 0.6])
    fig.colorbar(im, cax=cbar_ax, label="precip-anomaly")

    plt.show()
