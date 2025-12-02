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
def test_napariViewer():
    ''' check if napariGUI is working '''
    from viscope.gui.napariViewer.napariViewer import NapariViewer
    import napari
    import numpy as np

    viewer = NapariViewer()
    viewer.add_image(np.random.rand(100,100))
    napari.run()


@pytest.mark.GUI
def test_napariGUI():
    ''' check if napariGUI is working '''
    from viscope.main import viscope
    from viscope.gui.napariGUI import NapariGUI

    newGUI = NapariGUI(viscope)
    viscope.run()

@pytest.mark.GUI
def test_napariGUI2():
    ''' check if two napari gui are working properly - buttom issue'''
    from viscope.main import viscope
    from viscope.gui.napariGUI import NapariGUI
    import numpy as np

    newGUI = NapariGUI(viscope)
    newGUI.viewer.add_image(np.random.rand(100,100))
    newGUI2 = NapariGUI(viscope,vWindow='new')
    newGUI2.viewer.add_image(np.random.rand(100,100))
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

@pytest.mark.GUI
def test_allDeviceGUI():

    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualPump import VirtualPump

    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    stage1 = VirtualStage(name='Stage1')
    stage1.connect()
    stage2 = VirtualStage(name='Stage2')
    stage2.connect()
    laser1 = VirtualLaser(name='Laser1')
    laser1.connect()
    switch1 = VirtualSwitch(name='Switch1')
    switch1.connect()
    camera1 = VirtualCamera(name='Camera1')
    camera1.connect()
    camera1.setParameter('threadingNow',True)
    camera2 = VirtualCamera(name='Camera2')
    camera2.connect()
    camera2.setParameter('threadingNow',True)
    pump1 = VirtualPump(name='Pump1')
    pump1.connect()

    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([stage1,stage2,laser1,switch1,camera1,camera2,pump1])
    viscope.run()

    print('disconnecting')
    stage1.disconnect()
    stage2.disconnect()
    laser1.disconnect()
    switch1.disconnect()
    camera1.disconnect()
    camera2.disconnect()
    pump1.disconnect()

@pytest.mark.GUI
def test_switchGUI():

    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
    from viscope.main import viscope
    from viscope.gui.switchGUI import SwitchGUI

    switch = VirtualSwitch(name='Switch1')
    switch.connect(initialPosition=1)
    switch.positionList = ['up','middle','down']


    swGui  = SwitchGUI(viscope)
    swGui.setDevice(switch)
    viscope.run()

    switch.disconnect()


@pytest.mark.GUI
def test_ADetectorGUI():

    from viscope.instrument.virtual.virtualADetector import VirtualADetector
    from viscope.instrument.aDetectorProcessor import ADetectorProcessor
    from viscope.main import viscope
    from viscope.gui.aDetectorGUI import ADetectorGUI
    from viscope.gui.aDetectorViewGUI import ADetectorViewGUI

    aDet = VirtualADetector(name='ADetector')
    aDet.connect()
    aDet.setParameter('threadingNow',True)

    aDProc = ADetectorProcessor(name='ADetectorProcessor')
    aDProc.connect(aDetector=aDet)
    aDProc.setParameter('threadingNow',True)

    adGui  = ADetectorGUI(viscope)
    adGui.setDevice(aDet)

    advGui  = ADetectorViewGUI(viscope)
    advGui.setDevice(aDProc)

    viscope.run()

    aDProc.disconnect()

    aDet.disconnect()
   