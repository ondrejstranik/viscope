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


class SimpleMicroscopeNA(SimpleMicroscope):
    ''' class to emulate microscope with a diffraction limited PSF '''
    DEFAULT = {'magnification': 20,
                'NA': 0.1}

    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''

        # blur the sample with the diffraction limited PSF
        iFrame = Component.diffractionBlur(iFrame=self.sample.get(),
                NA=self.DEFAULT['NA'])

        # image sample onto camera
        oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera'],
                iFrame= iFrame,iPixelSize=self.sample.pixelSize,
                magnification= self.DEFAULT['magnification'])

        print('virtual Frame updated')

        return oFrame



#%%

if __name__ == '__main__':
    pass


