#!/usr/bin/env python3
import sys
import math
from unittest import result
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(LCDRange, self).__init__(parent)
        
        lcd = QtWidgets.QLCDNumber(2)
        lcd.setPalette(QtGui.QColor(10, 20, 10))
        # lcd.setAutoFillBackground(True)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)

    def setRange(self, vmin, vmax):
        if vmin < 0 or vmax > 99 or vmin > vmax:
            QtCore.qWarning(f"LCDRange::setRange({vmin:d}, {vmax:d})\n"
                "\tRange must be 0..99\n"
                "\tand minValue must not be greater than maxValue")
            return
        self.slider.setRange(vmin, vmax)


class CannonField(QtWidgets.QWidget):

    angleChanged = QtCore.Signal(int)
    forceChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)

        self.currentAngle = 45
        self.currentForce = 0
        self.timerCount = 0
        self.autoShooTimer = QtCore.QTimer(self)
        self.connect(self.autoShooTimer, QtCore.SIGNAL("timeout()"),
            self.moveShot)
        self.shootAngle = 0
        self.shootForce = 0
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)

    def angle(self):
        return self.currentAngle

    @QtCore.Slot(int)
    def setAngle(self, angle):
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
    def setForce(self, force):
        force = 0 if force < 0 else force
        if self.currentForce == force:
            return
        self.currentForce = force
        self.emit(QtCore.SIGNAL("forceChanged(int)"), self.currentForce)

    @QtCore.Slot()
    def shoot(self):
        if self.autoShooTimer.isActive():
            return
        self.timerCount = 0
        self.shootAngle = self.currentAngle
        self.shootForce = self.currentForce
        self.autoShooTimer.start(5)

    @QtCore.Slot()
    def moveShot(self):
        region = QtGui.QRegion(self.shotRect())
        self.timerCount += 1
        shotR = self.shotRect()
        if shotR.x() > self.width() or shotR.y() > self.height():
            self.autoShooTimer.stop()
        else:
            region = region.united(QtGui.QRegion(shotR))
        self.update(region)

    def paintEvent(self, event: QtCore.QEvent):
        painter = QtGui.QPainter(self)
        self.paintCannon(painter)
        if self.autoShooTimer.isActive():
            self.paintShot(painter)

    def paintShot(self, painter: QtGui.QPainter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

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
        velx = velocity * math.cos(radians)
        vely = velocity * math.sin(radians)
        x0 = (CannonField.barrelRect.right()+5)*math.cos(radians)
        y0 = (CannonField.barrelRect.right()+5)*math.sin(radians)
        x = x0 + velx * time
        y = y0 + vely * time - 0.5*gravity*time*time

        result = QtCore.QRect(0, 0, 6, 6)
        result.moveCenter(QtCore.QPoint(round(x), self.height()-1-round(y)))
        return result


class MyWidget(QtWidgets.QWidget):

    def __init__(self, root, parent=None):
        super(MyWidget, self).__init__(parent)

        quit = QtWidgets.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"),
            root, QtCore.SLOT("quit()"))

        angle = LCDRange()
        angle.setRange(5, 70)
        force = LCDRange()
        force.setRange(10, 50)
        cannonField = CannonField()

        self.connect(angle, QtCore.SIGNAL("valueChanged(int)"),
            cannonField.setAngle)
        self.connect(cannonField, QtCore.SIGNAL("angleChanged(int)"),
            angle.setValue)
        self.connect(force, QtCore.SIGNAL("valueChanged(int)"),
            cannonField.setForce)
        self.connect(cannonField, QtCore.SIGNAL("forceChanged(int)"),
            force.setValue)

        shoot = QtWidgets.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(shoot, QtCore.SIGNAL("clicked()"), cannonField.shoot)

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(shoot)
        topLayout.addStretch(1)

        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addWidget(angle)
        leftLayout.addWidget(force)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addWidget(cannonField, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        angle.setValue(60)
        force.setValue(25)
        angle.setFocus()



app = QtWidgets.QApplication(sys.argv)
widget = MyWidget(app)
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec())
