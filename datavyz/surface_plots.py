import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

from datavyz.scaling import *
from datavyz.legend import build_bar_legend_continuous
    
def twoD_plot(graph,
              x, y, z,
              ax=None, acb=None, fig=None,
              diverging=False,
              colormap=cm.viridis,
              alpha=1.,
              vmin=None,
              vmax=None,
              # scale='log',
              bar_legend=None,
              aspect='equal',
              interpolation='none'):
    """
    surface plots for x, y and z 1 dimensional data

    switch to bar_legend=None to remove the bar legend
    """
    
    if (ax is None) and (acb is None):
        fig, ax, acb = graph.figure(figsize=(.9,1), with_space_for_bar_legend=True)
    else:
        fig = plt.gcf()
        
    if diverging and (colormap==cm.viridis):
        colormap = cm.PiYG # we switch to a diverging colormap
        
    x, y = np.array(x), np.array(y)
    Z = np.ones((len(np.unique(y)), len(np.unique(x))))*np.nan
    for i, yy in enumerate(np.unique(y)):
        cond1 = y==yy
        for j, xx in enumerate(np.unique(x[cond1])):
            try:
                Z[i,j] = z[cond1][x[cond1]==xx]
            except ValueError:
                print('multiple values for the same (x=', xx, ', y=', yy, ') couple: ', z[cond1][x[cond1]==xx])
                Z[i,j] = np.mean(z[cond1][x[cond1]==xx])
    # z1 = np.array(Z).reshape(len(np.unique(y)), len(np.unique(x)))
    z1 = Z
    
    if vmin is None:
        if diverging:
            vmin = -np.max(np.abs(z))
        else:
            vmin = np.min(z)
    if vmax is None:
        if diverging:
            vmax = np.max(np.abs(z))
        else:
            vmax = np.max(z)
            
    ac = ax.imshow(z1,
                   interpolation=interpolation,
                   extent = (x.min(), x.max(), y.min(), y.max()),
                   vmin = vmin,
                   vmax = vmax,
                   alpha=alpha,
                   cmap=colormap,
                   origin='lower',
                   aspect=aspect)


    """
    Need to polish the integration of "build_bar_legend" within this function
    """
    if bar_legend is not None:
        for key, val in zip(['ticks', 'scale', 'label', 'labelpad'],
                            [np.unique(np.round(np.linspace(vmin, vmax, 5), 1)),
                             'linear', '', 1.]):
            if key not in bar_legend:
                bar_legend[key] = val
        build_bar_legend_continuous(acb, colormap,
                                    bounds=[vmin, vmax],
                                    scale=bar_legend['scale'],
                                    ticks=bar_legend['ticks'],
                                    label=bar_legend['label'],
                                    labelpad=bar_legend['labelpad'])
        
    return fig, ax, acb
    

def matrix(graph,
           x, y=None, z=None,
           ax=None, acb=None, fig=None,
           diverging=False,
           colormap=cm.viridis,
           alpha=1.,
           vmin=None, vmax=None,
           bar_legend={}, # switch to None to make it disappear
           aspect='equal', # switch to 'auto' if needed
           interpolation='none'):

    if (z is None) and (y is None):
        z = x
        x, y = np.meshgrid(np.arange(z.shape[0]), np.arange(z.shape[1]), indexing='ij')
        
    if (ax is None) and (acb is None):
        fig, ax, acb = graph.figure(figsize=(.9,1), with_space_for_bar_legend=True)
    else:
        fig = plt.gcf()
        
    if diverging and (colormap==cm.viridis):
        colormap = cm.PiYG # we switch to a diverging colormap

    if vmin is None:
        vmin=z.min()
    if vmax is None:
        vmax=z.max()

    im = ax.imshow(z.T,
                   interpolation=interpolation,
                   extent = (x.min(), x.max(), y.min(), y.max()),
                   vmin = vmin,
                   vmax = vmax,
                   alpha=alpha,
                   cmap=colormap,
                   origin='lower',
                   aspect=aspect)
    
    if bar_legend is not None:
        
        for key, val in zip(['ticks', 'scale', 'label', 'labelpad'],
                            [np.unique(np.round(np.linspace(vmin, vmax, 5), 1)),
                             'linear', '', 1.]):
            if key not in bar_legend:
                bar_legend[key] = val
                
        build_bar_legend_continuous(acb, colormap,
                                    bounds=[vmin, vmax],
                                    scale=bar_legend['scale'],
                                    ticks=bar_legend['ticks'],
                                    label=bar_legend['label'],
                                    labelpad=bar_legend['labelpad'])
        
    return fig, ax, acb


if __name__=='__main__':
    
    from datavyz.main import graph_env

    ge = graph_env('manuscript')

    x, y = np.meshgrid(np.arange(1, 20), np.arange(1, 11), indexing='ij')
    z = y

    fig1, ax, _ = matrix(ge, z)
    ge.set_plot(ax, xlabel='x-label (X)', ylabel='y-label (Y)')

    
    x, y, z = np.array(x).flatten(),\
              np.array(y).flatten(),\
              np.array(z).flatten()*np.random.randn(len(z.flatten()))
    index = (x<15) & (y<x)
    # np.random.shuffle(index)
    x, y, z = x[index], y[index], z[index]

    fig2, ax, acb = twoD_plot(ge, x, y, z,
                              vmin=-7, vmax=7,
                              bar_legend={'label':'color',
                                          'color_discretization':20})
    ge.set_plot(ax, xlabel='x-label (X)', ylabel='y-label (Y)')
    
    fig2.savefig('docs/surface-plot.png')
    ge.show()
