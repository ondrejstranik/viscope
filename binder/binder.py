''' standalone script version of tests/test_virtualMicroscope.py::test_twoCameraMicroscope
for running the virtual two-camera microscope demo on https://mybinder.org/ '''

from viscope.instrument.virtual.virtualCamera import VirtualCamera
from viscope.instrument.virtual.virtualStage import VirtualStage
from viscope.instrument.virtual.virtualLaser import VirtualLaser
from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

from viscope.virtualSystem.twoCameraMicroscope import TwoCameraMicroscope

from viscope.main import viscope
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

viewer  = AllDeviceGUI(viscope)
viewer.setDevice([camera1,camera2,laser,switch,stage])

viscope.run()

camera1.disconnect()
camera2.disconnect()
laser.disconnect()
stage.disconnect()
switch.disconnect()

vM.disconnect()
