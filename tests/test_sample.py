''' test for the Sample class '''

def test_setCell():
    ''' visualise a synthetic cell sample '''
    import napari
    from viscope.virtualSystem.component.sample import Sample

    sample = Sample()
    sample.setCell()
    # load multichannel image in one line
    viewer = napari.view_image(sample.get())
    napari.run()
