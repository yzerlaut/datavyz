import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

from datavyz.draw_figure import figure
from datavyz.adjust_plots import set_plot


###########################################################
######  Histogram
###########################################################

def hist(graph,
         x, bins=20, ax=None,
         orientation='horizontal',
         edgecolor='k', facecolor='lightgray',
         c=None,
         lw=0.3,
         xlabel='', ylabel='count', title='',
         normed=False,
         fig_args={}, axes_args={}):
    
    hist, be = np.histogram(x, bins=bins, density=normed)

    if c is not None:
        facecolor = c
        lw = 0
        
    if ax is None:
        fig, ax = graph.figure(**fig_args)
    else:
        fig = plt.gcf()

    if orientation=='vertical':
        ax.barh(.5*(be[1:]+be[:-1]), hist, height=be[1]-be[0], 
                edgecolor=edgecolor, facecolor=facecolor, lw=lw)
    elif orientation=='horizontal':
        ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], 
                edgecolor=edgecolor, facecolor=facecolor, lw=lw)

    if 'xlabel' not in axes_args:
        axes_args['xlabel'] = xlabel
    if 'ylabel' not in axes_args:
        axes_args['ylabel'] = ylabel
        
    graph.set_plot(ax, **axes_args)
    if title!='':
        graph.title(ax, title)
    
    return fig, ax


if __name__=='__main__':

    from datavyz.graph_env import graph_env
    ge = graph_env('manuscript')

    fig, ax = ge.hist(np.random.randn(100), xlabel='some value')
    ge.show()

