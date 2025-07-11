#%%
''' class for a virtual switch'''

import numpy as np
import time

from viscope.instrument.base.baseSwitch import BaseSwitch
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualSwitch(BaseSwitch):
    ''' main class to control a virtual switch'''
    DEFAULT = {'name':'virtualSwitch',
                'initialPosition':0,
                'switchingTime': 0.3 # [s]
                }

    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' switch initialisation'''
        super(VirtualSwitch,self).__init__(name=name,*args, **kwargs)
        
        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()

    def _setPosition(self,positionNumber):
        ''' set the position in the switcher '''
        self.position = positionNumber
        time.sleep(VirtualSwitch.DEFAULT['switchingTime'])

    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        super().setParameter(name,value)
        self.flagSetParameter.set(name)

    def connect(self,initialPosition=DEFAULT['initialPosition']):
        super().connect()
        self.setParameter('position',initialPosition)



if __name__ == '__main__':
    pass





# %%