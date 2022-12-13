# Generate the sptial pattern maps, and the distribution of index at 500hpa 
# geopotential height.

#%%
# imports
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import proplot as pplt
import seaborn as sns

#%%
# config
vertical_eof = 'dep'  # independently decompose each altitude levels
pattern = 'all'       # project onto the 'all' pattern (150 years and 100 ensemble members)

# the name of the folder to store the plots
if vertical_eof == 'dep':
    folder = 'all_whole_std'
elif vertical_eof == 'ind':
    folder = 'ind_all_whole'
# %%

# read eof data (spatial data)
odir = "/work/mh0033/m300883/3rdPanel/data/allPattern/"
sptial_path = odir + vertical_eof +"/" + pattern + "_pattern/all_all_eof.nc"
eof_all_all = xr.open_dataset(sptial_path).eof
eof_500hpa = eof_all_all.sel(hlayers = 50000)

# %%
# read index data
index_path = odir + vertical_eof +"/" + pattern + "_pattern/all_all_nonstd.nc"
all_all_index = xr.open_dataset(index_path).pc

# standardize index
def standardize(index,dim = ('time','ens')):
    """
    standardardize with the mean and std of 'time' and 'ens'.
    """
    mean = index.mean(dim = dim)
    std = index.std(dim = dim)
    index = (index-mean)/std
    return index
all_all_index = standardize(all_all_index)

first10_all_whole = all_all_index.isel(time = slice(0,10)) # first10 years projectecd on all, standardized with whole time
last10_all_whole = all_all_index.isel(time = slice(-10,all_all_index.time.size))

index_500hpa_first = first10_all_whole.sel(hlayers = 50000)
index_500hpa_last = last10_all_whole.sel(hlayers = 50000)

# to dataframe()
coords = xr.IndexVariable(dims = 'periods',data = ['first10','last10'])
index_500hpa = xr.concat([index_500hpa_first,index_500hpa_last],dim = coords)
index_500hpa = index_500hpa.to_dataframe().reset_index()
# %%
# plot
fig = pplt.figure(space=0, refwidth="25em",wspace = 3,hspace = 3)

fig.format(
    suptitle = 'spatial pattern and distribution of NAO and EA at 500hpa',
)

gs = pplt.GridSpec(ncols=2, nrows=2, hratios=(1.4, 1,))
modes = ["NAO", "EA"]

for i, mode in enumerate(modes):
    ax1 = fig.subplot(gs[0,i],proj = 'ortho',proj_kw = ({'lon_0':-20,'lat_0':60}))


    ax1.format(
        latlines = 20,
        lonlines = 30,
        coast = True,
        coastlinewidth = 0.5,
        coastcolor = 'charcoal',
        title = modes[i]
    )

    map = ax1.contourf(eof_500hpa.sel(mode = mode),
    levels = np.arange(-1,1.1,0.1),
    extend = 'both')
    if i == 1:
        ax1.colorbar(map, loc = 'r',title = 'std',ticks = 0.2, pad = 2)

    ax2 = fig.subplot(gs[1,i])
    violin =sns.violinplot(
        data = index_500hpa[index_500hpa['mode']==mode],
        y = 'pc',
        x = 'periods',
        ax = ax2,
        orient="v",
    )

    ax2.format(
        ylim = (-4.5,4.5),
        ytickminor=False,
        xlocator = (0,1),
    )

    ax2.spines.right.set_visible(False)
    ax2.spines.top.set_visible(False)

plt.savefig("/work/mh0033/m300883/3rdPanel/docs/source/plots/first10_last10/"+folder+"/spatial_pattern_violin500hpa.png",dpi = 300)

# %%
# plot
fig = pplt.figure(space=0, refwidth="25em",wspace = 3,hspace = 3)

fig.format(
    suptitle = 'spatial pattern and distribution of NAO and EA at 500hpa',
)

gs = pplt.GridSpec(ncols=2, nrows=2, hratios=(1.4, 1,))
modes = ["NAO", "EA"]

for i, mode in enumerate(modes):
    ax1 = fig.subplot(gs[0,i],proj = 'ortho',proj_kw = ({'lon_0':-20,'lat_0':60}))


    ax1.format(
        latlines = 20,
        lonlines = 30,
        coast = True,
        coastlinewidth = 0.5,
        coastcolor = 'charcoal',
        title = modes[i]
    )

    map = ax1.contourf(eof_500hpa.sel(mode = mode),
    levels = np.arange(-1,1.1,0.1),
    extend = 'both')
    if i == 1:
        ax1.colorbar(map, loc = 'r',title = 'std',ticks = 0.2, pad = 2)

    ax2 = fig.subplot(gs[1,i])
    violin =sns.histplot(data = index_500hpa[index_500hpa['mode']==mode],
                         x = 'pc',
                         hue = 'periods', 
                         multiple = "dodge",
                         shrink = 1, 
                         bins = np.arange(-4,4.1,0.5),
                         )
    violin.legend(ncol = 1,labels = ['last10','first10'],title = 'period')
    
    ax2.format(
        xtickminor=False,
        ytickminor=False,
        grid = False,
    )
    ax2.spines.right.set_visible(False)
    ax2.spines.top.set_visible(False)

plt.savefig("/work/mh0033/m300883/3rdPanel/docs/source/plots/first10_last10/"+folder+"/spatial_pattern_hist500hpa.png",dpi = 300)

# %%