"""
plasmon processor - process the spectral images

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

import os
import time
import numpy as np
from viscope.instrument.base.baseProcessor import BaseProcessor


class ADetectorProcessor(BaseProcessor):
    ''' class to collect data from virtual ADetector'''
    DEFAULT = {'name': 'ADetectorProcessor',
               'timeSpan': 10 # time span for holding the data
                }

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= ADetectorProcessor.DEFAULT['name']
        super().__init__(name=name, **kwargs)
        
        # asynchronous Detector
        self.aDetector = None
        
        # data
        self.time = None
        self.signal = None
        #self.timeStart = 0
        self.timeSpan = ADetectorProcessor.DEFAULT['timeSpan']

    def connect(self,aDetector=None):
        ''' connect data processor with aDetector'''
        super().connect()
        if aDetector is not None: self.setParameter('aDetector',aDetector)

    def setParameter(self,name, value):
        ''' set parameter of the spectral camera'''
        super().setParameter(name,value)

        if name== 'aDetector':
            self.aDetector = value
            self.flagToProcess = self.aDetector.flagLoop

    def getParameter(self,name):
        ''' get parameter of the camera '''
        _value = super().getParameter(name)
        if _value is not None: return _value        

        if name== 'aDetector':
            return self.aDetector


    def processData(self):
        ''' process newly arrived data '''
        #print(f"processing data from {self.DEFAULT['name']}")
        
        try:
            # add the data
            if self.time is None:
                self.timeStart = self.aDetector.stack[0,0]
                self.time = self.aDetector.stack[:,0] - self.timeStart
                self.signal = self.aDetector.stack[:,1]
            else:
                self.time = np.append(self.time,self.aDetector.stack[:,0] - self.timeStart)
                self.signal = np.append(self.signal,self.aDetector.stack[:,1])

            # cut the data if too large
            
            #print(f'time {self.time}')
            print(f'self.time shape {np.shape(self.time)}')
            print(f'self.signal shape {np.shape(self.signal)}')
            if self.time[-1]> self.timeSpan*1e9:
                print('hallo')
                idx = np.argmin(np.abs(self.time - self.timeSpan*1e9))
                print(f'idx {idx}')
                self.time = self.time[idx+1:-1] - self.time[idx+1]
                self.signal = self.signal[idx+1:-1]
                self.timeStart = self.timeStart + self.time[0]
                #self.time = self.time - self.timeStart

        except:
            print(f'time {self.time}')
            '''
            print(f'stack {self.aDetector.stack}')
            print(f'time {self.time}')
            print(f'signal {self.signal}')
            '''
            pass

        self.aDetector.flagLoop.clear()


#%%

if __name__ == '__main__':
    pass
