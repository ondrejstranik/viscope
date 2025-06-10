"""
base class for cameras

@author: ostranik
"""
#%%

import time
import numpy as np
from viscope.instrument.base.baseInstrument import BaseInstrument

class BaseCamera(BaseInstrument):
    ''' base class for camera
    name ... name of the camera
    exposureTime ... exposure time of camera in ms
    nFrames ... averaging of the image over the number of frames
    height ... height of the camera image
    width ... width of the camera image
    '''
    DEFAULT = {'name':'baseCamera',
                'exposureTime': 100, 
                'nFrame': 1,
                'height': 500,
                'width': 1000,
                  } 
    
    
    def __init__(self, name=None,*args, **kwargs):
        ''' initialisation '''

        if name is None: name=BaseCamera.DEFAULT['name']
        super().__init__(name=name,*args, **kwargs)

        # camera parameters
        self.exposureTime = BaseCamera.DEFAULT['exposureTime']
        self.nFrame = BaseCamera.DEFAULT['nFrame']
        self.height = BaseCamera.DEFAULT['height']
        self.width = BaseCamera.DEFAULT['width']

        # recorded only in threading mode
        self.dTime = 0 # acquisition/processing time
        self.t0 = time.time()

        # camera output image
        self.rawImage = np.empty((self.height,self.width))

       
    def getLastImage(self):
        ''' get the last image from the camera '''
        print('getLastImage of baseCamera')
        time.sleep(self.exposureTime/1000*self.nFrame)
        self.rawImage = np.ones((self.height,self.width))
        return self.rawImage
    
    def startAcquisition(self):
        ''' some camera have this implementation '''
        pass

    def stopAcquisition(self):
        ''' some camera have this implementation '''
        pass

    def _setExposureTime(self,value):
        self.exposureTime = value

    def _getExposureTime(self):
        return self.exposureTime

    def _setNFrame(self,value):
        self.nFrame = value

    def _getNFrame(self):
        return self.nFrame

    def _getWidth(self):
        return self.width

    def _getHeight(self):
        return self.height

    def setParameter(self,name,value):
        super().setParameter(name,value)
        if name=='exposureTime':
            self._setExposureTime(value)
        if name=='nFrame':
            self._setNFrame(value)

    def getParameter(self,name):
        _value = super().getParameter(name)
        if _value is not None: return _value
        
        if name=='exposureTime':
            return self._getExposureTime()
        if name=='nFrame':
            return self._getNFrame()
        if name=='width':
            return  self._getWidth()
        if name=='height':
            return self._getHeight()

    def loop(self):
        ''' infinite loop of the camera thread '''
        while True:
            self.rawImage = self.getLastImage()
            self.dTime = time.time() -self.t0
            self.t0 = self.t0 + self.dTime
            self.flagLoop.set()
            yield  
            time.sleep(0.03)

    def _displayStreamOfImages(self):
        ''' internal viewer for checking camera functionality
        implemented with napari'''

        import napari
        from napari.qt.threading import thread_worker, create_worker
        import time        

        def yieldHSImage():
            while True:
                yield  self.getLastImage()
                time.sleep(0.03)

        def update_layer(new_image):
            rawlayer.data = new_image


        # start napari        
        viewer = napari.Viewer()

        im = np.zeros((self.height,self.width))
        # raw image
        rawlayer = viewer.add_image(im, rgb=False, colormap="gray", 
                                            name='Raw',  blending='additive')

        # prepare threads
        worker = create_worker(yieldHSImage)
        worker.yielded.connect(update_layer)

        worker.start()
        napari.run()


#%%

if __name__ == '__main__':
    pass


# %%
