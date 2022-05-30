"""
some classical/typical plots of neurophysiology
"""
import numpy as np
import matplotlib.pylab as plt


##############################################################
####  plotting experimental data #############################
##############################################################

def Ca_trace_plot(graph, Data,
                  Data_original=None, t=None,
                  tzoom=[0, np.inf],
                  colors = None,
                  ax=None,
                  fig_args = None,
                  title='',
                  bar_fraction=0.7,
                  Tbar=10, Tbar_label=None, lw=0.5):
    

    keys = [key for key in Data]
    ncells = len(keys)
    if t is None:
        t = np.arange(len(Data[keys[0]]))
    t_cond = (t>=tzoom[0]) & (t>=tzoom[0])

    if ax is None:
        if fig_args is None:
            fig_args = dict(axes_extents=(4, int(.3*len(keys))+1), left=.5, bottom=0., top=.5)
        fig, ax = graph.figure(**fig_args)
    else:
        fig = None
    ax.axis('off')
    
    if colors is None:
        colors = [graph.colors[i%10] for i, k in enumerate(Data)]
        
    for i, key in enumerate(Data):
        if Data_original is not None:
            norm_factor = 1./(np.max(Data_original[key][t_cond])-np.min(Data_original[key][t_cond]))
            baseline = np.min(Data_original[key][t_cond])
            norm_Data_original = (Data_original[key][t_cond]-baseline)*norm_factor
            ax.plot(t[t_cond], ncells-i+norm_Data_original, colors[i], lw=0.2, alpha=.3)
        else:
            norm_factor = 1./(np.max(Data[key][t_cond])-np.min(Data[key][t_cond]))
            baseline = np.min(Data[key][t_cond]) 
           
        norm_Data = norm_factor*(Data[key][t_cond]-baseline)

        ax.plot(t[t_cond], ncells-i+norm_Data, colors[i], lw=lw)
        graph.annotate(ax, key, (t[t_cond][-1], ncells-i+1), color=colors[i],
                    xycoords='data', ha='left', size='small', va='top')
        
        # scale for that cell
        ax.plot([0, 0], [ncells-i, ncells-i+bar_fraction], color=graph.default_color)
        if 100.*norm_factor<1:
            graph.annotate(ax, '%.1f%%' % (100.*norm_factor),
                    (0, ncells-i), xycoords='data', ha='right', size='small')
        else:
            graph.annotate(ax, '%i%%' % int(100.*norm_factor),
                    (0, ncells-i), xycoords='data', ha='right', size='small')
        
    ax.plot([0, Tbar], [ncells+1, ncells+1], color=graph.default_color)
    if Tbar_label is None:
        Tbar_label = '%is' % Tbar
    graph.annotate(ax, Tbar_label, (0, ncells+1), xycoords='data', size='small')

    if title!='':
        graph.annotate(ax, title, (.5, 1.), ha='center', va='top')
        
    return fig, ax


#####################################
####  plotting model data ###########
#####################################


def response_to_current_pulse(graph, t, Vm, I, spikes,
                              Tbar=50.,
                              Vm_scale=10.,
                              loc=(150,-30),
                              Vpeak=-10,
                              with_artificial_spikes=True):

    fig, ax = graph.figure(figsize=(1.2,.8))
    
    ax.plot(t, Vm, 'k-', lw=1)
    try:
        DI = I.max()-I.min()
        I_Vm = Vm.min()-3-Vm_scale+I/DI*Vm_scale
        ax.plot(t, I_Vm, '-', color='grey', lw=1)
    except ZeroDivisionError:
        DI = 0
    if with_artificial_spikes:
        for tt in spikes:
            ax.plot([tt,tt], [Vm.max(), Vpeak], 'k:', lw=1)
        
    graph.draw_bar_scales(ax, 
                          Xbar=Tbar, Xbar_label="%ims"%Tbar,
                          Ybar=Vm_scale, Ybar_label="%imV" % Vm_scale,
                          # loc=loc,
                          # orientation='right-top',
                          Ybar_label2="%ipA" % DI, ycolor2='grey')
    graph.set_plot(ax, [])
    return fig, ax

