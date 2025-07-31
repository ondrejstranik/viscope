#%%
''' base class for the stage'''


import time
import numpy as np
import traceback
from viscope.instrument.base.baseInstrument import BaseInstrument, ThreadFlag


class BaseStage(BaseInstrument):
    ''' main class to control virtual stage'''

    DEFAULT = {'name':'baseStage'}


    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' stage initialisation'''
        super(BaseStage,self).__init__(name=name,*args, **kwargs)

        self.position = None
        self.flagSetPosition = ThreadFlag()
    
    def _getPosition(self):
        ''' get the position of the stage '''
        return self.position

    def _setPosition(self,newPosition):
        ''' move the stage'''
        self.position= newPosition
        #time.sleep(.3)

    def setParameter(self,name, value):
        ''' set parameters of the stage'''
        super().setParameter(name,value)

        if name== 'position':
            if self.worker is not None:
                self.flagSetPosition.set(value)
            else:
                self._setPosition(value)

    def getParameter(self,name):
        ''' get parameter '''
        _value = super().getParameter(name)
        if _value is not None: return _value
       
        if name=='position':
            return self._getPosition()

    def loop(self):
        ''' infinite loop of the thread '''
        while True:
            try:
                if self.flagSetPosition.is_set():
                    _newPosition = self.flagSetPosition.getLastData()
                    self._setPosition(_newPosition)
                    self.flagSetPosition.clear()
                    self.flagLoop.set()
                    yield
                time.sleep(0.03)
            except:
                print(f"An exception occurred in thread of {self.name}:\n")
                traceback.print_exc()
                yield False                

if __name__ == '__main__':

    pass


# %%
