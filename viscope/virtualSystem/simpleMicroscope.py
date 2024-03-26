"""
virtual basic microscope

components: camera

@author: ostranik
"""
#%%

import time

from viscope.virtualSystem.base.baseSystem import BaseSystem
from viscope.virtualSystem.component.component import Component


class SimpleMicroscope(BaseSystem):
    ''' class to emulate microscope '''
    DEFAULT = {'magnification': 1}
               
    
    def __init__(self,*args, **kwargs):
        ''' initialisation '''
        super(SimpleMicroscope,self).__init__(*args, **kwargs)

    def setVirtualDevice(self,camera=None):
        ''' set instruments of the microscope '''
        self.device['camera'] = camera

    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''

        # image sample onto camera
        oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera'],
                iFrame= self.sample.get(),iPixelSize=self.sample.pixelSize,
                magnification= self.DEFAULT['magnification'])

        print('virtual Frame updated')

        return oFrame


    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield 
            if self.deviceParameterIsChanged():
                print(f'calculate virtual frame')
                self.device['camera'].virtualFrame = self.calculateVirtualFrame()
                self.deviceParameterFlagClear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    vM = SimpleMicroscope()
    vM.setVirtualDevice(camera1)
    vM.connect()

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1])
    
    viscope.run()

    camera1.disconnect()
    vM.disconnect()


