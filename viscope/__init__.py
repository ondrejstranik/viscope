from pathlib import Path

dataFolder = str(Path(__file__).parent.joinpath('DATA'))

# it is necessary to load it in order to get load the picked class
#import HSIplasmon.algorithm.calibrateFrom3Images
#from HSIplasmon.algorithm.calibrateFrom3Images import CalibrateFrom3Images