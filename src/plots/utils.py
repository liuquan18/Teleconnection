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

from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LatitudeLocator, LongitudeFormatter
from cartopy.util import add_cyclic_point
from matplotlib.colorbar import Colorbar
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LatitudeLocator, LongitudeFormatter
from cartopy.util import add_cyclic_point
from matplotlib.colorbar import Colorbar
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import AxesGrid, make_axes_locatable


import iris
import iris.plot as iplt
import iris.quickplot as qplt


# function to erase the white line
def erase_white_line(data):
    data = data.transpose(..., "lon")  # make the lon as the last dim
    dims = data.dims  # all the dims
    res_dims = tuple(dim for dim in dims if dim != "lon")  # dims apart from lon
    res_coords = [data.coords[dim] for dim in res_dims]    # get the coords

    # add one more longitude to the data
    data_value, lons = add_cyclic_point(data, coord=data.lon, axis=-1)

    # make the lons as index
    lon_dim = xr.IndexVariable(
        "lon", lons, attrs={"standard_name": "longitude", "units": "degrees_east"}
    )

    # the new coords with changed lon
    new_coords = res_coords + [lon_dim]  # changed lon but new coords

    new_data = xr.DataArray(data_value, coords=new_coords, name=data.name)

    return new_data




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

