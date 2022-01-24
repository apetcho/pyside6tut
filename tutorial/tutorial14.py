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
        if self.gameEnded:
            return
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = True
        self.update()

    def restartGame(self):
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = False
        self.update()
        self.emit(QtCore.SIGNAL("canShoot(bool)"), True)

    @QtCore.Slot()
    def moveShot(self):
        region = QtGui.QRegion(self.shotRect())
        self.timerCount += 1

        shotR = self.shotRect()

        if shotR.intersects(self.targetRect()):
            self.autoShootTimer.stop()
            self.emit(QtCore.SIGNAL("hit()"))
            self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        elif (shotR.x() > self.width() or shotR.y() > self.height() or
             shotR.intersects(self.barrierRect())):
             self.autoShootTimer.stop()
             self.emit(QtCore.SIGNAL("missed()"))
             self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        else:
            region = region.united(QtGui.QRegion(shotR))

        self.update(region)

    def mousePressEvent(self, event: QtCore.QEvent):
        if event.button() != QtCore.Qt.LeftButton:
            return
        if self.barrelHit(event.position().toPoint()):
            self.barrelPressed = True

    def mouseMoveEvent(self, event: QtCore.QEvent):
        if not self.barrelPressed:
            return
        pos = event.position().toPoint()
        if pos.x() <= 0:
            pos.setX(1)
        if pos.y() >= self.height():
            pos.setY(self.height()-1)
        rad = math.atan((float(self.rect().bottom()) - pos.y())/pos.x())
        self.setAngle(round(rad * 180 / math.pi))

    def mouseReleaseEvent(self, event: QtCore.QEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.barrelPressed = False

    def paintEvent(self, event: QtCore.QEvent):
        painter = QtGui.QPainter(self)

        if self.gameEnded:
            painter.setPen(QtCore.Qt.black)
            painter.setFont(QtGui.QFont("Courier", 48, QtGui.QFont.Bold))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Game Over")

        self.paintCannon(painter)
        self.paintBarrier(painter)
        if self.isShooting():
            self.paintShot(painter)
        if not self.gameEnded:
            self.painterTarget(painter)

    def paintShot(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

    def painterTarget(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(self.targetRect())

    def paintBarrier(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.yellow)
        painter.drawRect(self.barrierRect())

    barrelRect = QtCore.QRect(33, -4, 15, 8)

    def paintCannon(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.blue)

        painter.save()
        painter.translate(0, self.height())
        painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90*16)
        painter.rotate(-self.currentAngle)
        painter.drawRect(CannonField.barrelRect)
        painter.restore()

    def cannonRect(self):
        result = QtCore.QRect(0, 0, 50, 50)
        result.moveBottomLeft(self.rect().bottomLect())
        return result

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
