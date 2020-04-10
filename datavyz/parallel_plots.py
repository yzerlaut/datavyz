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
                  ax=None):
    """
    manually constructed:
    everything is normalized to 1
    """

    if ax is None:
        fig, ax = graph.figure(axes_extents=[[[2,1]]], **fig_args)
    ax.axis('off')

    Y = np.array(Y)

    if COLORS is None:
        COLORS=['k' for k in range(Y.shape[0])]

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
                           xycoords='data', size='small', color='k', va='center')

        graph.annotate(ax, SET_OF_LABELS[j], (xx, -0.1), va='top', ha='center')

    ax.set_xlim([-tick_size/2, 1+tick_size/2])
    
    for i in range(Y.shape[0]):
        y_rescaled = []
        for y, (y0, y1) in zip(Y[i,:], SET_OF_LIMS):
            y_rescaled.append((y-y0)/(y1-y0))
        ax.plot(x, y_rescaled, lw=lw, color=COLORS[i])

    return fig, ax


if __name__=='__main__':
    
    from datavyz.main import graph_env
    ge = graph_env('manuscript')

    from sklearn.datasets import load_iris
    dataset = load_iris()
    fig, ax = ge.parallel_plot(dataset['data'],
                              SET_OF_LABELS=['sepal length\n(cm)','sepal width\n(cm)',
                                             'petal length\n(cm)', 'petal width\n(cm)'],
                              COLORS = [ge.viridis(x/2) for x in dataset['target']])
    for i, name in enumerate(dataset['target_names']):
        ge.annotate(ax, name, ((i+1)/3., 1.1), color=ge.viridis(i/2), ha='right')
    fig.savefig('docs/parallel-plot.png')
    ge.show()


