import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

import matplotlib.animation as animation

def animated_plot(x,
                  time_dep_y,
                  graph_env,
                  time=None,
                  annotation={'text':'t=%is','xy':(.5, .6), 'color':'r'},
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
    title = ax.annotate(annotation['text'] % time[0],
                        annotation['xy'],
                        color=annotation['color'],
                        xycoords='axes fraction', ha='center')
    graph_env.set_plot(ax, ylim=[time_dep_y.min(), time_dep_y.max()], **axes_args)

    # Init only required for blitting to give a clean slate.
    def init():
        title.set_text(annotation['text'] % time[0])
        line.set_ydata(np.ma.array(x, mask=True))
        return [line,title]
    
    def animate(i):
        title.set_text(annotation['text'] % time[i])
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
               time=None,
               annotation={'text':'t=%is','xy':(.5, .6), 'color':'r'},
               interval=400,
               cmap=None,
               axes_args={},
               fig_args={}):

    fig, ax = graph_env.figure(**fig_args)
    ax.axis('off')

    if time is None:
        time = np.arange(array.shape[0])
    if cmap is None:
        cmap = graph_env.binary
        
    im = ax.imshow(array[0,:,:], cmap=cmap,
                   interpolation=None,
                   aspect='equal')
    
    title = ax.annotate(annotation['text'] % time[0],
                        annotation['xy'],
                        color=annotation['color'],
                        xycoords='axes fraction', ha='center')

    # Init only required for blitting to give a clean slate.
    def init():
        title.set_text(annotation['text'] % time[0])
        im.set_array(array[0,:,:])
        return [im,title]
    
    def animate(i):
        title.set_text(annotation['text'] % time[i])
        im.set_array(array[i,:,:])
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
    
    # fig, ax, ani = animated_plot(np.arange(20),
    #                              np.random.randn(100, 20),
    #                              ge,
    #                              time = np.linspace(0, 1, 100),
    #                              annotation={'text':'t=%.1fs', 'xy':(.2,.7), 'color':ge.red},
    #                              axes_args={'xlabel':'xlabel (xunit)',
    #                                         'ylabel':'ylabel (yunit)'})


    fig, ax, ani = movie_plot(np.random.randn(100, 30, 30),
                              ge,
                              time = np.linspace(0, 1, 100),
                              annotation={'text':'t=%.1fs', 'xy':(.2,.7), 'color':ge.red},
                              axes_args={'xlabel':'xlabel (xunit)',
                                         'ylabel':'ylabel (yunit)'})
    
    plt.show()
