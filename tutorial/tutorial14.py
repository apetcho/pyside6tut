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
        if isinstance(text, QtWidgets.QWidget):
            parent = text
            text = None
        super(LCDRange, self).__init__(parent)

        self.init()
        if text:
            self.setText(text)

    def init(self):
        lcd = QtWidgets.QLCDNumber(2)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.Alignment | QtCore.Qt.AlignTop)
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred | QtWidgets.QSizePolicy.Fixed)

        self.connect(
            self.slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)")
        )
        self.connect(
            self.slider, QtCore.SIGNAL("valueChanged(int)"),
            self, QtCore.SIGNAL("valueChanged(int)")
        )
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)

    def text(self):
        return self.label.text()

    def setRange(self, vmin, vmax):
        if vmin < 0 or vmax > 99 or vmin > vmax:
            QtCore.qWarning(
                f"LCDRange::setRange({vmin:d}, {vmax:d})\n"
                "\tRange must be 0..99\n"
                "\tand vmin must not be greater than vmax"
            )
            return
        self.slider.setRange(vmin, vmax)

    def setText(self, text):
        self.label.setText(text)


class CannonField(QtWidgets.QWidget):

    angleChanged = QtCore.Signal(int)
    forceChanged = QtCore.Signal(int)
    hit = QtCore.Signal()
    missed = QtCore.Signal()
    canShoot = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)

        self.currentAngle = 45
        self.currentForce = 0
        self.timerCount = 0
        self.autoShootTimer = QtCore.QTimer(self)
        self.connect(
            self.autoShootTimer, QtCore.SIGNAL("timeout()"), self.moveShot
        )
        self.shootAngle = 0
        self.shootForce = 0
        self.target = QtCore.QPoint(0, 0)
        self.gameEnded = False
        self.barrelPressed = False
        self.setPalette(QtGui.QPalette(QtGui.QColor(2550, 250, 200)))
        self.setAutoFillBackground(True)
        self.newTarget()

    def angle(self):
        return self.currentAngle

    @QtCore.Slot(int)
    def setAngle(self, angle):
        angle = 5 if angle < 5 else angle
        angle = 85 if angle > 85 else angle
        if self.currentAngle == angle:
            return
        self.currentAngle = angle
        self.update()
        self.emit(QtCore.SIGNAL("angleChanged(int)"), self.currentAngle)

    def force(self):
        return self.currentForce

    @QtCore.Slot(int)
    def setForce(self, frc):
        frc = 0 if frc < 0 else frc
        if self.currentForce == frc:
            return
        self.currentForce = frc
        self.emit(QtCore.SIGNAL("forceChanged(int)"), self.currentForce)

    @QtCore.Slot()
    def shoot(self):
        if self.isShooting():
            return
        self.timerCount = 0
        self.shootAngle = self.currentAngle
        self.shootForce = self.currentForce
        self.autoShootTimer.start(5)
        self.emit(QtCore.SIGNAL("canShoot(bool)"), False)

    firstTime = True

    def newTarget(self):
        if CannonField.firstTime:
            CannonField.firstTime = False
            midnight = QtCore.QTime(0, 0, 0)
            random.seed(midnight.secsTo(QtCore.QTime.currentTime()))

        self.target = QtCore.QPoint(
            200 + random.randint(0, 190-1),
             10 + random.randint(0, 255-1)
        )
        self.update()

    def setGameOver(self):
        pass

    def restartGame(self):
        pass

    @QtCore.Slot()
    def moveShot(self):
        pass

    def mousePressEvent(self, event: QtCore.QEvent):
        pass

    def mouseMoveEvent(self, event: QtCore.QEvent):
        pass

    def mouseReleaseEvent(self, event: QtCore.QEvent):
        pass

    def paintEvent(self, event: QtCore.QEvent):
        pass

    def paintShot(self, painter: QtGui.QPainter):
        pass

    def painterTarget(self, painter: QtGui.QPainter):
        pass

    def paintBarrier(self, painter: QtGui.QPainter):
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

    def barrierRect(self):
        pass

    def barrelHit(self, pos):
        pass

    def gameOver(self):
        pass

    def isShooting(self):
        pass

    def sizeHint(self):
        pass


class GameBoard(QtWidgets.QWidget):

    def __init__(self, root, parent=None):
        pass

    @QtCore.Slot()
    def fire(self):
        pass

    @QtCore.Slot()
    def hit(self):
        pass

    @QtCore.Slot()
    def missed(self):
        pass

    @QtCore.Slot()
    def newGame(self):
        pass

def main():
    pass


main()
