#!/usr/bin/env python3
import sys
import time
import numpy as np
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QApplication
)
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


class ApplicationWindow(QMainWindow):

    def __init__(self, root):
        pass

    def _update_canvas(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
