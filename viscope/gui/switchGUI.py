'''
class for mirror control 
'''
import napari
from magicgui import magicgui
from typing import Annotated, Literal

from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtCore import Qt

from viscope.gui.baseGUI import BaseGUI

import numpy as np

class SwitchGUI(BaseGUI):
    ''' main class to control discrete switch'''

    DEFAULT = {'nameGUI': 'Switch'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterSwitchGui = None

        # prepare the gui of the class
        SwitchGUI.__setWidget(self)  

    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui(auto_call=True, switchPosition = {'widget_type': 'Slider'})
        def parameterSwitchGui(switchPosition):
            self.device.setParameter('position',switchPosition)
            self.parameterSwitchGui.switchPosition.label = self.device.positionList[switchPosition]

        # add widget parameterCameraGui 
        self.parameterSwitchGui = parameterSwitchGui
        self.dw = self.vWindow.addParameterGui(self.parameterSwitchGui,name=self.DEFAULT['nameGUI'])


    def setDevice(self,device):
        ''' set the switcher  in the qui'''
        super().setDevice(device)

        # update Gui
        self.parameterSwitchGui.switchPosition.max = len(self.device.positionList) - 1
        self.parameterSwitchGui.switchPosition.min = 0
        self.parameterSwitchGui.switchPosition.value = self.device.getParameter('position')
        self.parameterSwitchGui.switchPosition.label = self.device.positionList[self.device.getParameter('position')]

        self.dw.setWindowTitle(self.device.name)

if __name__ == "__main__":
        from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

        from viscope.main import VISCOPE

        print('starting switch')
        switch = VirtualSwitch()
        switch.connect()
        #switch.setParameter('position',0)

        viscope = VISCOPE()
        viewerSwitch  = SwitchGUI(viscope)
        viewerSwitch.setDevice(switch)
        
        viscope.run()


