''' test for each class'''

def test_BaseCamera():
    ''' check if the images are obtained from BaseCamera'''    
    from viscope.instrument.base.baseCamera import BaseCamera
    import time

    cam = BaseCamera()
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrame', 1)
    cam.setParameter('threadingNow',True)

    cTime = time.time()
    while time.time()-cTime < 10:
        if cam.flagLoop.is_set():
            print(cam.rawImage)
            cam.flagLoop.clear()

    cam.disconnect()


def test_BaseInstrument():
    ''' check the threading of the base Instrument '''
    from viscope.instrument.base.baseInstrument import BaseInstrument

    base = BaseInstrument()
    base.connect()
    base.setParameter('threadingNow',True)
    for ii in range(5):
        base.flagLoop.wait()
        print('worker loop reported')
        print(f' data: {base.flagLoop.data}')
        base.flagLoop.clear()
    base.disconnect()


def test_BaseProcessor():
    ''' check if the base processor loop is working '''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.base.baseProcessor import BaseProcessor
    import time
    import numpy as np
    
    cam = VirtualCamera()
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrame', 1)
    cam.setParameter('threadingNow',True)

    pro = BaseProcessor()
    pro.connect(cam.flagLoop)
    pro.setParameter('threadingNow',True)

    time.sleep(3)

    pro.disconnect()
    cam.disconnect()


def test_BaseStage():
    ''' check if the base Stage is working '''
    from viscope.instrument.base.baseStage import BaseStage
    import time

    stage = BaseStage()

    stage.connect()
    stage.setParameter('threadingNow',True)

    cTime = time.time()

    ii = 0

    stage.flagLoop.set()
    while time.time()-cTime < 2:
        if stage.flagLoop.is_set():
            stage.flagLoop.clear()
            _position = stage.getParameter('position')
            print(f'stage position {_position}')
            ii += 10
            print(f'next move to {ii}')
            time.sleep(0.3)
            stage.setParameter('position',[ii,ii])

        time.sleep(.03)

    stage.disconnect()


def test_BaseLaser():
    ''' check the functionality of BaseLaser '''
    from viscope.instrument.base.baseLaser import BaseLaser

    laser = BaseLaser()
    laser.connect()
    print(f'laser {laser.getParameter("power")}, KeySwitch {laser.getParameter("keySwitch")}')
    laser.disconnect()

def test_BasePump():
    ''' check the functionality  of BasePump '''
    from viscope.instrument.base.basePump import BasePump
    import time

    pump = BasePump()
    pump.connect()

    print(f'pump flow: {pump.getParameter("flow")}')
    pump.setParameter('flow',10)
    print(f'pump flow: {pump.getParameter("flow")}')
    time.sleep(1)
    pump.setParameter('flow',0)
    print(f'pump flow: {pump.getParameter("flow")}')

    pump.disconnect()


def test_BaseSequencer():
    ''' check the functionality of the BaseSequencer'''
    from viscope.instrument.base.baseSequencer import BaseSequencer
    import time

    seq = BaseSequencer()
    seq.connect()
    seq.setParameter('threadingNow',True)

    print('wait till the sequencer thread it running')
    while not seq.worker.is_running:
        time.sleep(.1)        

    # waiting till sequencer is finished
    while seq.worker.is_running:
        time.sleep(.1)
    
    seq.disconnect()

def test_BaseSequencer_2():
    ''' check the functionality of the BaseSequencer- no treading'''
    from viscope.instrument.base.baseSequencer import BaseSequencer
    import time

    seq = BaseSequencer()
    seq.connect()

    # run the sequencer
    for _ in seq.loop():
        pass

    time.sleep(.1)
    
    seq.disconnect()    


def test_BaseSwitch():
    ''' test the functionality of BaseSwitch'''
    from viscope.instrument.base.baseSwitch import BaseSwitch

    switch = BaseSwitch()
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

def test_BaseDetector():
    ''' check the functionality  of BaseDetector '''
    from viscope.instrument.base.baseDetector import BaseDetector
    import time

    detector = BaseDetector()
    detector.connect()

    detector.startAcquisition()
    cTime = time.time()

    ii = 0

    while time.time()-cTime < 2:
        _dataStack = detector.getTestStack()
        print(f'dataStack: {_dataStack}\n')
        time.sleep(.03)

    detector.stopAcquisition()
    detector.disconnect()


