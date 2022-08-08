import enum
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.path as mpath
from matplotlib.colorbar import Colorbar
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches


import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)

import seaborn as sns
import numpy as np
import xarray as xr


import sys
sys.path.append("..")
import src.spatial_pattern as ssp
import src.index_statistic as sis

import importlib
importlib.reload(ssp) # after changed the source code
importlib.reload(sis)



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
    EOFmaps = eof.plot.contourf('lon','lat',col = 'mode',
                                        levels = np.arange(-1,1.1,0.2),
                                        extend = 'both',
                                        subplot_kws=dict(projection = ccrs.LambertAzimuthalEqualArea(central_longitude=0.0,
                                                                                                    central_latitude=90.0),
                                                        )
                                        ,transform = ccrs.PlateCarree(),add_colorbar = True )

    for i,ax in enumerate(EOFmaps.axes.reshape(-1)):
        axbuild(ax)
        
        ax.set_title(f'mode={eof.mode[i].values}')
        
        
    fig = EOFmaps.fig
    fig.set_figheight(6)
    fig.set_figwidth(13.5)

    EOFmaps.cbar.set_label("gph/m")
    plt.show()

def visu_spatial_type(eofs,plev,mode = 'EA'):

    all_eof,first_eof,last_eof = [eof.sel(hlayers = plev) for eof in eofs]
    eof = xr.concat([first_eof,all_eof,last_eof],dim = 'type',coords='minimal',compat='override')
    eof['type'] = ['first','all','last']

    EOFmaps = eof.sel(mode=mode).plot.contourf('lon','lat',col = 'type',
                                        levels = np.arange(-1,1.1,0.2),
                                        extend = 'both',
                                        subplot_kws=dict(projection = ccrs.LambertAzimuthalEqualArea(central_longitude=0.0,
                                                                                                    central_latitude=90.0),
                                                        )
                                        ,transform = ccrs.PlateCarree(),add_colorbar = True )

    for i,ax in enumerate(EOFmaps.axes.reshape(-1)):
        axbuild(ax)
        
        ax.set_title(f'{eof.type[i].values}')
        
        
    fig = EOFmaps.fig
    fig.set_figheight(6)
    fig.set_figwidth(13.5)

    EOFmaps.cbar.set_label("gph/m")
    plt.suptitle(f"plev = {plev}")
    plt.show()


def tenyr_hist(data,hlayer = 50000,bins = 50):
    """
    visu 2d histplots of first-first---first-all, last-last---last-all
    """

    if hlayer == 'all':
        data = data
    else:
        data = data.loc[hlayer]
    fig,ax = plt.subplots()
    hf = sns.histplot(data = data,x = 'pc_all',y = 'pc_first',
    ax = ax,color= 'b', bins = bins,label = 'first',legend = False,alpha = 0.9)

    hl = sns.histplot(data = data,x = 'pc_all',y = 'pc_last',
    ax = ax,color = 'r', bins = bins,label = 'last',legend = False,alpha = 0.9)

    line = ax.plot(np.arange(-3,4,1),np.arange(-3,4,1),linestyle = 'dotted',color = 'k')

    blue_patch = mpatches.Patch(color='blue',label="first")
    red_patch = mpatches.Patch(color='red', label='last')

    plt.legend(handles=[blue_patch,red_patch],loc = 'upper left')


def tenyr_scatter(first,last,hlayer = 'all'):
    """
    make scaterplots of first_on_first v.s first_on_all and last_on_last v.s last_on_all.
    """

    fig, axes = plt.subplots(1,2,figsize = (8,3.5),dpi = 150)
    plt.subplots_adjust(wspace = 0.3)
    modes = ['NAO','EA']
    for i,ax in enumerate(axes):
        if hlayer=='all':
            first_data,last_data = first.loc[:,modes[i],:],last.loc[:,modes[i],:]
        else:
            first_data,last_data = first.loc[hlayer,modes[i],:],last.loc[hlayer,modes[i],:]

        scaf = sns.scatterplot(data = first_data, x = 'pc_all',y = 'pc_first',
        ax = ax,label = 'first')
        scar = sns.scatterplot(data = last_data, x = 'pc_all',y = 'pc_last',
        ax = ax,label = 'last',color = 'r',alpha=0.3)
        
        line = ax.plot(np.arange(-5,5,1),np.arange(-5,5,1),linestyle = 'dotted',color = 'k')

        ax.legend(loc = 'upper left')
        ax.set_ylabel('pc/std')
        ax.set_xlabel('pc_all/std')
    axes[0].set_title("NAO")
    axes[1].set_title("EA")
    plt.suptitle("first_first on first_all and last_last on last_all")


