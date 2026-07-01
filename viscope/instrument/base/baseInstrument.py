"""
Base class for all instruments in the viscope package.

Provides threading support, parameter get/set interface, and a flag-based
synchronisation mechanism shared by every instrument subclass.
"""
#%%
import time
#from napari.qt.threading import create_worker
from superqt.utils._qthreading import create_worker
from threading import Event, Lock
import traceback
#from dataclasses import dataclass,field

class ThreadFlag:
    """Thread-safe flag that can carry a list of data payloads.

    Wraps threading.Event and adds an optional data queue so that the
    thread that sets the flag can pass information to the thread that
    waits on it.
    """

    def __init__(self):
        self.event = Event()
        self.data: list = []

    def set(self, info=None):
        """Set the flag and optionally append a data payload."""
        self.event.set()
        if info is not None: self.data.append(info)

    def clear(self):
        """Clear the flag and discard all stored payloads."""
        self.event.clear()
        self.data = []

    def is_set(self):
        """Return True if the flag is currently set."""
        return self.event.is_set()

    def wait(self, timeout=None):
        """Block until the flag is set, with an optional timeout in seconds."""
        return self.event.wait(timeout)

    def getLastData(self):
        """Return the most recently appended data payload."""
        return self.data[-1]


class BaseInstrument():
    """Base class for all viscope instruments.

    Args:
        name: Unique identifier for the instrument instance.
        threading: If True, a superqt worker running ``loop()`` is created
            immediately. Pass False (default) to defer threading.
    """
    DEFAULT = {'name': 'baseInstrument',
                'threading':False}
    
    def __init__(self, name=None,threading=None,*args, **kwargs):
        ''' initialisation '''
        #super(BaseInstrument,self).__init__(*args, **kwargs)

        self.name = name if name is not None else BaseInstrument.DEFAULT['name']

        self.flagLoop = ThreadFlag()
        self.worker = None

        self.lock = Lock()

        if threading is not None:
            self._setWorker(threading) 
        else:
            self._setWorker(BaseInstrument.DEFAULT['threading'])

    def connect(self):
        """Connect to the instrument hardware."""
        print(f'connecting instrument - {self.name}  ')

    def disconnect(self):
        """Disconnect from the instrument and stop the worker thread if running."""
        print(f'disconnecting instrument - {self.name} ')
        if self.worker is not None:
            if self.worker.is_running: 
                print(f'quitting the thread loop of instrument  - {self.name} ')
                self.worker.quit()
            else:
                print(f'the thread loop of instrument  - {self.name} is already closed')
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
            try:
                print('output from BaseInstrument thread loop')
                self.flagLoop.set('output')
                yield True 
                time.sleep(1)
            except:
                print(f"An exception occurred in thread of {self.name}:\n")
                traceback.print_exc()
                yield False                


if __name__ == '__main__':
    pass
