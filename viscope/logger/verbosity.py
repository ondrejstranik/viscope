'''
global logging verbosity control for viscope/plim/spectralCamera.

Deliberately kept free of any Qt/napari import (unlike viscope.main, whose
import creates a QApplication as a side effect) so a headless script can
import just this and set the verbosity without pulling in the GUI stack.

Individual modules don't need to import anything from here to log - they
just use the standard library directly:

    import logging
    logger = logging.getLogger(__name__)
    ...
    logger.debug('...')       # routine/diagnostic messages
    logger.warning('...')     # recovered-but-notable issues
    logger.exception('...')   # inside an except block - attaches the
                               # current traceback automatically

setVerbosity() is only needed once, at a script's entry point, to choose
what actually gets shown.
'''
import logging

_configured = False


def setVerbosity(level):
    ''' level: 'DEBUG'/'INFO' to show everything, 'ERROR' to show only
    errors (or any standard logging level name/int).

    Applies globally, across viscope/plim/spectralCamera and any other
    module using logging.getLogger(__name__): every such logger falls back
    to the root logger's level unless it sets its own, so configuring the
    root here (logging.getLogger(), no name) is what makes this a single,
    package-wide switch rather than something scoped to just 'viscope.*'
    loggers. '''
    global _configured

    if not _configured:
        # basicConfig() only installs its handler the first time it's
        # called - later calls here just change the level (see below)
        logging.basicConfig(level=level, format='%(levelname)s %(name)s: %(message)s')
        _configured = True

    logging.getLogger().setLevel(level)


if __name__ == "__main__":
    pass
