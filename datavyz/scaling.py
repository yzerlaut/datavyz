"""
Set of functions and quantities for the scaling of figuers and text
"""
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

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
        if 'cls.facecolor' in key:
            print(key)

    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
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

