'''
class for live viewing spectral images
'''
#%%
import napari
#from typing import Annotated, Literal

import sys
from qtpy.QtWidgets import QApplication, QMainWindow


#from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt

#import numpy as np

#from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class ViewerWindow():
    ''' class for the main window'''
    def __init__(self,napariViewer= False):
        
        if napariViewer:
            self.viewer = napari.Viewer()
        else:
            self.viewer = QMainWindow()
            self.viewer.show()
        
        self.dockWidgetParameter = None


class BaseMain():
    ''' base top class for control'''

    DEFAULT = {'nameGUI': 'baseGUI',
                'napariViewer': False}

    def __init__(self, napariViewer= DEFAULT['napariViewer'], **kwargs ):
        ''' initialise the class '''

        self.app = QApplication([])

        self.vWindow = ViewerWindow(napariViewer)

        self.vWindowList = [self.vWindow]

        self.GUIList = []

    def addViewerWindow(self,napariViewer= DEFAULT['napariViewer']):
        ''' adding additional window '''
        newViewerWindow = ViewerWindow(napariViewer)
        self.vWindowList.append(newViewerWindow)
        return newViewerWindow

    def run(self):
        ''' start the gui viewer'''
        # start napari main gui
        self.app.exec()


if __name__ == "__main__":

        base = BaseMain()
        print('starting main event loop')

        base.run()

