import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

from matplotlib.pylab import Circle, setp

def pie(graph, data,
        ax=None,
        ext_labels= None,
        pie_labels = None,
        explodes=None,
        COLORS=None,
        ext_labels_distance = 1.1,
        pie_labels_distance = 0.6,
        pie_labels_digits = 1,
        ext_text_settings=dict(weight='normal'),
        pie_text_settings=dict(weight='normal', color='k'),
        center_circle=0.3,
        title='',
        fig_args=dict(bottom=0.3, left=0.3, top=3.),
        axes_args={},
        pie_args={},
        legend=None):

    """    
    return fig, ax
    """
    
    # getting or creating the axis
    if ax is None:
        if legend is not None:
            fig, ax = graph.figure(with_legend_space=True, left=1.5, right=2, top=0.1)
        else:
            fig, ax = graph.figure(**fig_args)
    else:
        fig = graph.gcf()
        
    if COLORS is None:
        COLORS = graph.colors[:len(data)]
    if (explodes is None):
        explodes = np.zeros(len(data))
    if (ext_labels is None):
        ext_labels = np.zeros(len(data), dtype=str)

    if pie_labels is not None:
        pie_labels_map = {}
        for pl, val in zip(pie_labels, data):
            pie_labels_map[str(np.round(100.*val/np.sum(data),pie_labels_digits))] = pl
        def func(pct):
            return pie_labels_map[str(np.round(pct,pie_labels_digits))]
    else:
        def func(pct):
            return ''
        
    
    wedges, ext_texts, pie_texts = ax.pie(data,
                                          labels=ext_labels,
                                          autopct=func,
                                          explode=explodes,
                                          pctdistance=pie_labels_distance,
                                          labeldistance=ext_labels_distance,
                                          colors=COLORS, **pie_args)
    setp(pie_texts, **pie_text_settings)
    setp(ext_texts, **ext_text_settings)
    
    Centre_Circle = Circle((0,0), center_circle, fc='white')
    ax.add_artist(Centre_Circle)
                                  
    if legend is not None:
        if 'loc' not in legend:
            legend['loc']=(1.21,.2)
        ax.legend(**legend)

    if title!='':
        graph.title(ax, title)
        
    ax.axis('equal')
    return fig, ax


if __name__=='__main__':
    
    from datavyz.main import graph_env

    ge = graph_env('manuscript')

    data = .5+np.abs(np.random.randn(3))*.4

    #plotting
    fig, ax = ge.pie(data,
                     ext_labels = ['Data1', 'Data2', 'Data3'],
                     pie_labels = ['%.1f%%' % (100*d/data.sum()) for d in data],
                     ext_labels_distance=1.2,
                     explodes=0.05*np.ones(len(data)),
                     center_circle=0.2,
                     COLORS = [ge.tab20(x) for x in np.linspace(0,1,len(data))],
                     # pie_args=dict(rotate=90), # e.g. for rotation
                     legend=None)  # set legend={} to have it appearing
    fig.savefig('docs/pie-plot.png')
    ge.show()
