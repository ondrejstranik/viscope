import time
import numpy as np

from viscope.instrument.base.baseInstrument import BaseInstrument, ThreadFlag

class BaseFilterChanger(BaseInstrument):
    ''' Main class to control a virtual filter changer '''

    DEFAULT = {'name': 'baseFilterChanger',
               'position': 1,
               'num_positions': 6}

    def __init__(self, name=DEFAULT['name'], num_positions=DEFAULT['num_positions'], *args, **kwargs):
        ''' Initialize the filter changer '''
        super(BaseFilterChanger, self).__init__(name=name, *args, **kwargs)

        self.num_positions = num_positions
        self.position = self.DEFAULT['position']  # Default to position 1
        self.flagSetPosition = ThreadFlag()

    def _getPosition(self):
        ''' Get the current filter position '''
        return self.position

    def _setPosition(self, positionNumber):
        ''' Move to a new filter position '''
        if 1 <= positionNumber <= self.num_positions:
            self.position = positionNumber
            print(f"filter moved to position {positionNumber}")
        else:
            raise ValueError(f"position {positionNumber} is out of range (1-{self.num_positions}).")

    def setParameter(self, name, value):
        ''' Set parameters of the filter changer '''
        super().setParameter(name, value)

        if name == 'position':
            if self.worker is not None:
                self.flagSetPosition.set(value)
            else:
                self._setPosition(value)

        #if name == 'num_positions':
            #self.num_positions = value

    def getParameter(self, name):
        ''' Get parameter values '''
        _value = super().getParameter(name)
        if _value is not None:
            return _value

        if name == 'position':
            return self._getPosition()

        if name=='num_positions':
            return self.num_positions

    def loop(self):
        ''' Infinite loop for thread handling '''
        while True:
            if self.flagSetPosition.is_set():
                _newPosition = self.flagSetPosition.getLastData()
                self._setPosition(_newPosition)
                self.flagSetPosition.clear()
                self.flagLoop.set()
                yield
            time.sleep(0.03)

if __name__ == '__main__':

    filter_changer = BaseFilterChanger()
    filter_changer.connect()
    filter_changer.setParameter('threadingNow', True)
    print(f'worker {filter_changer.worker}')
    # Example usage
    filter_changer = BaseFilterChanger()

    # Simulate moving to a specific position
    try:
        filter_changer.setParameter('position', 3)
        print(f"Current position: {filter_changer.getParameter('position')}")

        filter_changer.setParameter('position', 7)  # This will raise an exception
    except ValueError as e:
        print(e)
