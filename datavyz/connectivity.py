import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))

from datavyz.dependencies import *

from matplotlib.pylab import Circle, setp
import matplotlib.patches as patches

import matplotlib.pyplot as plt
import numpy as np


def connectivity_plot(graph,
                      POPS,
                      CONNEC,
                      size_pop_conversion_factor=5e-2,
                      connectivity_conversion_factor=2.):

    fig, ax = graph.figure(figsize=(3., 5.3), left=0, right=0., bottom=0., top=0.)

    for i, pop in enumerate(POPS):

        angle = i*2.*np.pi/len(POPS)
        radius = size_pop_conversion_factor*np.log10(POPS[pop]['Ncell'])
        x0, y0 = np.cos(angle), np.sin(angle)
        Centre_Circle = Circle((x0,y0), radius,
                               fc=POPS[pop]['color'], alpha=.5)
        ax.add_artist(Centre_Circle)
        ge.annotate(ax, pop, (x0, y0),
                    ha='center', va='center', xycoords='data', color='k', bold=True)


        # self connection
        dsc = size_pop_conversion_factor*np.log10(POPS[pop]['Ncell'])
        x1, y1 = x0+dsc*np.cos(angle), y0+dsc*np.sin(angle)
        sc_shift = 0.1
        dx, dy = sc_shift*np.cos(angle+np.pi/2.), sc_shift*np.sin(angle+np.pi/2.)
        sc = patches.FancyArrowPatch((x1-dx/2, y1-dy/2.), (x1+dx/2., y1+dy/2.),
                                     arrowstyle='->',
                                     patchA=None, patchB=None,
                                     connectionstyle="bar,fraction=1.",
                                     color=POPS[pop]['color'], lw=3)
        ax.add_patch(sc)

        # true connections
        for j, target in enumerate(POPS):
            if target!=pop: # see above for self connectivity
                
                angleJ = j*2.*np.pi/len(POPS)
                xj, yj = np.cos(angleJ)/2.+.5, np.sin(angleJ)/2.+.5
                radiusJ = size_pop_conversion_factor*np.log10(POPS[target]['Ncell'])
                relation_angle = (angleJ-angle)
                print(pop, target, relation_angle)
                xj1, yj1 = xj-radiusJ*np.cos(relation_angle), yj-radiusJ*np.sin(relation_angle)
                xi1, yi1 = x0+radius*np.cos(relation_angle), y0+radius*np.sin(relation_angle)

                print(pop, target, angle, angleJ)
                cij_shift = .1
                dx, dy = cij_shift*np.cos(relation_angle), cij_shift*np.sin(relation_angle)
                if i>j:
                    dcij_shift = +.05
                else:
                    dcij_shift = -.05
                dx2, dy2 = 0, 0 # dcij_shift*np.cos(relation_angle+np.pi/2), dcij_shift*np.sin(relation_angle+np.pi/2)
                
                # cij = patches.FancyArrowPatch((x0, y0),
                #                               (xj, yj),
                cij = patches.FancyArrowPatch((xi1-dx2, yi1+dx2),
                                              (xj1+dx2, yj1-dy2),
                                             arrowstyle='->',
                                             patchA=None, patchB=None,
                                             # connectionstyle="bar,fraction=0.7",
                                             color=POPS[pop]['color'], lw=3)
                
                ax.add_patch(cij)
                
    
    
    
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlim([-1.5, 1.5])
    ax.axis('equal')
    ax.axis('off')

    return fig, ax



if __name__=='__main__':
    
    from datavyz.main import graph_env

    ge = graph_env('screen')

    POPS = {'Pyr':{'Ncell':4000, 'color':ge.green},
            'PV':{'Ncell':500, 'color':ge.red},
            # 'SST':{'Ncell':250, 'color':ge.orange},
            'VIP':{'Ncell':250, 'color':ge.purple}}
    CONNEC = {'Pyr_PV':0.05,
              'Pyr_SST':0.05,
              'Pyr_Pyr':0.05,
              'Pyr_PV':0.05}
    
    connectivity_plot(ge, POPS, CONNEC)
    
    ge.show()

# rates_to_bases = {'r1': 'AT', 'r2': 'TA', 'r3': 'GA', 'r4': 'AG', 'r5': 'CA',
#                   'r6': 'AC', 'r7': 'GT', 'r8': 'TG', 'r9': 'CT', 'r10': 'TC',
#                   'r11': 'GC', 'r12': 'CG'}
# numbered_bases_to_rates = {v: k for k, v in rates_to_bases.items()}
# lettered_bases_to_rates = {v: 'r' + v for k, v in rates_to_bases.items()}


