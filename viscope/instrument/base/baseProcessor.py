"""
base class for cameras

@author: ostranik
"""
#%%

import time
import numpy as np
from viscope.instrument.base.baseInstrument import BaseInstrument, ThreadFlag

class BaseProcessor(BaseInstrument):
    ''' base class for data Processor
    name ... name of the camera
    '''
    DEFAULT = {'name':'baseProcessor',
                  } 
        
    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name is None: name=BaseProcessor.DEFAULT['name']
        super().__init__(name=name,**kwargs)

        self.flagToProcess = None

    def connect(self,flagToProcess=None):
        ''' connect to the flag '''
        super().connect()
        self.flagToProcess = flagToProcess

    def disconnect(self):
        super().disconnect()
        self.flagToProcess = None

    def processData(self):
        ''' processing data '''
        print(f"processing data from {self.DEFAULT['name']}")
        return None

    def loop(self):
        ''' infinite loop of the data process thread '''
        try:
            while self.flagToProcess is not None:
                self.flagToProcess.wait()
                self.processData()
                self.flagLoop.set()
                self.flagToProcess.clear()
                yield  
                time.sleep(0.03)

        except Exception as error:
            print(f"An exception occurred in thread of {self.name}:\n", error)


#%%

if __name__ == '__main__':
    pass
