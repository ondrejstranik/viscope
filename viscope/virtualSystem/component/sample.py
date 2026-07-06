"""
module to generate virtual sample

@author: ostranik
"""
#%%

import numpy as np
from skimage import data
from skimage.transform import resize
from skimage.draw import disk, polygon


class BaseSample():
    ''' base class to define a sample object of the microscope'''
    
    def __init__(self):
        ''' initialise and set uniform 2D plane'''

        self.pixelSize= 1 # size of the pixel in [um]
        self.size=(200,400) # size of the object in pixels
        self.position = np.array([0,0]) # position of the sample
        self.name = 'uniform'

        #data ... data representing the sample object
        self.data = np.ones(self.size)

    def get(self):
        ''' return the data representing the object '''
        return self.data

    def getName(self):
        ''' return the name of the sample '''
        return self.name

class Sample(BaseSample):
    ''' class to defining a various 2D fluorescence sample object'''

    def _irregularBlob(self,center,radius,rng,amplitude=0.15,harmonics=3,numPoints=24):
        ''' return the pixels and the bounding radius of a randomly deformed,
        star-shaped blob (smooth random radius-vs-angle profile), used to
        avoid drawing cells/nuclei as perfect circles'''

        angles = np.linspace(0,2*np.pi,numPoints,endpoint=False)
        coeffs = [(rng.uniform(0,amplitude),rng.uniform(0,2*np.pi)) for _ in range(harmonics)]

        radii = radius*(1+sum(a*np.cos((k+1)*angles+phase) for k,(a,phase) in enumerate(coeffs)))
        rows = center[0]+radii*np.sin(angles)
        cols = center[1]+radii*np.cos(angles)

        boundingRadius = radius*(1+sum(a for a,_ in coeffs))
        rr,cc = polygon(rows,cols,shape=self.size)

        return rr,cc,boundingRadius

    def setAstronaut(self,samplePixelSize=None,
                        sampleSize= None,
                        photonRateMax= None,
                        samplePosition = None):
        ''' define the sample.
        sample ... 2D spatial distribution of photon rates [#/s/pixelSize^2] (no noise)'''

        DEFAULT = {'photonRateMax':1e6,
                    'samplePixelSize':1, # um
                    'sampleSize': (200,400),
                    'samplePosition': np.array([0,0,0])} # pixels

        self.pixelSize=DEFAULT['samplePixelSize'] if samplePixelSize is None else samplePixelSize
        self.size=DEFAULT['sampleSize'] if sampleSize is None else sampleSize
        self.position=DEFAULT['samplePosition'] if samplePosition is None else samplePosition

        photonRateMax=DEFAULT['photonRateMax'] if photonRateMax is None else photonRateMax        

        # define
        _sample = np.sum(data.astronaut(), axis=2)

        # resize 
        _sample = resize(_sample, self.size)

        # normalise
        _sample = _sample/np.max(_sample)*photonRateMax

        self.data = _sample

    def setCell(self,samplePixelSize=None,
                        sampleSize= None,
                        photonRateMax= None,
                        samplePosition = None,
                        cellSize = None,
                        cellDistance = None):
        ''' define the sample.
        sample ... 2D spatial distribution of photon rates [#/s/pixelSize^2] (no noise)
        cellSize ... (mean) cell radius [um]
        cellDistance ... average distance between neighbouring cells [um]'''

        PROTEIN_NUMBER = 8 # number of protein puncta per cell
        PROTEIN_SIZE = 0.1 # protein radius [um] (100 nm)

        DEFAULT = {'photonRateMax':1e6,
                    'samplePixelSize':0.1, # um
                    'sampleSize': (1000,1000),
                    'samplePosition': np.array([0,0,0]), # pixels
                    'cellSize': 5, # radius of a cell [um]
                    'cellDistance': 30} # average distance between cells [um]

        self.pixelSize=DEFAULT['samplePixelSize'] if samplePixelSize is None else samplePixelSize
        self.size=DEFAULT['sampleSize'] if sampleSize is None else sampleSize
        self.position=DEFAULT['samplePosition'] if samplePosition is None else samplePosition

        photonRateMax=DEFAULT['photonRateMax'] if photonRateMax is None else photonRateMax
        cellSize=DEFAULT['cellSize'] if cellSize is None else cellSize
        cellDistance=DEFAULT['cellDistance'] if cellDistance is None else cellDistance

        # cell radius, average spacing and protein size, converted from [um] to [pixel]
        cellRadiusPixel = cellSize/self.pixelSize
        cellDistancePixel = cellDistance/self.pixelSize
        proteinRadiusPixel = PROTEIN_SIZE/self.pixelSize

        # number of cells expected for the given average spacing over the sample area
        cellNumber = max(1, int(round((self.size[0]*self.size[1])/cellDistancePixel**2)))

        # define, cells as randomly placed, non-overlapping, randomly sized and
        # irregularly shaped blobs, each with a brighter nucleus and a few small proteins
        _sample = np.zeros(self.size)

        rng = np.random.default_rng()
        placedCenter = []
        placedRadius = []
        maxAttempt = 100
        for _ in range(cellNumber):
            for _ in range(maxAttempt):
                center = np.array([rng.uniform(0,self.size[0]), rng.uniform(0,self.size[1])])
                radius = rng.uniform(0.7,1.3)*cellRadiusPixel
                rr,cc,boundingRadius = self._irregularBlob(center,radius,rng)

                fitsInImage = (center[0]-boundingRadius>=0 and center[1]-boundingRadius>=0
                                and center[0]+boundingRadius<=self.size[0]-1
                                and center[1]+boundingRadius<=self.size[1]-1)

                noOverlap = all(np.linalg.norm(center-otherCenter) >= max(boundingRadius+otherRadius,cellDistancePixel)
                                for otherCenter,otherRadius in zip(placedCenter,placedRadius))

                if fitsInImage and noOverlap:
                    break
            else:
                # could not find a spot that fits fully in the image and is far
                # enough from the other cells, skip this cell
                continue

            placedCenter.append(center)
            placedRadius.append(boundingRadius)

            # cytoplasm, an irregular (non-circular) blob
            _sample[rr,cc] += rng.uniform(0.2,0.4)

            # nucleus, slightly off-centre, also irregularly shaped
            nucleusRadius = radius*rng.uniform(0.35,0.5)
            nucleusCenter = center+rng.uniform(-0.15,0.15,2)*radius
            rrN,ccN,_ = self._irregularBlob(nucleusCenter,nucleusRadius,rng,amplitude=0.1)
            _sample[rrN,ccN] += rng.uniform(0.5,0.8)

            # small proteins scattered through the cytoplasm, placed on pixels that
            # are actually part of the cell so none end up outside its boundary
            if len(rr)>0:
                proteinIndex = rng.integers(0,len(rr),size=PROTEIN_NUMBER)
                for idx in proteinIndex:
                    proteinCenter = (rr[idx],cc[idx])
                    rrP,ccP = disk(proteinCenter, proteinRadiusPixel, shape=self.size)
                    _sample[rrP,ccP] += rng.uniform(0.3,0.6)

        # normalise
        if np.max(_sample)>0:
            _sample = _sample/np.max(_sample)*photonRateMax

        self.data = _sample

