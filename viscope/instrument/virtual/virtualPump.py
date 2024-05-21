#%%
''' class to control virtual laser'''

import numpy as np
import time

#from qtpy.QtCore import QObject, Signal
from viscope.instrument.base.basePump import BasePump
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualPump(BasePump):
    ''' main class to emulate pump'''

    DEFAULT = {'name':'virtualPump'}

    def __init__(self, name=DEFAULT['name'],*args, **kwargs):
        ''' pump initialisation'''
        super().__init__(name=name,*args, **kwargs)
        
        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()

    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        super().setParameter(name,value)
        self.flagSetParameter.set(name)

    def _setFlowRate(self,value):
        super()._setFlowRate(value)
        try:
            print(f'flowRate = {self.flowRate*self.flow}')
        except:
            print('flowRate not defined')

    def _setFlow(self,value):
        super()._setFlow(value)
        try:
            print(f'flowRate = {self.flowRate*self.flow}')
        except:
            print('flowRate not defined')



if __name__ == '__main__':

    pass





# %%