'''
class for live viewing spectral images
'''
#%%
#import napari
from magicgui import magicgui
#from typing import Annotated, Literal

import pyqtgraph as pg

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
#from qtpy.QtWidgets import QLabel, QSizePolicy
#from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI
from timeit import default_timer as timer
import numpy as np


class CameraView2GUI(BaseGUI):
    ''' main class to show images of a camera,
    uses pyqtgraph's imageView'''

    DEFAULT = {'nameLayer': 'Camera',
               'nameGUI': 'Camera'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # viewer parameters
        # last mouse position
        self.last_mouse_pos = None


        # prepare the gui of the class
        CameraView2GUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        central = QWidget()
        layout = QVBoxLayout(central)
        # add graph
        self.viewer = pg.ImageView()
        layout.addWidget(self.viewer)
        # add label
        self.label = QLabel("Value:")
        layout.addWidget(self.label)

        self.vWindow.addMainGUI(central, name=self.DEFAULT['nameGUI'])

        self.view = self.viewer.getView()

        # Track mouse
        self.proxy = pg.SignalProxy(
            self.view.scene().sigMouseMoved,
            rateLimit=60,
            slot=self.mouse_moved
        )

        # 🔥 IMPORTANT: update label when image changes
        self.viewer.getImageItem().sigImageChanged.connect(
            self.image_changed
        )

    def mouse_moved(self, evt):
        pos = evt[0]
        if self.view.sceneBoundingRect().contains(pos):
            self.last_mouse_pos = pos
            self.update_label()

    def image_changed(self):
        # Called whenever setImage() is used
        self.update_label()

    def update_label(self):
        if self.last_mouse_pos is None:
            return

        mouse_point = self.view.mapSceneToView(self.last_mouse_pos)
        x = int(mouse_point.x())
        y = int(mouse_point.y())

        image = self.viewer.image
        if image is None:
            return

        if (
            0 <= x < image.shape[0] and
            0 <= y < image.shape[1]
        ):
            value = image[x, y]
            self.label.setText(f"x={x}, y={y}, value={value:.4f}")



    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)
        self.vWindow.setWindowTitle(self.device.name)


    def updateGui(self):
        ''' update the data in gui '''
        # napari
        try:
            self.viewer.setImage(self.device.rawImage.T,
                                    autoRange=False,
                                    autoLevels=True)
        except Exception as e:
            print(f'error in updateGui in cameraView2GUI: {e}')


if __name__ == "__main__":
    pass


