"""
standard functiosn to plot single neuron properties/responses
"""
import numpy as np

def response_to_current_pulse(graph, t, Vm, I, spikes,
                              Tbar=50.,
                              Vm_scale=10.,
                              loc=(150,-30),
                              Vpeak=-10,
                              with_artificial_spikes=True):

    fig, ax = graph.figure(figsize=(1.2,.8),
                           bottom=0.01, left=0.01, right=0.01, top=0.01)
    
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
                          loc=loc,
                          orientation='right-top',
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

    
if __name__=='__main__':
    import numpy as np


    

