"""
Main viewer window and window manager for the viscope GUI.

ViewerWindow is a QMainWindow subclass that hosts dockable parameter panels
and a central viewer widget. WindowManager tracks all open windows and
synchronises the Windows menu on the top window.
"""
#%%
#import napari
#from typing import Annotated, Literal

from qtpy.QtWidgets import QApplication, QDockWidget, QMainWindow, QAction

#from qtpy.QtWidgets import QLabel, QSizePolicy, QDockWidget
from qtpy.QtCore import Qt, Signal,QObject

#import numpy as np

#from magicgui.widgets import MainWindow, Container, MainFunctionGui, FunctionGui

class WindowManager(QObject):
    """Tracks all windows and handles menu updates and shutdown."""
    sigWindowCreated = Signal(QMainWindow)

    def __init__(self):
        super().__init__()
        self.top_window = None
        self.windows = []

        # On new window creation → ask top window to add it to menu
        self.sigWindowCreated.connect(self._add_to_menu)

    def register(self, window: QMainWindow):
        """Register a window. First registered window becomes the top window."""
        if self.top_window is None:
            # First window becomes the "main / top" window
            self.top_window = window
            window._is_top_window = True

            window.setup_menu()  # Create menu only for top window

            # When top window closes → close all windows
            window.top_window_closed.connect(self._close_all_windows)

        else:
            # Managed window
            self.windows.append(window)
            window._is_top_window = False

            # New window → top window should add it to the menu
            self.sigWindowCreated.emit(window)

    def _add_to_menu(self, window: QMainWindow):
        """Forward the window to the top window for menu insertion."""
        if self.top_window is not None:
            self.top_window.add_window_entry(window)

    def _close_all_windows(self):
        """Close ALL windows including top."""
        # Close managed windows first
        for w in list(self.windows):
            w.close()

        # Then close the top window last
        if self.top_window is not None:
            self.top_window.close()

    def allWindows(self):
        """All registered windows, top window first."""
        windows = [self.top_window] if self.top_window is not None else []
        return windows + self.windows

    def applyLayout(self):
        """Size and position every registered window according to its
        `region` ('top' or 'bottom'): 'top' windows get the top 75% of the
        screen, 'bottom' windows the bottom 25%, tiled side-by-side within
        their region so windows sharing a region never overlap."""
        screen = QApplication.primaryScreen().availableGeometry()

        topWindows = [w for w in self.allWindows() if w.region == 'top']
        bottomWindows = [w for w in self.allWindows() if w.region == 'bottom']

        topHeight = round(screen.height() * 0.75)
        bottomHeight = round(screen.height() * 0.25)

        self._tileRow(topWindows, screen, screen.top(), topHeight)
        self._tileRow(bottomWindows, screen, screen.bottom() - bottomHeight + 1, bottomHeight)

    @staticmethod
    def _tileRow(windows, screen, y, height):
        """Place `windows` side-by-side across the full screen width at
        vertical position `y` with the given `height`."""
        n = len(windows)
        if n == 0:
            return
        width = screen.width() // n
        for i, window in enumerate(windows):
            x = screen.left() + i * width
            # last window absorbs the rounding remainder
            w = screen.width() - i * width if i == n - 1 else width
            window.setGeometry(x, y, w, height)


class ViewerWindow(QMainWindow):
    ''' class for the main window'''
    DEFAULT = {'nameGUI':'viewerWindow', 'region': 'top'}
    sigClose = Signal()
    visibilityChanged = Signal(bool)
    top_window_closed = Signal()  # emitted only by top window
    titleChangedSignal = Signal(str)


    def __init__(self, name=DEFAULT['nameGUI'], region=DEFAULT['region'], **kwarg):
        """Initialise the viewer window and show it."""
        super().__init__()
        self.setWindowTitle(name)
        self.dockWidgetParameter = None

        self._is_top_window = False
        self._menu_action_map = {}  # window -> QAction for title updates
        #self.topWindow = topWindow
        self.region = region

        self.show()

    def setRegion(self, region):
        ''' set which part of the screen ('top' or 'bottom') this window is
        tiled into by WindowManager.applyLayout() '''
        if region not in ('top', 'bottom'):
            raise ValueError(f"region must be 'top' or 'bottom', got {region!r}")
        self.region = region

    def setup_menu(self):
        ''' MENU SYSTEM (only for top window) '''

        menubar = self.menuBar()

        # System menu
        sys_menu = menubar.addMenu("System")
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        sys_menu.addAction(quit_action)

        # Windows menu (dynamic)
        self.windows_menu = menubar.addMenu("Windows")

    def add_window_entry(self, window):
        """Add an entry to the Windows menu (top window only)."""
        if not self._is_top_window:
            return

        action = QAction(window.windowTitle(), self, checkable=True)
        action.setChecked(window.isVisible())
        action.window = window

        # Menu toggles window visibility
        action.triggered.connect(lambda checked, w=window: w.setVisible(checked))

        # Keep menu in sync with window’s visibility
        window.visibilityChanged.connect(
            lambda visible, a=action: a.setChecked(visible)
        )

        # Sync title changes
        window.titleChangedSignal.connect(lambda title, a=action: a.setText(title))

        self._menu_action_map[window] = action
        self.windows_menu.addAction(action)

    def setWindowTitle(self, title):
        ''' update the menu if title of window is changed'''
        super().setWindowTitle(title)
        try:
            self.titleChangedSignal.emit(title)
        except RuntimeError:
            # Happens during destruction → safe to ignore
            pass

    def showEvent(self, event):
        """Emit visibilityChanged(True) when the window is shown."""
        super().showEvent(event)
        self.visibilityChanged.emit(True)

    def hideEvent(self, event):
        """Emit visibilityChanged(False) when the window is hidden."""
        super().hideEvent(event)
        self.visibilityChanged.emit(False)

    def closeEvent(self, event):
        ''' close all windows if the top windows closed'''
        super().closeEvent(event)

        # If THIS is the top window → notify manager to close everything
        if self._is_top_window:
            self.top_window_closed.emit()


    def addParameterGui(self, newGUI, name=DEFAULT['nameGUI']):
        """Add a GUI panel as a dockable widget at the bottom of the window."""

        dw=QDockWidget('Dockable',self)
        dw.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        dw.setWindowTitle(name)
        try:
            dw.setWidget(newGUI)
        except: # magicGui widgets
            dw.setWidget(newGUI.native)

        self.addDockWidget(Qt.BottomDockWidgetArea,dw)
        # tabify the widget
        if self.dockWidgetParameter is not None:
            self.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
            #self.dockWidgetParameter = dw
        
        return dw

    def addMainGUI(self, newGUI, name=DEFAULT['nameGUI']):
        """Set a GUI widget as the central (viewer) widget of the window."""
        self.setCentralWidget(newGUI)

