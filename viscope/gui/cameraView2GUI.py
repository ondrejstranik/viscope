'''
class for live viewing spectral images
'''
#%%
#import napari
from magicgui import magicgui
#from typing import Annotated, Literal

import pyqtgraph as pg

#from qtpy.QtWidgets import QLabel, QSizePolicy
#from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI
from timeit import default_timer as timer
from viscope.gui.napariViewer.napariViewer import NapariViewer
import numpy as np


class CameraView2GUI(BaseGUI):
    ''' main class to show images of a camera,
    uses pyqtgraph's imageView'''

    DEFAULT = {'nameLayer': 'Camera',
               'nameGUI': 'Camera'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # prepare the gui of the class
        CameraView2GUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # add graph
        self.viewer = pg.ImageView()
        self.vWindow.addMainGUI(self.viewer, name=self.DEFAULT['nameGUI'])

    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)
        self.vWindow.setWindowTitle(self.device.name)


    def updateGui(self):
        ''' update the data in gui '''
        # napari
        try:
            self.viewer.setImage(self.device.rawImage.T,
                                    autoRange=False,
                                    autoLevels=True)
        except Exception as e:
            print(f'error in updateGui in cameraView2GUI: {e}')


if __name__ == "__main__":
    pass


