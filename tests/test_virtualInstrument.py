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


