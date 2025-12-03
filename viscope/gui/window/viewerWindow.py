'''
class for live viewing spectral images
'''
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


class ViewerWindow(QMainWindow):
    ''' class for the main window'''
    DEFAULT = {'nameGUI':'viewerWindow'}
    sigClose = Signal()
    visibilityChanged = Signal(bool)
    top_window_closed = Signal()  # emitted only by top window
    titleChangedSignal = Signal(str)


    def __init__(self, name=DEFAULT['nameGUI'],**kwarg):
        ''' initalisation'''
        super().__init__()
        self.setWindowTitle(name)
        self.dockWidgetParameter = None

        self._is_top_window = False
        self._menu_action_map = {}  # window -> QAction for title updates
        #self.topWindow = topWindow

        self.show()

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
        ''' visibility (show) signals fow windows'''
        super().showEvent(event)
        self.visibilityChanged.emit(True)

    def hideEvent(self, event):
        ''' visibility (hide) signals fow windows'''
        super().hideEvent(event)
        self.visibilityChanged.emit(False)

    def closeEvent(self, event):
        ''' close all windows if the top windows closed'''
        super().closeEvent(event)

        # If THIS is the top window → notify manager to close everything
        if self._is_top_window:
            self.top_window_closed.emit()


    def addParameterGui(self,newGUI,name=DEFAULT['nameGUI']):
        ''' add  GUI as a dockable widget in this window (for parameters, position bottom)'''

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

    def addMainGUI(self,newGUI,name=DEFAULT['nameGUI']):
        ''' add GUI as a main widget (for viewers, position center)'''
        self.setCentralWidget(newGUI)

