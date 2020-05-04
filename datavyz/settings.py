import sys, os, platform, copy
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

ENVIRONMENTS = {}

"""
MANUSCRIPT ENVIRONMENT
"""
ENVIRONMENTS['manuscript'] = {
    'fontsize':8,
    'default_color':'k',
    'single_plot_size':(22., 16.), # mm
    'hspace_size':10., # mm
    'wspace_size':14., # mm
    'left_size':16., # mm
    'right_size':4., # mm
    'top_size':7., # mm
    'bottom_size':13., # mm
    'background':'none',
    'facecolor':'w',
    'transparency':True,
    'dpi':150,
    'markersize':2.5,
}


"""
SCREEN ENVIRONMENT
"""
# SCREEN ENVIRONMENT
# "screen" is just an expanded version of 
ENVIRONMENTS['screen'], screen_factor = {}, 2.
for key, val in ENVIRONMENTS['manuscript'].items():
    if 'plot_size' in key:
        ENVIRONMENTS['screen'][key]=(screen_factor*val[0],screen_factor*val[1])
    elif 'size' in key:
        ENVIRONMENTS['screen'][key]=screen_factor*np.float(val)
    else:
        ENVIRONMENTS['screen'][key] = val
        
"""
NOTEBOOK ENVIRONMENT
"""
ENVIRONMENTS['notebook'] = {
    'fontsize':13,
    'default_color':'k',
    'single_plot_size':(28.*2., 20.*2.), # mm
    'hspace_size':12.*2., # mm
    'wspace_size':16.*2., # mm
    'left_size':20*2., # mm
    'right_size':4.*2., # mm
    'top_size':7.*2., # mm
    'bottom_size':19.*2., # mm
    'background':'w',
    'facecolor':'w',
    'transparency':False,
    'dpi':200,
    'markersize':4.,
}
"""
DARK NOTEBOOK ENVIRONMENT
"""
# "screen" is just an expanded version of 
# ENVIRONMENTS['dark_notebook'] = {'facecolor':'none',
#                                  'default_color':'lightgray',
#                                  'fontsize':12.,
#                                  'transparency':True}
# for key, val in ENVIRONMENTS['notebook'].items():
#     if key not in ENVIRONMENTS['dark_notebook']:
#         ENVIRONMENTS['dark_notebook'][key] = val
ENVIRONMENTS['dark_notebook'] = {
	'fontsize':13,
        'markersize':4.,
        'default_color':'lightgray',
        'single_plot_size':(28.*2., 20.*2.), # mm
        'hspace_size':12.*2., # mm
        'wspace_size':16.*2., # mm
        'left_size':20*2., # mm
        'right_size':4.*2., # mm
        'top_size':7.*2., # mm
        'bottom_size':19.*2., # mm
        'background':'none',
        'facecolor':'none',
        'transparency':True,
        'dpi':200,
}

"""
VISUAL STIMULATION ENVIRONMENT
"""
ENVIRONMENTS['visual_stim'] = {
	'fontsize':12,
        'markersize':4.,
	'default_color':'w',
        'single_plot_size':(200.*16./9., 200.), # mm
        'hspace_size':1., # mm
        'wspace_size':1., # mm
        'left_size':1., # mm
        'right_size':1., # mm
        'top_size':1., # mm
        'bottom_size':1., # mm
        'background':'dark',
        'facecolor':'dimgrey',
        'transparency':True,
        'dpi':150,
}

def set_env_variables(cls, key):

    for key, val in ENVIRONMENTS[key].items():
        setattr(cls, key, val)

    for k, val in ENVIRONMENTS['manuscript'].items():
        if k not in dir(cls):
            setattr(cls, k, val)
        
    
# def update_rcParams(cls):
#     mpl.rcParams.update({'axes.labelsize': cls.fontsize,
#                          'axes.titlesize': cls.fontsize,
#                          'figure.titlesize': cls.fontsize,
#                          'font.size': cls.fontsize,
#                          'legend.fontsize': cls.fontsize,
#                          'xtick.labelsize': cls.fontsize,
#                          'ytick.labelsize': cls.fontsize,
#                          'legend.facecolor': cls.facecolor,
#                          'savefig.transparent':cls.transparency,
#                          'savefig.dpi':cls.dpi,
#                          'savefig.facecolor': cls.facecolor})

    
if __name__=='__main__':

    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
                    
    import numpy as np
    
    from main import graph_env
    for key in ENVIRONMENTS:
        ge = graph_env(key)
        ge.scatter(np.random.randn(100), np.random.randn(100))
        ge.title(plt.gca(), key)
        ge.show()
