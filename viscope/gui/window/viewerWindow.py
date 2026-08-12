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

    DEFAULT = {'vWindowAlignment': 'horizontal', 'regionRatio': 0.4}

    def __init__(self, vWindowAlignment=DEFAULT['vWindowAlignment']):
        super().__init__()
        self.top_window = None
        self.windows = []
        self.setVWindowAlignment(vWindowAlignment)
        self.regionRatio = {region: WindowManager.DEFAULT['regionRatio']
                             for region in ('left', 'right', 'top', 'bottom')}

        # On new window creation → ask top window to add it to menu
        self.sigWindowCreated.connect(self._add_to_menu)

    def setVWindowAlignment(self, vWindowAlignment):
        ''' set how multiple 'full' region windows are tiled among each
        other ('horizontal', 'vertical' or 'overlap') '''
        if vWindowAlignment not in ('horizontal', 'vertical', 'overlap'):
            raise ValueError(f"vWindowAlignment must be 'horizontal', 'vertical' or 'overlap', got {vWindowAlignment!r}")
        self.vWindowAlignment = vWindowAlignment

    def setRegionRatio(self, region, ratio):
        ''' set which fraction (0-1) of the screen width/height the 'left',
        'right', 'top' or 'bottom' region occupies (default 0.4) '''
        if region not in ('left', 'right', 'top', 'bottom'):
            raise ValueError(f"region must be 'left', 'right', 'top' or 'bottom', got {region!r}")
        if not 0 < ratio < 1:
            raise ValueError(f"ratio must be between 0 and 1, got {ratio!r}")
        self.regionRatio[region] = ratio

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
        `region` ('full', 'left', 'right', 'top' or 'bottom').

        'left'/'right' windows each form a column along their edge, sized by
        `self.regionRatio` (40% of the screen width by default) and the full
        screen height; several windows sharing the same column are tiled
        vertically within it. 'top'/'bottom' windows each form a strip along
        their edge, sized by `self.regionRatio` (40% of the screen height by
        default), spanning whatever width is not already taken by the
        'left'/'right' columns; several windows sharing the same strip are
        tiled horizontally within it. 'full' windows fill the remaining
        area in between (shrunk accordingly whenever a
        'left'/'right'/'top'/'bottom' region is present) and are tiled
        among themselves according to `self.vWindowAlignment`
        ('horizontal', 'vertical' or 'overlap')."""
        screen = QApplication.primaryScreen().availableGeometry()

        fullWindows = [w for w in self.allWindows() if w.region == 'full']
        leftWindows = [w for w in self.allWindows() if w.region == 'left']
        rightWindows = [w for w in self.allWindows() if w.region == 'right']
        topWindows = [w for w in self.allWindows() if w.region == 'top']
        bottomWindows = [w for w in self.allWindows() if w.region == 'bottom']

        leftWidth = round(screen.width() * self.regionRatio['left']) if leftWindows else 0
        rightWidth = round(screen.width() * self.regionRatio['right']) if rightWindows else 0
        topHeight = round(screen.height() * self.regionRatio['top']) if topWindows else 0
        bottomHeight = round(screen.height() * self.regionRatio['bottom']) if bottomWindows else 0

        self._tileColumn(leftWindows, screen.left(), screen.top(),
                          leftWidth, screen.height())

        self._tileColumn(rightWindows, screen.right() - rightWidth + 1, screen.top(),
                          rightWidth, screen.height())

        self._tileRow(topWindows, screen.left() + leftWidth, screen.top(),
                       screen.width() - leftWidth - rightWidth, topHeight)

        self._tileRow(bottomWindows, screen.left() + leftWidth, screen.bottom() - bottomHeight + 1,
                       screen.width() - leftWidth - rightWidth, bottomHeight)

        self._tileFull(fullWindows, screen.left() + leftWidth, screen.top() + topHeight,
                        screen.width() - leftWidth - rightWidth, screen.height() - topHeight - bottomHeight,
                        self.vWindowAlignment)

    @staticmethod
    def _placeWindow(window, x, y, width, height):
        """Position/resize `window` so its outer frame (title bar included)
        occupies exactly (x, y, width, height).

        QWidget.setGeometry() positions the frame-EXCLUDED client area, so
        calling it directly with y = screen top pushes the title bar above
        the visible screen (negative y) and it never gets painted. Here we
        read the window's current frame margins and compensate so the
        visible outer rect - not just the client area - lands where asked."""
        frame = window.frameGeometry()
        client = window.geometry()
        left = client.left() - frame.left()
        top = client.top() - frame.top()
        right = frame.right() - client.right()
        bottom = frame.bottom() - client.bottom()
        window.setGeometry(x + left, y + top, width - left - right, height - top - bottom)

    @staticmethod
    def _tileRow(windows, x, y, width, height):
        """Place `windows` side-by-side, spanning `width` at vertical position `y`."""
        n = len(windows)
        if n == 0:
            return
        w = width // n
        for i, window in enumerate(windows):
            # last window absorbs the rounding remainder
            windowWidth = width - i * w if i == n - 1 else w
            WindowManager._placeWindow(window, x + i * w, y, windowWidth, height)

    @staticmethod
    def _tileColumn(windows, x, y, width, height):
        """Place `windows` stacked top-to-bottom, spanning `height` at horizontal position `x`."""
        n = len(windows)
        if n == 0:
            return
        h = height // n
        for i, window in enumerate(windows):
            # last window absorbs the rounding remainder
            windowHeight = height - i * h if i == n - 1 else h
            WindowManager._placeWindow(window, x, y + i * h, width, windowHeight)

    @staticmethod
    def _tileFull(windows, x, y, width, height, alignment):
        """Arrange 'full' region windows among themselves according to `alignment`."""
        if not windows:
            return
        if alignment == 'vertical':
            WindowManager._tileColumn(windows, x, y, width, height)
        elif alignment == 'overlap':
            for window in windows:
                WindowManager._placeWindow(window, x, y, width, height)
        else:  # 'horizontal'
            WindowManager._tileRow(windows, x, y, width, height)


class ViewerWindow(QMainWindow):
    ''' class for the main window'''
    DEFAULT = {'nameGUI':'viewerWindow', 'region': 'full'}
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
        ''' set which part of the screen ('full', 'left', 'right', 'top' or
        'bottom') this window is placed in by WindowManager.applyLayout() '''
        if region not in ('full', 'left', 'right', 'top', 'bottom'):
            raise ValueError(f"region must be 'full', 'left', 'right', 'top' or 'bottom', got {region!r}")
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

