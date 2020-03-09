"""
Set of functions and quantities for the scaling of figuers and text
"""
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

A0_format = {'width':8.3, 'height':11.7}
Single_Plot_Size = (0.2, 0.12) # DEFAULT SIZE OF PLOT in terms of A0 format ratio

def update_rcParams(FONTSIZE,
                    facecolor='none',
                    transparency=True,
                    dpi=150):
    mpl.rcParams.update({'axes.labelsize': FONTSIZE,
                         'axes.titlesize': FONTSIZE,
                         'figure.titlesize': FONTSIZE,
                         'font.size': FONTSIZE,
                         'legend.fontsize': FONTSIZE,
                         'xtick.labelsize': FONTSIZE,
                         'ytick.labelsize': FONTSIZE,
                         'figure.facecolor': facecolor,
                         'legend.facecolor': facecolor,
                         'axes.facecolor': facecolor,
                         'savefig.transparent':transparency,
                         'savefig.dpi':dpi,
                         'savefig.facecolor': facecolor})

def mm2inch(x):
    return x/25.4
    
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)    

def inch2cm(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i*inch for i in tupl[0])
    else:
        return tuple(i*inch for i in tupl)    
    

if __name__=='__main__':

    for key in mpl.rcParams.keys():
        if 'facecolor' in key:
            print(key)

    from datavyz.main import graph_env
    ge = graph_env('manuscript')
    
    import sys

    try:
        FONTSIZE = int(sys.argv[-1])
    except ValueError:
        FONTSIZE = ge.FONTSIZE
        
    mpl.rcParams.update({'axes.labelsize': FONTSIZE,
                         'font.size': FONTSIZE,
                         'xtick.labelsize': FONTSIZE,
                         'ytick.labelsize': FONTSIZE})

    fig, ax = ge.figure()
    ge.top_left_letter(ax, 'a')
    ge.annotate(ax, 'The fontsize is \n now set to '+str(FONTSIZE), (.5,.97),
                va='top', ha='center', fontsize=FONTSIZE)
    ge.set_plot(ax,
                xlabel='my xlabel (Unit)', ylabel='my ylabel (Unit)',
                fontsize=FONTSIZE, num_xticks=3, num_yticks=3)
    # fig.savefig('fig.png')
    ge.show()

