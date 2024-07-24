"""
base class for cameras

@author: ostranik
"""
#%%

import time
from viscope.instrument.base.baseInstrument import BaseInstrument

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
                print(f'sequence step number {ii}')
                yield  
                time.sleep(1)
            
            # finishing
            self.flagLoop = None

        except Exception as error:
            print(f"An exception occurred in thread of {self.name}:\n", error)


#%%

if __name__ == '__main__':
    pass