# def make_arrow_plot(data, size=4, display='length', shape='right',
#                     max_arrow_width=0.03, arrow_sep=0.02, alpha=0.5,
#                     normalize_data=False, ec=None, labelcolor=None,
#                     head_starts_at_zero=True,
#                     rate_labels=lettered_bases_to_rates,
#                     **kwargs):
#     """Makes an arrow plot.

#     Parameters:

#     data: dict with probabilities for the bases and pair transitions.
#     size: size of the graph in inches.
#     display: 'length', 'width', or 'alpha' for arrow property to change.
#     shape: 'full', 'left', or 'right' for full or half arrows.
#     max_arrow_width: maximum width of an arrow, data coordinates.
#     arrow_sep: separation between arrows in a pair, data coordinates.
#     alpha: maximum opacity of arrows, default 0.8.

#     **kwargs can be anything allowed by a Arrow object, e.g.
#     linewidth and edgecolor.
#     """

#     plt.xlim(-0.5, 1.5)
#     plt.ylim(-0.5, 1.5)
#     plt.gcf().set_size_inches(size, size)
#     plt.xticks([])
#     plt.yticks([])
#     max_text_size = size * 12
#     min_text_size = size
#     label_text_size = size * 2.5
    
#     text_params = {'ha': 'center', 'va': 'center', 'family': 'sans-serif',
#                    'fontweight': 'bold'}
#     r2 = np.sqrt(2)

#     deltas = {
#         'AT': (1, 0),
#         'TA': (-1, 0),
#         'GA': (0, 1),
#         'AG': (0, -1),
#         'CA': (-1 / r2, 1 / r2),
#         'AC': (1 / r2, -1 / r2),
#         'GT': (1 / r2, 1 / r2),
#         'TG': (-1 / r2, -1 / r2),
#         'CT': (0, 1),
#         'TC': (0, -1),
#         'GC': (1, 0),
#         'CG': (-1, 0)}

#     colors = {
#         'AT': 'r',
#         'TA': 'k',
#         'GA': 'g',
#         'AG': 'r',
#         'CA': 'b',
#         'AC': 'r',
#         'GT': 'g',
#         'TG': 'k',
#         'CT': 'b',
#         'TC': 'k',
#         'GC': 'g',
#         'CG': 'b'}

#     label_positions = {
#         'AT': 'center',
#         'TA': 'center',
#         'GA': 'center',
#         'AG': 'center',
#         'CA': 'left',
#         'AC': 'left',
#         'GT': 'left',
#         'TG': 'left',
#         'CT': 'center',
#         'TC': 'center',
#         'GC': 'center',
#         'CG': 'center'}

#     def do_fontsize(k):
#         return float(np.clip(max_text_size * np.sqrt(data[k]),
#                              min_text_size, max_text_size))

#     A = plt.text(0, 1, '$A_3$', color='r', size=do_fontsize('A'),
#                  **text_params)
#     T = plt.text(1, 1, '$T_3$', color='k', size=do_fontsize('T'),
#                  **text_params)
#     G = plt.text(0, 0, '$G_3$', color='g', size=do_fontsize('G'),
#                  **text_params)
#     C = plt.text(1, 0, '$C_3$', color='b', size=do_fontsize('C'),
#                  **text_params)

#     arrow_h_offset = 0.25  # data coordinates, empirically determined
#     max_arrow_length = 1 - 2 * arrow_h_offset
#     max_head_width = 2.5 * max_arrow_width
#     max_head_length = 2 * max_arrow_width
#     arrow_params = {'length_includes_head': True, 'shape': shape,
#                     'head_starts_at_zero': head_starts_at_zero}
#     sf = 0.6  # max arrow size represents this in data coords

#     d = (r2 / 2 + arrow_h_offset - 0.5) / r2  # distance for diags
#     r2v = arrow_sep / r2  # offset for diags

#     # tuple of x, y for start position
#     positions = {
#         'AT': (arrow_h_offset, 1 + arrow_sep),
#         'TA': (1 - arrow_h_offset, 1 - arrow_sep),
#         'GA': (-arrow_sep, arrow_h_offset),
#         'AG': (arrow_sep, 1 - arrow_h_offset),
#         'CA': (1 - d - r2v, d - r2v),
#         'AC': (d + r2v, 1 - d + r2v),
#         'GT': (d - r2v, d + r2v),
#         'TG': (1 - d + r2v, 1 - d - r2v),
#         'CT': (1 - arrow_sep, arrow_h_offset),
#         'TC': (1 + arrow_sep, 1 - arrow_h_offset),
#         'GC': (arrow_h_offset, arrow_sep),
#         'CG': (1 - arrow_h_offset, -arrow_sep)}

