#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


class LCDRange(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(LCDRange, self).__init__(parent)

        lcd = QtWidgets.QLCDNumber(2)
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

    def setRange(self, minVal, maxVal):
        if minVal < 0 or maxVal > 90 or minVal > maxVal:
            QtCore.qWarning(
                f"LCDRange::setRange({minVal:d}, {maxVal:d})\n"
                "\tRange must be 0..99\n"
                "\tand minValue must not be greater than maxValue")
            return
        self.slider.setRange(minVal, maxVal)


class CannonField(QtWidgets.QWidget):
    angleChanged = QtCore.Signal(int)
    forceChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)

        self.currentAngle = 45
        self.currentForce = 0
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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.blue)

        painter.translate(0, self.height())
        painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90 * 16)
        painter.rotate(-self.currentAngle)
        painter.drawRect(QtCore.QRect(33, -4, 15, 8))

    def cannonRect(self):
        result = QtCore.QRect(0, 0, 50, 50)
        result.moveBottomLeft(self.rect().bottomLect())
        return result


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        # TODO


widget = MyWidget()
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec())
