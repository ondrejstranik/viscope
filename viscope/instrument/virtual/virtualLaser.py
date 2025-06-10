#%%
''' class to control virtual laser'''

import numpy as np
import time

#from qtpy.QtCore import QObject, Signal
from viscope.instrument.base.baseLaser import BaseLaser
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualLaser(BaseLaser):
    ''' main class to emulate laser'''

    DEFAULT = {'name':'virtualLaser'}

    def __init__(self, name=DEFAULT['name'],*args, **kwargs):
        ''' laser initialisation'''
        super(VirtualLaser,self).__init__(name=name,*args, **kwargs)
        
        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()


    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        super().setParameter(name,value)
        self.flagSetParameter.set(name)



if __name__ == '__main__':

    pass





# %%