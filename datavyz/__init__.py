import sys, os, platform

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')+os.path.sep
home = os.path.expanduser('~')+os.path.sep

from .dependencies import *

# import datavyz.single_cell_plots as scp
# from datavyz.plot_export import put_list_of_figs_to_svg_fig, multipanel_figure
# from datavyz.dynamic_plot import movie_plot, animated_plot
# from datavyz.time_freq import time_freq_plot
# from datavyz.neurophysio import Ca_trace_plot
# from datavyz.plot_export import put_list_of_figs_to_svg_fig, multipanel_figure
# from datavyz.dynamic_plot import movie_plot, animated_plot
# from datavyz.time_freq import time_freq_plot
# from datavyz.neurophysio import Ca_trace_plot

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

    from .adjust_plots import set_plot, compute_axes_args

    from .inset import inset 
    
    # ################################################
    # ###### Annotations and Legend functions ########
    # ################################################
    
    from .colors import give_color_attributes, viridis, binary_r 

    from .annotations import title, annotate, draw_bar_scales,\
            arrow, int_to_roman, int_to_letter,\
            sci_str, from_pval_to_star

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

    from .scatter_plots import scatter

    from .hist_plots import hist, hist2d

    from .parallel_plots import parallel_plot, components_plot

    from .pie_plots import pie

    from .cross_correl_plot import cross_correl_plot
    
    from .surface_plots import twoD_plot, matrix
    
    # def boxplot(self, data,
                # fig_args=dict(figsize=(.6,1.)),
                # axes_args={}, **args):
        # fig, ax = self.figure(**fig_args)
        # ax.boxplot(data, **args)
        # self.set_plot(ax, **axes_args)
        # return fig, ax
    
    # # animated plot
    # def animated_plot(self, x, time_dep_y, **args):
        # return animated_plot(self, x, time_dep_y, **args)
    
    # # twoD-plot with x-y axis from bottom left
    # def twoD_plot(self, x, y, z, **args):
        # return twoD_plot(self, x, y, z, **args)

    # def matrix(self, z, **args):
        # return matrix(self, z, **args)

    # # image plot
    # def image(self, X, cmap=binary_r, alpha=1., ax=None, title=''):
        # if ax is None:
            # fig, ax = self.figure()
        # else:
            # fig = plt.gcf()
        # ax.imshow(X.T, cmap=cmap, alpha=alpha,
                  # interpolation=None,
                  # origin='lower',
                  # aspect='equal')
        # ax.axis('off')
        # if title!='':
            # self.title(ax, title)
        # return fig, ax

    # # movie plot
    # def movie(self, array, **args):
        # return movie_plot(self, array, **args)
    
        
    # ################################################
    # ###### legend function #######################
    # ################################################

    # # def legend(self, list_of_lines, list_of_labels, **args):
    # #     return legend.legend(list_of_lines, list_of_labels, **args)
    # def legend(self, ax, **args):
        # return legend.legend(self, ax, **args)

    # def bar_legend(self, stuff, **args): # stuff can be either ax or fig
        # return legend.bar_legend(self, stuff, **args)

    # def build_bar_legend(self, X, ax, mymap, **args):
        # return legend.build_bar_legend(X, ax, mymap, **args)

    # def build_bar_legend_continuous(self, ax, mymap, **args):
        # return legend.build_bar_legend_continuous(ax, mymap, **args)
    
    # def get_linear_colormap(self, **args):
        # return legend.get_linear_colormap(**args)
    
    # ################################################
    # ###### Axes function #######################
    # ################################################
    
    # def inset(self, stuff, rect=[.5,.5,.5,.4], facecolor=None):
        # return inset(self, stuff, rect=rect, facecolor=facecolor)

    # def adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                      # xcolor='w', ycolor='w'):
        # if xcolor is None:
            # xcolor = self.default_color
        # if ycolor is None:
            # ycolor = self.default_color
        # ap.adjust_spines(ax, spines, tck_outward=3, tck_length=4.,
                             # xcolor=xcolor, ycolor=ycolor)

    # def set_plot(self, ax, spines=['left', 'bottom'], **args):
        # ap.set_plot(self, ax, spines, **args)

    # def add_to_axes_args(self, xlabel, ylabel, title, axes_args):
        # if xlabel is not None:
            # axes_args['xlabel'] = xlabel
        # if ylabel is not None:
            # axes_args['ylabel'] = ylabel
        # if title is not None:
            # axes_args['title'] = title
        # return axes_args
    
    # ################################################
    # ###### signal plots ########################
    # ################################################
    # def time_freq_plot(self, t, freqs, data, coefs, **args):
        # return time_freq_plot(self, t, freqs, data, coefs, **args)

    # ################################################
    # ###### stat plots ########################
    # ################################################

    # def two_variable_analysis(self, first_observations, second_observations, **args):
        # return scatter_plots.two_variable_analysis(first_observations, second_observations, cls=self, **args)

    # ################################################
    # ###### electrophy plots ########################
    # ################################################

    # def Ca_trace_plot(self, Data, **args):
        # return Ca_trace_plot(self, Data, **args)

    # def response_to_current_pulse(self, t, Vm, I, spikes, **args):
        # return scp.response_to_current_pulse(self, t, Vm, I, spikes, **args)

    # def response_to_multiple_current_pulse(self, t, VMS, II, SPIKES, **args):
        # return scp.response_to_multiple_current_pulse(self, t, VMS, II, SPIKES, **args)
    
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


