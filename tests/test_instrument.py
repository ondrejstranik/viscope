''' camera unitest '''

import pytest
from viscope.instrument.virtual.virtualCamera import VirtualCamera
from viscope.instrument.base.baseCamera import BaseCamera

CAMERA_LIST = [VirtualCamera,BaseCamera] 
PARAMETER_VALUE_LIST =  [
    ("exposureTime",300),
    ("nFrame",1)
]

@pytest.fixture(params=CAMERA_LIST)
def setCamera(request):
    cam = request.param()
    cam.connect()
    yield cam
    cam.disconnect()

@pytest.mark.parametrize("parameter, value",PARAMETER_VALUE_LIST)
def test_cameraParameterCheck(parameter, value, setCamera):
    cam = setCamera
    cam.setParameter(parameter,value)
    assert cam.getParameter(parameter) == value





