'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np

from viscope.gui.baseGUI import BaseGUI
from magicgui import magicgui

class SaveImageGUI(BaseGUI):
    ''' main class to save image'''

    DEFAULT = {'nameGUI': 'Save Image'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        if 'name' in kwargs: self.DEFAULT['nameGUI']= kwargs['name']

        # prepare the gui of the class
        SaveImageGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving file Path:","mode":'d'},
                fileName={"label": "Saving file Name:"},
                fileIdx = {"label": "File Index:"})
        def saveGui(filePath= Path(self.viscope.dataFolder), fileName: str = 'Image', fileIdx=0,idxIncrement=True):

            np.save(str(filePath / fileName) + f'_{fileIdx}',self.device.rawImage)            

            if idxIncrement:
                saveGui.fileIdx.value = saveGui.fileIdx.value + 1 

        # add widgets 
        self.saveGui = saveGui
        self.vWindow.addParameterGui(self.saveGui,name=self.DEFAULT['nameGUI'])
 

if __name__ == "__main__":
    pass


