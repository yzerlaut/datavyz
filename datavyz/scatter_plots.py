from matplotlib.cm import viridis
from scipy.stats import pearsonr
import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from datavyz.draw_figure import figure
from datavyz.adjust_plots import set_plot, compute_axes_args

def two_variable_analysis(first_observations,
                          second_observations,
                          cls=None,
                          with_correl_annotation=True,
                          ylabel='y-value', xlabel='x-value', title='',
                          fig_args={'right':4}, axes_args={},
                          colormap=None, ms=4):

    if len(first_observations)!=len(second_observations):
        print('Pb with sample size !! Test is not applicable !!')

    if cls is None:
        from datavyz import ge as cls
    
    if colormap is None:
        def colormap(x):
            return 'k'
        
    fig, ax = cls.figure(**fig_args)
    
    for i in range(len(first_observations)):
        ax.plot([first_observations[i]], [second_observations[i]], 'o', color=colormap(i/(len(first_observations)-1)), ms=ms)

    if with_correl_annotation:
        c, pval = pearsonr(first_observations, second_observations)
        lin = np.polyfit(first_observations, second_observations, 1)
        x = np.linspace(np.min(first_observations), np.max(first_observations), 3)
        ax.plot(x, np.polyval(lin, x), 'k:', lw=1)
        cls.annotate(ax, '  Pearson\ncorrelation:\n c=%.2f,\n p=%.2f' % (c, pval), (1.03,1.), va='top')
    else:
        c, pval = 0., 1.

    cls.set_plot(ax, **compute_axes_args(axes_args, xlabel=xlabel, ylabel=ylabel, title=title))
    
    return fig, ax, c, pval


def scatter(self,
            x=None, y=None, sx=None, sy=None, 
            X=None, Y=None, sX=None, sY=None,
            color=None, edgecolor=None, alpha=1.,
            COLORS=None, colormap=viridis,
            ax=None, fig=None,
            lw=0, alpha_std=0.3,
            ms=None,
            m='', ls='-',
            xlabel='', ylabel='', bar_label='', title='',
            label=None,
            LABELS=None,
            fig_args={},
            axes_args={},
            bar_legend_args=None,
            legend_args=None,
            no_set=False):
    
    """    
    return fig, ax
    """
    # getting or creating the axis
    if ax is None:
        fig, ax = self.figure(**fig_args)
        
    if color is None:
        color = self.default_color
    if ms is None:
        ms = self.markersize
        
    if (y is None) and (Y is None):
        y = x
        x = np.arange(len(y))

    if (Y is not None):
        if (X is None) and (x is not None):
            X = [x for i in range(len(Y))]
        elif (X is None):
            X = [np.arange(len(y)) for y in Y]

        multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,
                        colormap=colormap,
                        lw=lw, ms=ms)
    else:
        single_curve(ax, x, y, sx, sy,
                     color=color, edgecolor=edgecolor, alpha=alpha,
                     label=label, lw=lw, ms=ms)

    if bar_legend_args is not None:
        cb = self.bar_legend(ax, **bar_legend_args)
        # self.build_bar_legend(np.arange(len(LABELS)+1),
                              # cb,
                              # colormap,
                              # label=bar_label,
                              # ticks_labels=LABELS)

    if legend_args is not None:
        ax.legend(**legend_args)

    if not no_set:
        self.set_plot(ax, **self.compute_axes_args(axes_args, xlabel=xlabel, ylabel=ylabel, title=title))

    return fig, ax


def single_curve(ax, x, y, sx, sy,
                 color='k', edgecolor='None', marker='o', alpha=1,
                 label='',
                 lw=0, ms=3, elw=1):
    if (sy is None) and (sx is None):
        ax.scatter(x, y, marker=marker,
                   color=color, edgecolor=edgecolor,
                   alpha=alpha, lw=lw, s=ms,
                   label=label)
    elif (sy is None):
        ax.errorbar(x, y, xerr=sx,
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)
    elif (sx is None):
        ax.errorbar(x, y, yerr=sy,
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)
    else:
        ax.errorbar(x, y, xerr=sx, yerr=sy,
                    marker=marker, color=color,
                    lw=lw, ms=ms, elinewidth=elw, label=label)

def multiple_curves(ax, X, Y, sX, sY, COLORS, LABELS,
                    marker='o', lw=0,
                    colormap=viridis, ms=3, elw=1):
    
    # meaning we have to plot several curves
    if COLORS is None:
        COLORS = [colormap(i/(len(Y)-1)) for i in range(len(Y))]
    if (LABELS is None):
        LABELS = ['Y'+str(i+1) for i in range(len(Y))]

    if (sY is None) and (sX is None):
        for x, y, c, label in zip(X, Y, COLORS, LABELS):
            ax.errorbar(x, y,
                       color=c, marker=marker,
                       lw=lw, ms=ms, label=label)
    elif (sY is None):
        for x, y, sx, c, label in zip(X, Y, sX, COLORS, LABELS):
            ax.errorbar(x, y, xerr=sx,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)
    elif (sX is None):
        for x, y, sy, c, label in zip(X, Y, sY, COLORS, LABELS):
            ax.errorbar(x, y, yerr=sy,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)
    else:
        for x, y, sx, sy, c, label in zip(X, Y, sX, sY, COLORS, LABELS):
            ax.errorbar(x, y, xerr=sx, yerr=sy,
                        color=c, marker=marker,
                        lw=lw, ms=ms, elinewidth=elw, label=label)


if __name__=='__main__':
    
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
    from datavyz import ge
    
    fig, ax = ge.scatter(np.random.randn(20),
                         np.random.randn(20),
                         color='none', edgecolor=ge.brown, lw=5, alpha=.3, ms=20,
                         xlabel='xlabel (xunit)',
                         ylabel='ylabel (yunit)')
    # fig, ax = ge.scatter(Y=np.random.randn(4, 10),
    #                      sY=np.random.randn(4, 10),
    #                      xlabel='xlabel (xunit)',
    #                      ylabel='ylabel (yunit)',
    #                      title='datavyz demo plot')
    # ge.savefig(fig, 'docs/scatter.png')

    ge.two_variable_analysis(np.random.randn(10), np.random.randn(10),
                             colormap=viridis, fig_args=dict(right=5))
    ge.show()
    
