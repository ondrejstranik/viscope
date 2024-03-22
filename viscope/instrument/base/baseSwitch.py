#%%
''' base class for a switch'''

import numpy as np
import time

from viscope.instrument.base.baseInstrument import BaseInstrument, ThreadFlag

class BaseSwitch(BaseInstrument):
    ''' main class to control a switch with discrete positions'''
    DEFAULT = {'name':'baseSwitch',
                'positionList': ['up', 'down'],
                }

    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' switch initialisation'''
        super(BaseSwitch,self).__init__(name=name,*args, **kwargs)
        
        self.position = None
        self.positionList = BaseSwitch.DEFAULT['positionList']

        self.flagSetPosition = ThreadFlag()

    def _setPosition(self,positionNumber):
        ''' set the position in the switcher '''
        self.position = positionNumber

    def _getPosition(self):
        ''' set the position of the switcher '''
        return self.position

    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        super().setParameter(name,value)
        
        if name== 'position':
            if self.worker is not None:
                self.flagSetPosition.set(value)
            else:
                self._setPosition(value)

        if name== 'positionList':
            self.positionList = value

    def getParameter(self,name):
        ''' get parameter '''
        _value = super().getParameter(name)
        if _value is not None: return _value

        if name=='position':
            return self._getPosition()

        if name=='positionList':
            return self.positionList

    def loop(self):
        ''' infinite loop of the thread '''
        while True:
            if self.flagSetPosition.is_set():
                _newPosition = self.flagSetPosition.getLastData()
                self._setPosition(_newPosition)
                self.flagSetPosition.clear()
                self.flagLoop.set()
                yield
            time.sleep(0.03)


if __name__ == '__main__':

    switch = BaseSwitch()
    switch.connect()
    switch.setParameter('threadingNow',True)
    print( f'worker {switch.worker}')

    switch.setParameter('position',1)
    print( f'flagSetPosition {switch.flagSetPosition.is_set()}')

    switch.flagLoop.wait()
    switch.flagLoop.clear()    
    #print(f'switch position {switch.getParameter("positionList")[switch.getParameter("position")]}')
    print(f'switch position {switch.getParameter("position")}')
    switch.setParameter('position',0)
    switch.flagLoop.wait()
    switch.flagLoop.clear()
    #print(f'switcher position {switch.getParameter("positionList")[switch.getParameter("position")]}')
    print(f'switch position {switch.getParameter("position")}')
    
    switch.disconnect()





# %%