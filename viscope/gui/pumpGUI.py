'''
class for seting laser parameters
'''
import napari
from magicgui import magicgui
from typing import Annotated
from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

#TODO: finish the class
class PumpGUI(BaseGUI):
    ''' main class to control pump'''

    DEFAULT = {'nameGUI': 'Pump'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterPumpGui = None

        # prepare the gui of the class
        PumpGUI.__setWidget(self)        

    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui(auto_call=True,
                flowRate={'widget_type': "FloatSlider", 'min': -100, 'max': 100} 
        )
        def parameterPumpGui(
            flowRate = 0.0,
            flow = False,
            ):
            if self.device.getParameter('flowRate') != flowRate:
                self.device.setParameter('flowRate',flowRate)
            if self.device.getParameter('flow') != flow:
                self.device.setParameter('flow',flow)

            self.parameterPumpGui._auto_call = False
            self.parameterPumpGui.flowRate.value  = self.device.getParameter('flowRate')
            self.parameterPumpGui.flow.value = self.device.getParameter('flow')
            self.parameterPumpGui._auto_call = True


        # add widget parameterCameraGui 
        self.parameterPumpGui = parameterPumpGui
        self.dw =self.vWindow.addParameterGui(self.parameterPumpGui,name=self.DEFAULT['nameGUI'])


    def setDevice(self,device):
        ''' set the pump '''

        super().setDevice(device)

        # set gui parameters
        self.parameterPumpGui._auto_call = False
        self.parameterPumpGui.flowRate.value = self.device.getParameter('flowRate')
        self.parameterPumpGui.flow.value = self.device.getParameter('flow')
        self.parameterPumpGui._auto_call = True

        self.dw.setWindowTitle(self.device.name)


if __name__ == "__main__":
    pass


