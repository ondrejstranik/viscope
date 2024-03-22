"""
virtual basic microscope

components: camera
sample: default image of astronaout

@author: ostranik
"""
#%%

import time
import numpy as np
from qtpy.QtCore import QObject, Signal
from skimage import data
from skimage.transform import resize, rescale

from napari.qt.threading import create_worker

from viscope.instrument.base.baseInstrument import ThreadFlag

from viscope.virtualDevice.baseVirtualMicroscope import BaseVirtualMicroscope


class virtualMicroscope(BaseVirtualMicroscope):
    ''' class to emulate microscope '''
    DEFAULT = {'photonRateMax':1e6,
                'samplePixelSize':1, # um
                'samplePositionXYZ': [0,0,0], #um
                'magnification1': 1,
                'magnification2': 3,
                'sampleSize': (200,400)} # pixels
    
    def __init__(self,*args, **kwargs):
        ''' initialisation '''
        super(virtualMicroscope,self).__init__(*args, **kwargs)

        self.sample = None
        self.camera1 = None
        self.camera2 = None
        self.stage = None
        self.switch = None
        self.laser = laser


    def _mapImageToImage(self, destination,source,sourceOffset):
        ''' map 2D array to 2D array of different sizes with some offsets (Y,X)
        for 3D array the shape[0] (first axis) is the spectral dimension'''

        # rename and 
        # move spectral axis to the last axis for 3D array 
        if (destination.ndim ==3) and (source.ndim ==3):
            vFrame = np.moveaxis(destination,0,-1)
            sFrame = np.moveaxis(source,0,-1)
        else:
            vFrame = destination
            sFrame = source

        samplePositionXY =  sourceOffset

        sampleInsideFOV = True

        topLeft = [0,0]
        topLeftSample = [0,0]
        if (samplePositionXY[0]>0) and (samplePositionXY[0]<vFrame.shape[0]):
            topLeft[0] = samplePositionXY[0]
        if samplePositionXY[0]< 0:
            topLeftSample[0] = - samplePositionXY[0]
        if samplePositionXY[0]>vFrame.shape[0]:
            sampleInsideFOV = False
        if (samplePositionXY[1]>0) and (samplePositionXY[1]<vFrame.shape[1]):
            topLeft[1] = samplePositionXY[1]
        if samplePositionXY[1]< 0:
            topLeftSample[1] = - samplePositionXY[1]
        if samplePositionXY[1]>vFrame.shape[1]:
            sampleInsideFOV = False

        # bottom right  conner
        bottomRight = [vFrame.shape[0],vFrame.shape[1]]
        bottomRightSample = [sFrame.shape[0],sFrame.shape[1]]
        if ((samplePositionXY[0] + sFrame.shape[0]>0) and 
            (samplePositionXY[0]+ sFrame.shape[0]<vFrame.shape[0])):
            bottomRight[0] = samplePositionXY[0] + sFrame.shape[0]
        if samplePositionXY[0] + sFrame.shape[0] > vFrame.shape[0]:
            bottomRightSample[0] = -(samplePositionXY[0] + sFrame.shape[0] - vFrame.shape[0])
        if samplePositionXY[0] + sFrame.shape[0] <0:
            sampleInsideFOV = False
        if ((samplePositionXY[1] + sFrame.shape[1]>0) and 
            (samplePositionXY[1]+ sFrame.shape[1]<vFrame.shape[1])):
            bottomRight[1] = samplePositionXY[1] + sFrame.shape[1]
        if samplePositionXY[1] + sFrame.shape[1] > vFrame.shape[1]:
            bottomRightSample[1] = -(samplePositionXY[1] + sFrame.shape[1] - vFrame.shape[1])
        if samplePositionXY[1] + sFrame.shape[1] <0:
            sampleInsideFOV = False

        # set FOV
        print(f'sampleInsideFOV {sampleInsideFOV}')
        print(f'topLeft = {topLeft}')
        print(f'bottomRight = {bottomRight}')
        print(f'topLeftSample = {topLeftSample}')
        print(f'bottomRightSample = {bottomRightSample}')

        if sampleInsideFOV:
            if vFrame.ndim==2:
                vFrame[topLeft[0]:bottomRight[0]-1,topLeft[1]:bottomRight[1]-1] = (
                sFrame[topLeftSample[0]:bottomRightSample[0]-1,
                        topLeftSample[1]:bottomRightSample[1]-1]
                )
            if vFrame.ndim==3:
                vFrame[topLeft[0]:bottomRight[0]-1,topLeft[1]:bottomRight[1]-1,:] = (
                sFrame[topLeftSample[0]:bottomRightSample[0]-1,
                        topLeftSample[1]:bottomRightSample[1]-1,:]
                )

        # move the spectral axis back
        if (destination.ndim ==3) and (source.ndim ==3):
            vFrame = np.moveaxis(destination,-1,0)
            sFrame = np.moveaxis(source,-1,0)



    def setSample(self):
        ''' define the sample.
        sample ... spatial distribution of photon rates [#/s/pixelSize^2] (no noise)'''

        # define
        _sample = np.sum(data.astronaut(), axis=2)

        # resize 
        _sample = resize(_sample, self.DEFAULT['sampleSize'])

        # normalise
        _sample = _sample/np.max(_sample)*self.DEFAULT['photonRateMax']

        self.sample = _sample


    def setVirtualDevice(self,camera1=None,camera2=None,
                        stage=None,switch=None,laser=None):
        ''' set instruments of the microscope '''

        self.camera1 = camera1
        self.camera2 = camera2
        self.stage = stage
        self.switch = switch
        self.laser = laser

    def calculateVirtualFrame(self,cameraNumber):
        ''' update the virtual Frame of the camera '''

        # 0. laser
        eFrame = self.sample*self.laser.getParameter("power")
        if self.laser.getParameter("keySwitch") is False:
            eFrame *= 0

        # 1. stage
        samplePositionXYZ = self.DEFAULT['samplePositionXYZ'] + self.stage.position
        samplePositionXY = samplePositionXYZ[0:2]

        if cameraNumber ==1:
            
            # camera 1 
            # image -  magnify , ideal lens
            mag = self.DEFAULT['magnification1']*self.DEFAULT['samplePixelSize']/self.camera1.DEFAULT['cameraPixelSize']
            samplePositionXY = (samplePositionXY* mag).astype(int)
            sFrame = rescale(eFrame,(mag,mag), preserve_range=True)
            # adjust the number of photons
            sFrame /= mag**2        
            # aperture
            dFrame = np.zeros((self.camera1.getParameter('height'),
                    self.camera1.getParameter('width')))
            self._mapImageToImage(dFrame,sFrame, samplePositionXY )

            # camera
            ## integration time
            dFrame *= self.camera1.exposureTime/1e6 
            return dFrame

        if cameraNumber ==2:
            
            # camera 1 
            # image -  magnify , ideal lens
            mag = self.DEFAULT['magnification2']*self.DEFAULT['samplePixelSize']/self.camera2.DEFAULT['cameraPixelSize']
            samplePositionXY = (samplePositionXY* mag).astype(int)
            sFrame = rescale(eFrame,(mag,mag), preserve_range=True)
            # adjust the number of photons
            sFrame /= mag**2        
            # aperture
            dFrame = np.zeros((self.camera2.getParameter('height'),
                    self.camera2.getParameter('width')))
            self._mapImageToImage(dFrame,sFrame, samplePositionXY )

            # camera
            ## integration time
            dFrame *= self.camera2.exposureTime/1e6 
            return dFrame

    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield 
            if (self.camera1.flagSetParameter.is_set() or
            self.camera2.flagSetParameter.is_set() or
            self.laser.flagSetParameter.is_set() or
            self.switch.flagSetParameter.is_set() or
            self.stage.flagSetParameter.is_set()
            ):
                print(f'calculate virtual frame')
                self.camera1.virtualFrame = self.calculateVirtualFrame(1)
                self.camera2.virtualFrame = self.calculateVirtualFrame(2)
                self.camera1.flagSetParameter.clear()
                self.camera2.flagSetParameter.clear()
                self.laser.flagSetParameter.clear()
                self.stage.flagSetParameter.clear()
                self.switch.flagSetParameter.clear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

    from viscope.main.baseMain import BaseMain
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    print('starting camera 1')
    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    print('starting camera 2')
    camera2 = VirtualCamera()
    camera2.connect()
    camera2.setParameter('threadingNow',True)

    print('starting stage')
    stage = VirtualStage()
    stage.connect()

    print('starting laser')
    laser = VirtualLaser()
    laser.connect()
    laser.setParameter("power",1)
    laser.setParameter("keySwitch",True)

    print('starting switcher')
    switch = VirtualSwitch()
    switch.connect()

    print('starting virtual microscope')
    vM = virtualMicroscope()
    vM.setVirtualDevice(camera1=camera1, camera2=camera2, laser= laser,
    switch= switch, stage=stage)
    vM.setSample()
    vM.connect()

    print('starting main event loop')
    viscope = BaseMain()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1,camera2,laser,switch,stage])
    
    viscope.run()

    print('closing instruments')
    camera1.disconnect()
    camera2.disconnect()
    laser.disconnect()
    stage.disconnect()
    switch.disconnect()        

    print('closing virtualMicroscope')
    vM.disconnect()


