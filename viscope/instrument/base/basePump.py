#%%
''' class to control pump'''

from viscope.instrument.base.baseInstrument import BaseInstrument


class BasePump(BaseInstrument):
    ''' base class of a pump
    power ... laser power
    keySwitch ... with True the laser emits light'''

    DEFAULT = {'name':'basePump',
                'flowRate': 0,
                'flow': False} 
    
    def __init__(self,name=DEFAULT['name'],*args, **kwargs):
        ''' pump initialisation'''
        super().__init__(name=name,*args, **kwargs)
        
        self.flowRate = BasePump.DEFAULT['flowRate']
        self.flow = BasePump.DEFAULT['flow']

    def connect(self,*args):
        ''' connect to the pump '''
        super().connect()
        # prepare the pump
        self.setParameter('flowRate',self.flowRate)
        self.setParameter('flow',self.flow)

    def _setFlowRate(self,value):
        self.flowRate = value

    def _getFlowRate(self):
        return self.flowRate

    def _setFlow(self,value):
        self.flow = value

    def _getFlow(self):
        return self.flow        

    def setParameter(self,name, value):
        ''' set parameters'''
        super().setParameter(name,value)

        if name== 'flowRate':
            self._setFlowRate(value)
        if name== 'flow':
            self._setFlow(value)

    def getParameter(self,name):
        ''' get parameter'''
        _value = super().getParameter(name)
        if _value is not None: return _value

        if name=='flowRate':
            value = self._getFlowRate()
            return value
        if name=='flow':
            value = self._getFlow()
            return value 
        if name=='flowRateReal':
            value = 0 if not self._getFlow() else self._getFlowRate()
            return value


if __name__ == '__main__':

    pass





# %%
