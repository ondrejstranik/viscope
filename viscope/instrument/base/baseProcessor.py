"""
base class for cameras

@author: ostranik
"""
#%%

import time
from viscope.instrument.base.baseInstrument import BaseInstrument

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
        # TODO: check if it not create errors!
        #self.flagToProcess = None

    def processData(self):
        ''' processing data '''
        #print(f"processing data from {self.DEFAULT['name']}")
        return None

    def loop(self):
        ''' infinite loop of the data process thread '''
        try:
            while True:
                if ((self.flagToProcess is not None) and
                    (self.flagToProcess.is_set())):
                    self.processData()
                    self.flagLoop.set()
                    self.flagToProcess.clear()
                    print(f'baseProcessor data yielding')  
                    yield True
                else:
                    yield False

                time.sleep(0.03)

        except Exception as error:
            print(f"An exception occurred in thread of {self.name}:\n", error)
            yield


#%%

if __name__ == '__main__':
    pass
