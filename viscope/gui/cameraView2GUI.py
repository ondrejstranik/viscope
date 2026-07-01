"""
Camera viewer GUI using pyqtgraph ImageView.

Displays a live camera image with a custom black-to-blue colour map and
shows pixel coordinates and value under the mouse cursor.
"""
#%%
#import napari
import pyqtgraph as pg

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from viscope.gui.baseGUI import BaseGUI
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
    
        # set color map - min/max blue/red
        #lut = np.linspace(0, 255, 256, dtype=np.ubyte)
        #lut = np.stack([lut, lut, lut], axis=1)
        #lut[0]   = [255, 0, 0]
        #lut[255] = [0, 0, 255]
        #self.viewer.getImageItem().setLookupTable(lut)


        positions = np.array([0.0,0.99, 1.0])

        colors = np.array([
            [0,0,0],                # red  (low)
            [255, 255, 255],    # gray (middle)
            [0, 0, 255]         # blue (high)
        ], dtype=np.ubyte)

        cmap = pg.ColorMap(positions, colors)

        #cmap = pg.colormap.get('CET-D3')
        self.viewer.setColorMap(cmap)

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
        """Update the pixel-value label when the mouse moves over the image."""
        pos = evt[0]
        if self.view.sceneBoundingRect().contains(pos):
            self.last_mouse_pos = pos
            self.update_label()

    def image_changed(self):
        """Refresh the pixel-value label after a new image is set."""
        self.update_label()

    def update_label(self):
        """Write current mouse position and pixel value to the status label."""
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



    def setDevice(self, device):
        """Attach a camera device and connect its worker signal to the GUI refresh."""
        super().setDevice(device)
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


