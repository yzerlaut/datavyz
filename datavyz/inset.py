import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

def inset(graph, stuff,
          rect=[.5,.5,.5,.4],
          facecolor=None):

    if facecolor is None:
        facecolor = graph.facecolor
        
    if type(stuff)==mpl.figure.Figure: # if figure, no choice, if figure relative coordinates
        subax = stuff.add_axes(rect,facecolor=facecolor)
    else:
        fig = plt.gcf()
        box = stuff.get_position()
        width = box.width
        height = box.height
        inax_position  = stuff.transAxes.transform([rect[0], rect[1]])
        transFigure = fig.transFigure.inverted()
        infig_position = transFigure.transform(inax_position)    
        x = infig_position[0]
        y = infig_position[1]
        width *= rect[2]
        height *= rect[3]
        subax = fig.add_axes([x,y,width,height],facecolor=facecolor)
        
    return subax

# def add_inset(ax,
#               rect=[.5,.5,.5,.4],
#               facecolor='w'):
#     fig = plt.gcf()
#     box = ax.get_position()
#     width = box.width
#     height = box.height
#     inax_position  = ax.transAxes.transform(rect[0:2])
#     transFigure = fig.transFigure.inverted()
#     infig_position = transFigure.transform(inax_position)    
#     x = infig_position[0]
#     y = infig_position[1]
#     width *= rect[2]
#     height *= rect[3]  # <= Typo was here
#     subax = fig.add_axes([x,y,width,height],facecolor=facecolor)
#     # x_labelsize = subax.get_xticklabels()[0].get_size()
#     # y_labelsize = subax.get_yticklabels()[0].get_size()
#     # x_labelsize *= rect[2]**0.5
#     # y_labelsize *= rect[3]**0.5
#     # subax.xaxis.set_tick_params(labelsize=x_labelsize)
#     # subax.yaxis.set_tick_params(labelsize=y_labelsize)
#     return subax


if __name__=='__main__':

    from datavyz import ge

    y = np.exp(np.random.randn(100))
    fig, ax = ge.plot(y, xlabel='time', ylabel='y-value')
    sax = ge.inset(ax, [.5, .8, .5, .4])
    sax2 = ge.inset(fig, [0.1, 0.1, .3, .2])
    ge.hist(y, bins=10, ax=sax, axes_args={'spines':[]}, xlabel='y-value')
    ge.hist(y, bins=10, ax=sax2, axes_args={'spines':[]}, xlabel='y-value')
    ge.savefig(fig, 'docs/inset.png')
    ge.show()
