#%%
''' class to control virtual stage. xyz and rotation'''


import time
import numpy as np

from dataclasses import dataclass
from viscope.instrument.base.baseStage import BaseStage
from viscope.instrument.base.baseInstrument import ThreadFlag


@dataclass
class motor:
    """Class for motor info"""
    speed: float = 10
    position : float = 0


class VirtualStage(BaseStage):
    ''' main class to control virtual stage'''

    DEFAULT = {'name':'virtualStage'}

    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' stage initialisation'''
        super(VirtualStage,self).__init__(name=name,*args, **kwargs)

        self.motorX = None
        self.motorY = None
        self.motorZ = None

        # flag for virtual microscope logic
        self.flagSetParameter = ThreadFlag()

    def connect(self):
        ''' connect to all actuators'''

        self.motorX: motor = motor()
        self.motorY: motor = motor()
        self.motorZ: motor = motor()

        # get the current position of the stage
        self._getPosition()


    def disconnect(self):
        ''' disconnect all actuators'''
        self.motorX = None
        self.motorY = None
        self.motorZ = None

    def _getPosition(self):
        ''' get the position of the stage '''
        self.position = np.array([self.motorX.position,
                                     self.motorY.position,
                                      self.motorZ.position])

        return self.position

    def _setPosition(self,newPosition):
        ''' move the stage. wait until the movement is finished'''

        movingTime = np.max(np.abs(self.position-newPosition)/
        np.array([self.motorX.speed,self.motorY.speed,self.motorZ.speed]))

        # wait until the movement is finished
        start_time = time.time()
        while (time.time()-start_time < movingTime):
            time.sleep(0.2)

        self.motorX.position = newPosition[0]
        self.motorY.position = newPosition[1]
        self.motorZ.position = newPosition[2]

        self._getPosition()

    def setParameter(self,name, value):
        ''' set parameters of the stage'''
        super().setParameter(name,value)
        self.flagSetParameter.set(name)

if __name__ == '__main__':

    stage = VirtualStage(threading=True)

    stage.connect()

    stage.setParameter('threadingNow',True)

    print(f'stage position {stage.position}')

    print('moving stage')    
    relP = [10,0,0]
    stage.setParameter('position',stage.position + relP)

    stage.flagLoop.wait()

    print(f'new stage position {stage.position} ')

    stage.disconnect()
    

