import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

def time_freq_plot(graph, t, freqs, data, coefs,
                   xlabel='time (s)',
                   signal_label='data (unit)',
                   envelope_label='env. (unit)',
                   fig_args=dict(axes_extents=[[[4,1],[1,1]],
                                               [[4,2],[1,2]]],
                                 wspace=0.1, hspace=0.3, top=0.)):
    
    fig, AX = graph.figure(**fig_args)
    AX[0][1].axis('off')
    
    # plt.subplots_adjust(wspace=.8, hspace=.5, bottom=.2)
    # # signal plot
    AX[0][0].plot(t, data)
    graph.set_plot(AX[0][0], ['left'], ylabel=signal_label, xlim=[t[0], t[-1]])
    
    # # time frequency power plot
    c = AX[1][0].contourf(t, freqs, coefs, cmap='PRGn', aspect='auto')
    graph.set_plot(AX[1][0], ylabel='frequency (Hz)', xlim=[t[0], t[-1]], xlabel=xlabel)

    # # mean power plot over intervals
    AX[1][1].plot(np.abs(coefs).mean(axis=1), freqs,\
                  label='mean', color=graph.purple)
    # # max of power over intervals
    AX[1][1].plot(np.abs(coefs).max(axis=1), freqs,\
                  label='max.', color=graph.red)
    graph.set_plot(AX[1][1], xlabel=envelope_label)
    graph.legend(AX[1][1], loc=(0.1,1.))
    
    return fig, AX


if __name__=='__main__':

    from datavyz import ge
    from analyz.freq_analysis.wavelet_transform import my_cwt # continuous wavelet transform
    
    dt, tstop = 1e-4, 1.
    t = np.arange(int(tstop/dt))*dt
    
    freq1, width1, freq2, width2, freq3, width3 = 10., 100e-3, 40., 40e-3, 70., 20e-3
    data = 3.2+np.cos(2*np.pi*freq1*t)*np.exp(-(t-.5)**2/2./width1**2)+\
        np.cos(2*np.pi*freq2*t)*np.exp(-(t-.2)**2/2./width2**2)+\
        np.cos(2*np.pi*freq3*t)*np.exp(-(t-.8)**2/2./width3**2)

    # Continuous Wavelet Transform analysis
    freqs = np.linspace(1, 90, 40)
    coefs = my_cwt(data, freqs, dt)

    fig, AX = ge.time_freq_plot(t, freqs, data, coefs)    

    ge.savefig(fig, 'docs/time-freq.png')
