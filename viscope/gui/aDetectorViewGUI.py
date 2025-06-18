'''
module for live viewing of data from aDetector
'''
#%%
from magicgui import magicgui

import pyqtgraph as pg
from PyQt5.QtGui import QColor, QPen
from qtpy.QtWidgets import QLabel, QSizePolicy,QWidget, QApplication, QVBoxLayout
from qtpy.QtCore import Qt

from viscope.gui.baseGUI import BaseGUI

#from timeit import default_timer as timer

import numpy as np


class ADetectorViewGUI(BaseGUI):
    ''' main class to show data from A Detector'''

    DEFAULT = {'nameGUI': 'ADetector'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.graph = None

        # prepare the gui of the class
        ADetectorViewGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # add graph
        self.graph = pg.plot()
        self.graph.setTitle(f'Signal')
        styles = {'color':'r', 'font-size':'20px'}
        self.graph.setLabel('left', 'Signal', units='ul/min')
        self.graph.setLabel('bottom', 'time', units= 's')

        #layout = QVBoxLayout()
        #layout.addWidget(self.graph)
        #self.setLayout(layout)  

        self.vWindow.addMainGUI(self.graph, name=self.DEFAULT['nameGUI'])



    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)
        self.vWindow.setWindowTitle(self.device.name)

    def drawGraph(self):
            ''' draw all new lines in the spectraGraph '''

            # if there is no signal then do not continue
            if self.device.signal is None:
                return

            # remove all lines
            self.graph.clear()

            # draw line
            mypen = QPen()
            mypen.setWidth(0)
            lineplot = self.graph.plot()
            lineplot.setData(self.device.time, self.device.time)


    def updateGui(self):
        ''' update the data in gui '''
        #draw all new lines in the spectraGraph
        self.drawGraph()

if __name__ == "__main__":
    pass


