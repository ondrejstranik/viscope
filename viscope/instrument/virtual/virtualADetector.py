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
        self.acquisitionStopTime = None
        self.acquisitionStartTime = None
        self.lastStackTime = None

    def startAcquisition(self):
        '''start detector collecting data in a stack '''
        self.acquisitionStartTime = time.time_ns()
        self.lastStackTime = self.acquisitionStartTime*1
        self.acquisitionStopTime = None

    def stopAcquisition(self):
        '''stop detector collecting data in a stack '''
        self.acquisitionStopTime = time.time_ns()


    def getStack(self):
        ''' get data from the stack'''        

        # check if acquisition is running
        currentTime = time.time_ns()
        if self.acquisitionStopTime is not None:
            currentTime = self.acquisitionStopTime

        if self.acquisitionStopTime == self.lastStackTime:
            self.stack = None
        else:
            # generate the signal        
            dataTime = np.linspace(self.lastStackTime, currentTime,int(1e9/self.signalRate))
            nData = len(dataTime)
            signal = np.random.normal(self.value,self.sigma,nData)
            self.stack = np.vstack([dataTime,signal]).T

        self.lastStackTime = currentTime

        return self.stack

if __name__ == '__main__':

    pass





# %%