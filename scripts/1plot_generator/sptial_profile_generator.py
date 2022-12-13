"""
This script generat the plots for:
- the spatial patterns and distribution of index at 500 hpa
- the violin plots
- the vertical profile of extreme counts
- the return period of 500hpa
- the vertical profile of media return period
"""
#%%
# imports
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import proplot as pplt
import seaborn as sns


#%%
import src.plots.vertical_profile as profile_plots
import src.plots.PDF as pdf_plots
import src.plots.plot_violin as violin_plots
import src.plots.spatial_distribution_plot as spatial_dis_plots
import src.extreme.period_pattern_extreme as extreme


#%%
from pyextremes import get_extremes, get_return_periods

#%%
import importlib
importlib.reload(spatial_dis_plots)
#%%
class first10_last10_index:
    def __init__(
        self,
        vertical_eof: str,  # 'ind' or 'dep'
        fixed_pattern: str,  # 'all','first','last'
    ):
        self.vertical_eof = vertical_eof
        self.fixed_pattern = fixed_pattern

        self.prefix = (
            self.vertical_eof + "_" + self.fixed_pattern + "_"
        )  # for name/ ind_all_

        self.eof, self.pc, self.fra = self.read_data()
        self.pc['time'] = self.pc.indexes['time'].to_datetimeindex()

        # data of 500 hpa.
        self.eof_500hpa, self.pc_500hpa, self.fra_500hpa = self.sel_500hpa()
        self.pc_500hpa_df = self.first10_last10_index_df(self.pc_500hpa)

        # index of first10 and last10
        self.first10_pc = self.pc.isel(time=slice(0, 10))
        self.last10_pc = self.pc.isel(time=slice(-10, self.pc.time.size))

        # extreme counts
        self.first_ext_count = extreme.period_extreme_count(self.first10_pc)
        self.last_ext_count = extreme.period_extreme_count(self.last10_pc)

        # the destination for savinig plots
        self.save_dir = (
            "/work/mh0033/m300883/3rdPanel/docs/source/plots/class_decompose/"
        )

    def read_data(self):
        print("reading data...")
        odir = (
            "/work/mh0033/m300883/3rdPanel/data/class_decompose/"
            + self.fixed_pattern
            + "Pattern/"
            + self.vertical_eof
            + "/"
        )
        eof = xr.open_dataset(odir + self.prefix + "eof.nc").eof

        pc = xr.open_dataset(odir + self.prefix + "pc.nc").pc

        fra = xr.open_dataset(odir + self.prefix + "fra.nc").exp_var
        return eof, pc, fra

    def sel_500hpa(self):
        eof_500 = self.eof.sel(hlayers=50000)
        pc_500 = self.pc.sel(hlayers=50000)
        fra_500 = self.fra.sel(hlayers=50000)

        return eof_500, pc_500, fra_500

    def first10_last10_index_df(self, index):

        """
        select the period data, transform to dataframe
        """
        first10 = index.isel(
            time=slice(0, 10)
        )  # first10 years projectecd on all, standardized with whole time
        last10 = index.isel(time=slice(-10, self.pc.time.size))

        # to dataframe()
        coords = xr.IndexVariable(dims="periods", data=["first10", "last10"])
        index_500hpa = xr.concat([first10, last10], dim=coords)
        index_500hpa = index_500hpa.to_dataframe().reset_index()

        return index_500hpa

    def plot_500hpa_spatial_violin(self):
        """
        sptail maps and violin plots of indexes.
        """
        fig = spatial_dis_plots.spatialMap_violin(
            self.eof_500hpa, self.pc_500hpa_df, self.fra_500hpa
        )

        plt.savefig(
            self.save_dir + self.prefix + "spatial_pattern_violin500hpa.png", dpi=300
        )

    def plot_500hpa_spatial_hist(self):
        """
        sptail maps and violin plots of indexes.
        """
        fig = spatial_dis_plots.spatialMap_hist(self.eof_500hpa, self.pc_500hpa_df)

        plt.savefig(
            self.save_dir + self.prefix + "spatial_pattern_hist500hpa.png", dpi=300
        )

    def violin_profile(self):
        fig = violin_plots.plot_vilion(self.first10_pc, self.last10_pc, "whole")
        plt.savefig(self.save_dir + self.prefix + "violin_profile.png", dpi=300)


    def extreme_count_profile(self, mode):
        fig = profile_plots.plot_vertical_profile(
            self.first_ext_count, self.last_ext_count, mode=mode, std_type="all"
        )
        plt.savefig(
            self.save_dir + self.prefix + mode + "_extreme_count_profile.png", dpi=300
        )


# %%
