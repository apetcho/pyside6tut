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

        self.setFocusProxy(layout)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        pass

    def setRange(self, minVal, maxVal):
        pass


class CannonField(QtWidgets.QWidget):
    angleChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(CannonField, self).__init__(parent)
        # TODO

    def angle(self):
        pass

    @QtCore.Slot(int)
    def setAngle(self, angle):
        pass

    def paintEvent(self, event):
        pass


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        # TODO



widget = MyWidget()
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec())
