''' test for each class'''

def test_VirtualCamera():
    ''' check if the images are obtained'''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    import time
    import numpy as np
    
    cam = VirtualCamera()
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrame', 1)
    cam.setParameter('threadingNow',True)

    cTime = time.time()
    while time.time()-cTime < 3:    
        if cam.flagLoop.is_set():
            pixelSum = np.sum(cam.rawImage)
            print(f'sum of the pixels {pixelSum}')
            assert pixelSum > 0
            cam.flagLoop.clear()

    cam.disconnect()

def test_VirtualLaser():
    ''' check if laser parameters are obtained '''
    from viscope.instrument.virtual.virtualLaser import VirtualLaser

    laser = VirtualLaser()
    laser.connect()
    print(f'laser {laser.getParameter("power")}, KeySwitch {laser.getParameter("keySwitch")}')

    laser.disconnect()

def test_VirtualStage():
    ''' check if stage virtually moves'''

    from viscope.instrument.virtual.virtualStage import VirtualStage

    stage = VirtualStage(threading=True)
    stage.connect()
    stage.setParameter('threadingNow',True)

    print(f'stage position {stage.position}')

    print('moving stage')    
    relP = [10,0,0]
    stage.setParameter('position',stage.position + relP)

    stage.flagLoop.wait()
    print(f'new stage position {stage.position} ')

    stage.disconnect()

def test_VirtualSwitch():
    ''' check if switch virtually moves'''

    from viscope.instrument.virtual.virtualSwitch import VirtualSwitch

    switch = VirtualSwitch()
    switch.connect()
    switch.setParameter('threadingNow',True)

    switch.setParameter('position',1)
    print( f'flagSetPosition {switch.flagSetPosition.is_set()}')

    switch.flagLoop.wait()
    switch.flagLoop.clear()    
    #print(f'switch position {switch.getParameter("positionList")[switch.getParameter("position")]}')
    print(f'switch position {switch.getParameter("position")}')
    switch.setParameter('position',0)
    switch.flagLoop.wait()
    switch.flagLoop.clear()
    #print(f'switcher position {switch.getParameter("positionList")[switch.getParameter("position")]}')
    print(f'switch position {switch.getParameter("position")}')
    
    switch.disconnect()    


def test_VirtualADetector():
    ''' check if the data are obtained'''
    from viscope.instrument.virtual.virtualADetector import VirtualADetector
    import time
    import numpy as np
    
    det = VirtualADetector()
    det.connect()
    det.setParameter('threadingNow',True)
    det.startAcquisition()

    cTime = time.time()
    while time.time()-cTime < 3:    
        if det.flagLoop.is_set():
            data = det.getStack()
            print(f'stack \n {data}')

    det.stopAcquisition()
    det.disconnect()