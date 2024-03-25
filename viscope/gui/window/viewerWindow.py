'''
class for live viewing spectral images
'''
#%%
#import napari
#from typing import Annotated, Literal

from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow

#from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt

#import numpy as np

#from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class ViewerWindow(QMainWindow):
    ''' class for the main window'''
    DEFAULT = {'nameGUI':'viewerWindow'}


    def __init__(self, name=DEFAULT['nameGUI'] ):
        super().__init__()
        self.setWindowTitle(name)

        self.dockWidgetParameter = None

        self.show()

    def addParameterGui(self,newGUI,name=DEFAULT['nameGUI']):
        ''' add parameter GUI '''

        dw=QDockWidget('Dockable',self)
        dw.setWindowTitle(name)
        dw.setWidget(newGUI.native)
        self.addDockWidget(Qt.BottomDockWidgetArea,dw)
        # tabify the widget
        if self.dockWidgetParameter is not None:
            self.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
            #self.dockWidgetParameter = dw
        
        return dw

    def addMainGUI(self,newGUI,name=DEFAULT['nameGUI']):
        ''' add main GUI '''
        self.setCentralWidget(newGUI)

