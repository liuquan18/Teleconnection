"""
This is the source code for temporal index generator
"""

import numpy as np
import xarray as xr

import spatial_pattern as ssp

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
