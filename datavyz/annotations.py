import numpy as np
import matplotlib.pylab as plt
from matplotlib.figure import Figure

def set_fontsize(graph, size):
    """ set the fontsize given a size and the props of the graph class"""
    if size=='small':
        fontsize=graph.fontsize-1
    elif size=='x-small':
        fontsize=graph.fontsize-2
    elif size=='xx-small':
        fontsize=graph.fontsize-3
    elif size=='xxx-small':
        fontsize=graph.fontsize-4
    elif size=='xxxx-small':
        fontsize=graph.fontsize-5
    elif size=='large':
        fontsize=graph.fontsize+1
    elif size=='x-large':
        fontsize=graph.fontsize+2
    elif size=='xx-large':
        fontsize=graph.fontsize+3
    elif size=='xxx-large':
        fontsize=graph.fontsize+4
    elif size=='xxxx-large':
        fontsize=graph.fontsize+5
    else:
        fontsize=graph.fontsize
    return fontsize

def title(graph, ax, title,
          size=None, fontsize=None, color=None,
          bold=False, italic=False,
          weight='normal', style='normal'):

    if fontsize is None:
        fontsize=set_fontsize(graph, size)
    if color is None:
        color=graph.default_color
    if bold and (weight=='normal'):
        weight = 'bold'
    if italic and (style=='normal'):
        style = 'italic'
    ax.set_title(title,
                 weight=weight, fontsize=fontsize, style=style,
                 color=color)
    
def annotate(graph, stuff, s, xy,
             xycoords='axes fraction',
             bold=False, italic=False,
             rotation=0,
             fontsize=None, size=None, color=None, clip_on=False,
             ha='left', va='bottom', weight='normal', style='normal'):
    """
    stuff can be either a figure or a subplot
    """
    if color is None:
        color=graph.default_color
    if bold and (weight=='normal'):
        weight = 'bold'
    if italic and (style=='normal'):
        style = 'italic'
    if fontsize is None:
        fontsize=set_fontsize(graph, size)

    if type(stuff)==Figure: # if figure, no choice, if figure relative coordinates
        plt.annotate(s, xy, xycoords='figure fraction',
                     weight=weight, fontsize=fontsize, style=style,
                     color=color, rotation=rotation, ha=ha, va=va,
                     clip_on=clip_on)
    else: # means subplot
        stuff.annotate(s, xy, xycoords=xycoords,
                       weight=weight, fontsize=fontsize, style=style,
                       color=color, rotation=rotation, ha=ha, va=va,
                       clip_on=clip_on)

def arrow(graph, stuff,
          rect = [0.1, 0.1, 0.7, 0.],
          width=.02,
          head_width=0.15, head_length=0.02,
          width_margin=0., height_margin=0.1,
          shape='full',
          color='k'):
    
    [x0,y0, dx, dy] = rect

    if (dx==0) and width_margin==0:
        width_margin, height_margin = height_margin, 0
        
    if type(stuff)==Figure: # if figure, we create an axis
        if (dy<0) and (dx<0):
            sax = graph.inset(stuff,
                              [x0+dx-width_margin, y0+dy-height_margin,
                               -dx+2*width_margin,-dy+2*height_margin])
        elif (dx<0):
            sax = graph.inset(stuff,
                              [x0+dx-width_margin, y0-height_margin,
                               -dx+2*width_margin,dy+2*height_margin])
        elif (dy<0):
            sax = graph.inset(stuff,
                              [x0-width_margin, y0+dy-height_margin,
                               dx+2*width_margin,-dy+2*height_margin])
        else:
            sax = graph.inset(stuff,
                              [x0-width_margin, y0-height_margin,
                               dx+2*width_margin,dy+2*height_margin])
        sax.axis('off')
    else: # means subplot
        sax = stuff
        
    sax.arrow(x0, y0, dx, dy,
              length_includes_head=True,
              width=width, shape=shape,
              head_width=head_width, head_length=head_length,
              facecolor=color, edgecolor=color, clip_on=False)
    
