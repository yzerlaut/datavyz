import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *


def time_freq_plot(graph, t, freqs, data, coefs,
                   xunits='s', yunits='data (unit)'):
    if xunits=='ms':
        t = 1e3*t
        
    fig, AX = graph.figure(axes_extents=[\
                                         [[4,1],[1,1]],
                                         [[4,2],[1,2]]], wspace=0.1, hspace=0.1)
    AX[0][1].axis('off')

    
    # plt.subplots_adjust(wspace=.8, hspace=.5, bottom=.2)
    # # signal plot
    # plt.subplot2grid((3, 7), (0,0), colspan=6)
    AX[0][0].plot(t, data)
    graph.set_plot(AX[0][0], ylabel=yunits, xlim=[t[0], t[-1]])
    
    # # time frequency power plot
    # plt.subplot2grid((3, 7), (1,0), rowspan=2, colspan=6)
    c = AX[1][0].contourf(t, freqs, coefs, cmap='PRGn', aspect='auto')
    graph.set_plot(AX[1][0], ylabel='frequency (Hz)', xlim=[t[0], t[-1]], xlabel='time ('+xunits+')')

    # # mean power plot over intervals
    AX[1][1].barh(freqs, np.power(coefs,2).mean(axis=1),\
                  label='mean', height=freqs[-1]-freqs[-2], color=ge.purple)
    # # max of power over intervals
    AX[1][1].plot(np.power(coefs,2).max(axis=1), freqs,\
                  label='max.', color=ge.red)
    graph.set_plot(AX[1][1], xlabel=' power')
    AX[1][1].legend(prop={'size':'small'}, loc=(0.1,1.1))
    return fig, AX


if __name__=='__main__':

    from datavyz.main import graph_env
    ge = graph_env('manuscript')

    t = np.arange(100)
    freqs = np.linspace(0, 10)
    data = np.random.randn(100)
    coefs = np.random.randn(len(freqs), len(t))
    
    time_freq_plot(ge, t, freqs, data, coefs)    

    ge.show()
