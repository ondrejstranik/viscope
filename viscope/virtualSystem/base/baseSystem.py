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
from viscope.virtualSystem.component.sample import Sample


class BaseSystem():
    ''' base class for virtual microscope '''
    DEFAULT = {}
    
    def __init__(self, **kwargs):
        ''' initialisation '''
        super(BaseSystem,self).__init__(**kwargs)

        self.flagLoop = ThreadFlag()
        self.worker = None
        
        # set default sample
        self.sample = Sample()
        self.sample.setAstronaut()

        self.device = {}

    def setSample(self, sample):
        ''' set the sample.'''
        self.sample = sample

    def setVirtualDevice(self,device=None):
        ''' set instruments of the microscope '''
        self.device['device']= device

    def connect(self):
        ''' start the virtual microscope '''
        print(f'starting thread loop of {self.__class__.__name__}')
        
        self.worker = create_worker(self.loop)
        self.worker.start()

    def disconnect(self):
        ''' stop the virtual microscope '''
        if self.worker is not None: 
            print(f'quitting the thread loop of {self.__class__.__name__}')
            self.worker.quit()
            self.worker = None
            self.flagLoop = None
            time.sleep(1)

    def deviceParameterIsChanged(self):
        ''' set true if any of the instruments changed parameter '''
        flag = False
        for key in self.device:
            if hasattr(self.device[key],'flagSetParameter'):
                flag = flag or self.device[key].flagSetParameter.is_set()
        return flag
    
    def deviceParameterFlagClear(self):
        ''' set all flag of the devices to False '''
        for key in self.device:
            if hasattr(self.device[key],'flagSetParameter'):
                self.device[key].flagSetParameter.clear()



    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield
            print(f'loop of the {self.__class__.__name__}') 
            time.sleep(1)

        

#%%

if __name__ == '__main__':

    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI


    vM = BaseSystem()
    vM.connect()
    viscope = Viscope()
    viscope.run()

    vM.disconnect()