def from_pval_to_star(p,
                      threshold1=1e-3,
                      threshold2=1e-2,
                      threshold3=5e-2):
    if p<threshold1:
        return '***'
    elif p<threshold2:
        return '**'
    elif p<threshold3:
        return '*'
    else:
        return 'n.s.'
    
def sci_str(x, rounding=0, remove_0_in_exp=True):
    y = ('{:.' + str(int(rounding))+'e}').format(x)
    if remove_0_in_exp: y = y.replace('-0', '-')
    return y


def int_to_letter(integer, capitals=False):
    if capitals:
        return string.ascii_uppercase[integer]
    else:
        return string.ascii_lowercase[integer]

def int_to_roman(integer, capitals=False):
   """
   #########################################################
   TAKEN FROM:
   http://code.activestate.com/recipes/81611-roman-numerals/
   #########################################################
   
   Convert an integer to Roman numerals.
   """
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   if capitals:
       nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
   else:
       nums = ('m',  'cm', 'd', 'cd','c', 'xc','l','xl','x','ix','v','iv','i')
   result = ""
   for i in range(len(ints)):
      count = int(integer / ints[i])
      result += nums[i] * count
      integer -= ints[i] * count
   return result


def draw_bar_scales(graph,
                    ax,
                    Xbar=0., Xbar_label='', Xbar_fraction=0.1, Xbar_label_format='%.1f',
                    Ybar=0., Ybar_label='', Ybar_fraction=0.1, Ybar_label_format='%.1f',
                    loc='top-left',
                    orientation=None,
                    xyLoc=None, 
                    Xbar_label2='',Ybar_label2='',
                    color=None, xcolor=None, ycolor=None, ycolor2=None,
                    fontsize=None, size='normal',
                    shift_factor=20., lw=1,
                    remove_axis=False):
    """
    USE:

    fig, ax = figure()
    ax.plot(np.random.randn(10), np.random.randn(10), 'o')
    draw_bar_scales(ax, (0,0), 1, '1s', 2, '2s', orientation='right-bottom', Ybar_label2='12s')
    set_plot(ax)    
    """

    if fontsize is None:
        fontsize = set_fontsize(graph, size)
    if color is None:
        color = graph.default_color
    if xcolor is None:
        xcolor = graph.default_color
    if ycolor is None:
        ycolor = graph.default_color
    if ycolor2 is None:
        ycolor2 = graph.colors[0]

    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    if Xbar==0:
        Xbar = (xlim[1]-xlim[0])*Xbar_fraction
        Xbar_label = Xbar_label_format % Xbar
        print('X-bar label automatically set to: ', Xbar_label, ' Using the format', Xbar_label_format, ' --> adjust it and add units through the format !')
    if Ybar==0:
        Ybar = (ylim[1]-ylim[0])*Ybar_fraction
        Ybar_label = Ybar_label_format % Ybar
        print('Y-bar label automatically set to: ', Ybar_label, ' Using the format', Ybar_label_format, ' --> adjust it and add units through the format !')

    if type(loc) is tuple:
        xyLoc = xlim[0]+loc[0]*(xlim[1]-xlim[0]), ylim[0]+loc[1]*(ylim[1]-ylim[0])
        
    if (loc in ['top-right', 'right-top']) or (orientation in ['left-bottom','bottom-left']):

        if xyLoc is None:
            xyLoc = (xlim[1]-0.05*(xlim[1]-xlim[0]), ax.get_ylim()[1]-0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]))
            
        ax.plot(xyLoc[0]-np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]-np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=xcolor, va='bottom', ha='right',fontsize=fontsize, annotation_clip=False)
        ax.annotate(Ybar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=ycolor, va='top', ha='left',fontsize=fontsize, annotation_clip=False)
        if Ybar_label2!='':
            ax.annotate('\n'+Ybar_label2, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor),
                        color=ycolor2, va='top', ha='left',fontsize=fontsize, annotation_clip=False)
            
    elif (loc in ['top-left', 'left-top']) or (orientation in ['right-bottom','bottom-right']):
        
        if xyLoc is None:
            xyLoc = (xlim[0]+0.05*(xlim[1]-xlim[0]), ax.get_ylim()[1]-0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]))
            
        ax.plot(xyLoc[0]+np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]-np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=xcolor, va='bottom', ha='left',fontsize=fontsize, annotation_clip=False)
        ax.annotate(Ybar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=ycolor, va='top', ha='right',fontsize=fontsize, annotation_clip=False)
        if Ybar_label2!='':
            ax.annotate('\n'+Ybar_label2, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor),
                        color=ycolor2, va='top', ha='right',fontsize=fontsize, annotation_clip=False)

    elif (loc in ['bottom-right', 'right-bottom']) or (orientation in ['left-top','top-left']):
        
        if xyLoc is None:
            xyLoc = (xlim[1]-0.05*(xlim[1]-xlim[0]), ax.get_ylim()[0]+0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]))
            
        ax.plot(xyLoc[0]-np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]+np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=xcolor, va='top', ha='right',fontsize=fontsize, annotation_clip=False)
        ax.annotate(Ybar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=ycolor, va='bottom', ha='left',fontsize=fontsize, annotation_clip=False)
        if Ybar_label2!='':
            ax.annotate(Ybar_label2+'\n',
                        (xyLoc[0]+Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor),
                        color=ycolor2, va='bottom', ha='left',fontsize=fontsize, annotation_clip=False)

    elif (loc in ['bottom-left', 'left-bottom']) or (orientation in ['right-top','top-right']):
        
        if xyLoc is None:
            xyLoc = (xlim[0]+0.05*(xlim[1]-xlim[0]), ax.get_ylim()[0]+0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]))
            
        ax.plot(xyLoc[0]+np.arange(2)*Xbar,xyLoc[1]+np.zeros(2), lw=lw, color=color)
        ax.plot(xyLoc[0]+np.zeros(2),xyLoc[1]+np.arange(2)*Ybar, lw=lw, color=color)
        ax.annotate(Xbar_label, (xyLoc[0]+Xbar/shift_factor,xyLoc[1]-Ybar/shift_factor), color=xcolor, va='top', ha='left',fontsize=fontsize, annotation_clip=False)
        ax.annotate(Ybar_label, (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor), color=ycolor, va='bottom', ha='right',fontsize=fontsize, annotation_clip=False)
        if Ybar_label2!='':
            ax.annotate(Ybar_label2+'\n', (xyLoc[0]-Xbar/shift_factor,xyLoc[1]+Ybar/shift_factor),
                        color=ycolor2, va='bottom', ha='right',fontsize=fontsize, annotation_clip=False)
    else:
        print("""
        orientation not recognized, it should be one of
        - right-top, top-right
        - left-top, top-left
        - right-bottom, bottom-right
        - left-bottom, bottom-left
        """)
        
    if remove_axis:
        ax.axis('off')


if __name__=='__main__':

    import sys
    sys.path.append('./')
    from datavyz import graph_env_manuscript as ge

    x = 32.23545345e-5
    print(sci_str(x, rounding=2))
    print(from_pval_to_star(x))
    for i in range(20):
        print(int_to_roman(i))

    
    fig, AX= ge.figure(axes=(10,1), figsize=(.7,.7), bottom=1.5)
    for i, ax in enumerate(AX):
        # ge.top_left_letter(ax, ge.int_to_roman(i+1))
        ge.matrix(np.random.randn(10,10), ax=ax)

    sax = ge.arrow(fig, [0.04, .2, .93, 0.])
    ge.annotate(fig, 'time', (.5, .17), ha='center')

    # ge.savefig(fig, 'docs/annotations1.png')
    ge.show()
    
    # from datavyz..graphs import *
    # fig, ax = figure()
    # ax.plot(np.random.randn(30), np.random.randn(30), 'o')
    # bar_scales(ax, xbar=2, ybar=2, location='bottom left',
    #            ybar_label=r'10$\mu$V', xbar_label='200ms')
    # show()
