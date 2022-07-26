from pprint import pformat
import xarray as xr
import numpy as np
import pandas as pd
from eofs.standard import Eof
from tqdm.notebook import trange, tqdm


def lon_height(eof):
    """
    calculate zonally mean of eof
    **Arguments**
        *eof* The eofs to be averaged [time,lat,lon,plev]
    **Return**
        eof as a function of longitude and height
    """
    # time
    co2time = ['1856-03-03','1921-03-16','1991-03-16']
    co2time = pd.DatetimeIndex(co2time)
    eof_CO2 = eof.sel(time = eof.time.dt.year.isin(co2time.year))
    
    # height
    eof_height = eof_CO2.sel(hlayers = slice(20000,100000))
    eof_height['hlayers'] = eof_height['hlayers']/100

    # lats
    eof_lat = eof_height.sel(lat = slice(70,40))
    
    # groupby 
    lon_bins = np.arange(-90,41,5)
    EA_lon_height = eof_lat.sel(mode = 'EA').groupby_bins('lon',bins = lon_bins).mean(dim = 'lat')
    return EA_lon_height

def lat_height(eof,mode = 'NAO'):
    """
    calculate meridional mean of eof
    **Arguments**
        *eof* the eofs to be averaged.
        *mode* which mode to be calculated
    **Return**
        eof as function of lattitude and height.
    """
    # time
    co2time = ['1856-03-03','1921-03-16','1991-03-16']
    co2time = pd.DatetimeIndex(co2time)
    eof_CO2 = eof.sel(time = eof.time.dt.year.isin(co2time.year))
    
    # height
    eof_height = eof_CO2.sel(hlayers = slice(20000,100000))
    eof_height['hlayers'] = eof_height['hlayers']/100

    
    # groupby
    lat_bins = np.arange(20,81,4)
    lat_labels = np.arange(22,81,4)
    EA_lat_height = eof_height.sel(mode =mode).groupby_bins('lat',bins = lat_bins,labels = lat_labels).mean(dim = 'lon')
    return EA_lat_height


def 