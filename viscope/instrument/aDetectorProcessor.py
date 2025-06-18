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
        
        # add the data
        np.append(self.time,self.aDetector.stack[:,1])
        np.append(self.signal,self.aDetector.stack[:,2])
 

#%%

if __name__ == '__main__':
    pass
