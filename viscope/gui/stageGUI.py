'''
class for live viewing spectral images
'''
#%%
import napari
from magicgui import magicgui
from typing import Annotated, Literal

from qtpy.QtWidgets import QLabel, QSizePolicy, QShortcut, QMessageBox
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence
from viscope.gui.baseGUI import BaseGUI

import numpy as np

class StageGUI(BaseGUI):
    ''' main class to control stage'''

    DEFAULT = {'nameGUI': 'Stage'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # widget
        self.parameterStageGui = None

        # prepare the gui of the class
        StageGUI.__setWidget(self) 


    def _shortcutCommand(self,axis=None,direction='+'):
        ''' command for the short cut'''

        if self.parameterStageGui.native.underMouse()==False: return
        df = -1 if direction == '-' else 1
        if axis == 'X':  
            self.parameterStageGui(relX=df*np.abs(self.parameterStageGui.relX.value),relY=0,relZ=0)             
        if axis == 'Y':  
            self.parameterStageGui(relY=df*np.abs(self.parameterStageGui.relY.value),relX=0,relZ=0)             
        if axis == 'Z':  
            self.parameterStageGui(relZ=df*np.abs(self.parameterStageGui.relZ.value),relX=0,relY=0)             
           


    def __setWidget(self):
        ''' prepare the gui '''
        @magicgui()
        def parameterStageGui(
            relX: Annotated[float, {'widget_type': "FloatSlider", 'min': -1, 'max': 1}] = 0,
            absX: Annotated[float, {'widget_type': "LineEdit"}] = None,
            relY: Annotated[float, {'widget_type': "FloatSlider", 'min': -1, 'max': 1}] = 0,
            absY: Annotated[float, {'widget_type': "LineEdit"}] = None,
            relZ: Annotated[float, {'widget_type': "FloatSlider", 'min': -1, 'max': 1}] = 0,
            absZ: Annotated[float, {'widget_type': "LineEdit"}] = None
            ):
            
            # allow for absolute entry as well
            #try:
            #if float(absX) != self.device.position[0]:
            #    relX = float(absX) - self.device.position[0]
            #if float(absY) != self.device.position[1]:
            #    relY = float(absY) - self.device.position[1]
            #if float(absZ) != self.device.position[2]:
            #    relZ = float(absZ) - self.device.position[2]
            ##except:
            ##    print('input invalid value in stage')

            relP = [relX,relY,relZ]

            currentPosition = self.device.getParameter('position')

            self.device.setParameter('position',currentPosition + relP)
            
            # after the movement update the absolute values
            self.parameterStageGui.absX.value = self.device.position[0]
            self.parameterStageGui.absY.value = self.device.position[1]
            self.parameterStageGui.absZ.value = self.device.position[2]

        # add widget parameterCameraGui 
        self.parameterStageGui = parameterStageGui
        self.dw = self.vWindow.addParameterGui(self.parameterStageGui,name=self.DEFAULT['nameGUI'])

        # add keybinding
        QShortcut(QKeySequence('X'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='X',direction='+'))
        QShortcut(QKeySequence('Ctrl+X'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='X',direction='-'))
        QShortcut(QKeySequence('Y'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='Y',direction='+'))
        QShortcut(QKeySequence('Ctrl+Y'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='Y',direction='-'))
        QShortcut(QKeySequence('Z'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='Z',direction='+'))
        QShortcut(QKeySequence('Ctrl+Z'), self.vWindow).activated.connect(
            lambda: self._shortcutCommand(axis='Z',direction='-'))
      




    def setDevice(self,device):
        ''' set the stage '''
        super().setDevice(device)

        # update Gui
        #get the position of the stage
        myXYZ = self.device.position
        self.parameterStageGui.absX.value = myXYZ[0]
        self.parameterStageGui.absY.value = myXYZ[1]
        self.parameterStageGui.absZ.value = myXYZ[2]

        self.dw.setWindowTitle(self.device.name)

if __name__ == "__main__":
        from viscope.instrument.virtual.virtualStage import VirtualStage
        from viscope.main import Viscope

        print('starting stage')
        stage = VirtualStage()
        stage.connect()

        viscope = Viscope()
        viewerStage  = StageGUI(viscope)
        viewerStage.setDevice(stage)
        viscope.run()

        stage.disconnect()


