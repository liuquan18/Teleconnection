import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt

import src.plots.utils as utils


def composite_gph(first, last, levels, hlayers=100000):
    """
    composite map of first10 and last10 years, contourf and contour
    respectively.
    """
    proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
    fig, axes = plt.subplots(
        2,
        2,
        dpi=300,
        subplot_kw={"projection": proj},
    )

    periods = ["first10", "last10"]
    modes = ["NAO", "EA"]
    extr_type = ["pos", "neg"]
    levels = levels

    shadings = []
    for i, row in enumerate(axes):  # for extr_type
        for j, col in enumerate(row):  # for modes
            data_first = first.sel(
                extr_type=extr_type[i], mode=modes[j], hlayers=hlayers
            )
            data_last = last.sel(extr_type=extr_type[i], mode=modes[j], hlayers=hlayers)

            lats = data_first.lat
            lons = data_first.lon

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
            with mpl.rc_context({"lines.linewidth": 0.6}):
                iml = col.contour(
                    lons,
                    lats,
                    data_last,
                    levels=levels,
                    extend="both",
                    colors="k",
                    linewidth=0.1,
                    transform=ccrs.PlateCarree(),
                )

            col.set_title(f"{modes[j]}  {extr_type[i]}")
            utils.buildax(col, alpha_grid=0.3, alpha_coast=0.3)
    fig.subplots_adjust(hspace=0.3, wspace=0.1, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.5])
    cbar = fig.colorbar(
        imf,
        cax=cbar_ax,
        label="gph / std",
    )

    plt.show()
