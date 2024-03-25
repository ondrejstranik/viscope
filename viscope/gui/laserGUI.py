'''
class for seting laser parameters
'''
import napari
from magicgui import magicgui
from typing import Annotated
from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

class LaserGUI(BaseGUI):
    ''' main class to control laser'''

    DEFAULT = {'nameGUI': 'Laser',
                'napariViewer': False}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterLaserGui = None

        # prepare the gui of the class
        LaserGUI.__setWidget(self)        

    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui(
                power={'widget_type': "FloatSlider", 'min': 0, 'max': 1.3} 
        )
        def parameterLaserGui(
            power = 0.0,
            emission = False,
            ):
            self.device.setParameter('keySwitch',emission)
            self.device.setParameter('power',power)

            power = self.device.getParameter('power')
            emission = self.device.getParameter('keySwitch')

        # add widget parameterCameraGui 
        self.parameterLaserGui = parameterLaserGui
        self.dw =self.vWindow.addParameterGui(self.parameterLaserGui,name=self.DEFAULT['nameGUI'])


    def setDevice(self,device):
        ''' set the laser '''

        super().setDevice(device)

        # set gui parameters
        self.parameterLaserGui.power.value = self.device.getParameter('power')
        self.parameterLaserGui.emission.value = self.device.getParameter('keySwitch')
        self.dw.setWindowTitle(self.device.name)

if __name__ == "__main__":
        from viscope.instrument.virtual.virtualLaser import VirtualLaser
        from viscope.main import Viscope


        print('starting laser')
        laser = VirtualLaser()
        laser.connect()

        viscope = Viscope()
        viewerLaser  = LaserGUI(viscope)
        viewerLaser.setDevice(laser)
        viscope.run()

        laser.disconnect()


