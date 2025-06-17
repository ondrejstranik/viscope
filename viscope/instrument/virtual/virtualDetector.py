#%%
''' module for virtual detector'''

import numpy as np
import time

#from qtpy.QtCore import QObject, Signal
from viscope.instrument.base.baseDetector import BaseDetector
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualDetector(BaseDetector):
    ''' class to emulate detector'''

    DEFAULT = {'name':'virtualDetector',
               'signalRate': 100, # Hz
               'value': 10, # average value
               'sigma': 1} # noise on the signal 

    def __init__(self, name=DEFAULT['name'], **kwargs):
        ''' detector initialisation'''
        super().__init__(name=name, **kwargs)
        

        # variable to generate virtual data
        self.value = self.DEFAULT['value']
        self.sigma = self.DEFAULT['sigma']
        self.virtualStack = np.array([])
        self.acquisitionStopTime = None
        self.acquisitionStartTime = None

    def startAcquisition(self):
        '''start detector collecting data in a stack '''
        self.acquisitionStartTime = time.time_ns()
        self.acquisitionStopTime = None

    def stopAcquisition(self):
        '''stop detector collecting data in a stack '''
        self.acquisitionStopTime = time.time_ns()


    def getStack(self):
        ''' get the data from stack'''        
        
        return super().getStack()


if __name__ == '__main__':

    pass





# %%