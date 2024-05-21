''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_BaseGUI():
    ''' check if base gui is working '''
    from viscope.main import viscope
    from viscope.gui.baseGUI import BaseGUI

    base = BaseGUI(viscope)
    viscope.run()



@pytest.mark.GUI
def test_CameraGUI():
    ''' check if gui works'''
    from viscope.gui.cameraGUI import CameraGUI
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import viscope

    camera = VirtualCamera(name='camera1')
    camera.connect()

    newGUI  = CameraGUI(viscope)
    newGUI.setDevice(camera)
    viscope.run()

    camera.disconnect()

@pytest.mark.GUI
def test_CameraViewGUI():
    ''' check if gui works'''
    from viscope.gui.cameraViewGUI import CameraViewGUI
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import viscope

    camera = VirtualCamera(name='camera1')
    camera.connect()
    camera.setParameter('threadingNow',True)

    newGUI  = CameraViewGUI(viscope)
    newGUI.setDevice(camera)
    viscope.run()

    camera.disconnect()


@pytest.mark.GUI
def test_PumpGUI():
    ''' check if gui works '''
    from viscope.gui.pumpGUI import PumpGUI   
    from viscope.instrument.virtual.virtualPump import VirtualPump
    from viscope.main import viscope


    print('starting pump')
    pump = VirtualPump()
    pump.connect()

    viewer  = PumpGUI(viscope)
    viewer.setDevice(pump)
    viscope.run()

    pump.disconnect()    
