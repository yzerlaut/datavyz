###################################################################
#                                                                 #
#                     PLOTTING A LIVE GRAPH                       #
#                  ----------------------------                   #
#            EMBED A MATPLOTLIB ANIMATION INSIDE YOUR             #
#            OWN GUI!                                             #
#                                                                 #
###################################################################


import sys
import os
from datavyz.yQt5 import QtGui, QtWidgets, QtCore
import functools
import numpy as np
import random as rd
import matplotlib
matplotlib.use("Qt5Agg")
from datavyz.atplotlib.figure import Figure
from datavyz.atplotlib.animation import TimedAnimation
from datavyz.atplotlib.lines import Line2D
from datavyz.atplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from datavyz.my_graph import set_plot


def setCustomSize(x, width, height):
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(x.sizePolicy().hasHeightForWidth())
    x.setSizePolicy(sizePolicy)
    x.setMinimumSize(QtCore.QSize(width, height))
    x.setMaximumSize(QtCore.QSize(width, height))


class CustomMainWindow(QtWidgets.QMainWindow):

    def __init__(self, data, speed, dx, xlim, x_bar, x_units):

        super(CustomMainWindow, self).__init__()

        # Define the geometry of the main window
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Time-Varying plot")

        # Create FRAME_A
        self.FRAME_A = QtWidgets.QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(210,210,235,255).name())
        self.LAYOUT_A = QtWidgets.QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)

        # Place the zoom button
        self.zoomBtn = QtWidgets.QPushButton(text = 'zoom')
        setCustomSize(self.zoomBtn, 100, 50)
        self.zoomBtn.clicked.connect(self.zoomBtnAction)
        self.LAYOUT_A.addWidget(self.zoomBtn, *(0,1))
        
        # Place the matplotlib figure
        self.myFig = CustomFigCanvas(data, dx, xlim, x_bar, x_units)
        self.LAYOUT_A.addWidget(self.myFig, *(0,0))

        # Add the callbackfunc to ..
        myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (self.addData_callbackFunc,data,speed))
        myDataLoop.start()

        self.show()

    ''''''


    def zoomBtnAction(self):
        print("zoom in")
        self.myFig.zoomIn(5)

    ''''''

    def addData_callbackFunc(self, value):
        # print("Add data: " + str(value))
        self.myFig.addData(value)



''' End Class '''


class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self, data, dx, xlim, x_bar, x_units):

        self.addedData = []
        print(matplotlib.__version__)
        y0, y1 = data.min(), data.max()
        
        # The data
        self.xlim = min([len(data), int(xlim/dx)])
        self.n = np.linspace(0, self.xlim-1, self.xlim)
        self.y = (self.n * 0.0) + data.mean()

        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.fig.subplots_adjust(bottom=.05, left=.1)
        self.ax1 = self.fig.add_subplot(111)

        # self.ax1 settings
        bar_lim = min([int(x_bar/dx),int(3.*self.xlim/5)])
        self.xbar = self.ax1.plot([int(self.xlim/5), bar_lim+int(self.xlim/5)],\
                                  np.ones(2)*(y0+.1*(y1-y0)), 'k-', lw=5)
        self.ax1.plot([0, self.xlim-1],[y0,y1], 'w.', ms=1e-4)
        self.xbar_legend = self.ax1.annotate(str(int(x_bar))+x_units,\
                                             (int(self.xlim/5),y0))
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)

        set_plot(self.ax1, ['left'], xlim=[0, self.xlim - 1], xticks=[]) 
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])

    def addData(self, value):
        self.addedData.append(value)

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        
    def zoomOut(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]


''' End Class '''


# You need to setup a signal slot mechanism, to 
# send data to your GUI in a thread-safe way.
# Believe me, if you don't do this right, things
# go very very wrong..
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal(float)

''' End Class '''


def dataSendLoop(addData_callbackFunc, data=None, speed=0.1):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    if data is None:
        print('missing data ...')
        # Simulate some data
    i=0
    while i<len(data):
        time.sleep(speed)
        mySrc.data_signal.emit(data[i]) # <- Here you emit a signal!
        i += 1
    ###
###



if __name__== '__main__':

    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ 
     A movie plot of a time trace
     """
    ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s',"--speed",help="speed for the defilment",type=float,default=5)
    parser.add_argument('-xb',"--x_bar",help="bar for x-axis", type=float, default=20)
    parser.add_argument('-xu',"--x_units",help="units for x-axis", default='ms')
    parser.add_argument('-xl',"--x_lim",help="limits for x-axis", type=float, default=1000)
    parser.add_argument("--dx",help="units for x-axis", type=float, default=1e-1)
    parser.add_argument("--ylim",help="ylimits", nargs=2, type=float, default=[-1e9,1e9])
    parser.add_argument("--xzoom",help="zoom over x-axis", nargs=2,\
                        type=float, default=[0,1e9])
    parser.add_argument("-f", "--filename", help="filename")
    parser.add_argument("--key", help="key within the datafile", default='vm')
    args = parser.parse_args()
    
    if args.filename is not None:
        # means we have passed a datafile
        data = np.load(args.filename)
        y = data[args.key]
        y = y[max([int(args.xzoom[0]/args.dx),0]):min([int(args.xzoom[1]/args.dx),len(y)])]
        y[y<args.ylim[0]]= args.ylim[0]
        y[y>args.ylim[1]] = args.ylim[1]
    else:
        x = np.linspace(0, 499, 500)
        y = 50 + 25*(np.sin(x / 8.3)) + 10*(np.sin(x / 7.5)) - 5*(np.sin(x / 1.5))

    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow(y, args.speed/1e3, args.dx, args.x_lim, args.x_bar, args.x_units)
    sys.exit(app.exec_())

''''''
