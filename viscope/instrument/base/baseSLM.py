#%%
''' class to control laser'''

import numpy as np
import time
from viscope.instrument.base.baseInstrument import BaseInstrument


class BaseSLM(BaseInstrument):
    ''' base class of spatial light modulator
    image '''

    DEFAULT = {'name':'baseSML',
             'sizeX': 500,
             'sizeY': 200} 
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name, **kwargs)

        self.sizeX = BaseSLM.DEFAULT['sizeX']
        self.sizeY = BaseSLM.DEFAULT['sizeX']

        self.image = np.zeros((self.sizeY,self.sizeX))  

    def setImage(self,image):
        self.image = image

    def getTestImage(self):
        ''' set testing image (for internal use only) '''
        X,Y = np.meshgrid(np.linspace(0,self.sizeX,self.sizeX),np.linspace(0,self.sizeY,self.sizeY))
        return np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50))).astype('uint8')


    def getImage(self):
        return self.image

if __name__ == '__main__':

    pass





# %%