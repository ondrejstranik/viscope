"""
Base class for data processors.

Processors watch a ThreadFlag set by a source instrument and run
processData() each time new data arrives.
"""
#%%

import time
import logging
from timeit import default_timer as timer
from viscope.instrument.base.baseInstrument import BaseInstrument

logger = logging.getLogger(__name__)

class BaseProcessor(BaseInstrument):
    """Base class for all data processors.

    Args:
        name: Unique identifier for the processor instance.

    Attributes:
        flagToProcess: ThreadFlag from the source instrument; the loop
            calls processData() each time this flag is set.
        idleRatio: after processing, the loop sleeps at least
            idleRatio * processTime (and at least loopDelay). It limits the
            share of time the processing thread holds the GIL, so the GUI
            stays responsive even when processData() is slow and new data
            arrive faster than they can be processed.
            1 -> processing takes at most ~50 % of the time, 0 -> sleep
            only loopDelay (processes as fast as possible).
        processTime: smoothed duration of processData() in s.
    """
    DEFAULT = {'name':'baseProcessor',
               'idleRatio': 0, # 0 -> no extra idle time (processors may set e.g. 1)
               'processTimeSmoothing': 0.3 # weight of the newest duration in processTime
                  }

    def __init__(self, name: str = None, **kwargs):
        ''' initialisation '''

        if name is None: name=BaseProcessor.DEFAULT['name']
        super().__init__(name=name,**kwargs)

        self.flagToProcess = None
        self.idleRatio = BaseProcessor.DEFAULT['idleRatio']
        self.processTime = 0

    def connect(self,flagToProcess=None):
        ''' connect to the flag '''
        super().connect()
        self.flagToProcess = flagToProcess

    def disconnect(self):
        """Disconnect the processor and stop the worker thread."""
        super().disconnect()
        # TODO: check if it not create errors!
        #self.flagToProcess = None

    def setParameter(self,name,value):
        ''' set parameter of the processor '''
        super().setParameter(name,value)
        if name== 'idleRatio':
            self.idleRatio = value

    def getParameter(self,name):
        ''' get parameter of the processor '''
        _value = super().getParameter(name)
        if _value is not None: return _value

        if name== 'idleRatio':
            return self.idleRatio
        if name== 'processTime':
            return self.processTime

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
            # without new data poll every loopDelay
            idleTime = self.loopDelay
            try:
                if ((self.flagToProcess is not None) and
                    (self.flagToProcess.is_set())):
                    # clear before processing - new data arriving during
                    # processData() sets the flag again and is processed in
                    # the next iteration instead of being discarded
                    self.flagToProcess.clear()
                    start = timer()
                    self.processData()
                    # smoothed, so that a single slow iteration does not stall the loop
                    a = BaseProcessor.DEFAULT['processTimeSmoothing']
                    self.processTime = (1-a)*self.processTime + a*(timer() - start)
                    # give the GUI thread time proportional to the processing time
                    idleTime = max(self.loopDelay, self.idleRatio*self.processTime)
                    logger.debug('%s processTime %.4f s, idleTime %.4f s', self.name, self.processTime, idleTime)
                    self.flagLoop.set()
                    #print(f'{self.name} yielding new Data')
                    yield True
                else:
                    yield False
            except Exception:
                logger.exception(f"An exception occurred in thread of {self.name}")
                yield False
            time.sleep(idleTime)


#%%

if __name__ == '__main__':
    pass
