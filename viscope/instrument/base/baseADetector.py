#%%
''' module to control asynchronous detectors  '''

import numpy as np
from viscope.instrument.base.baseInstrument import BaseInstrument
import time


class BaseADetector(BaseInstrument):
    ''' base class of detectors collecting data asynchronously via stack'''

    DEFAULT = {'name':'baseADetector',
               'stackTime': 0.1} # in [s] time period of stack collection
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name, **kwargs)

        self.stack = None
        self.stackTime = BaseADetector.DEFAULT['stackTime']
        self.acquiring = False

    def startAcquisition(self):
        ''' some detector have this to start filling the stack '''
        self.acquiring = True

    def stopAcquisition(self):
        ''' some detector have this to stop filling the stack '''
        self.acquiring = False

    def _setStackTime(self,value):
        self.stackTime = value

    def _getStackTime(self):
        return self.stackTime

    def setParameter(self,name, value):
        ''' set parameters '''
        super().setParameter(name,value)
        if name== 'stackTime':
            self._setStackTime(value)

    def getParameter(self,name):
        ''' get parameters '''
        _value = super().getParameter(name)
        if _value is not None: return _value
        if name=='stackTime':
            return self._getStackTime()

    def _getTestStack(self):
        ''' set testing stack (for internal use only) '''
        self.stack = np.random.rand(50)
        return self.stack

    def getStack(self):
        ''' return stack with data '''
        return self.stack

    def loop(self):
        ''' threading loop of the instrument '''
        while True:
            self.getStack()
            self.flagLoop.set('output')
            yield  
            time.sleep(self.stackTime)


if __name__ == '__main__':

    pass





# %%