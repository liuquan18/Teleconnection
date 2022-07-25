
############ imports ###############
import xarray as xr
import numpy as np
import pandas as pd
from eofs.standard import Eof
from tqdm.notebook import trange, tqdm


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

########### functions to do pre-process ###########
def split_ens(xarr):
    """
    split a dataset generated by cdo -apply, where the 'plev' and 'ens' are mixed into 'plev' dim.
    Arguments:
        xarr: DataArray with plev and ens mixed.
    Returns:
        DataArray with splited dims.
    """

    # one dim: plev, i.e, the vetical gph of MPI-GE, the ture plev coordinate. 
    hlayers = np.array([1.00e+05, 9.25e+04, 8.50e+04, 7.75e+04, 7.00e+04, 6.00e+04, 5.00e+04,
        4.00e+04, 3.00e+04, 2.50e+04, 2.00e+04, 1.50e+04, 1.00e+04, 7.00e+03,
        5.00e+03, 3.00e+03, 2.00e+03, 1.00e+03, 7.00e+02, 5.00e+02, 3.00e+02,
        2.00e+02, 1.00e+02, 5.00e+01, 2.00e+01, 1.00e+01])

    # The other dim: ens, i.e, the index for ens
    ens = np.arange(100)

    # createa a multiindex which has the same length as the mix dim in xarr.
    ind = pd.MultiIndex.from_product((ens,hlayers),names=('ens','hlayers'))

    # replace the old coords with ind, and then unstack.
    replace = xarr.assign(plev = ind).unstack("plev")

    return replace


def rolling(xarr,win = 10):
    """
    rolling the xarr with a time window of 'win'. 
    Arguments:
        xarr: DataArray to be rolled.
        win: the window size
    Return:
        DataArray being rolled.
    """
    # using the rolling func in xarray.
    roller = xarr.rolling (time = win, center = True)

    # construct the rolling object to a DatArray
    rolled = roller.construct("windown_dim")

    return rolled


def stack_win_ens(xarr):
    """
    The first dim of input data for python-eofs-package standard interface should be 'time', but 
    here we do eof not along the time dim only, but the win (10) years of all ensembles. so should
    stack the dims 'win' and 'ens' together first.
    Arguments:
        xarr: the rolled DataArray to be stacked.
    Return:
        xarr: with the dim 'win' and 'ens' combined to 'com'. 
    """

    time_com_space = xarr.stack(com = ('ens','windown_dim'))
    return time_com_space

def standardize(xarr):
    """
    standardize the DataArray with the temporal mean and std.
    Arguments:
        xarr: The DataArray to be standarized.
    Returns:
        xarr: standarized DataArray 
    """
    time_mean = xarr.mean(dim = 'time')
    time_std = xarr.std(dim = 'time')
    return (xarr-time_mean)/time_std

########## Function to do EOF #####################

def sign_coef(eof):
    """
    function to calculate the coefficient for eof, so that the sign is consistent.
    for NAO, the positive NAO with a low in the North and high at the south.
    for EA, the positive EA with a low in the center.
    Arguments:
        eof: the eof (spatial pattern) to be changed. much include NAO and EA the same time.
    Returns:
        coefficient of NAO and EA in xarray.
    """
    # NAO
    coef_NAO = eof.sel(lat = slice(90,60),lon = slice(-70,-10),mode = 'NAO').mean(dim = ['lat','lon'])<0
    coef_NAO = (2*coef_NAO-1)  # to make 1 to 1 , 0 to -1

    # EA
    coef_EA = eof.sel(lat = slice(65,45),lon = slice(-40,40),mode = 'EA').mean(dim = ['lat','lon'])<0
    coef_EA = (2*coef_EA-1)

    return xr.concat([coef_NAO,coef_EA],dim = 'mode')

def detect_spdim(xarr):
    """
    output the length of the spatil dim. since some of the xarr is lon-lat, while some lon-lat-height.
    Arguments: 
        xarr: the DataArray, with spatil dim starting from the second dim. e.g, [com,lat,lon,height]
    Returns:
        np.array, the number of spatial dim, but with value of one.
    """
    # the number of spatial dims
    sp_dim_len = len(xarr.shape)-1 

    # output a np.array with same number of spatial dims.
    sp_dim = np.ones(sp_dim_len).astype('int')  # [1,1] or [1,1,1]
    return sp_dim


def sqrtcoslat (xarr):
    """
    calculte the square-root of the cosine of the latitude as the weight
    Arguments:
        xarr: the DataArray to calculate the weight, with the shape ['com','lat','lon',...]
    Returns:
        weight with the right shape.
    """
    # the shape of the weight should have the same number of spatial dims as the input DataArray. 
    # the first dim is lat of course, all the rest spatial dim should be 1.
    sp_dim = detect_spdim(xarr)
    weight_shape = np.hstack([-1,sp_dim[1:]]) # the size of 'lat' should not be 1.

    # cos of rad of latitude
    coslat = np.cos(np.deg2rad(xarr.lat)).clip(0.,1.)
    # sqrt
    wgts = np.sqrt(coslat.values).reshape(weight_shape)
    return wgts


