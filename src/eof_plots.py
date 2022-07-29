import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.path as mpath
from matplotlib.colorbar import Colorbar
import matplotlib.ticker as mticker

import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

import seaborn as sn
import numpy as np


def exp_time_height(exp_plot):
    """
    draw contourf of explained variance as function of time and height.
    """

    fig,axes = plt.subplots(1,3,figsize = (14,4),dpi = 150)
    naoexp= exp_plot.sel(hlayers = slice(200,1000),mode = 'NAO').plot(x = 'time',y = 'hlayers',
                                                        ax = axes[0],
                                                        levels = np.arange(30,46,2),
                                                        extend = 'both'
                                                                    )
    eaexp = exp_plot.sel(hlayers = slice(200,1000),mode = 'EA').plot(x = 'time',y = 'hlayers',
                                                        ax = axes[1],
                                                        # levels = np.arange(12,20,0.5),
                                                        extend = 'both')

    axes[0].set_ylim(1000,200)
    axes[1].set_ylim(1000,200)


    axes[0].set_ylabel("gph/hpa")
    axes[1].set_ylabel(None)

    naocb = naoexp.colorbar.ax
    naocb.set_ylabel('exp/%')

    eacb = eaexp.colorbar.ax
    eacb.set_ylabel('exp/%')

    axes[0].set_title("NAO explained variance")
    axes[1].set_title("EA explaeined variance")
# plt.savefig('/work/mh0033/m300883/output_plots/gr19/exp_var_allhieght.png')
    plt.show()

def axbuild(ax):
    
    theta = np.linspace(0,2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    
    
    # ax.coastlines()
    gl=ax.gridlines(crs = ccrs.PlateCarree(),draw_labels=False)
    gl.xformatter = LongitudeFormatter(zero_direction_label=False)
    gl.xlocator = mticker.FixedLocator(np.arange(-180,180,45))

    gl.ylocator = mticker.FixedLocator([20,40,60])
    gl.yformatter = LatitudeFormatter()

    ax.get_extent(crs = ccrs.PlateCarree())
    ax.set_extent([-180,180,20,90],crs = ccrs.PlateCarree())
    ax.set_boundary(circle, transform=ax.transAxes)

def visu_eofspa(eofs):
    fig,axes = plt.subplots(2,2,figsize = (8,8),
                        subplot_kw={'projection':
                                    ccrs.LambertAzimuthalEqualArea(
                                        central_longitude=0.0,
                                        central_latitude=90.0)
                                    })                     
    for ax in axes.flat:
        axbuild(ax)
    plev = ['500hpa','850hpa']
    mode = ['NAO','EA']
        
    for i,row in enumerate(axes): # plev
        for j, col in enumerate(row):  # mode
            data = eofs.isel(time = 0, plev = i, mode = j).values
            im = col.contourf(eofs.lon,eofs.lat,data,
                        levels = np.arange(-40,40.1,5.0),
                        extend = 'both',
                        transform = ccrs.PlateCarree(),
                        cmap = 'RdBu_r'
                        )
            col.set_title(f'plev:{plev[i]} mode:{mode[j]}')
    fig.subplots_adjust(hspace = 0.05,wspace = 0.05,right = 0.8)
    cbar_ax = fig.add_axes([0.85, 0.2, 0.03, 0.6])
    fig.colorbar(im, cax=cbar_ax,label = 'eofs')

    plt.show()