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
    return ax

def visu_eofspa(eofs,plev = [50000,85000]):
    fig,axes = plt.subplots(2,2,figsize = (8,8),
                        subplot_kw={'projection':
                                    ccrs.LambertAzimuthalEqualArea(
                                        central_longitude=0.0,
                                        central_latitude=90.0)
                                    })                     
    for ax in axes.flat:
        axbuild(ax)
    
    mode = ['NAO','EA']
        
    for i,row in enumerate(axes): # plev
        for j, col in enumerate(row):  # mode
            data = eofs.sel(hlayers = plev[i], mode = mode[j]).values
            im = col.contourf(eofs.lon,eofs.lat,data,
                        levels = np.arange(-1,1.1,0.2),
                        extend = 'both',
                        transform = ccrs.PlateCarree(),
                        cmap = 'RdBu_r'
                        )
            col.set_title(f'plev:{plev[i]} mode:{mode[j]}')
    fig.subplots_adjust(hspace = 0.05,wspace = 0.05,right = 0.8)
    cbar_ax = fig.add_axes([0.85, 0.2, 0.03, 0.6])
    fig.colorbar(im, cax=cbar_ax,label = 'eofs')

    plt.show()


def visu_eofspa_all(eofs,mode = 'EA'):

    cols = len(eofs.hlayers)//3+1
    fig,axes = plt.subplots(3,cols,figsize = (3*3,3*cols),
                        subplot_kw={'projection':
                                    ccrs.LambertAzimuthalEqualArea(
                                        central_longitude=0.0,
                                        central_latitude=90.0)
                                    })                     
    for i,ax in enumerate(axes.flat):
        axbuild(ax)
        if i < len(eofs.hlayers):
            data = eofs.sel(mode=mode).isel(hlayers = i).values
            im = ax.contourf(eofs.lon,eofs.lat,data,
                            levels = np.arange(-1,1.1,0.2),
                            extend = 'both',
                            transform = ccrs.PlateCarree(),
                            cmap = 'RdBu_r'        
            )
            ax.set_title("eof {}".format(eofs.isel(hlayers = i).hlayers.values))
    cbar_ax = fig.add_axes([0.85, 0.2, 0.03, 0.6])
    fig.colorbar(im, cax=cbar_ax,label = 'eofs')

    plt.show()
def visu_eof_single(eof):
    fig,ax = plt.subplots(1,1,subplot_kw={'projection':
                                    ccrs.LambertAzimuthalEqualArea(
                                        central_longitude=0.0,
                                        central_latitude=90.0)})
    ax = axbuild(ax)
    im = ax.contourf(eof.lon.values,eof.lat.values,eof.values,
                            levels = np.arange(-1,1.1,0.2),
                            extend = 'both',
                            transform = ccrs.PlateCarree(),
                            cmap = 'RdBu_r'      
    )
    cbar_ax = fig.add_axes([0.85, 0.2, 0.03, 0.6])
    fig.colorbar(im, cax=cbar_ax,label = 'eofs')
    plt.show()