def doeof(seasondata,nmode = 2):
    """
    do eof to seasonal data along a combined dim, which is gotten from the above function 
    'stack_win_ens'
    Arguments:
        seasondata: The data to be decomposed, where the first dim should be the dim of 'com' or 'time'.
        nmode: how many modes, mode=2,means NAO and EA respectively.
    Returns:
        eof: DataArray, spatial patterns scaled (multiplied) with the temporal std of seasonal index.
             has the same spatial size as the input seasondata.[mode, lat,lon,...]
        pc: DataArray, seasonal index, scaled (divided) by the temporal std of itself. [mode,time]]
        exp_var: explained variance of each mode. [mode]
    """
    
    # data pre-process
    seasondata = seasondata.transpose('com',...)

    # weights
    wgts = sqrtcoslat(seasondata)
    
    # EOF decompose
    solver = Eof(seasondata.values,weights = wgts,center = True)  
    eof = solver.eofs(neofs = nmode)     # (mode,lat,lon,...)
    pc = solver.pcs(npcs = nmode)        # (com,mode)
    fra = solver.varianceFraction(nmode) # (mode)
    
    # deweight
    eof_dw = eof/wgts
    
    # standarize coef
    std_pc = (np.std(pc,axis = 0)).astype('float64')  #(mode)
    dim_add_sp = np.hstack([-1,detect_spdim(seasondata)) #[-1,1,1] or [-1,1,1,1]
    std_pc_sp = std_pc.reshape(dim_add_sp) 

    # do standarization
    eof_stded = eof_dw*std_pc_sp
    pc_stded = pc/std_pc

    # xarray container for eof
    eof_cnt = seasondata.isel(com = slice(0,nmode))
    eof_cnt = eof_cnt.rename({'com':'mode'})
    eof_cnt['mode'] = ['NAO','EA']

    # to xarray
    eofx = eof_cnt.copy(data = eof_stded)
    
    frax = xr.DataArray(fra,dims= ['mode'],coords = {'mode':['NAO','EA']})
    
    
    # change sign
    coef = coefcal(eofx)
    eofx = eofx*coef
    

    return eofx,frax

'''
# In[ ]:





# In[ ]:





# In[ ]:





# # Do rolling EOF

# EOF

# In[48]:


validtime = pd.date_range('1856-01-31','1995-12-31',freq='A-JAN')


# In[49]:


validtime = season_data.sel(time = slice('1856','1995')).time


# In[51]:


from fastprogress import master_bar, progress_bar


# In[54]:


mb = master_bar(range(0, 26 ))


# In[58]:


mb = master_bar(range(0, 26 ))

# for all plevs
eofs = list()
pcs = list()
fras = list()

hlayers = season_data.hlayers

for i in mb:
    plev = hlayers[i]
    print(f"plev:{plev.values}")
    
    # for all valid time
    Fras = list()
    Eofs = list()
    
    for time in progress_bar(validtime,parent = mb):
        # print(f'year:{time.year}')
        data = season_data.sel(time = time,hlayers = plev)
        
        eof,fra = doeof(data)

        Eofs.append(eof)
        Fras.append(fra)
        
    FRAs = xr.concat(Fras, dim = validtime)
    EOFs = xr.concat(Eofs ,dim = validtime) 
    
    eofs.append(EOFs)
    fras.append(FRAs)
    


# In[ ]:





# In[ ]:





# In[59]:


Spap = xr.concat(eofs,dim =hlayers)
Expv = xr.concat(fras,dim =hlayers)


# In[60]:


Spap.name = 'eofs'
Expv.name = 'fras'


# In[61]:


# Spap.to_netcdf('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/EOF.nc')
# Expv.to_netcdf('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/FRA.nc')


# In[62]:


Spap


# In[ ]:





# # Explained variance

# In[11]:


Expv = xr.open_dataset('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/FRA.nc')
Spap = xr.open_dataset('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/EOF.nc')


# In[12]:


exp_plot = Expv.fras


# In[13]:


exp_plot['hlayers']=exp_plot['hlayers']/100
exp_plot = exp_plot*100
exp_sum = exp_plot.sel(mode = 'NAO')+exp_plot.sel(mode='EA')


# In[14]:


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

sumexp = exp_sum.sel(hlayers = slice(200,1000)).plot(x = 'time',y = 'hlayers',
                                                    ax = axes[2],
                                                     extend = 'both',
                                                     levels = np.arange(46,61,2)
                                                    )

axes[0].set_ylim(1000,200)
axes[1].set_ylim(1000,200)
axes[2].set_ylim(1000,200)


axes[0].set_ylabel("gph/hpa")
axes[1].set_ylabel(None)
axes[2].set_ylabel(None)

naocb = naoexp.colorbar.ax
naocb.set_ylabel('exp/%')

eacb = eaexp.colorbar.ax
eacb.set_ylabel('exp/%')

sumcb = sumexp.colorbar.ax
sumcb.set_ylabel('exp/%')

axes[0].set_title("NAO explained variance")
axes[1].set_title("EA explaeined variance")
axes[2].set_title("SUM explaeined variance")
# plt.savefig('/work/mh0033/m300883/output_plots/gr19/exp_var_allhieght.png')


# In[ ]:





# In[ ]:





# In[ ]:





# In[112]:


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



# gridspec inside gridspec
fig = plt.figure(figsize = (10,5),dpi = 150)

gs0 = gridspec.GridSpec(1, 2, figure=fig)

gs00 = gridspec.GridSpecFromSubplotSpec(4, 4, subplot_spec=gs0[0])

ax1 = fig.add_subplot(gs00[1:, :-1])
ax2 = fig.add_subplot(gs00[0, :-1])
ax3 = fig.add_subplot(gs00[1:, -1])

# the following syntax does the same as the GridSpecFromSubplotSpec call above:
gs01 = gs0[1].subgridspec(4, 4)

ax4 = fig.add_subplot(gs01[1:, :-1])
ax5 = fig.add_subplot(gs01[0, :-1])
ax6 = fig.add_subplot(gs01[1:, -1])

plt.suptitle("Explained Variance change")


exp_plot.sel(hlayers = slice(200,1000),mode = 'NAO').plot(x = 'time',y = 'hlayers',
                                                       ax = ax1,
                                                       levels = np.arange(30,46,2),
                                                       extend = 'both',add_colorbar = False,
                                                                 )
exp_plot.mean(dim = 'hlayers').sel(mode = 'NAO').plot(ax = ax2,color = 'k')
exp_plot.sel(hlayers = slice(200,1000)).mean(dim = 'time').sel(mode = 'NAO').plot(ax = ax3,y = 'hlayers',color = 'k')

ax1.set_ylim(1000,200)
ax3.set_ylim(1000,200)

exp_plot.sel(hlayers = slice(200,1000),mode = 'EA').plot(x = 'time',y = 'hlayers',
                                                       ax = ax4,
                                                       # levels = np.arange(30,46,2),
                                                       extend = 'both',add_colorbar = False,
                                                                 )
exp_plot.mean(dim = 'hlayers').sel(mode = 'EA').plot(ax = ax5,color = 'k')
exp_plot.sel(hlayers = slice(200,1000)).mean(dim = 'time').sel(mode = 'EA').plot(ax = ax6,y = 'hlayers',color = 'k')

ax4.set_ylim(1000,200)
ax6.set_ylim(1000,200)


# for ax in [ax2,ax3,ax5,ax6]:
#     ax.set_xlabel(None)
#     ax.set_ylabel(None)
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.set_title(None)

# axisy
for ax in [ax3,ax6]:
    ax.set_ylabel(None)
    ax.set_yticklabels([])
    ax.set_title(None)
    ax.set_xlabel("exp var(%)")
    
# axisx
for ax in [ax2,ax5]:
    ax.set_xlabel(None)
    ax.set_xticklabels([])
    ax.set_title(None)
    ax.set_ylabel("exp var(%)")
    
# main axis
for ax in [ax1,ax4]:
    ax.set_title(None)
ax1.set_ylabel("gph/hpa")
ax4.set_ylabel(None)
    
ax2.set_ylim(45,50)
ax3.set_xlim(30,45)

ax5.set_ylim(18,21)
ax6.set_xlim(15,18) 

ax2.set_title("NAO")
ax5.set_title("EA")
plt.show()
plt.savefig('/work/mh0033/m300883/output_plots/3rdPanel/gr19/exp_var_mean.png')


# # EOF

# ## Zonally mean

# ## Lat-height

# In[15]:


lat_bins = np.arange(20,81,4)


# In[16]:


lat_labels = np.arange(22,81,4)


# In[17]:


EOFs_lon = Spap.eofs.groupby_bins('lat',bins = lat_bins,labels = lat_labels).mean(dim = 'lon')


# In[18]:


co2time = ['1856-03-03','1921-03-16','1991-03-16']
co2time = pd.DatetimeIndex(co2time)


# In[19]:


co2time


# In[20]:


EOFs_lon_CO2 = EOFs_lon.sel(time = EOFs_lon.time.dt.year.isin(co2time.year))


# In[21]:


EOFs_lon_CO2


# In[29]:


EOFs_lon_CO2['hlayers'] = EOFs_lon_CO2['hlayers']/100


# In[33]:


EOFs_lon_height_CO2 = EOFs_lon_CO2.plot.contourf('lat','hlayers',row = 'mode',
                                                 col = 'time',
                                                 levels = np.arange(-40,40.1,5.0),
                                                 extend = 'both',
                    add_colorbar = True,ylim = (1000,200), xlim = (80,20))

EOFs_lon_height_CO2.fig.set_figwidth(14)
EOFs_lon_height_CO2.fig.set_dpi(300)
EOFs_lon_height_CO2.fig.set_figwidth(14)

EOFs_lon_height_CO2.axes[0,0].set_ylabel("gph/hpa")
EOFs_lon_height_CO2.axes[1,0].set_ylabel("gph/hpa")

# plt.show()
plt.savefig('/work/mh0033/m300883/output_plots/3rdPanel/gr19/vertical_spatial.png')


# In[ ]:





# In[ ]:


fig,axes = plt.subplots(2,3,figsize = (14,8))
plt.subplots_adjust(hspace = 0.4)

Levels = [np.arange(-1,1,0.2),np.arange(-0.6,0.6,0.1)]
IMs = []
for i,row in enumerate(axes):
    for j, col in enumerate(row):
        
        im = EOFs_lon_CO2_plot.isel(mode = i,time = j).plot.contourf('lat','hlayers',
                                                 levels = Levels[i],
                                                 extend = 'both',
                                                 add_colorbar = False,
                                                 ylim = (1000,200), xlim = (80,20),
                                                 ax = col
                                                                       )
        IMs.append(im)
        col.set_ylabel(None)

# colorbar NAO
NAO_cbar_ax = fig.add_axes([0.92, 0.57, 0.016, 0.3])
fig.colorbar(IMs[2], cax=NAO_cbar_ax,label = 'NAO')

# colorbar EA
EA_cbar_ax = fig.add_axes([0.92, 0.13, 0.016, 0.3])
fig.colorbar(IMs[-1], cax=EA_cbar_ax,label = 'EA')


axes[0,0].set_ylabel('gph/hpa')
axes[1,0].set_ylabel('gph/hpa')
        
plt.show()
# plt.savefig('/work/mh0033/m300883/output_plots/3rdPanel/gr19/vertical_spatial.png')


# In[ ]:





# In[ ]:





# In[ ]:





# In[180]:


NAO_lat_time = EOFs_lon.sel(mode = 'NAO').hvplot.contourf(groupby = 'time',x = 'lat',y = 'hlayers',
              levels = np.arange(-40,40.1,5.0),
              widget_type="scrubber",
              widget_location="bottom",
              cmap = 'RdBu_r',
              flip_xaxis = True,
              flip_yaxis = True,
             )


# In[182]:


EA_lat_time = EOFs_lon.sel(mode = 'EA').hvplot.contourf(groupby = 'time',x = 'lat',y = 'hlayers',
              levels = np.arange(-40,40.1,5.0),
              widget_type="scrubber",
              widget_location="bottom",
              cmap = 'RdBu_r',
              flip_xaxis = True,
              flip_yaxis = True,
             )


# In[183]:


NAO_lat_time


# In[184]:


EA_lat_time


# In[ ]:





# In[ ]:





# # select part of latitude

# In[22]:


lon_bins = np.arange(-90,41,5)


# In[23]:


EA_lat_part = Spap.sel(lat = slice(75,40))


# In[24]:


EA_lat =  EA_lat_part.sel(mode = 'EA').groupby_bins('lon',bins = lon_bins).mean(dim = 'lat')


# In[25]:


EA_lat_CO2 = EA_lat.sel(time = EOFs_lon.time.dt.year.isin(co2time.year))


# In[ ]:





# In[26]:


# EA_lat_CO2_plot = EA_lat_CO2.sel(hlayers = (20000,100000))
EA_lat_CO2['hlayers'] = EA_lat_CO2['hlayers']/100


# In[27]:


EA_lon_height_CO2 = EA_lat_CO2.eofs.plot.contourf('lon','hlayers',col = 'time',
                                             levels = np.arange(-40,41,5),extend = 'both',
                    add_colorbar = True,ylim = (1000,200))
EA_lon_height_CO2.fig.set_figwidth(14)
plt.show()


# In[32]:


# EA_lat_CO2.to_netcdf('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/EA_lon-height.nc')


# In[33]:


# exp_plot.to_netcdf('/work/mh0033/m300883/3rdPanel/gr19/EOF_result/exp_plot.nc')


# In[ ]:





# In[ ]:


'''
