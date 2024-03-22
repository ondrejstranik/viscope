'''
class for live viewing spectral images
'''
#%%
#import napari
from magicgui import magicgui
from typing import Annotated, Literal

#from qtpy.QtWidgets import QLabel, QSizePolicy
#from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

#import numpy as np

class CameraGUI(BaseGUI):
    ''' main class to control camera'''

    DEFAULT = {'nameGUI': 'Camera'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterCameraGui = None

        # prepare the gui of the class
        CameraGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui()
        def parameterCameraGui(
            exposure: Annotated[int, {'widget_type': "Slider", 'max': 10000, 'label':'exposure [ms]'}] = None,
            numberOfAverage: int  = None
            ):

            self.device.setParameter("exposureTime", exposure)
            self.device.setParameter("nFrame", numberOfAverage)

        # add widget parameterCameraGui 
        self.parameterCameraGui = parameterCameraGui
        self.addParameterGui(self.parameterCameraGui,name=self.DEFAULT['nameGUI'])

    def setDevice(self,device):
        ''' set the stage '''
        super().setDevice(device)

        self.parameterCameraGui.exposure.value = int(self.device.getParameter('exposureTime'))
        self.parameterCameraGui.numberOfAverage.value = int(self.device.getParameter('nFrame'))

if __name__ == "__main__":
        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.main.baseMain import BaseMain

        print('starting stage')
        camera = VirtualCamera()
        camera.connect()

        print('starting main event loop')
        viscope = BaseMain()
        newGUI  = CameraGUI(viscope)
        newGUI.setDevice(camera)
        viscope.run()

        camera.disconnect()


