'''
class for live viewing spectral images
'''
#%%
#import napari
from magicgui import magicgui
#from typing import Annotated, Literal

#from qtpy.QtWidgets import QLabel, QSizePolicy
#from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI
from timeit import default_timer as timer
from viscope.gui.napariViewer.napariViewer import NapariViewer
import numpy as np


class CameraViewGUI(BaseGUI):
    ''' main class to show images of a camera'''

    DEFAULT = {'nameLayer': 'Camera',
               'nameGUI': 'Camera'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.rawLayer = None

        # prepare the gui of the class
        CameraViewGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # create napari viewer
        self.viewer = NapariViewer(show=False)
        # napari can not work in a dock Window,
        # therefore it must run in the main Window
        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

        # set new napari layer
        self.rawLayer = self.viewer.add_image(np.ones((2,2)),
                        rgb=False, colormap="gray",
                        name='Raw',  blending='additive')

    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)
        self.vWindow.setWindowTitle(self.device.name)


    def updateGui(self):
        ''' update the data in gui '''
        # napari
        try:
            self.rawLayer.data = self.device.rawImage
        except Exception as e:
            print(f'error in updateGui in cameraViewGUI: {e}')


if __name__ == "__main__":
    pass


