#!/usr/bin/env python3
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from PySide6 import QtCore
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QComboBox, QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QSlider, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ApplicationWindow, self).__init__(parent)

        self.column_names = ["Column A", "Column B", "Column C"]

        # Centra widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # Main menu bar
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)

        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt", self,
            shortcut=QKeySequence(QKeySequence.HelpContents),
            triggered=qApp.aboutQt)
        self.menu_about.addAction(about)

        # Figure (Left)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)

        # Sliders (Left)
        self.slider_azim = QSlider(minimum=0, maximum=360,
            orientation=QtCore.Qt.Horizontal)
        self.slider_elev = QSlider(minimum=0, maximum=360,
            orientation=QtCore.Qt.Horizontal)

        self.slider_azim_layout = QHBoxLayout()
        self.slider_azim_layout.addWidget(
            QLabel(f"{self.slider_azim.minimum()}"))
        self.slider_azim_layout.addWidget(self.slider_azim)
        self.slider_azim_layout.addWidget(
            QLabel(f"{self.slider_azim.maximum()}"))

        self.slider_elev_layout = QHBoxLayout()
        self.slider_elev_layout.addWidget(
            QLabel(f"{self.slider_elev.minimum()}"))
        self.slider_elev_layout.addWidget(
            QLabel(f"{self.slider_elev.maximum()}"))

        # Table (Right)
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ComboBox (Right)
        self.combo = QComboBox()
        self.combo.addItems(
            ["Wired", "Surface", "Triangular Surface", "Sphere"])

        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Plot type:"))
        rlayout.addWidget(self.combo)
        rlayout.addWidget(self.table)

        # Left layout
        llayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(self.canvas, 88)
        llayout.addWidget(QLabel("Azimuth:"), 1)
        llayout.addLayout(self.slider_azim_layout, 5)
        llayout.addWidget(QLabel("Elevation:"), 1)
        llayout.addLayout(self.slider_azim_layout, 5)

        # Main layout
        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 70)
        layout.addLayout(rlayout, 30)

        # Signal and Slots connections
        self.combo.currentTextChanged.connect(self.combo_option)
        self.slider_azim.valueChanged.connect(self.rotate_azim)
        self.slider_elev.valueChanged.connect(self.rotate_elev)

        # Initial setup
        self.plot_wire()
        self._ax.view_init(30, 30)
        self.slider_azim.setValue(30)
        self.slider_elev.setValue(30)
        self.fig.canvas.mpl_connect("button_release_event", self.on_click)

    def on_click(self, event):
        pass

    def set_table_data(self, X, Y, Z):
        pass

    def set_canvas_table_configuration(self, row_count, data):
        pass

    def plot_wire(self):
        pass

    def plot_surface(self):
        pass

    def plot_triangular_surface(self):
        pass

    def plot_sphere(self):
        pass

    @QtCore.Slot()
    def combo_option(self, text):
        pass

    @QtCore.Slot()
    def rotate_azim(self, value):
        pass

    @QtCore.Slot()
    def rotate_elev(self, value):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
