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

