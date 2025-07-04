#%%
''' module for virtual detector having internal stack for the data'''

import numpy as np
import time

from viscope.instrument.base.baseADetector import BaseADetector


class VirtualADetector(BaseADetector):
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
        self.signalRate = self.DEFAULT['signalRate']
        self.acquiring = False
        if self.acquiring is False:
            self.acquisitionStopTime = 0
            self.lastStackTime = 0

    def startAcquisition(self):
        '''start detector collecting data in a stack '''
        super().startAcquisition()
        #self.acquisitionStartTime = time.time_ns()
        self.lastStackTime = time.time_ns() #self.acquisitionStartTime*1
        self.acquisitionStopTime = None

    def stopAcquisition(self):
        '''stop detector collecting data in a stack '''
        super().stopAcquisition()
        self.acquisitionStopTime = time.time_ns()

    def _calculateStack(self):
        ''' calculate the virtual stack'''
        currentTime = time.time_ns()
        
        if self.acquisitionStopTime is not None:
            currentTime = self.acquisitionStopTime

        if self.acquisitionStopTime == self.lastStackTime:
            virtualStack = None
        else:
            # generate the signal        
            dataTime = np.arange(self.lastStackTime, currentTime,int(1e9/self.signalRate))
            nData = len(dataTime)
            signal = np.random.normal(self.value,self.sigma,nData)
            virtualStack = np.vstack([dataTime,signal]).T

        self.lastStackTime = currentTime

        return virtualStack

    def updateStack(self):
        ''' get data from the stack'''        
        #print(f'getStack from {self.DEFAULT["name"]}')

        res = self._calculateStack()
        if self.stack is None:
            self.stack = res
        else:
            self.stack = np.vstack([self.stack,res])

        return self.stack

if __name__ == '__main__':

    pass





# %%