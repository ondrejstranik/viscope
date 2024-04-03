''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_CameraGUI():
    ''' check if gui works'''
    from viscope.gui.cameraGUI import CameraGUI
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope

    camera = VirtualCamera(name='camera1')
    camera.connect()

    viscope = Viscope()
    newGUI  = CameraGUI(viscope)
    newGUI.setDevice(camera)
    viscope.run()

    camera.disconnect()



