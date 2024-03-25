"""
virtual basic microscope

components: camera
sample: default image of astronaout

@author: ostranik
"""
#%%

import time

from napari.qt.threading import create_worker
from viscope.instrument.base.baseInstrument import ThreadFlag
from viscope.virtualDevice.component.sample import Sample


class BaseVirtualMicroscope():
    ''' base class for virtual microscope '''
    DEFAULT = {'name':'baseVirtualMicroscope'}
    
    def __init__(self, **kwargs):
        ''' initialisation '''
        super(BaseVirtualMicroscope,self).__init__(**kwargs)

        self.flagLoop = ThreadFlag()
        self.worker = None
        
        self.sample = Sample()
        self.sample.setAstronaut()

    def setSample(self, sample):
        ''' set the sample.'''
        self.sample = sample

    def setVirtualDevice(self,device):
        ''' set instruments of the microscope '''
        pass

    def connect(self):
        ''' start the virtual microscope '''
        print(f'starting thread loop of {self.DEFAULT["name"]}')
        
        self.worker = create_worker(self.loop)
        self.worker.start()

    def disconnect(self):
        ''' stop the virtual microscope '''
        if self.worker is not None: 
            print(f'quitting the thread loop of {self.DEFAULT["name"]}')
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
            print(f'loop of the {self.DEFAULT["name"]}') 
            time.sleep(1)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI


    vM = BaseVirtualMicroscope()
    vM.connect()
    viscope = Viscope()
    viscope.run()

    vM.disconnect()



