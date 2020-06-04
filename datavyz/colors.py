from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet,\
    PiYG, binary, binary_r, bone, Pastel1, Pastel2, Paired, Accent, Dark2, Set1, Set2,\
    Set3, tab10, tab20, tab20b, tab20c

import matplotlib.colors as mpl_colors

def get_linear_colormap(color1='blue', color2='red'):
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
    cls.cmaps = []
    for color in [viridis, viridis_r, copper, copper_r, cool, jet, PiYG, binary, binary_r, bone, Pastel1, Pastel2, Paired, Accent, Dark2, Set1, Set2, Set3, tab10, tab20, tab20b, tab20c]:
        setattr(cls, color.name, color)
        cls.cmaps.append(color)

    # then some linear colormaps
    for (c1, c2) in zip(['blue', 'red', 'blue', 'green', 'red', 'green', 'orange'],
                        ['red', 'blue', 'orange', 'red', 'green', 'orange', 'green']):
        setattr(cls, '%s_to_%s' % (c1, c2),
                get_linear_colormap(getattr(cls, c1), getattr(cls, c2)))

    cls.get_linear_colormap = get_linear_colormap

    
if __name__=='__main__':

    import numpy as np
    from datavyz import ges as ge

    colors = ['tab:blue', 'tab:red']
    fig, ax = ge.figure()
    for i, c in enumerate(ge.colors[:3]):
        ge.scatter([i], [i], color=c, ax=ax, no_set=True)
    fig, ax = ge.figure()
    for i, x in enumerate(np.linspace(0, 1, 50)):
        ax.scatter([i], [x], color=ge.get_linear_colormap(ge.blue, ge.red)(x))
    ge.show()
    
