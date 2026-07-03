# Examples

## Same code, virtual camera vs. real camera

This is the practical payoff of the [View / Model / Controller
split](architecture.md#mvc-overview): application code is written once
against the Model's device interface, and swapping a virtual device for a
real one (or back) doesn't touch that code.

### Virtual camera (`test_simpleSpectralMicroscope`)

```python
from viscope.instrument.virtual.virtualCamera import VirtualCamera
from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI
from spectralCamera.virtualSystem.simpleSpectralMicroscope import SimpleSpectralMicroscope

# set instruments
camera1 = VirtualCamera()
camera1.connect()
camera1.setParameter('threadingNow', True)

# set forward model -- simulates sensor data for the virtual camera
vM = SimpleSpectralMicroscope()
vM.setVirtualDevice(camera1)
vM.connect()

# set GUI
viewer = AllDeviceGUI(viscope)
viewer.setDevice([camera1])

# run GUI
viscope.run()

# disconnect devices
camera1.disconnect()
vM.disconnect()
```

### Real camera (`test_simpleSpectralMicroscopeRGBCamera`)

```python
from spectralCamera.instrument.camera.webCamera.webCamera import WebCamera
from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI

# set instruments
camera1 = WebCamera()
camera1.connect()
camera1.setParameter('threadingNow', True)

# set GUI
viewer = AllDeviceGUI(viscope)
viewer.setDevice([camera1])

# run GUI
viscope.run()

# disconnect devices
camera1.disconnect()
```

### What actually differs

Once `camera1` exists, both tests do **exactly the same thing** with it --
`connect()`, `setParameter('threadingNow', True)`, hand it to
`AllDeviceGUI`, run the event loop, `disconnect()`. Only two things change:

1. **The camera class**: `VirtualCamera` vs. `WebCamera`. Both are **Model**
   classes -- both extend the same
   [`BaseCamera`](reference/instrument/base/baseCamera.md) interface -- so
   `AllDeviceGUI` doesn't need to know or care which one it got.
   `WebCamera` is a *Real Device Implementation*: internally it wraps
   `cv2.VideoCapture` (OpenCV), which is the actual **Controller** here --
   the thing that talks to the physical hardware. `VirtualCamera` has no
   Controller at all; it just holds an in-memory array.
2. **The `SimpleSpectralMicroscope` (`vM`)**, created and connected only in
   the virtual case. This is the Virtual System Layer described in the
   [architecture overview](architecture.md) -- it exists purely to
   synthesize believable sensor data for a *virtual* camera. A real webcam
   produces its own data via `cv2`, so `test_simpleSpectralMicroscopeRGBCamera`
   skips creating and connecting a simulator entirely.

In MVC terms: the View (`AllDeviceGUI`) and the Model (`camera1`, via
`BaseCamera`) code paths never change. What changes is what actually
supplies the data underneath the Model object: a real Controller (`cv2`)
for `WebCamera`, or a Model-internal substitute (`SimpleSpectralMicroscope`)
for `VirtualCamera`.
