"""
Base class for hardware/software sequencers.

Sequencers execute a finite (or infinite) series of steps in a dedicated
worker thread, yielding between steps to keep the thread interruptible.
"""
#%%

import time
import logging
from viscope.instrument.base.baseInstrument import BaseInstrument

logger = logging.getLogger(__name__)

class BaseSequencer(BaseInstrument):
    ''' base class for carry out a sequence of hardware / software steps
    name ... name of the sequencer
    '''
    DEFAULT = {'name':'baseSequencer',
                  } 
        
    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name is None: name=BaseSequencer.DEFAULT['name']
        super().__init__(name=name,**kwargs)

    def loop(self):
        ''' finite (infinite) loop of the sequence'''
        try:
            for ii in range(10):
                logger.debug(f'sequence step number {ii}')
                yield True
                time.sleep(1)

            # finishing
            self.flagLoop = None

        except:
            logger.exception(f"An exception occurred in thread of {self.name}")
            # finishing
            self.flagLoop = None


#%%

if __name__ == '__main__':
    pass
