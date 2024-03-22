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
                'width': 1000,
                'cameraOffset':10,
                'electronicNoise': 3,
                'cameraPixelSize': 1} # um
    

    def __init__(self, name=DEFAULT['name'],*args, **kwargs):
        ''' initialisation '''

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
    import napari
    from qtpy.QtCore import QTimer

    cam = VirtualCamera()
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrame', 1)
    cam.setParameter('threadingNow',True)

    cTime = time.time()
    while time.time()-cTime < 3:    
        if cam.flagLoop.is_set():
            print(f'sum of the pixels {np.sum(cam.rawImage)}')
            cam.flagLoop.clear()

    cam.disconnect()


# %%
