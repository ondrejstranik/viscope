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

def test_CameraViewGUI():
    ''' check if gui works'''
    from viscope.gui.cameraViewGUI import CameraViewGUI
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope

    camera = VirtualCamera(name='camera1')
    camera.connect()
    camera.setParameter('threadingNow',True)

    viscope = Viscope()
    newGUI  = CameraViewGUI(viscope)
    newGUI.setDevice(camera)
    viscope.run()

    camera.disconnect()


