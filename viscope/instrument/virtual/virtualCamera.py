"""
virtual camera

@author: ostranik
""" 
#%%

import time
import numpy as np
from viscope.instrument.base.baseCamera import BaseCamera
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualCamera(BaseCamera):

    ''' class to emulate camera '''


    DEFAULT = {'name':'virtualCamera',
                'exposureTime': 100,
                'nFrames': 1,
                'height': 500,
                'width': 900,
                'cameraOffset':10,
                'electronicNoise': 3,
                'quantumEfficiency': 1,
                'gain': 1,
                'cameraPixelSize': 1} # um
    

    def __init__(self, name=None,*args, **kwargs):
        ''' initialisation '''

        if name is None: name=VirtualCamera.DEFAULT['name']
        super(VirtualCamera,self).__init__(name=name,*args, **kwargs)

        # camera parameters
        self.cameraOffset = VirtualCamera.DEFAULT['cameraOffset']
        self.electronicNoise = VirtualCamera.DEFAULT['electronicNoise']
        self.quantumEfficiency = VirtualCamera.DEFAULT['quantumEfficiency']
        self.gain = VirtualCamera.DEFAULT['gain']
        self.height = VirtualCamera.DEFAULT['height']
        self.width = VirtualCamera.DEFAULT['width']


        # virtual frame ... photon distribution on the camera chip
        # set to empty
        self.virtualFrame = np.zeros((self.height,self.width))

        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()


    def getLastImage(self):
        ''' get the last image from the camera '''
        time.sleep(self.nFrame*self.exposureTime/1000)

        # photon shot noise (virtualFrame is in photon numbers): the sum of
        # nFrame iid Poisson(lambda) draws is exactly Poisson(nFrame*lambda),
        # so the average over nFrame exposures can be drawn exactly with a
        # single Poisson call instead of nFrame separate ones
        photonFrame = np.random.poisson(self.virtualFrame*self.nFrame)/self.nFrame

        # convert photons to electrons, then electrons to counts
        meanFrame = photonFrame*self.quantumEfficiency*self.gain

        # electronic noise: Gaussian, scaled down by sqrt(nFrame) since it
        # is the noise of an average of nFrame independent exposures
        electronicNoiseStd = self.electronicNoise/np.sqrt(self.nFrame)

        myFrame = (meanFrame + self.cameraOffset +
                    np.random.normal(0, electronicNoiseStd, np.shape(meanFrame))
                    )

        self.rawImage = myFrame
        return self.rawImage

    def setParameter(self, name, value):
        """Set a camera parameter and notify the virtual microscope of the change."""
        super().setParameter(name, value)
        self.flagSetParameter.set(name)

#%%

if __name__ == '__main__':
    pass
