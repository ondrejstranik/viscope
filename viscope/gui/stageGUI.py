'''
class for live viewing spectral images
'''
#%%
import napari
from magicgui import magicgui
from typing import Annotated, Literal

from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI

import numpy as np

class StageGUI(BaseGUI):
    ''' main class to control stage'''

    DEFAULT = {'nameGUI': 'Stage',
                'napariViewer': False}


    def __init__(self, viscope, vWindow, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, vWindow, **kwargs)

        # widget
        self.parameterStageGui = None

        # prepare the gui of the class
        StageGUI.__setWidget(self) 


    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui()
        def parameterStageGui(
            relX: Annotated[int, {'widget_type': "Slider", 'min': -10, 'max': 10}] = 0,
            absX: Annotated[int, {'widget_type': "LineEdit"}] = None,
            relY: Annotated[int, {'widget_type': "Slider", 'min': -10, 'max': 10}] = 0,
            absY: Annotated[int, {'widget_type': "LineEdit"}] = None,
            relZ: Annotated[int, {'widget_type': "Slider", 'min': -10, 'max': 10}] = 0,
            absZ: Annotated[int, {'widget_type': "LineEdit"}] = None
            ):
            
            # allow for absolute entry as well
            try:
                if int(absX) != self.device.position[0]:
                    relX = int(absX) - self.device.position[0]
                if int(absY) != self.device.position[1]:
                    relY = int(absY) - self.device.position[1]
                if int(absZ) != self.device.position[2]:
                    relZ = int(absZ) - self.device.position[2]
            except:
                print('input invalid value in stage')

            relP = [relX,relY,relZ]

            self.device.setParameter('position',self.device.position + relP)
            
            # after the movement update the absolut values
            self.parameterStageGui.absX.value = self.device.position[0]
            self.parameterStageGui.absY.value = self.device.position[1]
            self.parameterStageGui.absZ.value = self.device.position[2]

        # adding keybinding for napari
        if False:
        
        #if isinstance(self.viewer,napari.Viewer):
            self.viewer.bind_key('Left')(lambda x: self.parameterStageGui(relX=-1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Right')(lambda x: self.parameterStageGui(relX=1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Up')(lambda x: self.parameterStageGui(relY=1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Down')(lambda x: self.parameterStageGui(relY=-1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('PageUp')(lambda x: self.parameterStageGui(relZ=1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('PageDown')(lambda x: self.parameterStageGui(relZ=-1) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-Left')(lambda x: self.parameterStageGui(relX=-10) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-Right')(lambda x: self.parameterStageGui(relX=10) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-Up')(lambda x: self.parameterStageGui(relY=10) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-Down')(lambda x: self.parameterStageGui(relY=-10) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-PageUp')(lambda x: self.parameterStageGui(relZ=10) if self.dockWidgetParameter.underMouse()==True else None)
            self.viewer.bind_key('Shift-PageDown')(lambda x: self.parameterStageGui(relZ=-10) if self.dockWidgetParameter.underMouse()==True else None)

        # add widget parameterCameraGui 
        self.parameterStageGui = parameterStageGui
        self.addParameterGui(self.parameterStageGui,name=self.DEFAULT['nameGUI'])

    def setDevice(self,device):
        ''' set the stage '''
        super().setDevice(device)

        # update Gui
        #get the position of the stage
        myXYZ = self.device.position
        self.parameterStageGui.absX.value = myXYZ[0]
        self.parameterStageGui.absY.value = myXYZ[1]
        self.parameterStageGui.absZ.value = myXYZ[2]

if __name__ == "__main__":
        from viscope.instrument.virtual.virtualStage import VirtualStage
        from viscope.main.baseMain import BaseMain

        print('starting stage')
        stage = VirtualStage()
        stage.connect()

        print('starting main event loop')
        viscope = BaseMain(True)
        viewerStage  = StageGUI(viscope,viscope.vWindow)
        viewerStage.setDevice(stage)
        viscope.run()

        stage.disconnect()


