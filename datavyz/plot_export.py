import sys, pathlib, os
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import string, datetime
from tempfile import gettempdir
from matplotlib.backends.backend_pdf import PdfPages

# SPECIAL PYTHON PACKAGES FOR:
import svgutils.compose as sg # SVG
# import fpdf # PDF
from PIL import Image # BITMAP (png, jpg, ...)
### /!\ need to have the inkscape 

from datavyz.scaling import inch2cm, cm2inch
from datavyz.dependencies import *

def put_list_of_figs_to_svg_fig(FIGS,
                                fig_name="fig.svg",
                                initial_guess=True,
                                visualize=False,
                                export_as_png=False,
                                Props = None,
                                figsize = None,
                                fontsize=9,
                                SCALING_FACTOR=1.34, # needed to get the right cm size ...
                                with_top_left_letter=False,
                                transparent=True):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]

    SIZE = []
    for fig in FIGS:
        if type(fig)==str:
            SIZE.append([1.,1.])
        else:
            SIZE.append(fig.get_size_inches())
            
    width = np.max([s[0] for s in SIZE])
    height = np.max([s[1] for s in SIZE])
    
    if Props is None:
        LABELS, XCOORD, YCOORD = [], [], []

        # saving as svg
        for i in range(len(FIGS)):
            LABELS.append(label[i])
            XCOORD.append((i%3)*width*100)
            YCOORD.append(int(i/3)*height*100)
        XCOORD_LABELS,\
            YCOORD_LABELS = XCOORD, YCOORD

    else:
        XCOORD, YCOORD = Props['XCOORD'],\
                Props['YCOORD'], 
        if 'LABELS' in Props:
            LABELS = Props['LABELS']
        else:
            LABELS = ['' for x in XCOORD]
        if 'XCOORD_LABELS' in Props:
            XCOORD_LABELS,\
                YCOORD_LABELS = Props['XCOORD_LABELS'],\
                                Props['YCOORD_LABELS']
        else:
            XCOORD_LABELS,\
                YCOORD_LABELS = XCOORD, YCOORD

    LOCATIONS = []
    for i in range(len(FIGS)):
        if type(FIGS[i]) is str:
            LOCATIONS.append(FIGS[i])
        else:
            LOCATIONS.append(os.path.join(gettempdir(), str(i)+'.svg'))
            FIGS[i].savefig(LOCATIONS[-1], format='svg',
                            transparent=transparent)
        
    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG(LOCATIONS[i]).move(XCOORD[i],YCOORD[i])))
                      
    for i in range(len(LABELS)):
        PANELS.append(sg.Panel(\
            sg.Text(LABELS[i], 15, 10,
                    size=fontsize, weight='bold').move(\
                                                       XCOORD_LABELS[i],YCOORD_LABELS[i]))\
        )

    sg.Figure("21cm", "29.7cm", *PANELS).scale(SCALING_FACTOR).save(fig_name)
    # if figsize is None:
    #     sg.Figure("21cm", "29.7cm", *PANELS).save(fig_name)
    # else:
    #     sg.Figure(str(inch2cm(figsize[0]*A0_format['width'])[0])+"cm",\
    #               str(inch2cm(figsize[1]*A0_format['height'])[0])+"cm",\
    #               *PANELS).scale(SCALING_FACTOR).save(fig_name)

    if visualize:
        os.system('open '+fig_name) # works well with 'Gapplin' on OS-X
        ## KEEP -> previous version
        # os.system('convert '+fig_name+' '+fig_name.replace('.svg', '.png'))
        # plt.close('all')
        # z = plt.imread(fig_name.replace('.svg', '.png'))
        # plt.imshow(z)
        # fig = plt.gcf()
        # # if figsize is not None:
        # #     fig.set_size_inches(fig.get_size_inches()[0]*3,
        # #                         fig.get_size_inches()[1]*3,
        # #                         forward=True)
        # if not no_show:
        #     from datavyz..graphs import show
        #     show()

def export_as_png(fig_name, dpi=300):
    instruction = 'inkscape '+fig_name+' --export-area-drawing --export-png='+\
                    fig_name.replace('.svg', '.png')+' --export-dpi='+str(dpi)
    print('RUNNING:', instruction)
    os.system(instruction)
    if os.path.isfile(fig_name.replace('.svg', '.png')):
        print('[ok] figure successfully exported as: %s' % fig_name.replace('.svg', '.png'))
    else:
        print('[!!] %s not exported as png' % fig_name)
        
def put_list_of_figs_to_multipage_pdf(FIGS,
                                      pdf_name='figures.pdf',
                                      pdf_title=''):
    """
    adapted from:
    http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
    """
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(pdf_name) as pdf:
        
        for fig in FIGS:
            pdf.savefig(fig)  # saves the current figure into a pdf page

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = u'Y. Zerlaut'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()


def concatenate_pngs(PNG_LIST, ordering='vertically', figname='fig.png'):
    
    images = map(Image.open, PNG_LIST)
    widths, heights = zip(*(i.size for i in images))

    if ordering=='vertically':
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for fig in PNG_LIST:
            im = Image.open(fig)
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

    new_im.save(figname)


if __name__=='__main__':

    from datavyz.graph_env import graph_env
    ge = graph_env()

    filedir=os.path.abspath(__file__).replace(os.path.basename(__file__),'')
    
    fig1, ax1 = ge.plot(Y=np.random.randn(10,4),\
                        sY=np.random.randn(10,4),
                        axes_args={'xlabel':'x-label', 'ylabel':'y-label'})
    fig1.savefig(filedir+'../output/fig.svg')
    
    fig2, ax2 = ge.scatter(X=np.arange(4)+0.1*np.random.randn(10,4),\
                           Y=np.random.randn(10,4),\
                           sY=np.random.randn(10,4), axes_args={'xlabel':'x-label', 'ylabel':'y-label'})

    # put_list_of_figs_to_multipage_pdf([fig1, fig2])
    put_list_of_figs_to_svg_fig([filedir+'../docs/schematic.svg', fig2, fig1],
                                fig_name=filedir+'../output/fig.svg',
                                Props={'XCOORD':[0,100,210],
                                       'YCOORD':[0, 0, 0],
                                       'XCOORD_LABELS':[0,90,195],
                                       'YCOORD_LABELS':np.zeros(3),
                                       'LABELS':['a','b','c']})
    
    export_as_png(filedir+'../output/fig.svg')

