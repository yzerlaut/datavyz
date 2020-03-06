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
            fig, ax = graph.figure(with_legend_space=True)
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
