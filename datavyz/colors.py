from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet,\
    PiYG, binary, binary_r, bone, Pastel1, Pastel2, Paired, Accent, Dark2, Set1, Set2,\
    Set3, tab10, tab20, tab20b, tab20c

import matplotlib.colors as mpl_colors

# CUSTOM colors
Blue, Orange, Green, Red, Purple, Brown, Pink, Grey,\
    Kaki, Cyan = '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',\
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'

Color_List = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]

def get_linear_colormap(color1='blue', color2='red'):
    return mpl_colors.LinearSegmentedColormap.from_list('mycolors',[color1, color2])


def give_color_attributes(cls):

    # an array with the default colors
    cls.colors = [Blue, Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan]

    # color attributes with their names
    cls.blue, cls.orange, cls.green, cls.red, cls.purple, cls.brown,\
        cls.pink, cls.grey, cls.kaki, cls.cyan = Blue,\
            Orange, Green, Red, Purple, Brown, Pink, Grey, Kaki, Cyan
    
    cls.viridis, cls.viridis_r, cls.copper, cls.copper_r, cls.cool, cls.jet,\
     cls.PiYG, cls.binary, cls.binary_r, cls.bone = viridis, viridis_r, copper, copper_r,\
                                         cool, jet, PiYG, binary, binary_r, bone
    
    cls.Pastel1, cls.Pastel2, cls.Paired, cls.Accent, cls.Dark2,\
        cls.Set1, cls.Set2, cls.Set3, cls.tab10, cls.tab20,\
        cls.tab20b, cls.tab20c = Pastel1, Pastel2, Paired,\
        Accent, Dark2, Set1, Set2, Set3, tab10, tab20, tab20b, tab20c

    cls.cmaps = [viridis, viridis_r, copper, copper_r, cool, jet, PiYG]
    cls.blue_to_red = get_linear_colormap(Blue, Red)
    cls.red_to_blue = get_linear_colormap(Red, Blue)
    cls.blue_to_orange = get_linear_colormap(Blue, Orange)
    cls.green_to_red = get_linear_colormap(Green, Red)
    cls.red_to_green = get_linear_colormap(Red, Green)
    cls.green_to_orange = get_linear_colormap(Green, Orange)
    cls.orange_to_green = get_linear_colormap,(Orange, Green)
    cls.b, cls.o, cls.g, cls.r = cls.blue, cls.orange, cls.green, cls.red

    cls.get_linear_colormap = get_linear_colormap
