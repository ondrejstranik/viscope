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


class virtualMicroscope():
    ''' class to emulate microscope '''
    DEFAULT = {'photonRateMax':1e6,
                'samplePixelSize':1, # um
                'magnification': 1,
                'sampleSize': (200,400)} # pixels
    
    def __init__(self,*args, **kwargs):
        ''' initialisation '''
        super(virtualMicroscope,self).__init__(*args, **kwargs)

        self.flagLoop = ThreadFlag()
        self.worker = None

        self.sample = None
        self.camera = None


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


    def setVirtualDevice(self,device):
        ''' set instruments of the microscope '''

        self.camera = device

    def connect(self):
        ''' start the virtual microscope '''
        self.worker = create_worker(self.loop)
        self.worker.start()

        # connect the signals from the instruments
        #self.camera.sigGetLastImage.connect(lambda : setattr(self,'flagNewImageRequest',True))
        #self.camera.sigSetParameter.connect(lambda: setattr(self,'flagNewState',True))


    def disconnect(self):
        ''' stop the virtual microscope '''
        self.worker.quit()


    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''
        
        # imaging 
        ## magnification
        sFrame = rescale(self.sample,self.DEFAULT['magnification'], preserve_range=True)
        ## adjust the number of photons
        sFrame *= (self.camera.DEFAULT['cameraPixelSize']/self.DEFAULT['samplePixelSize'])**2

        # camera
        ## field of view
        # 
        print(f'virtual camera object { self.camera}')
        print(f'camera size: { self.camera.getParameter("height")} {self.camera.getParameter("width")}')

        vFrame = np.zeros((self.camera.getParameter('height'),self.camera.getParameter('width')))
        minHeight = np.min((self.camera.getParameter('height'),sFrame.shape[0]))
        minWidth = np.min((self.camera.getParameter('width'),sFrame.shape[1]))
        vFrame[0:minHeight,0:minWidth]= sFrame[0:minHeight,0:minWidth]

        ## integration time
        vFrame *= self.camera.exposureTime/1e6

        return vFrame

        print('virtual Frame updated')

    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield 
            if self.camera.flagSetParameter.is_set():
                print(f'calculate virtual frame')
                self.camera.virtualFrame = self.calculateVirtualFrame()
                self.camera.flagSetParameter.clear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main.baseMain import BaseMain
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    print('starting camera 1')
    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    print('starting virtual microscope')
    vM = virtualMicroscope()
    vM.setVirtualDevice(camera1)
    vM.setSample()
    vM.connect()

    print('starting main event loop')
    viscope = BaseMain()
    viewer  = AllDeviceGUI(viscope,viscope.vWindow)
    viewer.setDevice([camera1])
    
    viscope.run()

    print('closing camera')
    camera1.disconnect()

    print('closing virtualMicroscope')
    vM.disconnect()


