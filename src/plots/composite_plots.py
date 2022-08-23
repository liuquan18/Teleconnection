import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def comp_count_plot(
    count:xr.DataArray,
    mode: str
    ):
    """
    plot the barplot of the extreme counts
    """
    count = count.sel(mode =mode).to_dataframe()
    count = count[['pc']].unstack(1)
    count.plot(kind='bar',stacked=True)

