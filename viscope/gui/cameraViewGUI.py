'''
class for live viewing spectral images
'''
#%%
import napari
from magicgui import magicgui
from typing import Annotated, Literal

from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

from timeit import default_timer as timer

import numpy as np

class CameraViewGUI(BaseGUI):
    ''' main class to show images of a camera'''

    DEFAULT = {'nameLayer': 'Camera'}


    def __init__(self, viscope, vWindow, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, vWindow, **kwargs)

        
        self.lastUpdateTime = timer()
        self.guiUpdateTime = 0.03

        # prepare the gui of the class
        CameraViewGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # set new napari layer
        self.rawLayer = self.vWindow.viewer.add_image(np.ones((2,2)),
                        rgb=False, colormap="gray",
                        name='Raw',  blending='additive')

    def guiUpdateTimed(self):
        ''' update gui according the update time '''
        timeNow = timer()
        if (timeNow -self.lastUpdateTime) > self.guiUpdateTime:
            self.updateGui()
            self.lastUpdateTime = timeNow    

    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)

    def updateGui(self):
        ''' update the data in gui '''
        # napari
        self.rawLayer.data = self.device.rawImage


if __name__ == "__main__":
        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.main.baseMain import BaseMain

        print('starting  camera')
        camera = VirtualCamera()
        camera.connect()
        camera.setParameter('threadingNow',True)

        print('starting main event loop')
        viscope = BaseMain(True)
        newGUI  = CameraViewGUI(viscope,viscope.vWindow)
        newGUI.setDevice(camera)
        viscope.run()

        camera.disconnect()


