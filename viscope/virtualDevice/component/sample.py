"""
class to generate virtual sample

@author: ostranik
"""
#%%

import numpy as np
from skimage import data
from skimage.transform import resize

class Sample():
    ''' class to define a sample object of the microscope'''
    DEFAULT = {}
    
    def __init__(self,*args, **kwargs):
        ''' initialisation '''
        super(Sample,self).__init__(*args, **kwargs)

        #sample ... spatial distribution of expected photon rates [#/s/pixelSize^2] (no noise)
        self.sample = None

    def setAstronaut(self,samplePixelSize=None,
                        sampleSize= None,
                        photonRateMax= None):
        ''' define the sample.
        sample ... spatial distribution of photon rates [#/s/pixelSize^2] (no noise)'''

        DEFAULT = {'photonRateMax':1e6,
                    'samplePixelSize':1, # um
                    'sampleSize': (200,400)} # pixels

        samplePixelSize=DEFAULT['samplePixelSize'] if samplePixelSize is None else samplePixelSize
        sampleSize=DEFAULT['sampleSize'] if sampleSize is None else sampleSize
        photonRateMax=DEFAULT['photonRateMax'] if photonRateMax is None else photonRateMax        

        # define
        _sample = np.sum(data.astronaut(), axis=2)

        # resize 
        _sample = resize(_sample, sampleSize)

        # normalise
        _sample = _sample/np.max(_sample)*photonRateMax

        self.sample = _sample

    def get(self):
        return self.sample


#%%

if __name__ == '__main__':

    import napari

    sample = Sample()
    sample.setAstronaut()
    # load multichannel image in one line
    viewer = napari.view_image(sample.get())
    napari.run()

