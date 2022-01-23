#!/usr/bin/env python3
import sys
import math
import random
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, text=None, parent=None):
        pass

    def init(self):
        pass

    def value(self):
        pass

    @QtCore.Slot(int)
    def setValue(self, value):
        pass

    def text(self):
        pass

    def setRange(self, vmin, vmax):
        pass

    def setText(self, text):
        pass
