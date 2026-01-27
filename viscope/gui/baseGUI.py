'''
class for live viewing spectral images
'''
#%%
#import napari
#from typing import Annotated, Literal

#import sys
#from qtpy.QtWidgets import QApplication, QMainWindow

#from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt, QObject
from qtpy.QtWidgets import QWidget

#import numpy as np

from napari.qt.threading import create_worker
from viscope.instrument.base.baseInstrument import ThreadFlag

#from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

from timeit import default_timer as timer


class BaseGUI(QObject):
    ''' base class for all GUI. It is inherited from QObject, so that it can generate Signals'''

    DEFAULT = {'nameGUI': 'baseGUI',
                'guiUpdateTime': 0.03, # [s]
                # restrict update time of the gui in the stream of new data
                #'threading': False}
    }

    def __init__(self, viscope, vWindow=None, threading = None, **kwargs ):
        ''' initialise the class '''
        super().__init__()

        self.viscope = viscope

        self.lastUpdateTime = timer()
        self.guiUpdateTime = BaseGUI.DEFAULT['guiUpdateTime']

        # set new Window 
        if vWindow == 'new':
            vWindow = self.viscope.addViewerWindow()

        # if not specific window than set the window to the main window of viscope 
        self.vWindow = vWindow if vWindow is not None else viscope.vWindow 

        #self.flagLoop = ThreadFlag()
        #self.worker = None

        #if threading is not None:
        #    self._setWorker(threading) 
        #else:
        #    self._setWorker(BaseGUI.DEFAULT['threading'])

         # prepare the gui of the class
        BaseGUI.__setWidget(self)

    def __setWidget(self):
        ''' prepare the gui '''
        self.viscope.GUIList.append(self)

    def setDevice(self,device):
        self.device = device
        self.vWindow.setWindowTitle(self.device.name)

    #def _setWorker(self,value:bool):
    #    ''' set the worker for the base gui '''
    #    self.worker = create_worker(self.loop) if value else None

    #def loop(self):
    #    ''' base threading loop of the data processing '''
    #    while True:
    #        print('output from BaseGUI thread loop')
    #        self.flagLoop.set('output')
    #        yield  
    #        time.sleep(1)

    def guiUpdateTimed(self,newData=True):
        ''' update gui according the update time 
        connect with corresponding yield of the device '''

        timeNow = timer()
        if newData and ((timeNow -self.lastUpdateTime) > self.guiUpdateTime):
            self.updateGui()
            self.lastUpdateTime = timeNow

        #if newData:
        #    print('newDataArrived') 

    def updateGui(self):
        ''' update the data in gui '''
        pass 


if __name__ == "__main__":
    pass

