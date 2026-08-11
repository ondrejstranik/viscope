'''
class for live viewing spectral images
'''
#%%
#import napari
from magicgui import magicgui
from typing import Annotated, Literal

from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

from timeit import default_timer as timer
from viscope.gui.napariViewer.napariViewer import NapariViewer

import numpy as np

class NapariGUI(BaseGUI):

    ''' main class to show napari viewer'''

    DEFAULT = {'nameGUI': 'Napari'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # prepare the gui of the class
        NapariGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        self.viewer = NapariViewer(show=False)

        # napari can not work in a dock Window,
        # therefore it must run in the main Window
        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])


if __name__ == "__main__":
    pass



