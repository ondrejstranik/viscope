'''
module for live viewing of histogram from Camera
'''
#%%
from magicgui import magicgui

import pyqtgraph as pg
from PyQt5.QtGui import QColor, QPen
from qtpy.QtWidgets import QLabel, QSizePolicy,QWidget, QApplication, QVBoxLayout
from qtpy.QtCore import Qt

from viscope.gui.baseGUI import BaseGUI

from viscope.instrument.base.baseCamera import BaseCamera


#from timeit import default_timer as timer

import numpy as np


class HistogramGUI(BaseGUI):
    ''' main class to show histogram of data'''

    DEFAULT = {'nameGUI': 'histogram'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # graph widget
        self.graph = None
        self.histLine = None

        # data
        self.data = None
        self.y = None
        self.x = None

        # prepare the gui of the class
        HistogramGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # add graph
        self.graph = pg.PlotWidget()
        self.graph.setTitle(f'Signal')
        self.graph.setLabel('left', '#')
        self.graph.setLabel('bottom', 'value')
        self.graph.setLogMode(y=True)
        self.histLine = self.graph.plot(stepMode=True, fillLevel=0)

        self.vWindow.addParameterGui(self.graph,name=self.DEFAULT['nameGUI'])
        #self.vWindow.addMainGUI(self.graph, name=self.DEFAULT['nameGUI'])

    def setDevice(self,device):
        super().setDevice(device)

        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)

    def drawGraph(self):
        ''' draw histogram in graph widget'''

        # if there is no signal then do not continue
        if self.data is None:
            return

        self.histLine.setData(self.x, self.y)

    def calculateHistogram(self):
        '''' calculate the histogram '''
        self.y , self.x = np.histogram(self.data, bins=50)         


    def updateGui(self):
        ''' update the data in gui '''

        if isinstance(self.device, BaseCamera):
             self.data = self.device.rawImage[:]
        self.calculateHistogram()
        self.drawGraph()

if __name__ == "__main__":
    pass


