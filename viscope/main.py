'''
class for live viewing spectral images
'''
#%%
#import napari
#from typing import Annotated, Literal

import sys
from qtpy.QtWidgets import QApplication, QMainWindow
from viscope.gui.window.viewerWindow import ViewerWindow


#from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
#from qtpy.QtCore import Qt

#import numpy as np

#from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class Viscope():
    ''' base top class for control'''

    DEFAULT = {'nameGUI': 'viscope'}

    def __init__(self, **kwargs ):
        ''' initialise the class '''

        self.app = QApplication([])
        self.app.aboutToQuit.connect(lambda : print('Viscope is closed'))

        self.vWindow = ViewerWindow(name=Viscope.DEFAULT['nameGUI'],topWindow=True)
        self.vWindow.sigClose.connect(self.closeAllWindow)

        self.vWindowList = [self.vWindow]

        self.GUIList = []

    def addViewerWindow(self, name=None):
        ''' adding additional window '''
        newViewerWindow = ViewerWindow(name=name)
        self.vWindowList.append(newViewerWindow)
        return newViewerWindow

    def closeAllWindow(self):
        ''' close all vWindow '''
        for vWindow in self.vWindowList:
            #print(f'closing window {vWindow}')
            vWindow.close()

    def run(self):
        ''' start the gui viewer'''
        # start napari main gui
        print('starting main viscope loop')
        self.app.exec()

if __name__ == "__main__":

        viscope = Viscope()


        viscope.run()