#     if normalize_data:
#         # find maximum value for rates, i.e. where keys are 2 chars long
#         max_val = max((v for k, v in data.items() if len(k) == 2), default=0)
#         # divide rates by max val, multiply by arrow scale factor
#         for k, v in data.items():
#             data[k] = v / max_val * sf

#     def draw_arrow(pair, alpha=alpha, ec=ec, labelcolor=labelcolor):
#         # set the length of the arrow
#         if display == 'length':
#             length = (max_head_length
#                       + data[pair] / sf * (max_arrow_length - max_head_length))
#         else:
#             length = max_arrow_length
#         # set the transparency of the arrow
#         if display == 'alpha':
#             alpha = min(data[pair] / sf, alpha)

#         # set the width of the arrow
#         if display == 'width':
#             scale = data[pair] / sf
#             width = max_arrow_width * scale
#             head_width = max_head_width * scale
#             head_length = max_head_length * scale
#         else:
#             width = max_arrow_width
#             head_width = max_head_width
#             head_length = max_head_length

#         fc = colors[pair]
#         ec = ec or fc

#         x_scale, y_scale = deltas[pair]
#         x_pos, y_pos = positions[pair]
#         plt.arrow(x_pos, y_pos, x_scale * length, y_scale * length,
#                   fc=fc, ec=ec, alpha=alpha, width=width,
#                   head_width=head_width, head_length=head_length,
#                   **arrow_params)

#         # figure out coordinates for text
#         # if drawing relative to base: x and y are same as for arrow
#         # dx and dy are one arrow width left and up
#         # need to rotate based on direction of arrow, use x_scale and y_scale
#         # as sin x and cos x?
#         sx, cx = y_scale, x_scale

#         where = label_positions[pair]
#         if where == 'left':
#             orig_position = 3 * np.array([[max_arrow_width, max_arrow_width]])
#         elif where == 'absolute':
#             orig_position = np.array([[max_arrow_length / 2.0,
#                                        3 * max_arrow_width]])
#         elif where == 'right':
#             orig_position = np.array([[length - 3 * max_arrow_width,
#                                        3 * max_arrow_width]])
#         elif where == 'center':
#             orig_position = np.array([[length / 2.0, 3 * max_arrow_width]])
#         else:
#             raise ValueError("Got unknown position parameter %s" % where)

#         M = np.array([[cx, sx], [-sx, cx]])
#         coords = np.dot(orig_position, M) + [[x_pos, y_pos]]
#         x, y = np.ravel(coords)
#         orig_label = rate_labels[pair]
#         label = r'$%s_{_{\mathrm{%s}}}$' % (orig_label[0], orig_label[1:])

#         plt.text(x, y, label, size=label_text_size, ha='center', va='center',
#                  color=labelcolor or fc)

#     for p in sorted(positions):
#         draw_arrow(p)


# # test data
# all_on_max = dict([(i, 1) for i in 'TCAG'] +
#                   [(i + j, 0.6) for i in 'TCAG' for j in 'TCAG'])

# realistic_data = {
#     'A': 0.4,
#     'T': 0.3,
#     'G': 0.5,
#     'C': 0.2,
#     'AT': 0.4,
#     'AC': 0.3,
#     'AG': 0.2,
#     'TA': 0.2,
#     'TC': 0.3,
#     'TG': 0.4,
#     'CT': 0.2,
#     'CG': 0.3,
#     'CA': 0.2,
#     'GA': 0.1,
#     'GT': 0.4,
#     'GC': 0.1}

# extreme_data = {
#     'A': 0.75,
#     'T': 0.10,
#     'G': 0.10,
#     'C': 0.05,
#     'AT': 0.6,
#     'AC': 0.3,
#     'AG': 0.1,
#     'TA': 0.02,
#     'TC': 0.3,
#     'TG': 0.01,
#     'CT': 0.2,
#     'CG': 0.5,
#     'CA': 0.2,
#     'GA': 0.1,
#     'GT': 0.4,
#     'GC': 0.2}

