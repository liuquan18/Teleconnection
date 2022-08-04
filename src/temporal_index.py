"""
This is the source code for temporal index generator
"""

import numpy as np
import xarray as xr

import sys
sys.path.append("..")
import src.spatial_pattern as ssp

import importlib
importlib.reload(ssp) # after changed the source code

def index_diff_pattern(xarr,independent = True, standard=True):
    """
    projeting the whole time series onto the three different patterns to get
    the corresponding index.
    Three patterns:
        - all: all the ensembles and years are fed to the EOF.
        - first: the ensembles of the first 10 years are fed to EOF.
        - last: the ensembles of the last 10 years are fed to EOF.
    The above three patterns can be derived with all-level-independent or 
    all-level-dependent, the latter is a common pattern for all levels.
    **Argument**:
        *xarr* the data to be projected and to get the spatial patterns
        *independent* how to get the spatil patterns.
        *standard* whether to do the standarization or not. here all the 
                   three indexes are standardized with the temporal mean 
                   and std of index from all-pattern.
    **Return**:
        Three indexes projected from the same time series (all the years) but onto 
        three different spatial patterns.
    """
    _,all_all,_ = ssp.season_eof(xarr, nmode=2,window=10,
    fixed_pattern="all",independent=independent)  # "method" doesn't matter since the pc is 
                        # calculated independently.
    _, all_first,_ = ssp.season_eof(xarr,nmode=2,window=10,
    fixed_pattern="first",independent=independent)
    _, all_last,_ = ssp.season_eof(xarr,nmode=2,window=10,
    fixed_pattern="last",independent=independent)    

    if standard:
        all_mean = all_all.mean(dim = 'time')
        all_std = all_all.std(dim = 'time')

        all_all = (all_all-all_mean)/all_std
        all_first = (all_first-all_mean)/all_std
        all_last = (all_last-all_mean)/all_std

    return all_all, all_first, all_last

def ten_period_index(all_indexes,period = 'first'):
    """
    get the first 10 or last 10 index. the index name can be seen from
    the table below:
    |spatial pattern|   all   |    first    |    last   |
    |temporal period|
    |---------------|---------|-------------| ----------|
    |first 10       |first-all| first-first | first-last|
    |last 10        |last-all | last-first  | last-last |
    **Arguments**
        *all_index* the three index of all years to the three patterns.
                    should be order in [all_all, all_first, all_last]
        *period* the first 10 or last 10 years of index
    **Return**
        the three index for first or last 10 years. ordered in 
        [_all,_first,_last]
    """
    if period=='first':
        ten_all, ten_first, ten_last = [all_index.isel(time = slice(0,10))
        for all_index in all_indexes]
    if period =='last':
        ten_all, ten_first, ten_last = [all_index.isel(time = slice(-10,None))
        for all_index in all_indexes]
    return ten_all, ten_first, ten_last

def ten_period_all(lxarr, rxarr,lsuffix,rsuffix = "_all"):
    """
    join two xarry into dataframes.
    **Arguments**
        *lxarr* the index of ten period onto first or last pattern.
        *rxarr* the index of ten period onto all pattern
        *lsuffix* "_first" or "_last"
        *rsuffix* "_all"
    **Return**
        one dataframe with the first column as "pc_first" or "pc_last" (lsuffix).
        the second column as "pc_all"
    """
    ten_ten_all = lxarr.to_dataframe().join(rxarr.to_dataframe(),
    lsuffix = lsuffix, rsuffix = rsuffix)  # ten_ten, ten_all
    return ten_ten_all

def first_first_all(all_all,all_first,all_last):
    """
    generate dataframe for first 10 period, with the columns of 'pc_first','pc_all',
    and 'pc_last','pc_all'.
    **Argument**:
        *all_all* all data projected on all pattern.
        *all_first* all data projected on first pattern.
        *all_last* all data projected on last pattern
    **Return**
        two Dataframe. the first with columns 'pc_first', the second with column
        'pc_last','pc_all'.
    """
    first_all, first_first,first_last = ten_period_index([all_all,all_first,all_last],
    period='first')
    first_first_all = ten_period_all(first_first,first_all, '_first','_all')
    first_last_all  = ten_period_all(first_last, first_all, '_last','_all')
    return first_first_all, first_last_all

def last_last_all(all_all, all_first,all_last):
    """
    generate dataframe for last 10 period, with the columsn of 'pc_first','pc_all'
    and 'pc_last','pc_all'
    **Argument**:
        *all_all* all data projected on all pattern.
        *all_first* all data projected on first pattern.
        *all_last* all data projected on last pattern
    **Return**
        two Dataframe. the first with columns 'pc_first', the second with column
        'pc_last','pc_all'.
    """
    last_all, last_first, last_last = ten_period_index([all_all,all_first,all_last],
    period = 'last')
    last_first_all = ten_period_all(last_first,last_all, '_first','_all')
    last_last_all  = ten_period_all(last_last,last_all, '_last','_all')
    return last_first_all,last_last_all

def first_last_all(all_all, all_first,all_last):
    """
    generate dataframe for first-first-first-all and last-last-last-all.
    **Argument**:
        *all_all* all data projected on all pattern.
        *all_first* all data projected on first pattern.
        *all_last* all data projected on last pattern
    **Return**
        two Dataframe. the first with columns 'pc_first', the second with column
        'pc_last','pc_all'.
    """
    first_all, first_first,_ = ten_period_index([all_all,all_first,all_last],
    period='first')
    last_all, _, last_last = ten_period_index([all_all,all_first,all_last],
    period = 'last')
    first_first_all = ten_period_all(first_first,first_all,'_first','_all')
    last_last_all = ten_period_all(last_last, last_all, '_last','_all')
    return first_first_all, last_last_all


def ten_all_dataframe(all_all,all_first,all_last,period='first'):
    """
    return the dataframe given the periods
    **Argument**:
        *all_all* all data projected on all pattern.
        *all_first* all data projected on first pattern.
        *all_last* all data projected on last pattern
        *period* 'first','last','dynamic'
    **Return**
        dataframe with the columns of ten_first, ten_all and ten_last, ten_all
    """
    if period == 'first':
        first, last = first_first_all(all_all,all_first, all_last)
    elif period == 'last':
        first, last = last_last_all (all_all, all_first, all_last)
    elif period == 'dynamic':
        first, last = first_last_all(all_all, all_first, all_last)
    return first, last