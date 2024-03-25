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

import numpy as np

from viscope.gui.napariGUI import NapariGUI

class CameraViewGUI(BaseGUI):
    ''' main class to show images of a camera'''

    DEFAULT = {'nameLayer': 'Camera'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        
        self.lastUpdateTime = timer()
        self.guiUpdateTime = 0.03


        # prepare the gui of the class
        CameraViewGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # create napari viewer
        newGUI  = NapariGUI(self.viscope,vWindow=self.vWindow)
        self.viewer = newGUI.viewer

        # set new napari layer
        self.rawLayer = self.viewer.add_image(np.ones((2,2)),
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
        self.vWindow.setWindowTitle(self.device.name)


    def updateGui(self):
        ''' update the data in gui '''
        # napari
        self.rawLayer.data = self.device.rawImage


if __name__ == "__main__":
        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.main import Viscope

        camera = VirtualCamera(name='camera1')
        camera.connect()
        camera.setParameter('threadingNow',True)

        viscope = Viscope()
        newGUI  = CameraViewGUI(viscope)
        newGUI.setDevice(camera)
        viscope.run()

        camera.disconnect()


