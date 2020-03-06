import sys, os
import matplotlib
matplotlib.use('Qt5Agg') 
from datavyz.atplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datavyz.atplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from datavyz.yQt5 import QtGui, QtWidgets, QtCore
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('../')
from datavyz.my_graph import set_plot, put_list_of_figs_to_svg_fig

def get_figure_list(DATA_FILE):
    plt.close('all')
    data = np.load(DATA_FILE)
    exec(str(data['plot']))
    FIG_LIST = []
    for i in plt.get_fignums():
        FIG_LIST.append(plt.figure(i))
    return FIG_LIST
    
def create_window(parent, FIG_LIST):

    # # get all figures with their size !
    width, height = 0, 0
    for fig in FIG_LIST[:3]:
        size = fig.get_size_inches()*fig.dpi*.9
        width += size[0]
    for fig in FIG_LIST[::3]:
        height += size[1]
    
    # Window size choosen appropriately
    window = QtWidgets.QDialog()
    window.setGeometry(100,150, width, height)
    
    # this is the Canvas Widget that displays the `figure`
    # it takes the `figure` instance as a parameter to __init__
    CANVAS = []
    for fig in FIG_LIST:
        CANVAS.append(FigureCanvas(fig))

    # this is the Navigation widget
    # it takes the Canvas widget and a parent
    layout = QtWidgets.QGridLayout(window)
    for ic in range(len(CANVAS)):
        layout.addWidget(CANVAS[ic], int(ic/3), ic%3)
    # toolbar = NavigationToolbar(canvas, parent)
    # layout.addWidget(toolbar)
    window.setLayout(layout)
    return window

def get_list_of_temp_files():
    F = []
    for file in os.listdir("/tmp")[::-1]:
        if file.endswith(".npz"):
            F.append('/tmp/'+file)
    return F
        
class Window(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None, DATA_LIST=None, KEYS=None):
        
        self.i_plot = 0
        self.FIG_LIST = []
        self.filename = get_list_of_temp_files()[self.i_plot] # on /tmp/        
        super(Window, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('my_logo.png'))
        self.setWindowTitle('.-* datavYZ *-.     Data vizualization software')
        self.setGeometry(50,50,500,70)

        # buttons
        btnq = QtWidgets.QPushButton("Quit", self)
        btnq.clicked.connect(self.close_app)
        btn1 = QtWidgets.QPushButton("Open File", self)
        btn1.clicked.connect(self.file_open)
        btn2 = QtWidgets.QPushButton("Save as SVG", self)
        btn2.clicked.connect(self.save_as_svg)
        btn3 = QtWidgets.QPushButton("Save as PNG", self)
        btn3.clicked.connect(self.save_as_png)
        for btn, shift in zip([btn1, btn2, btn3], 100*np.arange(1,4)):
            btn.move(shift, 0)

        # quit shortcut
        QuitAction = QtWidgets.QAction('Quit', self)
        QuitAction.setShortcut('q')
        QuitAction.setStatusTip('Close the app')
        QuitAction.triggered.connect(self.close_app)
        # next plot shortcut
        NextFile = QtWidgets.QAction('Next File', self)
        NextFile.setShortcut('n')
        NextFile.setStatusTip('Next File')
        NextFile.triggered.connect(self.next_plot)
        # previous plot shortcut
        PrevFile = QtWidgets.QAction('Prev. File', self)
        PrevFile.setShortcut('p')
        PrevFile.setStatusTip('Prev. File')
        PrevFile.triggered.connect(self.prev_plot)
        # update plot shortcut
        UpdatePlot = QtWidgets.QAction('Update', self)
        UpdatePlot.setShortcut('u')
        UpdatePlot.setStatusTip('Update')
        UpdatePlot.triggered.connect(self.update_plot)
        # save plot shortcut
        SaveAsSvg = QtWidgets.QAction('Save as .svg', self)
        SaveAsSvg.setShortcut('s')
        SaveAsSvg.setStatusTip('Save as .svg')
        SaveAsSvg.triggered.connect(self.save_as_svg)
        # save plot shortcut as PNG
        OpenFile = QtWidgets.QAction('Open File', self)
        OpenFile.setShortcut('o') # 'b' for bitmap !!
        OpenFile.setStatusTip('Open File')
        OpenFile.triggered.connect(self.file_open)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        
        for eA in [QuitAction, NextFile, PrevFile,\
                   UpdatePlot,SaveAsSvg, OpenFile]:
            fileMenu.addAction(eA)

        self.update_plot()    
        self.show()

    def update_plot(self):
        self.FIG_LIST = get_figure_list(self.filename)
        self.window = create_window(self, self.FIG_LIST)
        self.window.show()
        self.statusBar().showMessage('DATA file : '+self.filename)
        self.activateWindow()
        
    def close_app(self):
        sys.exit()

    def file_open(self):
        name=QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        print(name)
        self.filename = name[0]
        self.update_plot()    

        
    def save_as_svg(self):
        put_list_of_figs_to_svg_fig(self.FIG_LIST,\
                    fig_name='/Users/yzerlaut/Desktop/fig.svg')
        self.statusBar().showMessage(\
                'Figure saved as : /Users/yzerlaut/Desktop/fig.svg')

    def save_as_png(self):
        i=0
        for ii in range(len(self.FIG_LIST)):
            self.FIG_LIST[ii].savefig(\
                    '/Users/yzerlaut/Desktop/fig'+str(ii)+'.png')
        self.statusBar().showMessage(\
                'Figures saved as : ~/Desktop/figXX.png')
        
    def prev_plot(self):
        self.i_plot -=1
        if self.i_plot>=0:
            self.filename = get_list_of_temp_files()[self.i_plot]
            self.update_plot()    
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'<1 !!')
            self.i_plot +=1
    def next_plot(self, ii):
        self.i_plot +=1
        if (self.i_plot<len(get_list_of_temp_files())):
            self.filename = get_list_of_temp_files()[self.i_plot]
            self.update_plot()    
        else:
            self.statusBar().showMessage('Reached the Boudaries of the File List, i_plot='+str(self.i_plot+1)+'>'+str(len(get_list_of_temp_files())))
            self.i_plot -=1


if __name__ == '__main__':
    import time
    x = np.log(np.abs(np.random.randn(100)))
    y = np.log(np.abs(np.random.randn(100)))
    z = np.log(np.abs(np.random.randn(100)))
    args = {}
    np.savez('/tmp/'+time.strftime("%Y_%m_%d-%H:%M:%S")+'.npz',\
             args={'infos':'toy example'}, y=y, x=x, z=z,\
             plot="""
fig1, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['x'], bins=20, edgecolor='k', color='lightgray', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig2, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['y'], bins=20, edgecolor='b', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig3, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['z'], bins=20, edgecolor='r', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
fig4, ax = plt.subplots(1, figsize=(5,3))
plt.subplots_adjust(bottom=.25, left=.2)
ax.hist(data['z'], bins=20, edgecolor='r', color='w', lw=2)
set_plot(ax, xlabel='x (units)', ylabel='count')
""")
    
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
    # data = np.load('data.npz')
    # exec(str(data['plot']))
    # plt.show()
