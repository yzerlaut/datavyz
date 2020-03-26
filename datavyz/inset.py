import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

def inset(graph, stuff,
          x0=0.5, y0=0.5,
          dx=.5, dy=.5,
          facecolor='w'):
    if type(stuff)==mpl.figure.Figure: # if figure, no choice, if figure relative coordinates
        subax = stuff.add_axes([x0,y0,dx,dy],facecolor=facecolor)
    else:
        fig = graph.gcf()
        box = stuff.get_position()
        width = box.width
        height = box.height
        inax_position  = stuff.transAxes.transform([x0,y0])
        transFigure = fig.transFigure.inverted()
        infig_position = transFigure.transform(inax_position)    
        x = infig_position[0]
        y = infig_position[1]
        width *= dx
        height *= dy
        subax = fig.add_axes([x,y,width,height],facecolor=facecolor)
    return subax

def add_inset(ax,
              rect=[.5,.5,.5,.4],
              facecolor='w'):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)    
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height],facecolor=facecolor)
    # x_labelsize = subax.get_xticklabels()[0].get_size()
    # y_labelsize = subax.get_yticklabels()[0].get_size()
    # x_labelsize *= rect[2]**0.5
    # y_labelsize *= rect[3]**0.5
    # subax.xaxis.set_tick_params(labelsize=x_labelsize)
    # subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax


if __name__=='__main__':

    from main import graph_env
    ge = graph_env('manuscript')

    y = np.exp(np.random.randn(100))
    fig, ax = ge.plot(y, xlabel='time', ylabel='y-value')
    sax = ge.inset(ax, x0=.5, y0=.8, dx=.5, dy=.4)
    ge.hist(y, bins=10, ax=sax, axes_args={'spines':[]}, xlabel='y-value')
    fig.savefig('docs/inset.svg')
    ge.show()
