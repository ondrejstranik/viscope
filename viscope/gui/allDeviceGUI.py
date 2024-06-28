'''
class for live viewing spectral images
'''
#%%
#import napari
#from magicgui import magicgui
#from typing import Annotated, Literal

from viscope.gui.baseGUI import BaseGUI
from viscope.gui.stageGUI import StageGUI
from viscope.gui.laserGUI import LaserGUI
from viscope.gui.switchGUI import SwitchGUI
from viscope.gui.pumpGUI import PumpGUI
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from viscope.instrument.base.baseStage import BaseStage
from viscope.instrument.base.baseLaser import BaseLaser
from viscope.instrument.base.baseSwitch import BaseSwitch
from viscope.instrument.base.baseCamera import BaseCamera
from viscope.instrument.base.basePump import BasePump



#import numpy as np

class AllDeviceGUI(BaseGUI):
    ''' main class to control all devices'''

    DEFAULT = {}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)


    def setDevice(self,deviceList):

        if type(deviceList) is list:
            self.device = deviceList
        else:
            self.device = [deviceList]


        
        for ii in self.device:
            if isinstance(ii,BaseStage):
                deviceGUI  = StageGUI(self.viscope)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseLaser):
                deviceGUI  = LaserGUI(self.viscope)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseSwitch):
                deviceGUI  = SwitchGUI(self.viscope)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BasePump):
                deviceGUI  = PumpGUI(self.viscope)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseCamera):
                _vWindow = self.viscope.addViewerWindow()
                deviceGUI = CameraGUI(self.viscope,vWindow=_vWindow)
                deviceGUI.setDevice(ii)
                deviceGUI = CameraViewGUI(self.viscope,vWindow=_vWindow)
                deviceGUI.setDevice(ii)


if __name__ == "__main__":
    pass

#%%