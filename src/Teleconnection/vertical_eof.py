import numpy as np
import xarray as xr
from tqdm.notebook import tqdm

import src.Teleconnection.rolling_eof as rolling_eof


def vertical_eof(xarr, nmode, window=10, fixed_pattern="all", independent=True):
    """
    different way to do the eof vertically,
    **Arguments**:
        *xarr*: DataArry to decompose
        *independent*: all layers decompose independently or not.
                       if independent = True, the eof is applied independently over all levels.
                       if independent = False, the vertical dimension is seen as one of the
                       spatial dimension. so the eof stands for the common pattern of all layers.
    
    **Return**

        *eof*, *pc* and *fra*
    """
    if independent == True:
        eof, pc, fra = independent_eof(xarr, nmode, window, fixed_pattern)
    else:
        eof, pc, fra = dependent_eof(xarr, nmode, window, fixed_pattern)

    return eof, pc, fra

def independent_eof(xarr, nmode, window, fixed_pattern):
    """
    do eof independently over all layers.
    **Arguments**
        *xarr* : the xarr to be composed.
        *fixed_pattern* : the method to generate pc.
        *method*: "rolling_eof" or "eof"
    **Return**
        EOF, PC and FRA.
    """
    eofs = []
    pcs = []
    fras = []

    hlayers = xarr.hlayers
    for h in tqdm(hlayers):
        field = xarr.sel(hlayers=h)
        eof, pc, fra = rolling_eof.rolling_eof(field, nmode, window, fixed_pattern)

        eofs.append(eof)
        pcs.append(pc)
        fras.append(fra)
    eofs = xr.concat(eofs, dim=xarr.hlayers)
    pcs = xr.concat(pcs, dim=xarr.hlayers)
    fras = xr.concat(fras, dim=xarr.hlayers)
    return eofs, pcs, fras


def dependent_eof(xarr, nmode, window, fixed_pattern):
    """
    do eof independently over all layers.
    **Arguments**
        *xarr* : the xarr to be composed.
        *fixed_pattern* : the method to generate pc.
        *method*: "rolling_eof" or "eof"
    **Return**
        EOF, PC and FRA.
    """
    eofs, pcs, fras = rolling_eof(xarr, nmode, window, fixed_pattern)

    return eofs, pcs, fras

