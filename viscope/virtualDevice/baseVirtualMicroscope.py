"""
virtual basic microscope

components: camera
sample: default image of astronaout

@author: ostranik
"""
#%%

import time
#import numpy as np
#from qtpy.QtCore import QObject, Signal
#from skimage import data
#from skimage.transform import resize, rescale

from napari.qt.threading import create_worker
from viscope.instrument.base.baseInstrument import ThreadFlag


class BaseVirtualMicroscope():
    ''' base class for virtual microscope '''
    DEFAULT = {'name':'baseVirtualMicroscope'}
    
    def __init__(self, **kwargs):
        ''' initialisation '''
        super(BaseVirtualMicroscope,self).__init__(**kwargs)

        self.flagLoop = ThreadFlag()
        self.worker = None

    def setSample(self):
        ''' define the sample.
        sample ... spatial distribution of photon rates [#/s/pixelSize^2] (no noise)'''
        pass

    def setVirtualDevice(self,device):
        ''' set instruments of the microscope '''
        pass

    def connect(self):
        ''' start the virtual microscope '''
        self.worker = create_worker(self.loop)
        self.worker.start()

    def disconnect(self):
        ''' stop the virtual microscope '''
        if self.worker is not None: 
            print(f'quitting the thread loop of baseVirtualMicroscope')
            self.worker.quit()
            self.worker = None
            self.flagLoop = None
            time.sleep(1)


    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''
        pass        

    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield
            print('loop of the baseVirtualMicroscope') 
            time.sleep(1)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main.baseMain import BaseMain
    from viscope.gui.allDeviceGUI import AllDeviceGUI


    print('starting virtual microscope')
    vM = BaseVirtualMicroscope()
    vM.connect()

    print('starting main event loop')
    viscope = BaseMain()
    viscope.run()

    print('closing virtualMicroscope')
    vM.disconnect()

    #time.sleep(3)


