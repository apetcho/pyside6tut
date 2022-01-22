#!/usr/bin/env python3
import sys
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


class LCDRange(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(QtWidgets, self).__init__(parent)

        lcd = QtWidgets.QLCDNumber(2)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.setValue(0)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
            self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def value(self):
        return self.slider.value()

    @QtCore.Slot(int)
    def setValue(self, value):
        self.slider.setValue(value)


class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
            self, QtCore.SLOT("quit()"))

        grid = QtWidgets.QGridLayout()
        previousRange = None

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(quit)
        layout.addLayout(grid)
        self.setLayout(layout)

        for row in range(3):
            for column in range(3):
                lcdRange = LCDRange()
                grid.addWidget(lcdRange, row, column)

                if previousRange:
                    self.connect(lcdRange, QtCore.SIGNAL("valueChanged(int)"),
                        previousRange.setValue)
                previousRange = lcdRange


widget = MyWidget()
widget.show()
sys.exit(app.exec())
