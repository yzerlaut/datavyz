import sys, pathlib, os, json

# specific modules
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from neural_network_dynamics import main as ntwk # based on Brian2

import matplotlib.animation as animation
from matplotlib.collections import LineCollection, PatchCollection
import matplotlib.patches as mpatches


def coordinate_projection(x, y, z, x0 ,y0, z0, polar_angle, azimuth_angle):
    """
    /!\
    need to do this propertly, not working yet !!
    """
    x = np.cos(polar_angle)*(x-x0)+np.sin(polar_angle)*(y-y0)
    y = np.sin(polar_angle)*(x-x0)+np.cos(polar_angle)*(y-y0)
    z = z
    return x, y, z


def plot_nrn_shape(graph,
                   SEGMENTS,
                   ax=None,
                   center = {'x0':0, 'y0':0., 'z0':0.},
                   scale_bar=100, xshift=0.,
                   polar_angle=0, azimuth_angle=np.pi/2., 
                   density_quantity=None,
                   colors=None,
                   annotation_color=None,
                   diameter_magnification=2.,
                   lw=1):
    """
    by default: soma_comp = COMP_LIST[0]
    """

    if ax is None:
        fig, ax = graph.figure(figsize=(1.,1.2), left=0., top=2., bottom=0., right=0.)
    else:
        fig = None

    x0, y0, z0 = center['x0'], center['y0'], center['z0'] # possibility to control the center of the rotation 

    segments, seg_diameters, circles, circle_colors = [], [], [], []
    
    for iseg in range(len(SEGMENTS['x'])):

        if (SEGMENTS['start_x'][iseg]==SEGMENTS['end_x'][iseg]) and\
           (SEGMENTS['start_y'][iseg]==SEGMENTS['end_y'][iseg]) and\
           (SEGMENTS['start_z'][iseg]==SEGMENTS['end_z'][iseg]):
            # circle of diameter
            sx, sy, _ = coordinate_projection(SEGMENTS['start_x'][iseg],
                                              SEGMENTS['start_y'][iseg],
                                              SEGMENTS['start_z'][iseg],
                                              x0 ,y0, z0, polar_angle, azimuth_angle)
            if colors is None:
                circles.append(mpatches.Circle((1e6*sx, 1e6*sy), 1e6*SEGMENTS['diameter'][iseg]/2., color=graph.default_color))
            else:
                circles.append(mpatches.Circle((1e6*sx, 1e6*sy), 1e6*SEGMENTS['diameter'][iseg]/2.,
                                               color=colors[iseg]))
        else:
            sx, sy, _ = coordinate_projection(SEGMENTS['start_x'][iseg],
                                              SEGMENTS['start_y'][iseg],
                                              SEGMENTS['start_z'][iseg],
                                              x0 ,y0, z0, polar_angle, azimuth_angle)
            ex, ey, _ = coordinate_projection(SEGMENTS['end_x'][iseg],
                                              SEGMENTS['end_y'][iseg],
                                              SEGMENTS['end_z'][iseg],
                                              x0 ,y0, z0, polar_angle, azimuth_angle)
            segments.append([(1e6*(sx+xshift), 1e6*sy),(1e6*(ex+xshift), 1e6*ey)])
            seg_diameters.append(1e6*SEGMENTS['diameter'][iseg])

    if colors is None:
        colors = [graph.default_color for i in range(len(segments))]

    line_segments = LineCollection(segments, linewidths=seg_diameters, colors=colors, linestyles='solid')
    ax.add_collection(line_segments)
    collection = PatchCollection(circles)
    ax.add_collection(collection)
    ax.autoscale()


    # adding a bar for the spatial scale
    if scale_bar is not None and scale_bar>0:
        ax.set_aspect('equal')
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        if annotation_color is None:
            annotation_color = graph.default_color
            ax.plot(xlim[0]*np.ones(2), ylim[1]-np.array([0,scale_bar]),
                    lw=1, color=annotation_color)
            ax.annotate(str(scale_bar)+'$\mu$m', (xlim[0]+1, ylim[1]-1),
                        color=annotation_color)
        ax.axis('off')
        
    return fig, ax

def add_dot_on_morpho(graph, ax,
                      comp,
                      index=0,
                      soma_comp=None,
                      polar_angle=0, azimuth_angle=np.pi/2., 
                      color=None,
                      lw=3, s=100):
    """
    """
    if color is None:
        color = graph.default_color
    [x0, y0, z0] = soma_comp[0].x, soma_comp[0].y, soma_comp[0].z
    x, y, _ = coordinate_projection(comp, x0 ,y0, z0, polar_angle, azimuth_angle)
    ax.scatter(1e6*x[index], 1e6*y[index],
            s=s, edgecolors=color, marker='o', facecolors='none', lw=lw)
        

def dist_to_soma(comp, soma):
    return np.sqrt((comp.x-soma.x)**2+\
                   (comp.y-soma.y)**2+\
                   (comp.z-soma.z)**2)[0]/brian2.um


