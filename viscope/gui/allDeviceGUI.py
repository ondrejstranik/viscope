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
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from viscope.instrument.base.baseStage import BaseStage
from viscope.instrument.base.baseLaser import BaseLaser
from viscope.instrument.base.baseSwitch import BaseSwitch
from viscope.instrument.base.baseCamera import BaseCamera

#import numpy as np

class AllDeviceGUI(BaseGUI):
    ''' main class to control all devices'''

    DEFAULT = {}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)


    def setDevice(self,deviceList):

        self.device = deviceList
        
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
            if isinstance(ii,BaseCamera):
                _vWindow = self.viscope.addViewerWindow()
                deviceGUI = CameraGUI(self.viscope,vWindow=_vWindow)
                deviceGUI.setDevice(ii)
                deviceGUI = CameraViewGUI(self.viscope,vWindow=_vWindow)
                deviceGUI.setDevice(ii)


if __name__ == "__main__":
    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
    from viscope.instrument.virtual.virtualCamera import VirtualCamera

    from viscope.main import Viscope

    stage1 = VirtualStage(name='Stage1')
    stage1.connect()
    stage2 = VirtualStage(name='Stage2')
    stage2.connect()
    laser1 = VirtualLaser(name='Laser1')
    laser1.connect()
    switch1 = VirtualSwitch(name='Switch1')
    switch1.connect()
    camera1 = VirtualCamera(name='Camera1')
    camera1.connect()
    camera1.setParameter('threadingNow',True)
    camera2 = VirtualCamera(name='Camera2')
    camera2.connect()
    camera2.setParameter('threadingNow',True)

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([stage1,stage2,laser1,switch1,camera1,camera2])
    viscope.run()

    print('disconnecting')
    stage1.disconnect()
    stage2.disconnect()
    laser1.disconnect()
    switch1.disconnect()
    camera1.disconnect()
    camera2.disconnect()


