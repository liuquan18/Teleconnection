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
filename = example_data_path('hgt_djf.nc')
z_djf = xr.open_dataset(filename)
z_djf = z_djf.z

#%% standardize.
z_djf_mean = z_djf.mean(dim = 'time')
z_djf_std = z_djf.std(dim = 'time')
z_djf = (z_djf - z_djf_mean)/z_djf_std
#%% do eof

# weights
coslat = np.cos(np.deg2rad(z_djf.latitude)).values.clip(0., 1.)
wgts = np.sqrt(coslat)[..., np.newaxis]

solver = Eof(z_djf.values, weights=wgts,center=True)
nmode = 2
# Retrieve the leading EOF,
eof = solver.eofs(neofs=nmode)
pc = solver.pcs(npcs = nmode)
fra = solver.varianceFraction(neigs=nmode)

# to xarray
eof_container = z_djf.isel(time = slice(0,nmode)).rename({'time':'mode'})
eofx = eof_container.copy(data = eof)
pcx = xr.DataArray(pc,dims = ['time','mode'],coords = {'time':z_djf.time,'mode':['NAO','EA']})


#%% show here eof
eofplots = eofx.isel(mode=1).plot(subplot_kws={'projection':ccrs.Orthographic(central_longitude=-20, central_latitude=60)},
transform = ccrs.PlateCarree())
eofplots.axes.coastlines()
eofplots.axes.gridlines()

#%% plot pc
pcx.isel(mode=1).plot()
plt.suptitle('pc from python eofs')

#%% using the projectField function from the package
ppc = solver.projectField(z_djf.values,neofs = 2)
ppcx = xr.DataArray(ppc,dims = ['time','mode'],coords = {'time':z_djf.time,'mode':['NAO','EA']})

ppcx.isel(mode=1).plot()
plt.suptitle("pc from eofs.projectField")


#%% using the hand defined project_field function.
