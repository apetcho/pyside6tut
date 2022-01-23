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


class CannonField(QtWidgets.QWidget):

    angleChanged = QtCore.Signal(int)
    forceChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        pass

    def angle(self):
        pass

    @QtCore.Slot(int)
    def setAngle(self, angle):
        pass

    def force(self):
        pass

    @QtCore.Slot(int)
    def setForce(self, force):
        pass

    @QtCore.Slot()
    def shoot(self):
        pass

    firstTime = True

    def newTarget(self):
        pass

    @QtCore.Slot()
    def moveShot(self):
        pass

    def paintEvent(self, event: QtCore.QEvent):
        pass

    def paintShot(self, painter: QtGui.QPainter):
        pass

    def paintTarget(self, painter: QtGui.QPainter):
        pass

    barrelRect = QtCore.QRect(33, -4, 15, 8)


    def paintCannon(self, painter: QtGui.QPainter):
        pass

    def cannonRect(self):
        pass

    def shotRect(self):
        pass

    def targetRect(self):
        pass


class MyWidget(QtWidgets.QWidget):

    def __init__(self, root, parent=None):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget(app)
    widget.setGeometry(100, 100, 500, 355)
    widget.show()
    sys.exit(app.exec())


main()
