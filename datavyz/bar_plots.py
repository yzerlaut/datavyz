import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

from scipy.stats import ttest_rel, ttest_ind


def bar(graph, y,
        yerr=None,
        bins=None, width=None,
        ax=None,
        lw=0, alpha=1., bottom=0.,
        color='silver', COLORS=None,
        xlabel='', ylabel='', title='', label='',
        fig_args={},
        axes_args={},
        legend_args=None,
        no_set=False):

    """    
    return fig, ax
    """
    # getting or creating the axis
    if ax is None:
        fig, ax = graph.figure(**fig_args)
    else:
        fig = graph.gcf()
        
    if COLORS is None:
        COLORS = [color for i in range(len(y))]
        
    if bins is None:
        bins = np.arange(len(y))
    if width is None:
        width = .9*(bins[1]-bins[0])
        
    if axes_args=={}:
        axes_args = {'xticks':bins, 'xticks_labels':[]}

    if yerr is None:
        yerr = 0.*y
        
    ax.bar(bins, y, yerr=yerr, width=width,
           color=COLORS,
           lw=lw, alpha=alpha,
           bottom=bottom)

    if legend_args is not None:
        ax.legend(**legend_args)

    if 'xlabel' not in axes_args:
        axes_args['xlabel'] = xlabel
    if 'ylabel' not in axes_args:
        axes_args['ylabel'] = ylabel

    if not no_set:
        graph.set_plot(ax, **axes_args)
    if title!='':
        graph.title(ax, title)

    return fig, ax


def related_samples_two_conditions_comparison(graph,
                                              first_observations,
                                              second_observations,
                                              with_annotation=True,
                                              xticks_rotation=0,
                                              lw=.5,
                                              color1='#1f77b4', color2='#ff7f0e',
                                              ylabel='value',
                                              xticks=[0, 1],
                                              xticks_labels=['cond1', 'cond2'],
                                              fig_args=dict(right=4., figsize=(.7,1.), left=1.2, top=1.5),
                                              colormap=None):

    if len(first_observations)!=len(second_observations):
        print('Pb with sample size !! Test is not applicable !!')

    pval = ttest_rel(first_observations, second_observations)[1]

    if colormap is None:
        def colormap(x):return 'k'
        
    fig, ax = graph.figure(**fig_args)
    
    for i in range(len(first_observations)):
        ax.plot([0, 1], [first_observations[i], second_observations[i]], '-', lw=lw, color=colormap(i/(len(first_observations)-1)))
        
    ax.bar([0], [np.mean(first_observations)], yerr=np.std(first_observations), color=color1, lw=lw)
    ax.bar([1], [np.mean(second_observations)], yerr=np.std(second_observations), color=color2, lw=lw)
    
    if with_annotation:
        graph.title(ax, 'paired t-test:\np=%.2f' % pval)
        
    graph.set_plot(ax, ylabel=ylabel,
             xticks=xticks,
             xticks_labels=xticks_labels,
             xticks_rotation=xticks_rotation)
    
    return fig, ax, pval

def unrelated_samples_two_conditions_comparison(graph,
                                                first_observations,
                                                second_observations,
                                                with_annotation=True,
                                                xticks_rotation=0,
                                                lw=.5,
                                                color1='#1f77b4', color2='#ff7f0e',
                                                ylabel='value',
                                                xticks=[0, 1],
                                                fig_args=dict(right=4., figsize=(.7,1.), left=1.2, top=1.5),
                                                xticks_labels=['cond1', 'cond2']):

    pval = ttest_ind(first_observations, second_observations)[1]

    fig, ax = graph.figure(**fig_args)
    
    for i in range(len(first_observations)):
        ax.plot([0+np.random.randn()*.1], [first_observations[i]], 'o', ms=2, color=color1)
        ax.plot([1+np.random.randn()*.1], [second_observations[i]], 'o', ms=2, color=color2)
        
    ax.bar([0], [np.mean(first_observations)], yerr=np.std(first_observations), color=color1, lw=lw, alpha=.7)
    ax.bar([1], [np.mean(second_observations)], yerr=np.std(second_observations), color=color2, lw=lw, alpha=.7)
    
    if with_annotation:
        graph.title(ax, 'unpaired t-test:\np=%.2f' % pval)
        
    graph.set_plot(ax, ylabel=ylabel,
             xticks=xticks,
             xticks_labels=xticks_labels,
             xticks_rotation=xticks_rotation)
    
    return fig, ax, pval

if __name__=='__main__':

    from datavyz import ge

    # fig1, _ = ge.unrelated_samples_two_conditions_comparison(\
    #     np.random.randn(10)+1.4, np.random.randn(12)+1.4,
    #     xticks_labels=['$\||$cc($V_m$,$V_{ext}$)$\||$', '$cc(V_m,pLFP)$'],
    #     xticks_rotation=75)
    
    fig, ax, pval = ge.related_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
                                                                 xticks_labels=['Ctrl', 'Test'],
                                                                 xticks_rotation=45)

    ge.savefig(fig, 'docs/related-samples.png')
    
    fig, ax, pval = ge.unrelated_samples_two_conditions_comparison(np.random.randn(10)+2., np.random.randn(10)+2.,
                                                                   xticks_labels=['Ctrl', 'Test'],
                                                                   xticks_rotation=45)
    ge.savefig(fig, 'docs/unrelated-samples.png')
    
    # # ge.bar(np.random.randn(5), yerr=.3*np.random.randn(5), bottom=-3, COLORS=ge.colors[:5])
    ge.show()
    
