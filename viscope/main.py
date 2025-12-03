'''
class for live viewing spectral images
'''
#%%

import sys
from qtpy.QtWidgets import QApplication, QMainWindow
from viscope.gui.window.viewerWindow import ViewerWindow, WindowManager

from pathlib import Path

class VISCOPE():
    ''' base top class for control'''

    DEFAULT = {'nameGUI': 'viscope',
                'dataFolder': 'DATA'}

    def __init__(self, **kwargs ):
        ''' initialise the class '''

        self.app = QApplication([])
        self.app.aboutToQuit.connect(lambda : print('Viscope is closed'))

        self.wManager = WindowManager()

        name= kwargs['name'] if 'name' in kwargs else VISCOPE.DEFAULT['nameGUI'] 
        # vWindow ...this is the main Window of Viscope
        self.vWindow = ViewerWindow(name=name)
        self.wManager.register(self.vWindow)

        self.GUIList = []
        
        self.dataFolder = str(Path(__file__).parent.joinpath(self.DEFAULT['dataFolder']))


    def addViewerWindow(self, name=None):
        ''' adding additional window '''
        newViewerWindow = ViewerWindow(name=name)
        self.wManager.register(newViewerWindow)
        return newViewerWindow

    def run(self):
        # in the case that napari is used, then it rewrite the self.app
        # causing the at close it run gracefull exit, closing all the threads.
        # this is not consistent with the case napari is not run.
        # therefore, the self.app is initiated again.
        self.app = QApplication([])
        ''' start the gui viewer'''
        # start main event loop
        print('starting main viscope loop')
        self.app.exec()

viscope = VISCOPE()

