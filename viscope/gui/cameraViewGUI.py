'''
class for live viewing spectral images
'''
#%%
#import napari
import logging
from magicgui import magicgui
#from typing import Annotated, Literal

#from qtpy.QtWidgets import QLabel, QSizePolicy
#from qtpy.QtCore import Qt
from viscope.gui.baseGUI import BaseGUI
from timeit import default_timer as timer
from viscope.gui.napariViewer.napariViewer import NapariViewer
import numpy as np

logger = logging.getLogger(__name__)


class CameraViewGUI(BaseGUI):
    ''' main class to show images of a camera'''

    DEFAULT = {'nameLayer': 'Camera',
               'nameGUI': 'Camera'}


    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.rawLayer = None

        # prepare the gui of the class
        CameraViewGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        # create napari viewer
        self.viewer = NapariViewer(show=False)
        # napari can not work in a dock Window,
        # therefore it must run in the main Window
        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

        # set new napari layer
        self.rawLayer = self.viewer.add_image(np.ones((2,2)),
                        rgb=False, colormap="gray",
                        name='Raw',  blending='additive')
        # keep the contrast limits auto-scaling to the data on every update
        self.rawLayer._keep_auto_contrast = True
        # best-effort: also press the actual 'continuous' auto-contrast
        # button so its icon in the layer controls panel matches the state
        # set above. The path into napari's private Qt widgets differs by
        # napari version (e.g. controls.autoScaleBar pre-0.6 vs.
        # controls._contrast_limits_control.auto_scale_bar from 0.6.6), so
        # don't let a lookup failure on either break the auto-contrast itself
        try:
            controls = self.viewer.window._qt_viewer.controls.widgets[self.rawLayer]
            autoScaleBar = getattr(controls, 'autoScaleBar', None) or controls._contrast_limits_control.auto_scale_bar
            autoScaleBar._auto_btn.setChecked(True)
        except (KeyError, AttributeError):
            pass

    def setDevice(self,device):
        super().setDevice(device)
        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)
        self.vWindow.setWindowTitle(self.device.name)


    def updateGui(self):
        ''' update the data in gui '''
        # napari
        try:
            resetView = self.rawLayer.data.shape != self.device.rawImage.shape
            self.rawLayer.data = self.device.rawImage
            if resetView:
                self.viewer.reset_view()
        except Exception:
            logger.exception('error in updateGui in cameraViewGUI')


if __name__ == "__main__":
    pass


