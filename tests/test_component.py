''' test components'''
import pytest


def test_mapImageToImage():
    ''' check the mapping'''
    from viscope.virtualSystem.component.component import Component
    import numpy as np

    source = np.ones((20,10,10))
    destination = np.zeros((20,10,10))
    Component._mapImageToImage(destination,source,[0,0])
    np.testing.assert_array_almost_equal(destination,source)






