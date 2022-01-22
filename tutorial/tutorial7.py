#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(QtWidgets, self).__init__(parent)
        # TODO

    def value(self):
        pass

    @QtCore.Slot(int)
    def setValue(self, value):
        pass
