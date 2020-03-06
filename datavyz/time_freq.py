import matplotlib.pylab as plt
import numpy as np

def time_freq_plot(t, freqs, data, coefs, xunits='s', yunits=''):
    if xunits=='ms':
        t = 1e3*t
    fig = plt.figure(figsize=(12,6))
    plt.subplots_adjust(wspace=.8, hspace=.5, bottom=.2)
    # signal plot
    plt.subplot2grid((3, 7), (0,0), colspan=6)
    plt.plot(t, data)
    plt.ylabel(yunits)
    plt.xlim([t[0], t[-1]])
    # time frequency power plot
    plt.subplot2grid((3, 7), (1,0), rowspan=2, colspan=6)
    c = plt.contourf(t, freqs, coefs, cmap='PRGn', aspect='auto')
    plt.xlabel('time ('+xunits+')')
    plt.ylabel('frequency (Hz)')
    # mean power plot over intervals
    plt.subplot2grid((3, 7), (1, 6), rowspan=2)
    plt.xlabel('power')
    # max of power over intervals
    plt.subplot2grid((3, 8), (1, 7), rowspan=2)
    plt.barh(freqs, np.power(coefs,2).mean(axis=1),\
             label='mean', height=freqs[-1]-freqs[-2])
    # plt.plot(np.power(coefs,2).max(axis=1), freqs,\
    #          label='max.')
    plt.xlabel(' power')
    plt.legend(prop={'size':'small'}, loc=(0.1,1.1))
    return fig

