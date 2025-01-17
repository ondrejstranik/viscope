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

#recently add by Mehrad/ to be verified


#recently added by Mehrad, to be verified
def test_BaseFilterChanger():
    ''' Check the functionality of the BaseFilterChanger '''
    from viscope.instrument.base.baseFilterChanger import BaseFilterChanger
    import time

    filter_changer = BaseFilterChanger()
    filter_changer.connect()
    filter_changer.setParameter('threadingNow', True)

    # Test switching positions
    for position in range(1, filter_changer.getParameter('num_positions') +1):
        filter_changer.setParameter('position', position)
        print(f'Switched to position {position}')

        time.sleep(0.5)

        # Checking to see if the position matches or not
        current_position = filter_changer.getParameter('position')
        print(f'Current position: {current_position}')
        assert current_position == position, f"Expected position {position}, but got {current_position}"

    filter_changer.disconnect()





