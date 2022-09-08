from matplotlib.cm import viridis, PRGn, tab10, jet, binary
import matplotlib.colors as mpl_colors

def get_linear_colormap(cls, color1='blue', color2='red'):
    # linear gradient
    return mpl_colors.LinearSegmentedColormap.from_list('mycolors',[color1, color2])

def lin_cmap(cls, color1='blue', color2='red'):
    # a shorter versoin of it
    return mpl_colors.LinearSegmentedColormap.from_list('mycolors',[color1, color2])


def give_color_attributes(cls):

    # colors
    cls.colors = []
    for name in list(mpl_colors.TABLEAU_COLORS):
        setattr(cls, name.replace('tab:',''), mpl_colors.TABLEAU_COLORS[name])
        cls.colors.append(mpl_colors.TABLEAU_COLORS[name])

    for name in list(mpl_colors.CSS4_COLORS):
        if not hasattr(cls, name): # not set by "tab" (e.g. not "blue")
            setattr(cls, name, mpl_colors.CSS4_COLORS[name])
            cls.colors.append(mpl_colors.CSS4_COLORS[name])

    # color maps
    for color in [viridis, PRGn, tab10, jet, binary]:
        setattr(cls, color.name, color)

    # some 'ge.b' instead of 'ge.blue'
    for s, l in zip(['b', 'g', 'o', 'r', 'y', 'p'],
                     ['blue', 'green', 'orange', 'red',\
                             'yellow', 'purple']):
        setattr(cls, s, getattr(cls, l))
    
if __name__=='__main__':

    import sys
    sys.path.append('./')
    import numpy as np
    from datavyz import graph_env_manuscript as ge

    colors = ['tab:blue', 'tab:red']

    fig, ax = ge.figure()
    for i, c in enumerate(ge.colors[:3]):
        ge.scatter([i], [i], color=c, ax=ax, no_set=True)

    fig, ax = ge.figure()
    for i, x in enumerate(np.linspace(0, 1, 50)):
        ax.scatter([i], [x], color=ge.lin_cmap(ge.b, ge.r)(x))

    ge.show()
    
