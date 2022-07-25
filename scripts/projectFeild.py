def project_field(solver, field, neofs=None, eofscaling=0, weighted=True):
    """Project a field onto the EOFs.

    Given a data set, projects it onto the EOFs to generate a
    corresponding set of pseudo-PCs.

    **Argument:**

    *field*
        A `numpy.ndarray` or `numpy.ma.MaskedArray` with two or more
        dimensions containing the data to be projected onto the
        EOFs. It must have the same corresponding spatial dimensions
        (including missing values in the same places) as the `Eof`
        input *dataset*. *field* may have a different length time
        dimension to the `Eof` input *dataset* or no time dimension
        at all.

    **Optional arguments:**

    *neofs*
        Number of EOFs to project onto. Defaults to all EOFs. If the
        number of EOFs requested is more than the number that are
        available, then the field will be projected onto all
        available EOFs.

    *eofscaling*
        Set the scaling of the EOFs that are projected onto. The
        following values are accepted:

        * *0* : Un-scaled EOFs (default).
        * *1* : EOFs are divided by the square-root of their
            eigenvalue.
        * *2* : EOFs are multiplied by the square-root of their
            eigenvalue.

    *weighted*
        If *True* then *field* is weighted using the same weights
        used for the EOF analysis prior to projection. If *False*
        then no weighting is applied. Defaults to *True* (weighting
        is applied). Generally only the default setting should be
        used.

    **Returns:**

    *pseudo_pcs*
        An array where the columns are the ordered pseudo-PCs.

    **Examples:**

    Project a data set onto all EOFs::

        pseudo_pcs = solver.projectField(data)

    Project a data set onto the four leading EOFs::

        pseudo_pcs = solver.projectField(data, neofs=4)

    """
    # Check that the shape/dimension of the data set is compatible with
    # the EOFs.
    solver._verify_projection_shape(field, solver._originalshape)
    input_ndim = field.ndim
    eof_ndim = len(solver._originalshape) + 1
    # Create a slice object for truncating the EOFs.
    slicer = slice(0, neofs)
    # If required, weight the data set with the same weighting that was
    # used to compute the EOFs.
    field = field.copy()
    if weighted:
        wts = solver.getWeights()
        if wts is not None:
            field = field * wts
    # Fill missing values with NaN if this is a masked array.
    try:
        field = field.filled(fill_value=np.nan)
    except AttributeError:
        pass
    # Flatten the data set into [time, space] dimensionality.
    if eof_ndim > input_ndim:
        field = field.reshape((1,) + field.shape)
    records = field.shape[0]
    channels = np.product(field.shape[1:])
    field_flat = field.reshape([records, channels])
    # Locate the non-missing values and isolate them.
    if not solver._valid_nan(field_flat):
        raise ValueError('missing values detected in different '
                            'locations at different times')
    nonMissingIndex = np.where(np.logical_not(np.isnan(field_flat[0])))[0]
    field_flat = field_flat[:, nonMissingIndex]
    # Locate the non-missing values in the EOFs and check they match those
    # in the data set, then isolate the non-missing values.
    eofNonMissingIndex = np.where(
        np.logical_not(np.isnan(solver._flatE[0])))[0]
    if eofNonMissingIndex.shape != nonMissingIndex.shape or \
            (eofNonMissingIndex != nonMissingIndex).any():
        raise ValueError('field and EOFs have different '
                            'missing value locations')
    eofs_flat = solver._flatE[slicer, eofNonMissingIndex]
    if eofscaling == 1:
        eofs_flat /= np.sqrt(solver._L[slicer])[:, np.newaxis]
    elif eofscaling == 2:
        eofs_flat *= np.sqrt(solver._L[slicer])[:, np.newaxis]
    # Project the data set onto the EOFs using a matrix multiplication.
    projected_pcs = np.dot(field_flat, eofs_flat.T)
    if eof_ndim > input_ndim:
        # If an extra dimension was introduced, remove it before returning
        # the projected PCs.
        projected_pcs = projected_pcs[0]
    return projected_pcs