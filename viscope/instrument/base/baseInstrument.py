"""
base class for all instruments

@author: ostranik
"""
#%%
import time
from napari.qt.threading import create_worker
from threading import Event
#from dataclasses import dataclass,field


class ThreadFlag:
    def __init__(self):
        self.event = Event()
        self.data: list = []

    def set(self,info=None):
        self.event.set()
        if info is not None: self.data.append(info)

    def clear(self):
        self.event.clear()
        self.data = []

    def is_set(self):
        return self.event.is_set()

    def wait(self,timeout=None):
        return self.event.wait(timeout)

    def getLastData(self):
        return self.data[-1]


class BaseInstrument():
    ''' base class of all instruments 
    name ... name of the instrument
             It should be unique for each instrument
    threading ... if true a worker running a thread loop is prepared
    '''
    DEFAULT = {'name': 'baseInstrument',
                'threading':False}
    
    def __init__(self, name=None,threading=None,*args, **kwargs):
        ''' initialisation '''
        #super(BaseInstrument,self).__init__(*args, **kwargs)

        self.name = name if name is not None else BaseInstrument.DEFAULT['name']

        self.flagLoop = ThreadFlag()
        self.worker = None

        if threading is not None:
            self._setWorker(threading) 
        else:
            self._setWorker(BaseInstrument.DEFAULT['threading'])

    def connect(self):
        print(f'connecting instrument - {self.name}  ')

    def disconnect(self):
        print(f'disconnecting instrument - {self.name} ')
        if self.worker is not None: 
            print(f'quitting the thread loop of instrument  - {self.name} ')
            self.worker.quit()
            # TODO: check if it not create errors!
            #self.flagLoop = None

    def setParameter(self,name,value):
        ''' set parameter of the instrument '''
        if name== 'name':
            self.name= value
        if name== 'threading':
            self._setWorker(value)
        if name== 'threadingNow':
            self._setWorker(True)
            if value: self.worker.start()  
        

    def getParameter(self,name):
        ''' get parameter of the instrument'''
        if name=='name':
            return self.name
        if name=='threading':
            return True if self.worker is not None else False

    def _setWorker(self,value:bool):
        ''' set the worker for the base instrument '''
        if value:
            print(f'starting thread loop of instrument - {self.name}')
            self.worker = create_worker(self.loop)
        else:
            self.worker = None


    def loop(self):
        ''' base threading loop of the instrument '''
        while True:
            print('output from BaseInstrument thread loop')
            self.flagLoop.set('output')
            yield  
            time.sleep(1)


if __name__ == '__main__':
    pass