def tenyr_scatter_extreme(first,last,hlayer = 'all'):
    """
    make scaterplots of two first_on_first_first_on_all and last_on_last_last_on_all.
    """

    fig, axes = plt.subplots(2,2,figsize = (7,7),dpi = 150)
    plt.subplots_adjust(wspace = 0.3,hspace = 0.3)
    modes = ['NAO','EA']
    for i,row in enumerate(axes.T):
        for ax in row:
            if hlayer=='all':
                first_data,last_data = first.loc[:,modes[i],:],last.loc[:,modes[i],:]
            else:
                first_data,last_data = first.loc[hlayer,modes[i],:],last.loc[hlayer,modes[i],:]

            scaf = sns.scatterplot(data = first_data, x = 'pc_all',y = 'pc_first',
            ax = ax,label = 'first')
            scar = sns.scatterplot(data = last_data, x = 'pc_all',y = 'pc_last',
            ax = ax,label = 'last',color = 'r',alpha=0.3)
            
            line = ax.plot(np.arange(-5,5,1),np.arange(-5,5,1),linestyle = 'dotted',color = 'k')

            ax.legend(loc = 'upper left')
            ax.set_ylabel('pc/std')
            ax.set_xlabel('pc_all/std')


    axes[0,0].set_xlim(2,4)
    axes[0,0].set_ylim(2,4)

    axes[0,1].set_xlim(2,4)
    axes[0,1].set_ylim(2,4)

    axes[1,0].set_xlim(-4,-2)
    axes[1,0].set_ylim(-4,-2)
    axes[1,1].set_xlim(-4,-2)
    axes[1,1].set_ylim(-4,-2) 

    axes[0,0].set_title("NAO")
    axes[0,1].set_title("EA")


def scatter_extreme(*args,mode = 'NAO', hlayer = 'all'):
    """
    plot extreme scatter of one mode at all three periods (first10, last10, dynamic)
    **Arguments**
        *dfs* the three rows of dataframes to plot.
               for each period, dataframes of projection on first and last10 should be 
               included. e.g. [first_first_all, last_first_all]
    """
    nperiods = len(args)
    fig, axes = plt.subplots(2,nperiods,figsize = (8,5),dpi = 150) # rows for pos-neg, 
                                                                   # columns for periods.
    plt.subplots_adjust(hspace = 0.4,wspace = 0.4)
    for row in axes: # first row for positive extreme, second row for negative extreme
        for i, period in enumerate(args):
            if hlayer == 'all':
                firstPattern, lastPattern = [period_ten.loc[:,mode,:,:]
                for period_ten in period]
            else:
                firstPattern, lastPattern = [period_ten.loc[hlayer,mode,:,:]
                for period_ten in period]
            
            scatterfirst = sns.scatterplot(data = firstPattern,x = 'pc_all',y = 'pc_first',
            ax = row[i],label = 'first_pattern')
            scatterlast = sns.scatterplot(data = lastPattern,x = 'pc_all',y = 'pc_last',
            ax = row[i], label = 'last_pattern',color = 'r',alpha=0.5)

            line = row[i].plot(np.arange(-5,5,1),np.arange(-5,5,1),
            linestyle = 'dotted',color = 'k')

            row[i].legend(loc = 'upper left',fontsize = 7)
            row[i].set_ylabel("index")
            row[i].set_xlabel("index_all")
    for ax in axes[0]:
        ax.set_xlim(2,4)
        ax.set_ylim(2,4)
    for ax in axes[1]:
        ax.set_xlim(-4,-2)
        ax.set_ylim(-4,-2)
    axes[0,0].set_title("first 10 period")
    axes[0,1].set_title("dynamic")
    axes[0,2].set_title("last 10 period")

def extreme_bar(extreme_counts,mode = 'NAO',hlayer = 'all',ylim = 360):
    """
    plot the barplot of extreme counts. rows for 'pos' or 'neg'. cols for 'ind' or 'dep'
    **Arguments**
        *extreme_counts* the data for 'ind' and 'dep'.
        *mode* 'NAO' or 'EA'
    **Return**
        plots
    """
    fig,axes = plt.subplots(2,2,figsize = (6,3),dpi = 150)
    plt.subplots_adjust(hspace = 0)

    colors = ['#1f77b4', '#2ca02c', '#d62728']
    extr_type = ['pos','neg']

    for i, row in enumerate(axes):
        for j, col in enumerate(row): # ['ind' or 'dep']
            if hlayer == 'all':
                data = sis.all_layer_counts(extreme_counts[j]).loc[extr_type[i],mode]
            else:
                data = extreme_counts[j].loc[extr_type[i],mode,hlayer]
            sns.barplot(data = data, x = 'period',y = 'extreme_counts',ax = col,
            hue = 'pattern', hue_order=['first','all','last'],palette = colors)
            if i ==0:
                col.set_ylim(0,ylim)
            if i ==1:
                col.set_ylim(ylim,0)

    axes[0,0].set_ylabel("positive")
    axes[1,0].set_ylabel("negative")

    axes[0,1].set_ylabel(None)
    axes[1,1].set_ylabel(None)
    axes[0,1].get_legend().remove()
    axes[1,0].get_legend().remove()
    axes[1,1].get_legend().remove()
    axes[0,0].legend(loc = 'upper left')


def extreme_allh_line(extreme_count):
    """
    plot the vertical profile of extreme counts. 
    x-axis the counts, y-axis the height. different color the pattern,
    solid or dashed for pos or negative. different panel for periods.
    **Arguments**
        *extreme_count* a dataframe produced by function sis.extr_count_df
    """
    fig, axes = plt.subplots()