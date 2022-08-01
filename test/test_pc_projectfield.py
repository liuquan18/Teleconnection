#%%
from contextlib import AsyncExitStack
import sys
sys.path.append("..")
import scripts.project_field as pjh

import importlib
importlib.reload(pjh) # after changed the source code


#%%
"""
Compute and plot the leading EOF of geopotential height on the 500 hPa
pressure surface over the European/Atlantic sector during winter time.

"""
#%%
import cartopy.crs as ccrs
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

from eofs.standard import Eof
from eofs.examples import example_data_path
import xarray as xr

#%%
# Read geopotential height data using the netCDF4 module. The file contains
# December-February averages of geopotential height at 500 hPa for the
# European/Atlantic domain (80W-40E, 20-90N).
filename = "/work/mh0033/m300883/3rdPanel/data/sample.nc"
z_djf = xr.open_dataset(filename)
z_djf = z_djf.var156
z_djf = z_djf.isel(hlayers = 0)

#%% standardize.
z_djf_mean = z_djf.mean(dim = 'time')
z_djf_std = z_djf.std(dim = 'time')
z_djf = (z_djf - z_djf_mean)/z_djf_std
z_djf = z_djf.stack(com = ('time','ens'))
z_djf['com'] = np.arange(len(z_djf['com']))
z_djf = z_djf.transpose('com',...)
#%% do eof
# weights
coslat = np.cos(np.deg2rad(z_djf.lat)).values.clip(0., 1.)
wgts = np.sqrt(coslat)[..., np.newaxis]

solver = Eof(z_djf.values, weights=wgts,center=True)
nmode = 2
# Retrieve the leading EOF,
eof = solver.eofs(neofs=nmode)
pc = solver.pcs(npcs = nmode)
fra = solver.varianceFraction(neigs=nmode)

# to xarray
eof_container = z_djf.isel(com = slice(0,nmode)).rename({'com':'mode'})
eof_container['mode'] = ['NAO','EA']
eofx = eof_container.copy(data = eof)
pcx = xr.DataArray(pc,dims = ['com','mode'],coords = {'com':np.arange(len(z_djf.com)),'mode':['NAO','EA']})


#%% show here eof
eofplots = eofx.isel(mode=1).plot(subplot_kws={'projection':ccrs.Orthographic(central_longitude=-20, central_latitude=60)},
transform = ccrs.PlateCarree())
eofplots.axes.coastlines()
eofplots.axes.gridlines()

#%% plot pc
pcx.isel(mode=1).plot()
plt.suptitle('pc from python solver.pcs')

#%% using the projectField function from the package
ppc = solver.projectField(z_djf.values,neofs = 2,weighted = True)
ppcx = xr.DataArray(ppc,dims = ['com','mode'],coords = {'com':np.arange(len(z_djf.com)),'mode':['NAO','EA']})

ppcx.isel(mode=1).plot()
plt.suptitle("pc from solver.projectField")


#%% using the hand defined project_field function.
hpc = pjh.project_field(z_djf.values,eof,wgts)
hpcx = xr.DataArray(hpc,dims = ['time','mode'],coords = {'time':z_djf.time,'mode':['NAO','EA']})
hpcx.isel(mode=1).plot()
plt.suptitle("pc from hand defined func projectField")

# %% using the linear regression np.polyfit
nppc = pjh.project_polyfit(z_djf.isel(pressure=0),eofx.sel(mode='EA').isel(pressure=0),wgts)
nppcx = xr.DataArray(nppc,dims = ['time','mode'],coords = {'time':z_djf.time,'mode':['EA']})
nppcx.isel(mode =0).plot()
# %%
A = z_djf.isel(pressure=0)
B = eofx.isel(mode=1,pressure=0)
C = pjh.project_polyfit(A,B,wgts)
# %%
C.plot()
# %%
fig,axes = plt.subplots(2,2,dpi = 150,figsize = (8,8))
plt.subplots_adjust(hspace = 0.5)

pcx.isel(mode=1).plot(ax = axes[0,0])
axes[0,0].set_title('package: solver.pcs')

ppcx.isel(mode=1).plot(ax = axes[0,1])
axes[0,1].set_title("package: solver.projectField")

hpcx.isel(mode=1).plot(ax = axes[1,0])
axes[1,0].set_title("hand_define: projectField")

C.plot(ax=axes[1,1])
axes[1,1].set_title("hand_define: linear regrssion")
plt.show()
# %%


D = pjh.project_field(A.values,eofx.isel(pressure = 0)[1].values,wgts)
D = xr.DataArray(D,dims = ['time','mode'],coords = {'time':z_djf.time,'mode':['NAO','EA']})
D.isel(mode=1).plot()
plt.suptitle("pc from hand defined func projectField")
# %% std pc first
pcx_std = (pcx-pcx.mean(dim = 'time'))/pcx.std(dim = 'time')
pcx_std.isel(mode=1).plot()

# %%
