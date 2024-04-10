''' test for each class'''

def test_twoCameraMicroscope():
    ''' test that the twoCameraMicroscope is working'''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualStage import VirtualStage
    from viscope.instrument.virtual.virtualLaser import VirtualLaser
    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

    from viscope.virtualSystem.twoCameraMicroscope import TwoCameraMicroscope

    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI


    camera1 = VirtualCamera('camera1')
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    camera2 = VirtualCamera('camera2')
    camera2.connect()
    camera2.setParameter('threadingNow',True)

    stage = VirtualStage('stage')
    stage.connect()

    laser = VirtualLaser('laser')
    laser.connect()
    laser.setParameter("power",1)
    laser.setParameter("keySwitch",True)

    switch = VirtualSwitch('switch')
    switch.setParameter('positionList',['up', 'middle', 'down'])
    switch.connect(initialPosition=1)

    vM = TwoCameraMicroscope()
    vM.setVirtualDevice(camera1=camera1, camera2=camera2, laser= laser,
    switch= switch, stage=stage)
    vM.connect()

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1,camera2,laser,switch,stage])
    
    viscope.run()

    camera1.disconnect()
    camera2.disconnect()
    laser.disconnect()
    stage.disconnect()
    switch.disconnect()        

    vM.disconnect()

def test_simpleMicroscope():
    ''' test that the simpleMicroscope is working'''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.virtualSystem.simpleMicroscope import SimpleMicroscope
    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    vM = SimpleMicroscope()
    vM.setVirtualDevice(camera1)
    vM.connect()

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1])
    
    viscope.run()

    camera1.disconnect()
    vM.disconnect()

