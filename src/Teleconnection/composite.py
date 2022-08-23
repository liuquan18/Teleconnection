

################## composite analysis ##############################
def _composite(extreme_index,data,reduction='mean'):
    """
    output the composite mean field of extreme pos (neg) index
        - determine the coordinate.
        - select the data
        - calculate the mean.
    **Arguments**
        *index* the extrme index from func 'extreme',from which the coordinates of 
        extreme neg or pos cases are determined.
        *data* the field that are going to be selected and averaged.
    **Return**
        *comp_mean* the mean field of the given condition.
    """

    coords = extreme_index.dropna(dim = 'com')
    composite = data.where(coords)
    if reduction == 'mean':
        composite = composite.mean(dim = 'com')
    elif reduction == 'counts':
        composite = composite.count(dim = 'com')

    return composite

def composite(
    index:xr.DataArray,
    data:xr.DataArray,
    reduction: str='mean',
    period: str= 'all'):
    """
    composite mean maps of extreme cases.
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

    # get the extreme index, reduce over 'time' and 'ens' dims.
    extr_index = sti.extreme(index)\
        .stack(temp = ('extr_type','mode'),com = ('time','ens'))
    data = data.stack(com = ('time','ens'))

    composite = extr_index.groupby('temp').map(_composite,data = data,reduction = reduction)
    return composite.unstack()




    