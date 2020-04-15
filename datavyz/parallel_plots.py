import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *


def parallel_plot(graph, Y,
                  SET_OF_LIMS=None,
                  SET_OF_TICKS=None,
                  SET_OF_LABELS=None,
                  COLORS=None,
                  tick_number = 5, tick_size=0.01,
                  expansion_factor=0.01,
                  color='k', lw=0.5,
                  fig_args=dict(bottom=.5, left=.5, right=2.),
                  label_annotation_args=dict(va='top', ha='center',rotation=0.),                  
                  ticks_annotation_args=dict(size='small', color='k', va='center'),
                  ax=None):
    """
    manually constructed:
    everything is normalized to 1
    """

    if ax is None:
        fig, ax = graph.figure(axes_extents=[[[2,1]]], **fig_args)
    else:
        fig = None
        
    ax.axis('off')

    Y = np.array(Y)

    if COLORS is None:
        COLORS=[color for k in range(Y.shape[0])]

    if SET_OF_LIMS is None:
        SET_OF_LIMS = [((1-expansion_factor)*Y[:,i].min(),
                        (1+expansion_factor)*Y[:,i].max())\
                       for i in range(Y.shape[1])]
    if SET_OF_TICKS is None:
        SET_OF_TICKS = [\
            np.linspace(SET_OF_LIMS[j][0], SET_OF_LIMS[j][1], tick_number)\
                        for j in range(Y.shape[1])]

    if SET_OF_LABELS is None:
        SET_OF_LABELS = ['Dim%i' %(j+1) for j in range(Y.shape[1])]
    elif SET_OF_LABELS=='None':
        SET_OF_LABELS = ['' for j in range(Y.shape[1])]


    # x-abcissa
    x = np.linspace(0, 1, Y.shape[1])
    for j, xx in enumerate(x):
        ax.plot([xx,xx], [0,1], 'k-', lw=.5)
        # ticks
        for tn in range(tick_number):
            ax.plot([xx-tick_size/2, xx+tick_size/2],
                    tn/(tick_number-1)*np.ones(2), 'k-', lw=.5)
            
            graph.annotate(ax, '%.1f' % np.linspace(SET_OF_LIMS[j][0],
                                                    SET_OF_LIMS[j][1],
                                                    tick_number)[tn],
                           (xx, tn/(tick_number-1)),
                           xycoords='data',
                           **ticks_annotation_args)

        graph.annotate(ax, SET_OF_LABELS[j], (xx, -0.1),
                       **label_annotation_args)

    ax.set_xlim([-tick_size/2, 1+tick_size/2])
    
    for i in range(Y.shape[0]):
        y_rescaled = []
        for y, (y0, y1) in zip(Y[i,:], SET_OF_LIMS):
            y_rescaled.append((y-y0)/(y1-y0))
        ax.plot(x, y_rescaled, lw=lw, color=COLORS[i])

    return fig, ax

def components_plot(graph,
                    components,
                    features_label='features',
                    components_label='components',
                    axes_args={'size':'small', 'ha':'right', 'va':'center'},
                    fig_args=dict(figsize=(2.,.4), left=.5, top=5)):

    fig, AX = graph.figure(axes=(components.shape[0],1), **fig_args)

    SET_OF_LIMS = [(y1,y2) for (y1,y2) in zip(components.min(axis=0), components.max(axis=0))]
    for i, ax in enumerate(AX):
        graph.parallel_plot([components[i,:]], ax=ax,
                         ticks_annotation_args=dict(size='xxx-small', color='k', va='center'),
                         SET_OF_LIMS=SET_OF_LIMS, lw=2, SET_OF_LABELS='None')
        # graph.annotate(ax, 'comp. %i' % (i+1), (-0.01,.5), **annotation_args)

    graph.arrow(fig, [.18, .9, 0., -0.8], width=.01, head_width=0.05)
    graph.annotate(fig, components_label, (.08,.5), rotation=90)
    graph.arrow(fig, [0.1, .87, 0.83, 0.], width=.01, head_width=0.05)
    graph.annotate(fig, features_label, (.55,.95))
    
    return fig, AX

if __name__=='__main__':
    
    from datavyz import ge as ge

    # LOADING THE DATA
    from sklearn.datasets import load_breast_cancer
    data = load_breast_cancer()

    # PERFORMING PCA
    from sklearn.decomposition import PCA as sklPCA
    pca = sklPCA(n_components=10)
    pca.fit_transform(data['data'])

    # PLOT
    fig, AX = ge.components_plot(pca.components_)
    ge.savefig(fig, 'docs/components-plot.png')
    ge.show()


    from sklearn.datasets import load_iris
    dataset = load_iris()
    fig, ax = ge.parallel_plot(dataset['data'],
                              SET_OF_LABELS=['sepal length\n(cm)','sepal width\n(cm)',
                                             'petal length\n(cm)', 'petal width\n(cm)'],
                              COLORS = [ge.viridis(x/2) for x in dataset['target']])
    for i, name in enumerate(dataset['target_names']):
        ge.annotate(ax, name, ((i+1)/3., 1.1), color=ge.viridis(i/2), ha='right')
    ge.savefig(fig, 'docs/parallel-plot.png')
    ge.show()