# sample_data = {
#     'A': 0.2137,
#     'T': 0.3541,
#     'G': 0.1946,
#     'C': 0.2376,
#     'AT': 0.0228,
#     'AC': 0.0684,
#     'AG': 0.2056,
#     'TA': 0.0315,
#     'TC': 0.0629,
#     'TG': 0.0315,
#     'CT': 0.1355,
#     'CG': 0.0401,
#     'CA': 0.0703,
#     'GA': 0.1824,
#     'GT': 0.0387,
#     'GC': 0.1106}


# if __name__ == '__main__':
#     from sys import argv
#     d = None
#     if len(argv) > 1:
#         if argv[1] == 'full':
#             d = all_on_max
#             scaled = False
#         elif argv[1] == 'extreme':
#             d = extreme_data
#             scaled = False
#         elif argv[1] == 'realistic':
#             d = realistic_data
#             scaled = False
#         elif argv[1] == 'sample':
#             d = sample_data
#             scaled = True
#     if d is None:
#         d = all_on_max
#         scaled = False
#     if len(argv) > 2:
#         display = argv[2]
#     else:
#         display = 'length'

#     size = 4
#     plt.figure(figsize=(size, size))

#     make_arrow_plot(d, display=display, linewidth=0.001, edgecolor=None,
#                     normalize_data=scaled, head_starts_at_zero=True, size=size)

#     plt.show()

    
# def pie(graph, data,
#         ax=None,
#         ext_labels= None,
#         pie_labels = None,
#         explodes=None,
#         COLORS=None,
#         ext_labels_distance = 1.1,
#         pie_labels_distance = 0.6,
#         pie_labels_digits = 1,
#         ext_text_settings=dict(weight='normal'),
#         pie_text_settings=dict(weight='normal', color='k'),
#         center_circle=0.3,
#         title='',
#         fig_args=dict(bottom=0.3, left=0.3, top=3.),
#         axes_args={},
#         pie_args={},
#         legend=None):

#     """    
#     return fig, ax
#     """
    
#     # getting or creating the axis
#     if ax is None:
#         if legend is not None:
#             fig, ax = graph.figure(with_legend_space=True, left=1.5, right=2, top=0.1)
#         else:
#             fig, ax = graph.figure(**fig_args)
#     else:
#         fig = graph.gcf()
        
#     if COLORS is None:
#         COLORS = graph.colors[:len(data)]
#     if (explodes is None):
#         explodes = np.zeros(len(data))
#     if (ext_labels is None):
#         ext_labels = np.zeros(len(data), dtype=str)

#     if pie_labels is not None:
#         pie_labels_map = {}
#         for pl, val in zip(pie_labels, data):
#             pie_labels_map[str(np.round(100.*val/np.sum(data),pie_labels_digits))] = pl
#         def func(pct):
#             return pie_labels_map[str(np.round(pct,pie_labels_digits))]
#     else:
#         def func(pct):
#             return ''
        
    
#     wedges, ext_texts, pie_texts = ax.pie(data,
#                                           labels=ext_labels,
#                                           autopct=func,
#                                           explode=explodes,
#                                           pctdistance=pie_labels_distance,
#                                           labeldistance=ext_labels_distance,
#                                           colors=COLORS, **pie_args)
#     setp(pie_texts, **pie_text_settings)
#     setp(ext_texts, **ext_text_settings)
    
#     Centre_Circle = Circle((0,0), center_circle, fc='white')
#     ax.add_artist(Centre_Circle)
                                  
#     if legend is not None:
#         if 'loc' not in legend:
#             legend['loc']=(1.21,.2)
#         ax.legend(**legend)

#     if title!='':
#         graph.title(ax, title)
        
#     ax.axis('equal')
#     return fig, ax


# if __name__=='__main__':
    
#     from datavyz.main import graph_env

#     ge = graph_env('manuscript')

#     data = .5+np.abs(np.random.randn(3))*.4

#     #plotting
#     fig, ax = ge.pie(data,
#                      ext_labels = ['Data1', 'Data2', 'Data3'],
#                      pie_labels = ['%.1f%%' % (100*d/data.sum()) for d in data],
#                      ext_labels_distance=1.2,
#                      explodes=0.05*np.ones(len(data)),
#                      center_circle=0.2,
#                      COLORS = [ge.tab20(x) for x in np.linspace(0,1,len(data))],
#                      # pie_args=dict(rotate=90), # e.g. for rotation
#                      legend=None)  # set legend={} to have it appearing
#     # fig.savefig('docs/pie-plot.png')
#     ge.show()
