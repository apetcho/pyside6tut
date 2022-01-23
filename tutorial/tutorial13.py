#!/usr/bin/env python3
import sys
import math
import random
from PySide6 import QtCore, QtGui, QtWidgets


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
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            self, QtCore.SLOT("valueChanged(int)"))     # XXX

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
            QtCore.qWarning(f"LCDRange::setRange({vmin:d}, {vmax:d})\n"
                "\tRange must b 0..99\n"
                "\tand minValue must not be greater than maxValue")
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
        self.connect(self.autoShootTimer, QtCore.SIGNAL("timeout()"),
            self.moveShot)
        self.shootAngle = 0
        self.shootForce = 0
        self.target = QtCore.QPoint(0, 0)
        self.gameEnded = False
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        self.newTarget()

    def angle(self):
        return self.currentAngle

    @QtCore.Slot(int)
    def setAngle(self, angle) -> None:
        angle = 5 if angle < 5 else angle
        angle = 70 if angle > 70 else angle
        if self.currentAngle == angle:
            return
        self.currentAngle = angle
        self.update()
        self.emit(QtCore.SIGNAL("angleChanged(int)"), self.currentAngle)

    def force(self):
        return self.currentForce

    @QtCore.Slot(int)
    def setForce(self, force) -> None:
        force = 0 if force < 0 else force
        if self.currentForce == force:
            return
        self.currentForce = force
        self.emit(QtCore.SIGNAL("forceChanged(int)"), self.currentForce)

    @QtCore.Slot()
    def shoot(self) -> None:
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
        self.target = QtCore.QPoint(200+random.randint(0, 190 -1),
            10 + random.randint(0, 255-1))
        self.update()

    def setGameOver(self) -> None:
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
        elif shotR.x() > self.width() or shotR.y() > self.height():
            self.autoShootTimer.stop()
            self.emit(QtCore.SIGNAL("missed()"))
            self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        else:
            region = region.united(QtGui.QRegion(shotR))

        self.update(region)

    def paintEvent(self, event: QtCore.QEvent):
        painter = QtGui.QPainter(self)
        if self.gameEnded:
            painter.setPen(QtCore.Qt.black)
            painter.setFont(QtGui.QFont("Courier", 48, QtGui.QFont.Bold))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter,
                " G A M E   O V E R ")

        self.paintCannon(painter)
        if self.isShooting():
            self.paintShot(painter)
        if not self.gameEnded:
            self.paintTarget(painter)

    def paintShot(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

    def paintTarget(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(self.targetRect())

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
        gravity = 4.0

        time = self.timerCount / 40.0
        velocity = self.shootForce
        radians = self.shootAngle * math.pi / 180

        vx = velocity * math.cos(radians)
        vy = velocity * math.sin(radians)
        x0 = (CannonField.barrelRect.right()+5)*math.cos(radians)
        y0 = (CannonField.barrelRect.right()+5)*math.sin(radians)
        x = x0 + vx*time
        y = y0 + vy*time -0.5*gravity*time*time
        result = QtCore.QRect(0, 0, 6, 6)
        result.moveCenter(QtCore.QPoint(round(x), self.height()-1-round(y)))
        return result

    def targetRect(self):
        result = QtCore.QRect(0, 0, 20, 10)
        result.moveCenter(QtCore.QPoint(self.target.x(),
            self.height()-1-self.target.y()))
        return result

    def gameOver(self):
        pass

    def isShooting(self):
        pass


class GameBoard(QtWidgets.QWidget):

    def __init__(self, parent=None):
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
