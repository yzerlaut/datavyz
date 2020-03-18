import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

import matplotlib.animation as animation

def animated_plot(x,
                  time_dep_y,
                  graph_env,
                  time=None,
                  annotation_text='t=%is',
                  annotation_xy=(.5, .6),
                  annotation_args={'color':'r', 'weight':'bold'},
                  interval=400,
                  color=None,
                  lw=1, ms=0., marker='o',
                  axes_args={},
                  fig_args={}):

    fig, ax = graph_env.figure(**fig_args)

    if time is None:
        time = np.arange(time_dep_y.shape[0])
    if color is None:
        color = graph_env.default_color
        
    line, = ax.plot(x, time_dep_y[0,:], lw=lw, color=color, ms=ms, marker=marker)
    title = ax.annotate(annotation_text % time[0],
                        annotation_xy,
                        **annotation_args)
    graph_env.set_plot(ax, ylim=[time_dep_y.min(), time_dep_y.max()], **axes_args)

    # Init only required for blitting to give a clean slate.
    def init():
        title.set_text(annotation_text % time[0])
        line.set_ydata(np.ma.array(x, mask=True))
        return [line,title]
    
    def animate(i):
        title.set_text(annotation_text % time[i])
        line.set_ydata(time_dep_y[i,:])
        return [line,title]


    ani = animation.FuncAnimation(fig,
                                  animate,
                                  np.arange(len(time)),
                                  init_func=init,
                                  interval=interval,
                                  blit=True)
    

    return fig, ax, ani

def movie_plot(array,
               graph_env,
               x=None,
               y=None,
               time=None,
               vmin=None, vmax=None,
               annotation_text='t=%is',
               annotation_xy=(.5, .6),
               annotation_args={'color':'r', 'weight':'bold'},
               interval=400,
               cmap=None,
               aspect='equal',
               axes_args={},
               fig_args={}):

    fig, ax = graph_env.figure(**fig_args)
    ax.axis('off')

    if time is None:
        time = np.arange(array.shape[0])
    if cmap is None:
        cmap = graph_env.binary
    if vmin is None:
        vmin=array.min()
    if vmax is None:
        vmax=array.max()
    if (x is None):
        x, y = np.meshgrid(np.arange(array.shape[0]),\
                           np.arange(array.shape[1]), indexing='ij')
    
    im = ax.imshow(array[0,:,:].T,
                   extent = (x.min(), x.max(), y.min(), y.max()),
                   vmin = vmin, vmax = vmax,
                   cmap=cmap,
                   interpolation=None,
                   origin='lower',                
                   aspect=aspect)
    
    title = ax.annotate(annotation_text % time[0],
                        annotation_xy,
                        **annotation_args)

    # Init only required for blitting to give a clean slate.
    def init():
        title.set_text(annotation_text % time[0])
        im.set_array(array[0,:,:].T)
        return [im,title]
    
    def animate(i):
        title.set_text(annotation_text % time[i])
        im.set_array(array[i,:,:].T)
        return [im,title]

    ani = animation.FuncAnimation(fig,
                                  animate,
                                  np.arange(len(time)),
                                  init_func=init,
                                  interval=interval,
                                  blit=True)
    

    return fig, ax, ani


if __name__=='__main__':
    """
    A simple example of an animated plot
    """
    from datavyz.main import graph_env
    ge = graph_env('manuscript')
    
    fig, ax, ani = animated_plot(np.arange(20),
                                 np.random.randn(100, 20),
                                 ge,
                                 time = np.linspace(0, 1, 100),
                                 axes_args={'xlabel':'xlabel (xunit)',
                                            'ylabel':'ylabel (yunit)'})

    fig, ax, ani = movie_plot(np.random.randn(100, 16, 9),
                              ge,
                              time = np.linspace(0, 1, 100),
                              annotation_text='t=%.1fs',
                              annotation_args={'color':ge.red, 'weight':'bold'},
                              axes_args={'xlabel':'xlabel (xunit)',
                                         'ylabel':'ylabel (yunit)'})

    # fig, ax = ge.twoD_plot(np.arange(50), np.arange(30), np.random.randn(50, 30))
    # fig, ax = ge.image(np.random.randn(50, 30))
    
    
    ge.show()
