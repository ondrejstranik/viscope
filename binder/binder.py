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

vWindows = viscope.wManager.allWindows()
vWindows[0].setRegion('right')
viscope.wManager.setRegionRatio('right', 0.15)
# mybinder.org's remote desktop doesn't keep its taskbar's reserved space
# in sync with QScreen.availableGeometry(), so windows can end up placed
# behind it - reserve that space manually instead
viscope.wManager.setScreenMargin(bottom=40)


viscope.run()

camera1.disconnect()
camera2.disconnect()
laser.disconnect()
stage.disconnect()
switch.disconnect()

vM.disconnect()
