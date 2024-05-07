'''
class for live viewing spectral images
'''
#%%
import napari
from typing import Annotated, Literal

import sys
from qtpy.QtWidgets import QApplication, QMainWindow

from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt, QObject

import numpy as np

from napari.qt.threading import create_worker
from viscope.instrument.base.baseInstrument import ThreadFlag

from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class BaseGUI(QObject):
#class BaseGUI():
    ''' base class for all GUI'''

    DEFAULT = {'nameGUI': 'baseGUI',
                'threading': False}

    def __init__(self, viscope, vWindow=None, threading = None, **kwargs ):
        ''' initialise the class '''
        super().__init__()


        self.viscope = viscope
        
        # if not specific window than set the window to the main window of viscope 
        self.vWindow = vWindow if vWindow is not None else viscope.vWindow 

        self.flagLoop = ThreadFlag()
        self.worker = None

        if threading is not None:
            self._setWorker(threading) 
        else:
            self._setWorker(BaseGUI.DEFAULT['threading'])

         # prepare the gui of the class
        BaseGUI.__setWidget(self)

    def __setWidget(self):
        ''' prepare the gui '''
        self.viscope.GUIList.append(self)

    def setDevice(self,device):
        self.device = device

    def _setWorker(self,value:bool):
        ''' set the worker for the base gui '''
        self.worker = create_worker(self.loop) if value else None

    def loop(self):
        ''' base threading loop of the data processing '''
        while True:
            print('output from BaseGUI thread loop')
            self.flagLoop.set('output')
            yield  
            time.sleep(1)


if __name__ == "__main__":
    pass

