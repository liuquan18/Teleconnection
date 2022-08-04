"""
source code for index statistics
"""
from pprint import pformat
from pyrsistent import PSet
import xarray as xr
import numpy as np
import pandas as pd
from eofs.standard import Eof
from tqdm.notebook import trange, tqdm
import seaborn as sns

def df_sel(df,condition):
    """
    select dataframe rows depend on the condition of items in columns. {'column':'item'}
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

def merge_df(dfs,on=['hlayers','mode','ens','time']):
    """
    merge dataframe along the selected columns. 
    """

    dfm = pd.merge(dfs[0],dfs[1],on = on)

    dfm = pd.merge(dfm,dfs[2],on = on)

    old_columns = dfs[0].columns[:4]
    new_columns = [dfs[0].columns[-1],dfs[1].columns[-1],dfs[2].columns[-1]]

    dfm.columns = np.r_[old_columns,new_columns]
    return dfm

def show_allyears_ens(df,mode):
    Z200_EA = df_sel(df,{'hlayers':20000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    Z500_EA = df_sel(df,{'hlayers':50000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    Z850_EA = df_sel(df,{'hlayers':85000,'mode':mode}).set_index(['hlayers','mode','ens','time'])
    return Z200_EA,Z500_EA,Z850_EA


def pc_column(pcs,mode='NAO'):
    """
    combine all three pcs make them into three columns of dataframe.
    **Arguments**
        *pcs* list of pcs in xarray, [first,all,last]
        *mode* mode to plot.
    """
    dfs = [pc.sel(mode=mode).to_dataframe()[['pc']] for pc in pcs]
    df = dfs[0].join(dfs[1],lsuffix = '_first',rsuffix = '_all')
    df = df.join(dfs[2])
    df.columns = ['pc_first','pc_all','pc_last']

    df = df.stack()
    df = pd.DataFrame(df,columns = ['pc'])
    df.index.names = ['hlayers','ens','time','spap']
    return df

def count_extreme(xarr):
    """
    count the number of extreme cases in xarr
    """

