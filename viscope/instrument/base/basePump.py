"""
Base class for pump instruments.

Provides flow-rate and on/off control shared by all pump subclasses.
"""
#%%

from viscope.instrument.base.baseInstrument import BaseInstrument


class BasePump(BaseInstrument):
    """Base class for all pumps.

    Attributes:
        flowRate: Desired flow rate in device-specific units.
        flow: True when the pump is actively flowing.
    """

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

    def _setFlowRate(self, value):
        """Set the target flow rate."""
        self.flowRate = value

    def _getFlowRate(self):
        """Return the current target flow rate."""
        return self.flowRate

    def _setFlow(self, value):
        """Enable or disable active flow."""
        self.flow = value

    def _getFlow(self):
        """Return True if the pump is currently flowing."""
        return self.flow

    def setParameter(self, name, value):
        """Set a named pump parameter (flowRate, flow, or any base parameter)."""
        super().setParameter(name, value)

        if name== 'flowRate':
            self._setFlowRate(value)
        if name== 'flow':
            self._setFlow(value)

    def getParameter(self, name):
        """Return the value of a named pump parameter."""
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
