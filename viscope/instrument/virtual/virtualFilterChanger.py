import time

from viscope.instrument.base.baseFilterChanger import BaseFilterChanger
from viscope.instrument.base.baseInstrument import ThreadFlag

class VirtualFilterChanger(BaseFilterChanger):
    ''' Class to control a virtual filter changer '''

    DEFAULT = {
        **BaseFilterChanger.DEFAULT,
        'name': 'virtualFilterChanger',
        'initialPosition': 1,
        'switchingTime': 0.5,  # [s]
        'num_positions': 6  # Default number of filter positions
    }

    def __init__(self, name=DEFAULT['name'], num_positions=DEFAULT['num_positions'], *args, **kwargs):
        ''' Initialize the virtual filter changer '''
        super(VirtualFilterChanger, self).__init__(name=name, *args, **kwargs)

        self.num_positions = num_positions  # Number of filter positions
        self.flagSetParameter = ThreadFlag()

    def _setPosition(self, positionNumber):
        ''' Set the position in the virtual filter changer '''
        if 1 <= positionNumber <= self.num_positions:
            self.position = positionNumber
            time.sleep(VirtualFilterChanger.DEFAULT['switchingTime'])
            print(f"Filter moved to position {positionNumber}")
        else:
            raise ValueError(f"Position {positionNumber} is out of range (1-{self.num_positions}).")
        self.position = positionNumber
        time.sleep(VirtualFilterChanger.DEFAULT['switchingTime'])

    def setParameter(self, name, value):
        ''' Set parameters of the filter changer '''
        if name == 'position':
            if not (1 <= value <= self.num_positions):
                raise ValueError(f"Position {value} is out of range (1-{self.num_positions}).")
        super().setParameter(name, value)
        self.flagSetParameter.set(name)

    def connect(self, initialPosition=DEFAULT['initialPosition']):
        ''' Connect the virtual filter changer '''
        super().connect()
        self.setParameter('position', initialPosition)


if __name__ == '__main__':
    filter_changer = VirtualFilterChanger()
    filter_changer.connect()
    filter_changer.setParameter('threadingNow', True)

    try:
        filter_changer.setParameter('position', 2)
        # print(f 'filter_changer position {switch.getParameter("positionList")[switch.getParameter("position")]}')
        print(f'filter changer position: {filter_changer.getParameter("position")}')
        filter_changer.flagLoop.wait()
        filter_changer.flagLoop.clear()

        filter_changer.setParameter('position', 7)
    except ValueError as e:
        print(e)


    # print(f' filter changer {filterchanger.getParameter("positionList")[switch.getParameter("position")]}')
    #print(f'filter changer position: {filter_changer.getParameter("position")}')

    filter_changer.disconnect()