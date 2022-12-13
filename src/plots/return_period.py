import proplot as pplt
import src.EVT.return_period as EVT

def plot_return_period(index,mode, hlayers = 50000):
    """
    return period plot
    """

    first10_all_pos, last10_all_pos, first10_median_pos, last10_median_pos, first10_all_neg, last10_all_neg, first10_median_neg, last10_median_neg\
        =EVT.mode_return_period(index, mode = mode, hlayers = hlayers)
    
    fig, axes = pplt.subplots(nrows = 1,ncols = 2, figwidth=8, span=False,share = False)

    axes.format(
        abc = 'a',
        abcloc = 'ul',
        xlim = (0,10),
        xminorlocator = 'null',
        yminorlocator = 'null',
        suptitle = f"return period of {mode} index at {hlayers/100:.0f}hpa",
        xlabel = "return period / yr",
        ylabel = "pc / std"
    )

    # pos
    axes[0].scatter(x = 'return period',y = 'pc', data = first10_all_pos,label = 'first10')
    axes[0].scatter(x = 'return period',y = 'pc', data = last10_all_pos,color = 'r',label = 'last10')

    axes[0].scatter(x = 'return period',y = 'pc', data = first10_median_pos,color = 'k',label = 'first10 median',marker = '+',s = 80)
    axes[0].scatter(x = 'return period',y = 'pc', data = last10_median_pos,color = 'k',label = 'last10 median',marker = "*",s = 80)

    # neg
    axes[1].scatter(x = 'return period',y = 'pc', data = first10_all_neg,label = 'first10')
    axes[1].scatter(x = 'return period',y = 'pc', data = last10_all_neg,color = 'r',label = 'last10')

    axes[1].scatter(x = 'return period',y = 'pc', data = first10_median_neg,color = 'k',label = 'first10 median',marker = '+',s = 80)
    axes[1].scatter(x = 'return period',y = 'pc', data = last10_median_neg,color = 'k',label = 'last10 median',marker = "*",s = 80)

    if mode == 'NAO':
        ix = axes[1].inset_axes(
            [6,-2.8,3.8,0.2],transform = 'data',zoom = False
        )
        ix.format(
            xlim = (0,300),
            ylim = (-4,-2.6),
            xminorlocator = 'null',
            yminorlocator = 'null',
            title = "zoom out"
        )
        ix.scatter(x = 'return period',y = 'pc', data = last10_all_neg,color = 'r')
        ix.set_xlabel(None)
        ix.set_ylabel(None)

    axes[0].legend(loc = 'lr',ncols = 1)