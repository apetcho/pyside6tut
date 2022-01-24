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
        super(ApplicationWindow, self).__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D
        self._line, = self._dynamic_ax.plot(t, np.sin(t+time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


def main():
    pass


if __name__ == "__main__":
    main()
