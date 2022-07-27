import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# %%
def project_field(field,eof,wgts):
    neofs = eof.shape[0]
    
    # weight
    field = field*wgts

    # fill with nan
    field = field.filled(fill_value = np.nan)

    # flat field to [time,space]
    records = field.shape[0]
    channels = np.product(field.shape[1:])
    field_flat = field.reshape([records, channels])

    # non missing value check
    nonMissingIndex = np.where(np.logical_not(np.isnan(field_flat[0])))[0]
    field_flat = field_flat[:, nonMissingIndex]

    # flat eof to [mode, space]
    _flatE = eof.reshape(neofs,-1)
    eofNonMissingIndex = np.where(
        np.logical_not(np.isnan(_flatE[0])))[0]

    # missing value check
    if eofNonMissingIndex.shape != nonMissingIndex.shape or \
            (eofNonMissingIndex != nonMissingIndex).any():
        raise ValueError('field and EOFs have different '
                            'missing value locations')
    eofs_flat = _flatE[:, eofNonMissingIndex]

    # projection
    projected_pcs = np.dot(field_flat, eofs_flat.T)

    return projected_pcs