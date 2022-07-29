from pprint import pformat
from pyrsistent import PSet
import xarray as xr
import numpy as np
import pandas as pd
from eofs.standard import Eof
from tqdm.notebook import trange, tqdm
import seaborn as sn

def lon_height(eof,mode='EA'):
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
    EA_lon_height = eof_lat.sel(mode = mode).groupby_bins('lon',bins = lon_bins).mean(dim = 'lat')
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

def df_sel(df,condition):
    """
    select rows depend on the condition of items in columns. {'column':'item'}
    """
    for item in condition.items():
        col = item[0]
        value = item[1]
        df = df[df[col]==value]

    return df

def pc_todf(xarr,name):
    """
    transform xarray to dataframe.
    **Arguments**
        *xarr* the dataarray to be transoformed
        *name* the column name for the dataframe.
    """
    df = xarr.__xarray_dataarray_variable__.to_dataframe().reset_index()
    df = df.rename(columns = {'__xarray_dataarray_variable__':name})
    return df

def merge_df(dfs):

    dfm = pd.merge(dfs[0],dfs[1],on =['hlayers','mode','ens','time'])

    dfm = pd.merge(dfm,dfs[2],on = ['hlayers','mode','ens','time'])

    old_columns = dfs[0].columns[:4]
    new_columns = [dfs[0].columns[-1],dfs[1].columns[-1],dfs[2].columns[-1]]

    dfm.columns = np.r_[old_columns,new_columns]
    return dfm

def show_allyears_ens(df,mode):
    Z200_EA = df_sel(df,{'hlayers':20000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    Z500_EA = df_sel(df,{'hlayers':50000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    Z850_EA = df_sel(df,{'hlayers':85000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    return Z200_EA,Z500_EA,Z850_EA