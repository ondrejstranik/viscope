"""
Two Napari viewers in one Qt window, with a custom floating toolbar placed
inside the Layer List dock of the left viewer.

Fixes: ensures proper spacing (no overlap) by forcing the floating widget
to size to its contents (QLayout.SetFixedSize + adjustSize()).
"""

import os
import napari
import numpy as np
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QToolButton,
    QLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QIcon, QPixmap, QPainter, QColor
from qtpy.QtSvg import QSvgRenderer

ICON_FOLDER = os.path.join(os.path.dirname(__file__), "resources", "icons")

import os
import napari
from qtpy.QtWidgets import QWidget, QHBoxLayout, QToolButton, QLayout
from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPixmap, QPainter, QColor
from qtpy.QtSvg import QSvgRenderer

ICON_FOLDER = os.path.dirname(__file__)

class NapariViewer:
    """
    Factory class that returns a modified napari.Viewer instance with a custom toolbar.
    Usage:
        viewer = CustomNapariViewer()
    """

    ICON_COLOR = "#CCCCCC"  # light gray

    def __new__(cls,**kwargs):
        self = super().__new__(cls)

        # ---- Create the napari viewer ----
        if 'show' in kwargs:        
            viewer = napari.Viewer(show=kwargs['show'])
        else:
            viewer = napari.Viewer()
        
        # Hide axes
        viewer.axes.visible = False

        # Install the custom toolbar
        cls._install_toolbar(self, viewer)

        return viewer

    # -----------------------------
    # SVG icon loader (light gray)
    # -----------------------------
    def _load_icon(self, svg_path, size=24):
        renderer = QSvgRenderer(svg_path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        img = pixmap.toImage()
        color = QColor(self.ICON_COLOR)
        for y in range(img.height()):
            for x in range(img.width()):
                c = img.pixelColor(x, y)
                if c.alpha() > 0:
                    img.setPixelColor(x, y, QColor(color.red(), color.green(), color.blue(), c.alpha()))
        return QIcon(QPixmap.fromImage(img))

    def _make_button(self, svg_name, tooltip, callback):
        btn = QToolButton()
        svg_path = os.path.join(ICON_FOLDER, svg_name)
        btn.setIcon(self._load_icon(svg_path))
        btn.setIconSize(QSize(24, 24))
        btn.setFixedSize(28, 28)
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        return btn

    # -----------------------------
    # Layer operations
    # -----------------------------
    def _transpose_layer(self, viewer):
        layer = viewer.layers.selection.active
        if layer is None: return
        data = layer.data
        if data.ndim >= 2:
            layer.data = data.transpose(1, 0, *range(2, data.ndim))

    def _reorder_layer(self, viewer):
        layer = viewer.layers.selection.active
        if layer is None: return
        data = layer.data
        n = data.ndim
        layer.data = data.transpose(list(range(1, n)) + [0])

    # -----------------------------
    # Toolbar installer
    # -----------------------------
    @classmethod
    def _install_toolbar(cls, self, viewer):

        qt_viewer = viewer.window._qt_viewer

        # Hide napari default buttons
        try:
            qt_viewer.viewerButtons.setVisible(False)
        except Exception:
            pass

        dock = qt_viewer.dockLayerList.widget()

        # Floating container
        container = QWidget(dock)
        container.setObjectName("CustomToolbar")
        container.setStyleSheet("""
            QWidget#CustomToolbar QToolButton {
                background-color: #444;
                border-radius: 4px;
                padding: 0;
                margin: 0;
            }
            QWidget#CustomToolbar QToolButton:hover {
                background-color: #666;
            }
        """)

        # get existing layout
        layout = dock.layout()

        h = QHBoxLayout(container)
        h.setContentsMargins(6, 6, 6, 6)
        h.setSpacing(6)
        h.setSizeConstraint(QLayout.SetFixedSize)

        # ---- 2D / 3D toggle button ----
        icon2d = self._load_icon(os.path.join(ICON_FOLDER, "2D.svg"))
        icon3d = self._load_icon(os.path.join(ICON_FOLDER, "3D.svg"))
        btn_2d3d = QToolButton()
        btn_2d3d.setIcon(icon2d)
        btn_2d3d.setIconSize(QSize(24, 24))
        btn_2d3d.setFixedSize(28, 28)
        btn_2d3d.setToolTip("Toggle 2D / 3D")
        def toggle_2d3d():
            if viewer.dims.ndisplay == 2:
                viewer.dims.ndisplay = 3
                btn_2d3d.setIcon(icon3d)
            else:
                viewer.dims.ndisplay = 2
                btn_2d3d.setIcon(icon2d)
        btn_2d3d.clicked.connect(toggle_2d3d)

        # ---- Reorder button ----
        btn_reorder = cls._make_button(self, "roll.svg", "Reorder dimensions", lambda: self._reorder_layer(viewer))

        # ---- Transpose button ----
        btn_transpose = cls._make_button(self, "transpose.svg", "Transpose layer", lambda: self._transpose_layer(viewer))

        # ---- Grid toggle button ----
        icon_grid_off = self._load_icon(os.path.join(ICON_FOLDER, "canvas-standard-view.svg"))
        icon_grid_on  = self._load_icon(os.path.join(ICON_FOLDER, "canvas-grid-view.svg"))

        btn_grid = QToolButton()
        btn_grid.setIcon(icon_grid_on if viewer.grid.enabled else icon_grid_off)
        btn_grid.setIconSize(QSize(24, 24))
        btn_grid.setFixedSize(28, 28)
        btn_grid.setToolTip("Toggle Grid")
        def toggle_grid():
            viewer.grid.enabled = not viewer.grid.enabled
            btn_grid.setIcon(icon_grid_on if viewer.grid.enabled else icon_grid_off)
        btn_grid.clicked.connect(toggle_grid)

        # ---- Home / Reset view ----
        btn_home = cls._make_button(self, "home.svg", "Reset view", viewer.reset_view)

        # ---- Add all buttons in order ----
        h.addWidget(btn_2d3d)
        h.addWidget(btn_reorder)
        h.addWidget(btn_transpose)
        h.addWidget(btn_grid)
        h.addWidget(btn_home)

        container.adjustSize()

        # ---- Position bottom-left inside dock ----
        def reposition(event=None):
            container.move(6, dock.height() - container.height() - 6)

        old_resize = dock.resizeEvent
        def new_resize(e):
            if old_resize:
                old_resize(e)
            reposition()
        dock.resizeEvent = new_resize
        reposition()

        # Insert into napari's layout (napari will own it)
        # Napari uses: header (0), list view (1), status (last)
        layout.insertWidget(layout.count()- 1, container)   # <-- this makes it part of napari UI

if __name__ == "__main__":
    pass
