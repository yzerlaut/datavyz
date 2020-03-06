import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
import matplotlib.pylab as plt
import numpy as np

def raster_plot(graph, SPK_LIST, ID_LIST,
                tlim=None,
                ID_ZOOM_LIST=None,
                COLORS=None,
                with_fig=None, MS=1):
    
    if with_fig is not None:
        fig, ax = graph.figure()
    else:
        fig, ax = plt.subplots(1, figsize=(5, 3))
        plt.subplots_adjust(left=.25, bottom=.25)
        
    # time limit
    if tlim is None:
        tlim = np.array([0,1])
        for i in range(len(ID_LIST)):
            try:
                tlim[0] = np.min([tlim[0], np.min(SPK_LIST[i])])
                tlim[1] = np.max([tlim[1], np.max(SPK_LIST[i])])
            except ValueError:
                pass
    # neurons limit
    if ID_ZOOM_LIST is None:
        ID_ZOOM_LIST = []
        for i in range(len(ID_LIST)):
            id_zoom = [0,1]
            try:
                id_zoom[0] = np.min([id_zoom[0], np.min(ID_LIST[i])])
                id_zoom[1] = np.max([id_zoom[1], np.max(ID_LIST[i])])
            except ValueError:
                pass
            ID_ZOOM_LIST.append(id_zoom)
                
    # colors
    if COLORS is None:
        COLORS = ['g']+['r']+['k' for i in range(len(ID_LIST)-2)]

    ii=0 # index for plotting
    for spks, ids, id_zoom, col in zip(SPK_LIST, ID_LIST, ID_ZOOM_LIST, COLORS):
        if ID_ZOOM_LIST is not None:
            cond = (spks>=tlim[0]) & (spks<=tlim[1]) &\
                   (ids>=id_zoom[0]) & (ids<=id_zoom[1])
        else:
            cond = (spks>=tlim[0]) & (spks<=tlim[1])

        spks2, ids2 = spks[cond], ids[cond]
        plt.plot(spks2, ii+ids2, '.', color=col, ms=MS)
        ii+=id_zoom[1]-id_zoom[0]
    tot_neurons_num = int(round(np.sum([(I[1]-I[0]) for I in ID_ZOOM_LIST])/100.,0)*100)
    ax.set_title(str(tot_neurons_num)+' neurons sample', fontsize=14)
    graph.set_plot(ax, xlabel='time (ms)', yticks=[], ylabel='neuron index')
    return fig, ax

def POP_ACT_PLOT(t, POP_ACT_LIST, tlim=None, pop_act_zoom=None,
                 COLORS=None, with_fig=None):
    
    if with_fig is not None:
        fig, ax = plt.gcf(), plt.gca()
    else:
        fig, ax = plt.subplots(1, figsize=(5,3))
        plt.subplots_adjust(left=.25, bottom=.25)
    
    # time limit
    if tlim is None:
        tlim = [t.min(), t.max()]
    # pop act lim
    if pop_act_zoom is None:
        pop_act_zoom = [0,1]
        for i in range(len(POP_ACT_LIST)):
            try:
                pop_act_zoom[0] = np.min([pop_act_zoom[0], POP_ACT_LIST[i].min()])
                pop_act_zoom[1] = np.max([pop_act_zoom[1], POP_ACT_LIST[i].max()])
            except ValueError:
                pass
    # colors
    if COLORS is None:
        COLORS = ['g']+['r']+['k' for i in range(len(POP_ACT_LIST)-2)]

    for act, col in zip(POP_ACT_LIST[::-1], COLORS[::-1]):
        try:
            plt.plot(t[(t>=tlim[0]) & (t<=tlim[1])],
                     act[(t>=tlim[0]) & (t<=tlim[1])], '-', color=col)
        except IndexError:
            print('no activity for a population')
    set_plot(ax, xlabel='time (ms)', ylabel='pop. act. (Hz)',\
                      ylim=pop_act_zoom)
    return fig, ax

if __name__=='__main__':

    from datavyz..graphs import graphs
    mg = graphs()

    raster_plot(mg,
        [np.random.randn(3000),np.random.randn(1000)],
        [np.random.randint(3000, size=3000),np.random.randint(1000, size=1000)])
    
    mg.show()
