import xarray as xr
import pandas as pd
import numpy as np


def extreme(
    xarr: xr.DataArray,
    extreme_type: str,
    threshold: int=2,
)-> xr.DataArray:
    """
    select only the extreme cases from the index.
    detect the extreme cases identified from the threshold.
    **Arguments**
        *xarr* the index to be checked.
        *extrem_type*: 'pos' or 'neg
        *threshold* the threshold to identify extreme cases.
    **Return**
        *extreme* the extreme dataArray with neg and pos.
    """
    if extreme_type=='pos':
        extreme = xarr.where(xarr>threshold,drop=True)
    elif extreme_type == 'neg':
        extreme = xarr.where(xarr<-1*threshold,drop=True)
    
    return extreme

def _composite(index,data,reduction='mean'):
    """
    the composite mean or count of data, determined by the extreme state
    of index.
        - get the extreme index
        - determine the coordinate.
        - select the data
        - calculate the mean.
    **Arguments**
        *index* the from which the coordinates of 
        extreme neg or pos cases are determined.
        *data* the field that are going to be selected and averaged.
    **Return**
        *comp_mean* the mean field of the given condition.
    """
    data = data.stack(com = ('time','ens'))
    index = index.stack(com = ('time','ens'))

    extreme_composite = []
    extreme_type = xr.DataArray(['pos','neg'],dims = ['extr_type'])
    for extr_type in extreme_type.values:
        extr_index = extreme(index,extreme_type=extr_type)
        extr_data = data.where(extr_index)
        if reduction == 'mean':
            composite = extr_data.mean(dim = 'com')
        elif reduction == 'count':
            composite = extr_index.count(dim = 'com')
        extreme_composite.append(composite)
    extreme_composite = xr.concat(extreme_composite,dim=extreme_type)

    return extreme_composite

def composite(
    index:xr.DataArray,
    data:xr.DataArray,
    reduction: str='mean',
    period: str= 'all'):
    """
    composite mean maps of extreme cases or counts of extreme cases.
    given the index and the data, determine the time and ens coordinates 
    where extreme cases happen from the index, and select the data with 
    those indexes, average the selected fields.
    **Arguments**
        *index* the index of NAO and EA
        *data* the original geopotential data.
        *reduction* mean or count
        *period* 'first10','last10','all'
    **Return**
        *compostie* the composite mean of the extreme cases.
    """
    if period == 'all':
        index = index
    elif period == 'first10':
        index = index.isel(time = slice(0,10)) # the index actually started from 1856,so wrong here.
    elif period == 'last10':
        index = index.isel(time = slice(-10,None))
    data  = data.sel(time = index.time)

    extreme_type = xr.DataArray(['pos','neg'],dims = ['extr_type'])
    # postive extreme
    pos_index = extreme(index,extreme_type='pos')
    pos_index = pos_index.stack(tmp = ('mode','hlayers')) # a combined dim to keep after groupby
    pos_composite = pos_index.groupby('tmp').map(
        _composite,data = data, reduction = reduction)
    
    # negtive extreme
    neg_index = extreme(index,extreme_type='neg')
    neg_index = neg_index.stack(tmp = ('mode','hlayers'))
    neg_composite = neg_index.groupby('tmp').map(
        _composite,data = data,reduction = reduction
    )

    # get the extreme index, reduce over 'time' and 'ens' dims.
    extr_index = extreme(index)\
        .stack(temp = ('extr_type','mode'),com = ('time','ens'))
    data = data.stack(com = ('time','ens'))

    composite = extr_index.groupby('temp').map(_composite,data = data,reduction = reduction)
    return composite.unstack()




    