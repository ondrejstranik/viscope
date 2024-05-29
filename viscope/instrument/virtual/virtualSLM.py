#%%
''' class to control virtual laser'''

import numpy as np
import time

#from qtpy.QtCore import QObject, Signal
from viscope.instrument.base.baseSLM import BaseSLM
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualSLM(BaseSLM):
    ''' main class to emulate slm'''

    DEFAULT = {'name':'virtualSLM'}

    def __init__(self, name=DEFAULT['name'], **kwargs):
        ''' slm initialisation'''
        super(VirtualSLM,self).__init__(name=name, **kwargs)
        
        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()

    def setImage(self,image):
        super().setImage(image)
        self.flagSetParameter.set('image')

    def setParameter(self,name, value):
        ''' set parameters of the laser'''
        super().setParameter(name,value)
        self.flagSetParameter.set(name)



if __name__ == '__main__':
    pass





# %%