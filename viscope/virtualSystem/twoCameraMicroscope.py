"""
virtual basic microscope

components: camera
sample: default image of astronaout

@author: ostranik
"""
#%%

import time
import numpy as np
#from qtpy.QtCore import QObject, Signal
#from skimage import data
#from skimage.transform import resize, rescale

#from napari.qt.threading import create_worker

#from viscope.instrument.base.baseInstrument import ThreadFlag

from viscope.virtualSystem.base.baseSystem import BaseSystem
from viscope.virtualSystem.component.component import Component

class TwoCameraMicroscope(BaseSystem):
    ''' class to emulate microscope '''
    DEFAULT = {'magnification1': 1,
               'magnification2': 3}
               
    
    def __init__(self,*args, **kwargs):
        ''' initialisation '''
        super(TwoCameraMicroscope,self).__init__(*args, **kwargs)

    def setVirtualDevice(self,camera1=None,camera2=None,
                        stage=None,switch=None,laser=None):
        ''' set instruments of the microscope '''

        self.device['camera1'] = camera1
        self.device['camera2'] = camera2
        self.device['stage'] = stage
        self.device['switch'] = switch
        self.device['laser'] = laser

    def calculateVirtualFrame(self,cameraNumber):
        ''' update the virtual Frame of the camera '''

        # 0. laser
        oFrame = Component.laserIllumination(self.sample.get(),self.device['laser'])

        # 1. stage
        samplePosition = self.sample.position + self.device['stage'].position
        samplePositionXY = samplePosition[0:2]

        # camera 1 
        if cameraNumber ==1:
            oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera1'],
                    iFrame= oFrame,iPixelSize=self.sample.pixelSize,
                    iFramePosition = samplePositionXY,
                    magnification= self.DEFAULT['magnification1'])
            # switch
            if self.device['switch'].getParameter('position') ==1:
                oFrame /= 2
            if self.device['switch'].getParameter('position') ==2:
                oFrame *= 0
            print(f'virtual Frame of camera - {self.device["camera1"].name}  - updated')
            return oFrame

        # camera 2 
        if cameraNumber ==2:
            oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera2'],
                    iFrame= oFrame,iPixelSize=self.sample.pixelSize,
                    iFramePosition = samplePositionXY,
                    magnification= self.DEFAULT['magnification2'])
            # switch
            if self.device['switch'].getParameter('position') ==1:
                oFrame /= 2
            if self.device['switch'].getParameter('position') ==0:
                oFrame *= 0
            print(f'virtual Frame of camera - {self.device["camera2"].name}  - updated')
            return oFrame

    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield
            if self.deviceParameterIsChanged():            
                print(f'calculate virtual frame')
                self.device['camera1'].virtualFrame = self.calculateVirtualFrame(1)
                self.device['camera2'].virtualFrame = self.calculateVirtualFrame(2)
                self.deviceParameterFlagClear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI


    camera1 = VirtualCamera('camera1')
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    camera2 = VirtualCamera('camera2')
    camera2.connect()
    camera2.setParameter('threadingNow',True)

    stage = VirtualStage('stage')
    stage.connect()

    laser = VirtualLaser('laser')
    laser.connect()
    laser.setParameter("power",1)
    laser.setParameter("keySwitch",True)

    switch = VirtualSwitch('switch')
    switch.setParameter('positionList',['up', 'middle', 'down'])
    switch.connect(initialPosition=1)

    vM = TwoCameraMicroscope()
    vM.setVirtualDevice(camera1=camera1, camera2=camera2, laser= laser,
    switch= switch, stage=stage)
    vM.connect()

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1,camera2,laser,switch,stage])
    
    viscope.run()

    camera1.disconnect()
    camera2.disconnect()
    laser.disconnect()
    stage.disconnect()
    switch.disconnect()        

    vM.disconnect()


