#%%
''' module to control asynchronous detectors  '''

import numpy as np
from viscope.instrument.base.baseInstrument import BaseInstrument
import time
import traceback


class BaseADetector(BaseInstrument):
    ''' base class of detectors collecting data asynchronously via stack'''

    DEFAULT = {'name':'baseADetector',
               'stackTime': 0.005} # in [s] time period of stack collection
    
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
        ''' return stack with data and clear the stack'''
        #with self.lock:
        #    wholeChunkOfStack = self.stack
        #    self.stack = None
        wholeChunkOfStack = self.stack
        self.stack = None
        self.flagLoop.clear()
        return wholeChunkOfStack

    def updateStack(self):
        ''' update the stack'''
        pass

    def isEmptyStack(self):
        ''' check if stack is empty'''
        res = False
        #with self.lock:
        #    if (self.stack is None) or (self.stack.size == 0):
        #        res = True
        if (self.stack is None) or (self.stack.size == 0):
            res = True
        return res

    def loop(self):
        ''' threading loop of the instrument '''
        while True:
            try:
                #with self.lock:
                #    self.updateStack()
                self.updateStack()
                if not self.isEmptyStack(): # only if new data arrived then set flag
                        self.flagLoop.set('output')
                        yield True
                        #print(f'{self.name} yielding new Data')
                else:
                    yield False
                time.sleep(self.stackTime)
            except:
                print(f"An exception occurred in thread of {self.name}:\n")
                traceback.print_exc()
                yield False


if __name__ == '__main__':

    pass






# %%