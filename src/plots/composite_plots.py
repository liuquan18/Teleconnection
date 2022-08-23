from typing_extensions import assert_type
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


def vertical_profile(counts,mode = 'NAO'):
    """
    using matplotlib to plot the vertical profile.
    solve the problem of y-axis sort.
    """

    counts['hlayers'] = (counts['hlayers']/100).astype(int)
    y = counts['hlayers'].values

    # plot  
    fig, axes = plt.subplots(figsize = (6,6),dpi = 150)
    plt.subplots_adjust(wspace = 0.3)

    modes = counts.mode
    extr_types = counts.extr_type

    

    for i, mode in enumerate(modes):
        for j, extr_type in enumerate(extr_types):
            data = counts.sel(mode = mode, extr_type=extr_type)
            plt.plot(data,y)


"""
    for i, ax in enumerate(axes):  # periods
        period_data = all[i]

        for j, pattern in enumerate(period_data.columns.levels[0]):
            pattern_data = period_data[pattern].sort_index()
            y = (pattern_data.index.values/100).astype(int)

            ax.plot(pattern_data['pos'], y, color = colors[j])
            ax.plot(pattern_data['neg'], y, color = colors[j],dashes = [3,3])

            ax.set_ylim(1000,200)
            if i<2:
                ax.set_xlim(0,50)
            elif i ==2:
                ax.set_xlim(-10,40)

            ax.set_title(f"{mode} {periods[i]}")

            ax.set_xlabel("extreme counts")
            if i == 0:
                ax.set_ylabel("gph/hpa")

    # legend
    custom_lines = [Line2D([0],[0],color = colors[0]),
                    Line2D([0],[0],color = colors[1]),
                    Line2D([0],[0],color = colors[2]),
                    Line2D([0],[0],color = colors[3]),
                    Line2D([0],[0],color = None,alpha = 0),
                    Line2D([0],[0],color = 'k'),
                    Line2D([0],[0],dashes = [3,3],color = 'k')]
    type_legend = axes[-1].legend(custom_lines,['first','all','last','dynamic','','pos','neg'],
    loc = 'lower right',fontsize = 6)
    axes[-1].add_artist(type_legend)
"""