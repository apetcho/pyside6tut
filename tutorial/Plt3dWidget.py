#!/usr/bin/env python3
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QComboBox, QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QSlider, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        pass

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

    @Slot()
    def combo_option(self, text):
        pass

    @Slot()
    def rotate_azim(self, value):
        pass

    @Slot()
    def rotate_elev(self, value):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
