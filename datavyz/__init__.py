import sys, os, platform

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep

import matplotlib.pylab as plt
import numpy as np
    
# import datavyz.single_cell_plots as scp

from .settings import set_env_variables #, update_rcParams


class graph_env:
    

    def __init__(self,
                 env='manuscript'):
        """
        accepts the styles described in 'settings.py'

        use of seaborn and ggplot deprecated ....
        """
        self.override_style=True
        set_env_variables(self, env)

        self.give_color_attributes()

        # if ('dark' in env) or (self.background is 'dark'):
        #     self.set_style('dark_background')
        # elif 'ggplot' in env:
        #     self.default_color = 'dimgrey'
        #     self.set_style('ggplot')
        #     self.override_style = False
        # elif 'seaborn' in env:
        #     self.set_style('seaborn')
        #     self.override_style = False
        # update_rcParams(self)

    
    # ################################################
    # ###### Figure and Axes construction ############
    # ################################################

    from .draw_figure import figure

    from .adjust_plots import set_plot, compute_axes_args,\
            set_ticks_to_log10_axis

    from .inset import inset 
    
    # ################################################
    # ###### Annotations and Legend functions ########
    # ################################################
    
    from .colors import give_color_attributes,\
            get_linear_colormap, lin_cmap

    from .annotations import title, annotate, draw_bar_scales,\
            arrow, int_to_roman, int_to_letter,\
            sci_str, from_pval_to_star, set_fontsize

    from .legend import legend, bar_legend, build_bar_legend,\
            set_bar_legend, build_bar_legend_continuous

    # def set_style(self, style='default'):
        # plt.style.use(style)
        # if style=='dark_background':
            # self.default_color = 'w'


    # ################################################
    # ###### Classical plot functions ################
    # ################################################

    from .line_plots import plot, multicolored_line

    from .bar_plots import bar,\
            related_samples_two_conditions_comparison,\
            unrelated_samples_two_conditions_comparison

    from .scatter_plots import scatter, two_variable_analysis

    from .hist_plots import hist, hist2d

    from .parallel_plots import parallel_plot, components_plot

    from .pie_plots import pie

    from .cross_correl_plot import cross_correl_plot
    
    from .surface_plots import twoD_plot, matrix
    
    from .images import image

    # def boxplot(self, data,
                # fig_args=dict(figsize=(.6,1.)),
                # axes_args={}, **args):
        # fig, ax = self.figure(**fig_args)
        # ax.boxplot(data, **args)
        # self.set_plot(ax, **axes_args)
        # return fig, ax
    
    # ###############################
    # ###### special plots ##########
    # ###############################

    from .connectivity import connectivity_plot

    from .time_freq import time_freq_plot

    from .neurophysio import Ca_trace_plot, raster_plot,\
        response_to_current_pulse, response_to_multiple_current_pulse
    
    # ##################################################
    # ######  FIG TOOLS   ##############################
    # ##################################################
    
    def flat(self, AX):
        """
        to be used in 
        "for ax in ge.flat(AX)"
        """
        List = []
        for ax in AX:
            if type(ax) is list:
                List = List+ax
            else:
                List.append(ax)        
        return np.array(List).flatten()

    def set_common_xlims(self, AX, lims=None):
        if lims is None:
            lims = [np.inf, -np.inf]
            for ax in self.flat(AX):
                lims = [np.min([ax.get_xlim()[0], lims[0]]), np.max([ax.get_xlim()[1], lims[1]])]
        for ax in self.flat(AX):
            ax.set_xlim(lims)
            
    def set_common_ylims(self, AX, lims=None):
        if lims is None:
            lims = [np.inf, -np.inf]
            for ax in self.flat(AX):
                lims = [np.min([ax.get_ylim()[0], lims[0]]), np.max([ax.get_ylim()[1], lims[1]])]
        for ax in self.flat(AX):
            ax.set_ylim(lims)
        
    # ##################################################
    # ######  FIG OUTPUT  ##############################
    # ##################################################

    from .plot_export import multipanel_figure,\
                    put_list_of_figs_to_svg_fig,\
                    export_as_png

    def show(self, block=False):
        if platform.system()=='Windows':
            plt.show()
        elif platform.system()=='Darwin':
            plt.show(block=block)
            input('Hit Enter To Close')
            plt.close()
        else:
            plt.show()

        
    def savefig(self, fig, figname='temp.svg',
                dpi=None, transparent=None, facecolor=None):
        if dpi is None:
            dpi=self.dpi
        if transparent is None:
            transparent=self.transparency
        if facecolor is None:
            facecolor=self.facecolor
        fig.savefig(figname,
                    dpi=dpi, transparent=transparent,
                    facecolor=facecolor)
        
    def save_on_desktop(self, fig, figname='temp.svg', dpi=None):
        if figname.endswith('.png'):
            self.savefig(fig, desktop+figname, dpi=dpi)
        else:
            self.savefig(fig, desktop+figname)

    def gcf(self):
        return plt.gcf()


