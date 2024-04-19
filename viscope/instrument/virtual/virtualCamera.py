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
                'cameraPixelSize': 1} # um
    

    def __init__(self, name=None,*args, **kwargs):
        ''' initialisation '''

        if name is None: name=VirtualCamera.DEFAULT['name']
        super(VirtualCamera,self).__init__(name=name,*args, **kwargs)

        # camera parameters
        self.cameraOffset = VirtualCamera.DEFAULT['cameraOffset']
        self.electronicNoise = VirtualCamera.DEFAULT['electronicNoise']
        self.height = VirtualCamera.DEFAULT['height']
        self.width = VirtualCamera.DEFAULT['width']


        # virtual frame ... photon distribution on the camera chip
        # set to empty
        self.virtualFrame = np.zeros((self.height,self.width))

        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()


    def getLastImage(self):
        ''' get the last image from the camera '''
        myFrame = None
        for ii in range(self.nFrame):
            time.sleep(self.exposureTime/1000)
            if myFrame is None:
                myFrame = self.virtualFrame.astype(float)
            else:
                myFrame = myFrame + self.virtualFrame.astype(float)
            
            # add offset and electronic noise
            myFrame = (myFrame + 
                    np.random.normal(self.cameraOffset,
                                    self.electronicNoise,
                                    np.shape(myFrame))
                        )            

        myFrame = myFrame/self.nFrame
        self.rawImage = myFrame
        return self.rawImage

    def setParameter(self,name,value):
        super().setParameter(name,value)
        self.flagSetParameter.set(name)

#%%

if __name__ == '__main__':
    import pytest
    retcode = pytest.main(['tests/test_class.py::test_VirtualCamera'])
