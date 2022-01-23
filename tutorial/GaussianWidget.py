#!/usr/bin/env python3
import sys
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication, QWidget, QDoubleSpinBox, QVBoxLayout, QHBoxLayout
)


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        pass

    @Slot()
    def on_change(self):
        pass
