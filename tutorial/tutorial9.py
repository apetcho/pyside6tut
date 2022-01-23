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
        if minVal < 0 or maxVal > 99 or minVal > maxVal:
            QtCore.qWarning(
                f"LCDRange.setRange({minVal}, {maxVal})\n"
                "\tRange must be 0..9\n"
                "\tand minValue must not be greater than maxValue")
            return
        self.slider.setRange(minVal, maxVal)


class CannonField(QtWidgets.QWidget):

    angleChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)

        self.currentAngle = 45
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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawText(200, 200, f"Angle = {self.currentAngle}")


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(
            quit, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("quit()")
        )

        angle = LCDRange()
        angle.setRange(5, 70)

        cannonField = CannonField()

        self.connect(angle, QtCore.SIGNAL("valueChanged(int)"),
            cannonField.setAngle)
        self.connect(cannonField, QtCore.SIGNAL("angleChanged(int)"),
            angle.setValue)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addWidget(angle, 1, 0)
        gridLayout.addWidget(cannonField, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        self.setVisible(60)
        angle.setFocus()   


widget = MyWidget()
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec())