def response_to_multiple_current_pulse(graph,
                                       t, VMS, II, SPIKES,
                                       Tbar=50.,
                                       Vm_scale=10.,
                                       loc=(150,-30),
                                       Vpeak=-10,
                                       colormap=None,
                                       with_artificial_spikes=True):

    fig, ax = graph.figure(figsize=(1.2,.8),
                           bottom=0.01, left=0.01, right=0.01, top=0.01)

    if colormap is None:
        colormap = graph.copper
        
    Vm_min = np.min([np.min(Vm) for Vm in VMS])
    DI_max = np.max([np.max(I)-np.min(I) for I in II])
    for i, Vm, I, spikes in zip(range(len(VMS)), VMS, II, SPIKES):
        ax.plot(t, Vm, '-', lw=1, color=colormap(i/(len(VMS)+1)))
        I_Vm = Vm_min-1.3*Vm_scale+I/DI_max*Vm_scale
        ax.plot(t, I_Vm, '-', color=colormap(i/(len(VMS)+2)), lw=1)
        if with_artificial_spikes:
            for tt in spikes:
                ax.plot([tt,tt], [Vm.max(), Vpeak], ':', lw=1, color=colormap(i/(len(VMS)+2)))
        
    graph.draw_bar_scales(ax, loc,
                          Tbar, "%ims" % Tbar,
                          Vm_scale, "%imV" % Vm_scale,
                          orientation='right-top',
                          Ybar_label2="%ipA" % DI_max)
    graph.set_plot(ax, [])
    return fig, ax

def raster_plot(graph,
                SPK_LIST, ID_LIST,
                tlim=None,
                ID_ZOOM_LIST=None,
                COLORS=None,
                with_fig=None, MS=1):
    """ 

    """ 
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

# def POP_ACT_PLOT(t, POP_ACT_LIST, tlim=None, pop_act_zoom=None,
                 # COLORS=None, with_fig=None):
    
    # if with_fig is not None:
        # fig, ax = plt.gcf(), plt.gca()
    # else:
        # fig, ax = plt.subplots(1, figsize=(5,3))
        # plt.subplots_adjust(left=.25, bottom=.25)
    
    # # time limit
    # if tlim is None:
        # tlim = [t.min(), t.max()]
    # # pop act lim
    # if pop_act_zoom is None:
        # pop_act_zoom = [0,1]
        # for i in range(len(POP_ACT_LIST)):
            # try:
                # pop_act_zoom[0] = np.min([pop_act_zoom[0], POP_ACT_LIST[i].min()])
                # pop_act_zoom[1] = np.max([pop_act_zoom[1], POP_ACT_LIST[i].max()])
            # except ValueError:
                # pass
    # # colors
    # if COLORS is None:
        # COLORS = ['g']+['r']+['k' for i in range(len(POP_ACT_LIST)-2)]

    # for act, col in zip(POP_ACT_LIST[::-1], COLORS[::-1]):
        # try:
            # plt.plot(t[(t>=tlim[0]) & (t<=tlim[1])],
                     # act[(t>=tlim[0]) & (t<=tlim[1])], '-', color=col)
        # except IndexError:
            # print('no activity for a population')
    # set_plot(ax, xlabel='time (ms)', ylabel='pop. act. (Hz)',\
                      # ylim=pop_act_zoom)
    # return fig, ax

if __name__=='__main__':

    import sys
    sys.path.append('./')

    from datavyz import graph_env_manuscript as ge
    
    ge.raster_plot(\
        [np.random.randn(3000),np.random.randn(1000)],
        [np.random.randint(3000, size=3000),np.random.randint(1000, size=1000)])
    
    data = {}
    for i in range(30):
        data['cell%i' % (i+1)] = np.random.randn(1000)

    fig, ax = ge.figure(axes_extents=(5,5), top=0., bottom=0., right=0.5, left=0.1)
    ge.Ca_trace_plot(data, Tbar_label='X-s', title='Ca activity', ax=ax)

    ge.show()
