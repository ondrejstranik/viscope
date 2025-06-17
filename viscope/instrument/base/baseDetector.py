#%%
''' module to control detectors'''

import numpy as np
from viscope.instrument.base.baseInstrument import BaseInstrument


class BaseDetector(BaseInstrument):
    ''' base class of detectors'''

    DEFAULT = {'name':'baseDetector'} 
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name, **kwargs)

        self.stack = None

    def startAcquisition(self):
        ''' some detector have this to start filling the stack '''
        pass

    def stopAcquisition(self):
        ''' some detector have this to stop filling the stack '''
        pass

    def getTestStack(self):
        ''' set testing stack (for internal use only) '''
        testStack = np.random.rand(50)
        return testStack

    def getStack(self):
        ''' return stack with data '''
        return self.stack

if __name__ == '__main__':

    pass





# %%