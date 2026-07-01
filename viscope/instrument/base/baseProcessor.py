"""
Base class for data processors.

Processors watch a ThreadFlag set by a source instrument and run
processData() each time new data arrives.
"""
#%%

import time
from viscope.instrument.base.baseInstrument import BaseInstrument
import traceback

class BaseProcessor(BaseInstrument):
    """Base class for all data processors.

    Args:
        name: Unique identifier for the processor instance.

    Attributes:
        flagToProcess: ThreadFlag from the source instrument; the loop
            calls processData() each time this flag is set.
    """
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
        """Disconnect the processor and stop the worker thread."""
        super().disconnect()
        # TODO: check if it not create errors!
        #self.flagToProcess = None

    def processData(self):
        ''' processing data '''
        #print(f"processing data from {self.DEFAULT['name']}")
        return None

    def loop(self):
        """Infinite loop of the data process thread.

        Yields True when new data was processed, False otherwise.
        Yields regularly so the thread can be interrupted cleanly.
        """
        while True:
            try:
                if ((self.flagToProcess is not None) and
                    (self.flagToProcess.is_set())):
                    self.processData()
                    self.flagLoop.set()
                    self.flagToProcess.clear()
                    #print(f'{self.name} yielding new Data')  
                    yield True
                else:
                    yield False

                time.sleep(0.03)
            except:
                print(f"An exception occurred in thread of {self.name}:\n")
                traceback.print_exc()
                yield False


#%%

if __name__ == '__main__':
    pass
