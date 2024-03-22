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
from viscope.gui.stageGUI import StageGUI
from viscope.gui.laserGUI import LaserGUI
from viscope.gui.switchGUI import SwitchGUI
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from viscope.instrument.base.baseStage import BaseStage
from viscope.instrument.base.baseLaser import BaseLaser
from viscope.instrument.base.baseSwitch import BaseSwitch
from viscope.instrument.base.baseCamera import BaseCamera


import numpy as np

class AllDeviceGUI(BaseGUI):
    ''' main class to control all devices'''

    DEFAULT = {}


    def __init__(self, viscope, vWindow, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, vWindow, **kwargs)



    def setDevice(self,deviceList):

        self.device = deviceList
        
        for ii in self.device:
            if isinstance(ii,BaseStage):
                deviceGUI  = StageGUI(self.viscope,self.vWindow)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseLaser):
                deviceGUI  = LaserGUI(self.viscope,self.vWindow)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseSwitch):
                deviceGUI  = SwitchGUI(self.viscope,self.vWindow)
                deviceGUI.setDevice(ii)
            if isinstance(ii,BaseCamera):
                deviceGUI = CameraGUI(self.viscope,self.vWindow)
                deviceGUI.setDevice(ii)
                _vWindow = self.viscope.addViewerWindow(napariViewer=True)
                deviceGUI = CameraViewGUI(self.viscope,_vWindow)
                deviceGUI.setDevice(ii)



if __name__ == "__main__":
    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
    from viscope.instrument.virtual.virtualCamera import VirtualCamera

    from viscope.main.baseMain import BaseMain

    print('starting stage 1')
    stage1 = VirtualStage()
    stage1.connect()

    print('starting stage 2')
    stage2 = VirtualStage()
    stage2.connect()

    print('starting laser 1')
    laser1 = VirtualLaser()
    laser1.connect()

    print('starting switch 1')
    switch1 = VirtualSwitch()
    switch1.connect()

    print('starting camera 1')
    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    print('starting camera 2')
    camera2 = VirtualCamera()
    camera2.connect()
    camera2.setParameter('threadingNow',True)

    print('starting main event loop')
    viscope = BaseMain()
    viewer  = AllDeviceGUI(viscope,viscope.vWindow)
    viewer.setDevice([stage1,stage2,laser1,switch1,camera1,camera2])
    
    viscope.run()

    print('disconnecting')
    stage1.disconnect()
    stage2.disconnect()
    laser1.disconnect()
    switch1.disconnect()
    camera1.disconnect()


