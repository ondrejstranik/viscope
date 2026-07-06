"""
class to generate virtual sample

@author: ostranik
"""
#%%

import numpy as np
from skimage import data
from skimage.transform import resize, rescale
from skimage.filters import gaussian

class Component():
    ''' class to calculate light propagation through different optical componenets'''
    DEFAULT = {}

    @classmethod
    def psfSize(cls,NA,wavelength=0.55):
        ''' return the lateral size (radius of the first minimum) of the
        diffraction limited PSF in [um], classic Rayleigh criterion
        NA ... numerical aperture of the objective
        wavelength ... wavelength of the light [um]'''

        size = 0.61*wavelength/NA

        return size

    @classmethod
    def diffractionBlur(cls,iFrame,NA,wavelength=0.55):
        ''' blur the image with a Gaussian approximation of the diffraction
        limited PSF, the blur size (sigma) is set by the psfSize function
        (pixel size is assumed to be 1 um)
        for 3D array the shape[0] (first axis) is the spectral dimension and
        is not blurred
        iFrame ... input image
        NA ... numerical aperture of the objective
        wavelength ... wavelength of the light [um]'''

        sigma = cls.psfSize(NA,wavelength)

        if iFrame.ndim==3:
            sigma = (0,sigma,sigma)

        oFrame = gaussian(iFrame,sigma=sigma,preserve_range=True)

        return oFrame

    @classmethod
    def laserIllumination(cls,iFrame:np.ndarray, laser):
        ''' modify the number of photon depending on the power of the laser
        simple approximation'''

        oFrame = iFrame*laser.getParameter("power")
        if laser.getParameter("keySwitch") is False:
            oFrame *= 0

        return oFrame        

    @classmethod
    def _mapImageToImage(cls, destination,source,sourceOffset):
        ''' map 2D array to 2D array of different sizes with some offsets (Y,X)
        for 3D array the shape[0] (first axis) is the spectral dimension'''

        # rename and 
        # move spectral axis to the last axis for 3D array 
        if (destination.ndim ==3) and (source.ndim ==3):
            vFrame = np.moveaxis(destination,0,-1)
            sFrame = np.moveaxis(source,0,-1)
        else:
            vFrame = destination
            sFrame = source

        samplePositionXY =  sourceOffset

        sampleInsideFOV = True

        topLeft = [0,0]
        topLeftSample = [0,0]
        if (samplePositionXY[0]>0) and (samplePositionXY[0]<vFrame.shape[0]):
            topLeft[0] = samplePositionXY[0]
        if samplePositionXY[0]< 0:
            topLeftSample[0] = - samplePositionXY[0]
        if samplePositionXY[0]>vFrame.shape[0]:
            sampleInsideFOV = False
        if (samplePositionXY[1]>0) and (samplePositionXY[1]<vFrame.shape[1]):
            topLeft[1] = samplePositionXY[1]
        if samplePositionXY[1]< 0:
            topLeftSample[1] = - samplePositionXY[1]
        if samplePositionXY[1]>vFrame.shape[1]:
            sampleInsideFOV = False

        # bottom right  conner
        bottomRight = [vFrame.shape[0],vFrame.shape[1]]
        bottomRightSample = [sFrame.shape[0],sFrame.shape[1]]
        if ((samplePositionXY[0] + sFrame.shape[0]>0) and 
            (samplePositionXY[0]+ sFrame.shape[0]<vFrame.shape[0])):
            bottomRight[0] = samplePositionXY[0] + sFrame.shape[0]
        if samplePositionXY[0] + sFrame.shape[0] > vFrame.shape[0]:
            bottomRightSample[0] = -(samplePositionXY[0] + sFrame.shape[0] - vFrame.shape[0])
        if samplePositionXY[0] + sFrame.shape[0] <0:
            sampleInsideFOV = False
        if ((samplePositionXY[1] + sFrame.shape[1]>0) and 
            (samplePositionXY[1]+ sFrame.shape[1]<vFrame.shape[1])):
            bottomRight[1] = samplePositionXY[1] + sFrame.shape[1]
        if samplePositionXY[1] + sFrame.shape[1] > vFrame.shape[1]:
            bottomRightSample[1] = -(samplePositionXY[1] + sFrame.shape[1] - vFrame.shape[1])
        if samplePositionXY[1] + sFrame.shape[1] <0:
            sampleInsideFOV = False

        #print(f'sampleInsideFOV {sampleInsideFOV}')
        #print(f'topLeft = {topLeft}')
        #print(f'bottomRight = {bottomRight}')
        #print(f'topLeftSample = {topLeftSample}')
        #print(f'bottomRightSample = {bottomRightSample}')

        # set FOV
        if sampleInsideFOV:
            if vFrame.ndim==2:
                vFrame[topLeft[0]:bottomRight[0]-1,topLeft[1]:bottomRight[1]-1] = (
                sFrame[topLeftSample[0]:bottomRightSample[0]-1,
                        topLeftSample[1]:bottomRightSample[1]-1]
                )
            if vFrame.ndim==3:
                vFrame[topLeft[0]:bottomRight[0]-1,topLeft[1]:bottomRight[1]-1,:] = (
                sFrame[topLeftSample[0]:bottomRightSample[0]-1,
                        topLeftSample[1]:bottomRightSample[1]-1,:]
                )

        # move the spectral axis back
        if (destination.ndim ==3) and (source.ndim ==3):
            vFrame = np.moveaxis(destination,-1,0)
            sFrame = np.moveaxis(source,-1,0)
    
    @classmethod
    def ideal4fImaging(cls,iFrame=None,oFrame=None,iFramePosition = np.array([0,0]),
                        magnification=1,iPixelSize=1,oPixelSize=1):
        ''' image Frame with 4f system, all spatial frequency are preserved
        the iFrame and oFrame has to be given '''

        # image -  magnify , ideal lens
        mag = magnification*iPixelSize/oPixelSize
        iFramePosition = (iFramePosition* mag).astype(int)
        if iFrame.ndim==2: sFrame = rescale(iFrame,(mag,mag), preserve_range=True)
        if iFrame.ndim==3: sFrame = rescale(iFrame,(1,mag,mag), preserve_range=True)
        # adjust the number of photons
        sFrame /= mag**2        
        # aperture
        cls._mapImageToImage(oFrame,sFrame, iFramePosition)

        return oFrame

    @classmethod
    def ideal4fImagingOnCamera(cls,camera=None,iFrame=None,
                                iFramePosition=np.array([0,0]),iPixelSize=1,
                                magnification=1):
        ''' ideal 4f imaging onto a camera. uses ideal4fImaging function
        account for exposure time '''

        # all spectral channels comes added on the same pixel
        if iFrame.ndim >2:
            iFrame = np.sum(iFrame,axis=0)
        oFrame = np.zeros((camera.getParameter('height'),
                    camera.getParameter('width')))
        cls.ideal4fImaging(iFrame,oFrame,iFramePosition,magnification,iPixelSize,
        camera.DEFAULT['cameraPixelSize'])

        ## integration time of the camera
        oFrame *= camera.exposureTime/1e6

        return oFrame




#%%