graph_env_manuscript = graph_env('manuscript')
ge = graph_env()

if __name__=='__main__':

    fig, AX = figure(axes_extents=[\
                                  [[3,2], [1,2] ],
                                   [[1,1], [1,1], [2,1] ] ],
                     left=.3, bottom=.4, hspace=1.4, wspace=1.2,
                     figsize=[.8, .35])
    
    plot(Y=[
        np.random.randn(20),
        np.random.randn(20),
        np.random.randn(20),
        np.random.randn(20)],
         sY=[
             np.ones(20),
             np.ones(20),
             np.random.randn(20),
             np.random.randn(20)],
         ax=AX[0][0],
         COLORS=[Red, Purple, Blue, Green],
         legend_args={'frameon':False},
         axes_args={'spines':['left']})
    
    scatter(X=np.random.randn(4,5), Y=np.random.randn(4,5),
            sX=np.random.randn(4,5),sY=np.random.randn(4,5),
            ax=AX[1][0],
            bar_legend_args={},
            bar_label='condition')
    
    plot(np.random.randn(20), sy=np.random.randn(20),
         ax=AX[1][2])
    scatter(np.random.randn(20), sy=np.random.randn(20),
            ax=AX[1][2])
    plot(np.random.randn(20), sy=np.random.randn(20),
            ax=AX[1][2], color=Red)
    scatter(np.random.randn(20), sy=np.random.randn(20),
            ax=AX[1][2], color=Red)
    plot(np.sin(np.linspace(0,1,30)*3*np.pi)*2,
         ax=AX[1][2], color=Purple)
    plot(np.cos(np.linspace(0,1,30)*3*np.pi)*2,
         ax=AX[1][2], color=Green)
    
    hist(np.random.randn(200), ax=AX[0][1],\
         orientation='vertical',
         axes_args={'ylim':AX[0][0].get_ylim(), 'spines':['left']})
    
    AX[1][1].axis('off')
    # fig.savefig('fig.png', dpi=200)
    # save_on_desktop(fig, figname='fig.png')

    # fig2, AX = figure(axes=(2,1),
    #                   left=.4, bottom=.4, hspace=1.4, wspace=1.2,
    #                   figsize=[.45, .3])
    # import itertools
    # for i in range(2):
    #     plot(np.random.randn(20), sy=np.random.randn(20),
    #          ax=AX[i])
    # # fig2.savefig('fig2.png', dpi=200)
    # fig1, AX = figure(axes_extents=[\
    #                                [[3,1], [1,1] ],
    #                                [[1,1], [2,1], [1,1] ] ] )
    # fig2, AX = figure(axes=(2,1))
    # for ax in AX:
    #     scatter(np.abs(np.exp(np.random.randn(100))), np.abs(np.exp(np.random.randn(100))), ax=ax)
    #     set_plot(ax, yscale='log', xscale='log')
    # show()
    # print('should be 1, 1')
    # fig2, AX = figure(axes=(1,1))
    # print('should be 2, 1')
    # fig2, AX = figure(axes=(2,1))
    # print('should be 1, 2')
    # fig2, AX = figure(axes=(1,2))
    # print('should be 3, 2')
    # fig2, AX = figure(axes=(3,2))
    # # show()

    # fig, _ = figure()
    # fig, _ = plot(Y=np.random.randn(4, 10), sY=np.random.randn(4, 10),
    #               axes_args={'spines':['left', 'bottom'], 'xlabel':'my-x value', 'ylabel':'my-y value'})
    # save_on_desktop(fig, figname='2.svg')
    # show()

    # mg = graphs('ggplot_npotebook')
    # mg = graphs()
    # mg.hist(np.random.randn(100), xlabel='ksjdfh')
    

    # ge.boxplot(np.exp(np.random.randn(100)),
    #            axes_args=dict(xticks=[1],
    #                           xticks_labels=['data']))

    # fig_lf, AX = ge.figure(axes_extents=[[[3,1]],[[1,2],[1,2],[1,2]]], figsize=(1.,.5), wspace=3., hspace=2.)
    # for ax in [item for sublist in AX for item in sublist]:
        # ge.top_left_letter(ax, 'a')
    # # _, ax, _ = ge.figure(with_bar_legend=True)
    # AX[1][0].hist(np.random.randn(100))
    # fig, ax = ge.figure()
    # ax.hist(np.random.randn(100))
    # ge.panel_label(ax, 'a')
    # ge.annotate(ax, 'blabla', (0.7, 0.8), italic=True)
    # ge.set_plot(ax)
    # ge.set_common_xlims(AX)
    # ge.show()

    ge = graph_env()

    # ge.show()


