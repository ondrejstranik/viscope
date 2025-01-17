from magicgui import magicgui
from typing import Annotated
from qtpy.QtWidgets import QShortcut
from qtpy.QtGui import QKeySequence
from viscope.gui.baseGUI import BaseGUI

class FilterChangerGUI(BaseGUI):
    ''' Main class to control the filter changer GUI with a slider '''

    DEFAULT = {'nameGUI': 'FilterChanger'}


    def __init__(self, viscope, **kwargs):
        ''' Initialize the class '''
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterFilterChangerGui = None

        # Prepare the GUI of the class
        FilterChangerGUI.__setWidget(self)


    def __setWidget(self):
        ''' Prepare the GUI '''
        @magicgui()
        def parameterFilterChangerGui(
            position: Annotated[int, {'widget_type': "FloatSlider", 'min': 1, 'max': 6, 'step': 1, 'label': 'Position'}] = 1,
        ):
            ''' Handle filter position change '''
            self.device.setParameter('position', int(position))
            #print(f"Filter moved to position {int(position)}")

        # Add widget parameterFilterChangerGui
        self.parameterFilterChangerGui = parameterFilterChangerGui
        self.dw = self.vWindow.addParameterGui(self.parameterFilterChangerGui, name=self.DEFAULT['nameGUI'])

    def setDevice(self, device):
        ''' Set the filter changer device '''
        super().setDevice(device)

        # Initialize position in the GUI
        self.parameterFilterChangerGui.position.value = self.device.getParameter('position')
        self.dw.setWindowTitle(self.device.name)

if __name__ == "__main__":
    from viscope.instrument.virtual.virtualFilterChanger import VirtualFilterChanger
    from viscope.main import VISCOPE

    # Initialize filter changer and connect
    filter_changer = VirtualFilterChanger()
    filter_changer.connect()

    viscope = VISCOPE()
    viewerFilterChanger = FilterChangerGUI(viscope)
    viewerFilterChanger.setDevice(filter_changer)
    viscope.run()

    filter_changer.disconnect()
