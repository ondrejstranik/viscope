'''
class for live viewing spectral images
'''
#%%
import napari
from typing import Annotated, Literal

import sys
from qtpy.QtWidgets import QApplication, QMainWindow

from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt

import numpy as np

from napari.qt.threading import create_worker
from viscope.instrument.base.baseInstrument import ThreadFlag

from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class BaseGUI():
    ''' base class for all GUI'''

    DEFAULT = {'nameGUI': 'baseGUI',
                'threading': False}

    def __init__(self, viscope, vWindow, threading = None, **kwargs ):
        ''' initialise the class '''

        self.viscope = viscope
        self.vWindow = vWindow

        self.flagLoop = ThreadFlag()
        self.worker = None

        if threading is not None:
            self._setWorker(threading) 
        else:
            self._setWorker(BaseGUI.DEFAULT['threading'])

         # prepare the gui of the class
        BaseGUI.__setWidget(self)

    def addParameterGui(self,newGUI,name=DEFAULT['nameGUI']):
        ''' add parameter GUI '''

        if isinstance(self.vWindow.viewer,napari.Viewer):
            dw = self.vWindow.viewer.window.add_dock_widget(newGUI, name = name, area= 'bottom')
            # tabify the widget
            if self.vWindow.dockWidgetParameter is not None:
                self.vWindow.viewer.window._qt_window.tabifyDockWidget(self.vWindow.dockWidgetParameter,dw)
                print(f'instance {self} has dockWidgetParameter')
            else:
                print(f'instance {self} DOES NOT has dockWidgetParameter')

            self.vWindow.dockWidgetParameter = dw
            #self.dockWidgetParameter = dw
            self.vWindow.viewer.window._qt_window.resizeDocks([dw], [100], Qt.Vertical)
        else:
            dw=QDockWidget('Dockable',self.vWindow.viewer)
            dw.setWindowTitle(name)
            dw.setWidget(newGUI.native)
            self.vWindow.viewer.addDockWidget(Qt.BottomDockWidgetArea,dw)
            # tabify the widget
            if self.vWindow.dockWidgetParameter is not None:
                self.vWindow.viewer.tabifyDockWidget(self.vWindow.dockWidgetParameter,dw)
            self.vWindow.dockWidgetParameter = dw
            #self.dockWidgetParameter = dw

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
        from viscope.main.baseMain import BaseMain

        viscope = BaseMain()
                
        base = BaseGUI(viscope,viscope.vWindow)
        print('starting main event loop')

        viscope.run()

