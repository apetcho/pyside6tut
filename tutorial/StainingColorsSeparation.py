#!/usr/bin/env python3
import sys
import numpy as np

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from skimage import data
from skimage.color import rgb2hed
from skimage.exposure import rescale_intensity


class ApplicationWindow(QMainWindow):
    """Example base on the example by 'scikit-image' gallery"""

    def __init__(self, root, parent=None):
        super(ApplicationWindow, self).__init__(parent)
        # TODO    

    def set_buttons_state(self, states):
        pass

    @Slot()
    def plot_hematoxylin(self):
        pass

    @Slot()
    def plot_eosin(self):
        pass

    @Slot()
    def plot_final(self):
        pass

