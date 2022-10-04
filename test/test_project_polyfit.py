# #%%
# import cartopy.crs as ccrs
# import matplotlib.pyplot as plt
# import numpy as np

# from eofs.standard import Eof
# from eofs.examples import example_data_path
# import xarray as xr
# # %%
# #%%
# def _compute_slope(x,y):
#     """
#     private function to compute linear coefficient.
#     """
#     x = x.reshape(-1)
#     y = y.reshape(-1)
#     return np.polyfit(x,y,1)[0]

# def project_polyfit(field,eof):
#     """
#     project by linearly regress the data onto the patterns.
#     """


#     slopes = xr.apply_ufunc(_compute_slope,
#                             eof,field,
#                             vectorize=True,
#                             dask='parallelized', 
#                             input_core_dims=[['latitude','longitude'],
#                             ['latitude','longitude']],
#                             # output_core_dims = [['time'],['time']],
#                             output_dtypes=[float]
#     )
#     return slopes

# # %%
# A = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/sample_field.nc').z
# B = xr.open_dataset('/work/mh0033/m300883/3rdPanel/data/sample_eof.nc').z
# # %%c
# C = project_polyfit(A,B)

# # %%
# C.plot()
# # %%
