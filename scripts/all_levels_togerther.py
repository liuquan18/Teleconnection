# script for all levels together, common patterns. 
#%%
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
#%%
import src.Teleconnection.spatial_pattern as sp
import src.Teleconnection.eof_plots as ept


# %%
allens = xr.open_dataset("/work/mh0033/m300883/transition/gr19/gphSeason/allens_season_time.nc")
#%% split ens
splitens = sp.split_ens(allens)

#%% demean ens-mean
demean = splitens-splitens.mean(dim = 'ens')

#%% select traposphere
trop = demean.sel(hlayers = slice(20000,100000))



########## independent ##############
# %%
# standard-independent-rolling fixed all eof
eof_sira,pc_sira,fra_sira = sp.season_eof(trop.var156,nmode=2,method ="rolling_eof",
window=10,fixed_pattern='all',return_full_eof= False,independent = True,standard=True)

#%%
eof_sira.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_all/eof.nc")
pc_sira.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_all/pc.nc")
fra_sira.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_all/fra.nc")

#%%
del(eof_sira)
del(pc_sira)
del(fra_sira)


# %%
# standard-independent-rolling fixed first eof
eof_sirf,pc_sirf,fra_sirf = sp.season_eof(trop.var156,nmode=2,method ="rolling_eof",
window=10,fixed_pattern='first',return_full_eof= False,independent = True,standard=True)

#%%
# eof_sirf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_first/eof.nc")
pc_sirf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_first/pc.nc")
fra_sirf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_first/fra.nc")

#%%
del(eof_sirf)
del(pc_sirf)
del(fra_sirf)


# %%
# standard-independent-rolling fixed first eof
eof_sirl,pc_sirl,fra_sirl = sp.season_eof(trop.var156,nmode=2,method ="rolling_eof",
window=10,fixed_pattern='last',return_full_eof= False,independent = True,standard=True)

#%%
# eof_sirl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_last/eof.nc")
pc_sirl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_last/pc.nc")
fra_sirl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_ind_rolling_last/fra.nc")

#%%
del(eof_sirl)
del(pc_sirl)
del(fra_sirl)



############# non independent ########################

# %%
# standard-alllevel-rolling eof all pattern
eof_snra,pc_snra,fra_snra = sp.season_eof(trop.var156,nmode=2,fixed_pattern='all',
standard=True,method = 'rolling_eof',independent = False)

eof_snra.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_all/eof.nc")
pc_snra.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_all/pc.nc")
fra_snra.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_all/fra.nc")

#%%
del(eof_snra)
del(pc_snra)
del(fra_snra)


# %%
# standard-alllevel-rolling eof first pattern
eof_snrf,pc_snrf,fra_snrf = sp.season_eof(trop.var156,nmode=2,fixed_pattern='first',
standard=True,method = 'rolling_eof',independent = False)

eof_snrf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_first/eof.nc")
pc_snrf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_first/pc.nc")
fra_snrf.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_first/fra.nc")

#%%
del(eof_snrf)
del(pc_snrf)
del(fra_snrf)

# %%
# standard-alllevel-rolling eof first pattern
eof_snrl,pc_snrl,fra_snrl = sp.season_eof(trop.var156,nmode=2,fixed_pattern='last',
standard=True,method = 'rolling_eof',independent = False)

eof_snrl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_last/eof.nc")
pc_snrl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_last/pc.nc")
fra_snrl.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/std_nonind_rolling_last/fra.nc")

#%%
del(eof_snrl)
del(pc_snrl)
del(fra_snrl)


#%% spatial patterns of all years and all ensembles.
eof_all,_,_ = sp.season_eof(trop.var156,nmode=2,method ="eof",independent = True)


#%%
eof_all.to_netcdf("/work/mh0033/m300883/3rdPanel/data/EOF_result/eof_all/eof_all.nc")


#%% Z500 only test
trop500 = trop.sel(hlayers = 50000).var156
# %%
trop500std = sp.standardize(trop500)
# %%
trop500com = sp.stack_ens(trop500,withdim ='time')
# %%
trop500com
# %%
eof500,_,_ = sp.doeof(trop500com)
# %%
ept.visu_eof_single(eof500)




# %%
trop_sm = trop.sel(hlayers = [50000,85000])
# %%
trop_sm.to_netcdf("/work/mh0033/m300883/3rdPanel/data/sample/Z500_850.nc")
# %%