def show_animated_time_varying_trace(t, Quant0, SEGMENT_LIST,
                                     fig, ax, graph,
                                     picked_locations = None,
                                     polar_angle=0, azimuth_angle=np.pi/2.,
                                     quant_label='$V_m$ (mV)',
                                     time_label='time (ms)',
                                     segment_condition=None,
                                     colormap=viridis_r,
                                     ms=0.5):
    """

    "picked_locations" should be given as a compartment index
    we highlight the first picked_locations with a special marker because it will usually be the stimulation point
    """
    # preparing animations params
    if segment_condition is None:
        segment_condition = np.empty(Quant0.shape[0], dtype=bool)+True
    Quant = (Quant0[segment_condition]-Quant0[segment_condition].min())/(Quant0[segment_condition].max()-Quant0[segment_condition].min())
        
    # adding inset of time plots and bar legends
    ax2 = graph.inset(ax, rect=[0.1,-0.05,.9,.1])
    ax3 = graph.inset(ax, rect=[0.83,0.8,.03,.2])
    graph.build_bar_legend(np.linspace(Quant0[segment_condition].min(), Quant0[segment_condition].max(), 5), ax3, colormap,
                     color_discretization=30, label=quant_label)
    
    # picking up locations
    if picked_locations is None:
        picked_locations = np.concatenate([[0], np.random.randint(1, Quant.shape[0], 4)])
    for pp, p in enumerate(picked_locations):
        ax2.plot(t, Quant0[segment_condition,:][p,:], 'k:', lw=1)
        ax.scatter([1e6*SEGMENT_LIST['xcoords'][segment_condition][p]],
                   [1e6*SEGMENT_LIST['ycoords'][segment_condition][p]], 
                   s=25+30*(1-np.sign(pp)),
                   c=list(['k']+graph.colors)[pp])
    graph.set_plot(ax2, xlabel=time_label, ylabel=quant_label, num_yticks=2)

    LINES = []
    # plotting each segment
    line = ax.scatter(1e6*SEGMENT_LIST['xcoords'][segment_condition], 1e6*SEGMENT_LIST['ycoords'][segment_condition],
                      color=colormap(Quant[:,0]), s=ms, marker='o')
    LINES.append(line)
    # then highlighted points
    for pp, p in enumerate(picked_locations):
        line, = ax2.plot([t[0]], [Quant0[segment_condition,:][p,0]], 'o',
                         ms=4+4*(1-np.sign(pp)),
                         color=list(['k']+graph.colors)[pp])
        LINES.append(line)
    
    # Init only required for blitting to give a clean slate.
    def init():
        return LINES

    def animate(i):
        LINES[0].set_color(colormap(Quant[:,i]))  # update the data
        for pp, p in enumerate(picked_locations):
            LINES[pp+1].set_xdata([t[i]])
            LINES[pp+1].set_ydata([Quant0[segment_condition,:][p,i]])
        return LINES


    ani = animation.FuncAnimation(fig, animate, np.arange(len(t)),
                                  init_func=init,
                                  interval=50, blit=True)
    return ani



if __name__=='__main__':

    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
                                   """ 
                                   Plots a 2D representation of the morphological reconstruction of a single cell
                                   """
                                   ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-lw", "--linewidth",help="", type=float, default=0.2)
    parser.add_argument("-ac", "--axon_color",help="", default='r')
    parser.add_argument("-pa", "--polar_angle",help="", type=float, default=0.)
    parser.add_argument("-aa", "--azimuth_angle",help="", type=float, default=0.)
    parser.add_argument("-wa", "--without_axon",help="", action="store_true")
    parser.add_argument("-m", "--movie_demo",help="", action="store_true")
    parser.add_argument("--filename", '-f', help="filename", type=str,
        default='../neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L5pyr-j140408b.CNG.swc')
    parser.add_argument("--directory", '-d', help="directory", type=str,
        default='../neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015')
    # filename = home+'work/neural_network_dynamics/single_cell_integration/morphologies/Jiang_et_al_2015/L23pyr-j150123a.CNG.swc'
    args = parser.parse_args()

    print('[...] loading morphology')
    morpho = ntwk.Morphology.from_swc_file(args.filename)
    print('[...] creating list of compartments')
    SEGMENTS = ntwk.morpho_analysis.compute_segments(morpho)
    
    from datavyz.main import graph_env
    ge = graph_env()
    
    n = 0
    AX = []
    for fn in os.listdir(args.directory):
        if fn.endswith('swc'):
            morpho = ntwk.Morphology.from_swc_file(os.path.join(args.directory, fn))
            SEGMENTS = ntwk.morpho_analysis.compute_segments(morpho)
            colors = [ge.green if comp_type=='axon' else ge.red for comp_type in SEGMENTS['comp_type']]
            fig, ax = plot_nrn_shape(ge, SEGMENTS, colors=colors)
            ax.set_title(fn.split('-')[0], weight='bold', style='italic')
            AX.append(ax)
            n+=1
    
    # fig, ax = plot_nrn_shape(ge,
    #                          SEGMENTS,
    #                          lw=args.linewidth,
    #                          polar_angle=args.polar_angle, azimuth_angle=args.azimuth_angle)

    # if args.movie_demo:
    #     t = np.arange(100)*0.001
    #     Quant = np.array([.5*(1-np.cos(20*np.pi*t))*i/len(SEGMENT_LIST['xcoords']) \
    #                       for i in np.arange(len(SEGMENT_LIST['xcoords']))])*20-70
    #     ani = show_animated_time_varying_trace(1e3*t, Quant, SEGMENT_LIST,
    #                                            fig, ax,
    #                                            polar_angle=args.polar_angle, azimuth_angle=args.azimuth_angle)
        
    ge.show()
