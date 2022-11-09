import numpy as np
import pandas as pd
import xarray as xr


def extreme(
    xarr: xr.DataArray,
    extreme_type: str,
    threshold: int = 2,
) -> xr.DataArray:
    """
    select only the positive or extreme cases from the index.
    detect the extreme cases identified from the threshold.
    **Arguments**
        *xarr* the index to be checked.
        *extrem_type*: 'pos' or 'neg
        *threshold* the threshold to identify extreme cases.
    **Return**
        *extreme* the extreme dataArray with neg and pos.
    """
    if extreme_type == "pos":
        extreme = xarr.where(xarr > threshold, drop=True)
    elif extreme_type == "neg":
        extreme = xarr.where(xarr < -1 * threshold, drop=True)

    return extreme


def composite(index, data, reduction="mean", dim="com"):
    """
    the composite mean or count of data, in terms of different extreme type.
        - stack to one series.
        - for pos and neg:
            - get the extreme index
            - select the data
            - calculate the mean or counts.
        - concat pos and neg.
    **Arguments**
        *index* the from which the coordinates of
        extreme neg or pos cases are determined.
        *data* the field that are going to be selected and averaged.
    **Return**
        *extreme_composite* the mean field or counts of extreme cases.
    """
    extreme_composite = []
    extreme_type = xr.DataArray(["pos", "neg"], dims=["extr_type"])
    for extr_type in extreme_type.values:

        # get the coordinates of the extremes
        extr_index = extreme(index, extreme_type=extr_type)

        # get the data at the extreme coordinates
        extr_data = data.where(extr_index)

        if reduction == "mean":
            composite = extr_data.mean(dim=dim)
        elif reduction == "count":
            composite = extr_index.count(dim=dim)
        extreme_composite.append(composite)
    extreme_composite = xr.concat(extreme_composite, dim=extreme_type)

    return extreme_composite
