"""
This is the source code for temporal index generator
"""

from unittest.util import _count_diff_all_purpose
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

def period_index(all_indexes,period = 'first'):
    """
    get the first 10 or last 10 year index from the whole time series of teleconnection.
    the index name can be seen from the table below:
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

def join_xarr(lxarr, rxarr,lsuffix,rsuffix = "_all"):
    """
    join two xarry into dataframes, with the first column being the index 
    from first(last)-pattern, and the second the index from all-pattern.
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

def pattern_compare(all_indexes):
    """
    compare the index from first (last) pattern and all pattern. 
    **Argument**
        *all_indexes* index of projecting all the time series onto three patterns.
        *period* "first","last","dynamic", corresponding to the comparation between
            - first-first --- first-all, first-last --- first-all
            - last-first  --- last-all,  last-last  --- last-all
            - first-first --- first-all, last-last --- last-all
            here the first 'first' represent period, the second 'first' represent pattern.
    **Return**
        dataframe with the first column being the index from first pattern ,the second
        column being the index from all.
    """
    # getting the index for the two periods
    first_all, first_first,first_last = period_index(all_indexes,period = 'first') # ten-->period
    last_all, last_first, last_last = period_index(all_indexes,period = 'last')
    
    # first 10 periods
    first_first_all = join_xarr(first_first,first_all,lsuffix='_first')
    first_last_all  = join_xarr(first_last, first_all,lsuffix='_last')

    # last 10 periods
    last_first_all = join_xarr(last_first,last_all,lsuffix='_first')
    last_last_all = join_xarr(last_last, last_all,lsuffix='_last')

    return [first_first_all, first_last_all],[last_first_all,last_last_all],\
        [first_first_all,last_last_all]

def extreme(xarr,threshod = 2):
    """
    mask out non-extreme data.
    **Arguments**
        *xarr* the xarr to be process
    **Return**
        new xarray with one extra dimension called 'extr_type'
    """
    pos_ex = xarr.where(xarr>threshod)
    neg_ex = xarr.where(xarr<-1*threshod)
    ex = xr.concat([pos_ex,neg_ex],dim = ['pos','neg'])
    ex = ex.rename({'concat_dim':'extr_type'})
    return ex

def period_extreme(all_indexes,period = 'first'):
    """
    The same as period_index, but now mask out the non-extreme elements.
    **Arguments**
        *all_index* the three index of all years from the three patterns.
                    should be order in [all_all, all_first, all_last]
        *period* the first 10 or last 10 years of index
    **Return**
        the three index for 10 period, only with the extreme elements.
        ordered in [_all,_first,_last]
    """
    ten_all, ten_first, ten_last  = period_index(all_indexes,period = period)
    ten_all, ten_first, ten_last = [extreme(ten_all),extreme(ten_first),
        extreme(ten_last)]
    return ten_all, ten_first,ten_last

def count_nonzero(xarr):
    """
    count the number of extreme cases in xarr
    **Arguments**
        *xarr* the xarr where the non-extreme points are marked as np.nan
    **Return**
        number of extreme cases, with the coordinate of 'hlayer' and 'mode'
        reserved.
    """
    return xarr.count(dim = ('time','ens'))

def extreme_count(all_indexes):
    """
    count the number of extreme cases in the period of first 10 years and 
    last 10 years.
    **Arguments**
        *all_indexes* the three index of all years from the three patterns.
                      should be order in [all_all, all_first, all_last]
    **Return**
        three for each period (six in total) extreme counts.
    """
    # getting the extreme indexes
    fA, fF, fL = period_extreme(all_indexes,period = 'first')
    lA, lF, lL = period_extreme(all_indexes, period = 'last')

    # count the extreme cases
    fA, fF, fL = [count_nonzero(fA),count_nonzero(fF),count_nonzero(fL)]
    lA, lF, lL = [count_nonzero(lA),count_nonzero(lF),count_nonzero(lL)]
    return lA,fF,fL,lA,lF,lL



def main():
    all_all_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_all_ind.nc').pc
    all_first_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_first_ind.nc').pc
    all_last_ind = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/indexDiffPattern/all_last_ind.nc').pc

    ind_fA,ind_fF,ind_fL,ind_lA,ind_lF,ind_lL = extreme_count([all_all_ind,all_first_ind,all_last_ind])


if __name__ == "__main__":
    main()
