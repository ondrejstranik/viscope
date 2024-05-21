#%%
''' class to control laser'''

import numpy as np
import time
from viscope.instrument.base.baseInstrument import BaseInstrument


class BaseLaser(BaseInstrument):
    ''' base class of laser
    power ... laser power
    keySwitch ... with True the laser emits light'''

    DEFAULT = {'name':'baseLaser',
                'power': 0,
                'keySwitch': False } 
    
    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' laser initialisation'''
        super(BaseLaser,self).__init__(name=name,*args, **kwargs)
        
        self.power = None
        self.keySwitch = None

    def connect(self,*args):
        ''' connect to the laser '''
        super().connect()
        # prepare the laser
        self.setParameter('keySwitch',BaseLaser.DEFAULT['power'])
        self.setParameter('power',BaseLaser.DEFAULT['keySwitch'])

    def _setPower(self,value):
        self.power = value

    def _setKeySwitch(self,value):
        self.keySwitch = value

    def _getPower(self):
        return self.power

    def _getKeySwitch(self):
        return self.keySwitch

    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        if name== 'power':
            self._setPower(value)
        if name== 'keySwitch':
            self._setKeySwitch(value)

    def getParameter(self,name):
        ''' get parameter of the laser '''
        if name=='power':
            return self._getPower()
        if name=='keySwitch':
            return self._getKeySwitch()

if __name__ == '__main__':

    pass





# %%